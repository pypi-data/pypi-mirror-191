"""Some utilities for manipulating GeoSpatial data."""
from __future__ import annotations

import itertools
import tempfile
import uuid
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Sequence, Tuple, TypeVar, Union, cast

import cytoolz.curried as tlz
import dask.config
import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import pyproj
import rasterio.features as rio_features
import rasterio.transform as rio_transform
import rioxarray as rxr
import shapely.geometry as sgeom
import ujson as json
import xarray as xr
from pyproj.exceptions import CRSError as ProjCRSError
from rasterio import MemoryFile
from scipy.interpolate import BSpline
from shapely import ops
from shapely.geometry import LineString, MultiPolygon, Polygon

from pygeoutils import _utils as utils
from pygeoutils.exceptions import (
    EmptyResponseError,
    InputRangeError,
    InputTypeError,
    InputValueError,
    MatchingCRSError,
    MissingColumnError,
    MissingCRSError,
    UnprojectedCRSError,
)

BOX_ORD = "(west, south, east, north)"
NUMBER = Union[int, float, np.number]  # type: ignore
if TYPE_CHECKING:
    from rasterio import Affine

    GTYPE = Union[Polygon, MultiPolygon, Tuple[float, float, float, float]]
    GDF = TypeVar("GDF", gpd.GeoDataFrame, gpd.GeoSeries)
    XD = TypeVar("XD", xr.Dataset, xr.DataArray)
    CRSTYPE = Union[int, str, pyproj.CRS]

__all__ = [
    "snap2nearest",
    "break_lines",
    "json2geodf",
    "arcgis2geojson",
    "geo2polygon",
    "get_transform",
    "geometry_list",
    "xarray_geomask",
    "gtiff2xarray",
    "xarray2geodf",
    "geodf2xarray",
    "Coordinates",
    "GeoBSpline",
    "query_indices",
    "nested_polygons",
]


def arcgis2geojson(arcgis: str | dict[str, Any], id_attr: str | None = None) -> dict[str, Any]:
    """Convert ESRIGeoJSON format to GeoJSON.

    Notes
    -----
    Based on `arcgis2geojson <https://github.com/chris48s/arcgis2geojson>`__.

    Parameters
    ----------
    arcgis : str or binary
        The ESRIGeoJSON format str (or binary)
    id_attr : str, optional
        ID of the attribute of interest, defaults to ``None``.

    Returns
    -------
    dict
        A GeoJSON file readable by GeoPandas.
    """
    if isinstance(arcgis, str):
        return utils.convert(json.loads(arcgis), id_attr)

    return utils.convert(arcgis, id_attr)


def json2geodf(
    content: list[dict[str, Any]] | dict[str, Any],
    in_crs: CRSTYPE = 4326,
    crs: CRSTYPE = 4326,
) -> gpd.GeoDataFrame:
    """Create GeoDataFrame from (Geo)JSON.

    Parameters
    ----------
    content : dict or list of dict
        A (Geo)JSON dictionary e.g., response.json() or a list of them.
    in_crs : int, str, or pyproj.CRS, optional
        CRS of the content, defaults to ``epsg:4326``.
    crs : int, str, or pyproj.CRS, optional
        The target CRS of the output GeoDataFrame, defaults to ``epsg:4326``.

    Returns
    -------
    geopandas.GeoDataFrame
        Generated geo-data frame from a GeoJSON
    """
    if not isinstance(content, (list, dict)):
        raise InputTypeError("content", "list or list of dict ((geo)json)")

    content = content if isinstance(content, list) else [content]
    try:
        geodf = gpd.GeoDataFrame.from_features(next(iter(content)))
    except TypeError:
        content = [arcgis2geojson(c) for c in content]
        geodf = gpd.GeoDataFrame.from_features(content[0])
    except StopIteration as ex:
        raise EmptyResponseError from ex

    if len(content) > 1:
        geodf = gpd.GeoDataFrame(pd.concat(gpd.GeoDataFrame.from_features(c) for c in content))

    if "geometry" in geodf and not geodf.geometry.is_empty.all():
        geodf = geodf.set_crs(in_crs)
        if in_crs != crs:
            geodf = geodf.to_crs(crs)
    geodf = cast("gpd.GeoDataFrame", geodf)
    return geodf


def geo2polygon(
    geometry: GTYPE,
    geo_crs: CRSTYPE | None = None,
    crs: CRSTYPE | None = None,
) -> Polygon | MultiPolygon:
    """Convert a geometry to a Shapely's Polygon and transform to any CRS.

    Parameters
    ----------
    geometry : Polygon or tuple of length 4
        Polygon or bounding box (west, south, east, north).
    geo_crs : int, str, or pyproj.CRS, optional
        Spatial reference of the input geometry, defaults to ``None``.
    crs : int, str, or pyproj.CRS
        Target spatial reference, defaults to ``None``.

    Returns
    -------
    shapely.Polygon or shapely.MultiPolygon
        A (Multi)Polygon in the target CRS, if different from the input CRS.
    """
    if isinstance(geometry, (Polygon, MultiPolygon)):
        geom = geometry
    elif isinstance(geometry, (tuple, list)) and len(geometry) == 4:
        geom = sgeom.box(*geometry)
    else:
        raise InputTypeError("geometry", "(Multi)Polygon or tuple of length 4")

    if geo_crs and crs and pyproj.CRS(geo_crs) != pyproj.CRS(crs):
        project = pyproj.Transformer.from_crs(geo_crs, crs, always_xy=True).transform
        geom = ops.transform(project, geom)

    geom = cast("Polygon | MultiPolygon", geom)
    if not geom.is_valid:
        geom = geom.buffer(0.0)
        geom = cast("Polygon | MultiPolygon", geom)
    return geom


def xarray_geomask(
    ds: XD,
    geometry: GTYPE,
    crs: CRSTYPE,
    all_touched: bool = False,
    drop: bool = True,
    from_disk: bool = False,
) -> XD:
    """Mask a ``xarray.Dataset`` based on a geometry.

    Parameters
    ----------
    ds : xarray.Dataset or xarray.DataArray
        The dataset(array) to be masked
    geometry : Polygon, MultiPolygon, or tuple of length 4
        The geometry to mask the data
    crs : int, str, or pyproj.CRS
        The spatial reference of the input geometry
    all_touched : bool, optional
        Include a pixel in the mask if it touches any of the shapes.
        If False (default), include a pixel only if its center is within one
        of the shapes, or if it is selected by Bresenham's line algorithm.
    drop : bool, optional
        If True, drop the data outside of the extent of the mask geometries.
        Otherwise, it will return the same raster with the data masked.
        Default is True.
    from_disk : bool, optional
         If True, it will clip from disk using rasterio.mask.mask if possible.
         This is beneficial when the size of the data is larger than memory.
         Default is False.

    Returns
    -------
    xarray.Dataset or xarray.DataArray
        The input dataset with a mask applied (np.nan)
    """
    ds_attrs = ds.attrs
    da_attrs = {v: ds[v].attrs for v in ds} if isinstance(ds, xr.Dataset) else {}

    if ds.rio.crs is None:
        raise MissingCRSError

    geom = geo2polygon(geometry, crs, ds.rio.crs)
    ds = utils.write_crs(ds)
    ds = ds.rio.clip_box(*geom.bounds, auto_expand=True)
    if isinstance(geometry, (Polygon, MultiPolygon)):
        ds = ds.rio.clip([geom], all_touched=all_touched, drop=drop, from_disk=from_disk)

    if drop:
        ds = utils.write_crs(ds)
    ds.rio.update_attrs(ds_attrs, inplace=True)
    if isinstance(ds, xr.Dataset):
        _ = [ds[v].rio.update_attrs(da_attrs[v], inplace=True) for v in ds]
    ds.rio.update_encoding(ds.encoding, inplace=True)
    return ds


def gtiff2xarray(
    r_dict: dict[str, bytes],
    geometry: GTYPE | None = None,
    geo_crs: CRSTYPE | None = None,
    ds_dims: tuple[str, str] | None = None,
    driver: str | None = None,
    all_touched: bool = False,
    nodata: NUMBER | None = None,
    drop: bool = True,
) -> xr.DataArray | xr.Dataset:
    """Convert (Geo)Tiff byte responses to ``xarray.Dataset``.

    Parameters
    ----------
    r_dict : dict
        Dictionary of (Geo)Tiff byte responses where keys are some names that are used
        for naming each responses, and values are bytes.
    geometry : Polygon, MultiPolygon, or tuple, optional
        The geometry to mask the data that should be in the same CRS as the r_dict.
        Defaults to ``None``.
    geo_crs : int, str, or pyproj.CRS, optional
        The spatial reference of the input geometry, defaults to ``None``. This
        argument should be given when ``geometry`` is given.
    ds_dims : tuple of str, optional
        The names of the vertical and horizontal dimensions (in that order)
        of the target dataset, default to None. If None, dimension names are determined
        from a list of common names.
    driver : str, optional
        A GDAL driver for reading the content, defaults to automatic detection. A list of
        the drivers can be found here: https://gdal.org/drivers/raster/index.html
    all_touched : bool, optional
        Include a pixel in the mask if it touches any of the shapes.
        If False (default), include a pixel only if its center is within one
        of the shapes, or if it is selected by Bresenham's line algorithm.
    nodata : float or int, optional
        The nodata value of the raster, defaults to None, i.e., is determined from the raster.
    drop : bool, optional
        If True, drop the data outside of the extent of the mask geometries.
        Otherwise, it will return the same raster with the data masked.
        Default is True.

    Returns
    -------
    xarray.Dataset or xarray.DataAraay
        Parallel (with dask) dataset or dataarray.
    """
    if not isinstance(r_dict, dict):
        raise InputTypeError("r_dict", "dict", '{"name": bytes}')  # noqa: FS003

    try:
        key1 = next(iter(r_dict.keys()))
    except StopIteration as ex:
        raise EmptyResponseError from ex

    var_name = dict(zip(r_dict, r_dict))
    if "_dd_" in key1:
        var_name = {lyr: "_".join(lyr.split("_")[:-3]) for lyr in r_dict.keys()}

    attrs = utils.get_gtiff_attrs(r_dict[key1], ds_dims, driver, nodata)
    dtypes: dict[str, type] = {}
    nodata_dict: dict[str, NUMBER] = {}

    tmp_dir = tempfile.gettempdir()

    def to_dataset(lyr: str, resp: bytes) -> Path:
        with MemoryFile() as memfile:
            memfile.write(resp)
            with memfile.open(driver=driver) as vrt:
                ds = rxr.open_rasterio(vrt)  # type: ignore
                ds = cast("xr.Dataset", ds)
                if "band" in ds.dims:
                    ds = ds.squeeze("band", drop=True)
                ds.name = var_name[lyr]
                dtypes[ds.name] = ds.dtype
                nodata_dict[ds.name] = utils.get_nodata(vrt) if nodata is None else nodata
                ds = ds.rio.write_nodata(nodata_dict[ds.name])
                fpath = Path(tmp_dir, f"{uuid.uuid4().hex}.nc")
                ds.to_netcdf(fpath)
                return fpath

    with dask.config.set(**{"array.slicing.split_large_chunks": True}):
        ds = xr.open_mfdataset(
            itertools.starmap(to_dataset, r_dict.items()),  # type: ignore
            chunks="auto",
            parallel=True,
            engine="rasterio",
        )

    if "band" in ds.dims:
        ds = ds.squeeze("band", drop=True)

    variables = list(ds)
    variables = cast("str", variables)

    if len(variables) == 1:
        ds = ds[variables[0]].copy()
        ds = ds.astype(dtypes[variables[0]])
        name = cast("str", ds.name)
        ds.attrs["crs"] = attrs.crs.to_string()
        ds.attrs["nodatavals"] = (nodata_dict[name],)
        ds = ds.rio.write_nodata(nodata_dict[name])
    else:
        ds.attrs["crs"] = attrs.crs.to_string()
        for v in variables:
            ds[v] = ds[v].astype(dtypes[v])
            ds[v].attrs["crs"] = attrs.crs.to_string()
            ds[v].attrs["nodatavals"] = (nodata_dict[v],)
            ds[v] = ds[v].rio.write_nodata(nodata_dict[v])

    ds = ds.rio.write_transform()
    ds = ds.rio.write_crs(attrs.crs)
    ds = ds.rio.write_coordinate_system()

    if geometry:
        if geo_crs is None:
            raise MissingCRSError
        return xarray_geomask(ds, geometry, geo_crs, all_touched, drop)
    return ds


def get_transform(
    ds: xr.Dataset | xr.DataArray,
    ds_dims: tuple[str, str] = ("y", "x"),
) -> tuple[Affine, int, int]:
    """Get transform of a ``xarray.Dataset`` or ``xarray.DataArray``.

    Parameters
    ----------
    ds : xarray.Dataset or xarray.DataArray
        The dataset(array) to be masked
    ds_dims : tuple, optional
        Names of the coordinames in the dataset, defaults to ``("y", "x")``.
        The order of the dimension names must be (vertical, horizontal).

    Returns
    -------
    rasterio.Affine, int, int
        The affine transform, width, and height
    """
    ydim, xdim = ds_dims
    height, width = ds.sizes[ydim], ds.sizes[xdim]

    left, bottom, right, top = utils.get_bounds(ds, ds_dims)

    x_res = abs(left - right) / width
    y_res = abs(top - bottom) / height

    left -= x_res * 0.5
    right += x_res * 0.5
    top += y_res * 0.5
    bottom -= y_res * 0.5

    transform = rio_transform.from_bounds(left, bottom, right, top, width, height)
    return transform, width, height


def xarray2geodf(
    da: xr.DataArray, dtype: str, mask_da: xr.DataArray | None = None, connectivity: int = 8
) -> gpd.GeoDataFrame:
    """Vectorize a ``xarray.DataArray`` to a ``geopandas.GeoDataFrame``.

    Parameters
    ----------
    da : xarray.DataArray
        The dataarray to vectorize.
    dtype : type
        The data type of the dataarray. Valid types are ``int16``, ``int32``,
        ``uint8``, ``uint16``, and ``float32``.
    mask_da : xarray.DataArray, optional
        The dataarray to use as a mask, defaults to ``None``.
    connectivity : int, optional
        Use 4 or 8 pixel connectivity for grouping pixels into features,
        defaults to 8.

    Returns
    -------
    geopandas.GeoDataFrame
        The vectorized dataarray.
    """
    if not isinstance(da, xr.DataArray):
        raise InputTypeError("da", "xarray.DataArray")

    if not isinstance(mask_da, (xr.DataArray, type(None))):
        raise InputTypeError("da", "xarray.DataArray or None")

    valid_types = ["int16", "int32", "uint8", "uint16", "float32"]
    if dtype not in valid_types:
        raise InputValueError("dtype", valid_types)

    crs = da.rio.crs if da.attrs.get("crs") is None else da.crs
    if crs is None:
        raise MissingCRSError

    mask = None if mask_da is None else mask_da.to_numpy()
    shapes = rio_features.shapes(
        source=da.to_numpy().astype(dtype),
        transform=da.rio.transform(),
        mask=mask,
        connectivity=connectivity,
    )
    geojsons, values = zip(*shapes)
    geojsons = cast("tuple[dict[str, Any], ...]", geojsons)
    return gpd.GeoDataFrame(
        data={str(da.name): np.array(values, dtype)},
        geometry=[sgeom.shape(g) for g in geojsons],
        crs=crs,
    )


def geodf2xarray(
    geodf: GDF,
    resolution: float,
    attr_col: str | None = None,
    fill: int | float = 0,
    projected_crs: CRSTYPE = 5070,
) -> xr.Dataset:
    """Rasterize a ``geopandas.GeoDataFrame`` to ``xarray.DataArray``.

    Parameters
    ----------
    geodf : geopandas.GeoDataFrame or geopandas.GeoSeries
        GeoDataFrame or GeoSeries to rasterize.
    resolution : float
        Target resolution of the output raster in the ``projected_crs`` unit. Since
        the default ``projected_crs`` is ``EPSG:5070``, the default unit for the
        resolution is meters.
    attr_col : str, optional
        Column name of the attribute to use as variable., defaults to ``None``,
        i.e., the variable will be a boolean mask where 1 indicates the presence of
        a geometry. Also, note that the attribute must be numeric and have one of the
        following ``numpy`` types: ``int16``, ``int32``, ``uint8``, ``uint16``,
        ``uint32``, ``float32``, and ``float64``.
    fill : int or float, optional
        Value to use for filling the missing values (mask) of the output raster,
        defaults to ``0``.
    projected_crs : int, str, or pyproj.CRS, optional
        A projected CRS to use for the output raster, defaults to ``EPSG:5070``.

    Returns
    -------
    xarray.Dataset
        The xarray Dataset with a single variable.
    """
    if not pyproj.CRS(projected_crs).is_projected:
        raise InputTypeError("projected_crs", "a projected CRS")

    gdf = geodf.to_crs(projected_crs) if geodf.crs != pyproj.CRS(projected_crs) else geodf
    gdf = cast("gpd.GeoDataFrame", gdf)
    west, south, east, north = gdf.total_bounds
    width = np.ceil(abs(west - east) / resolution).astype(int)
    height = np.ceil(abs(north - south) / resolution).astype(int)
    affine = rio_transform.from_bounds(west, south, east, north, width, height)

    if attr_col:
        _types = ["int16", "int32", "uint8", "uint16", "uint32", "float32", "float64"]
        valid_types = [np.dtype(t) for t in _types]
        dtype = geodf[attr_col].dtype
        if dtype not in valid_types:
            raise InputTypeError("attr_col", ", ".join(_types))

        ds = xr.DataArray(
            rio_features.rasterize(
                shapes=zip(gdf.geometry, gdf[attr_col]),
                out_shape=(height, width),
                transform=affine,
                dtype=dtype,
                fill=fill,
            ),
            coords={"x": np.linspace(west, east, width), "y": np.linspace(north, south, height)},
            dims=("y", "x"),
            name=attr_col,
        )
    else:
        ds = xr.DataArray(
            rio_features.rasterize(
                shapes=gdf.geometry,
                out_shape=(height, width),
                transform=affine,
            ),
            coords={"x": np.linspace(west, east, width), "y": np.linspace(north, south, height)},
            dims=("y", "x"),
        )
    ds = ds.rio.write_transform(affine)
    ds = ds.rio.write_crs(projected_crs)
    ds = ds.rio.write_coordinate_system()
    return ds


@dataclass
class Coordinates:
    """Generate validated and normalized coordinates in WGS84.

    Parameters
    ----------
    lon : float or list of floats
        Longitude(s) in decimal degrees.
    lat : float or list of floats
        Latitude(s) in decimal degrees.
    bounds : tuple of length 4, optional
        The bounding box to check of the input coordinates fall within.
        Defaults to WGS84 bounds.

    Examples
    --------
    >>> from pygeoutils import Coordinates
    >>> c = Coordinates([460, 20, -30], [80, 200, 10])
    >>> c.points.x.tolist()
    [100.0, -30.0]
    """

    lon: NUMBER | Sequence[NUMBER]
    lat: NUMBER | Sequence[NUMBER]
    bounds: tuple[float, float, float, float] | None = None

    @staticmethod
    def __box_geo(bounds: tuple[float, float, float, float] | None) -> sgeom.Polygon:
        """Get EPSG:4326 CRS."""
        wgs84_bounds = pyproj.CRS(4326).area_of_use.bounds  # type: ignore
        if bounds is None:
            return sgeom.box(*wgs84_bounds)

        if not isinstance(bounds, (tuple, list)) or len(bounds) != 4:
            raise InputTypeError("bounds", "tuple of length 4")

        bbox = sgeom.box(*bounds)
        if not bbox.within(sgeom.box(*wgs84_bounds)):
            raise InputRangeError("bounds", "within EPSG:4326")
        return bbox

    @staticmethod
    def __validate(pts: gpd.GeoSeries, bbox: sgeom.Polygon) -> gpd.GeoSeries:
        """Create a ``geopandas.GeoSeries`` from valid coords within a bounding box."""
        return pts[pts.sindex.query(bbox)].sort_index()

    def __post_init__(self) -> None:
        """Normalize the longitude value within [-180, 180)."""
        if isinstance(self.lon, (int, float, np.number)):
            _lon = np.array([self.lon], "f8")
        else:
            _lon = np.array(self.lon, "f8")

        if isinstance(self.lat, (int, float, np.number)):
            lat = np.array([self.lat], "f8")
        else:
            lat = np.array(self.lat, "f8")

        lon = np.mod(np.mod(_lon, 360.0) + 540.0, 360.0) - 180.0
        pts = gpd.GeoSeries([sgeom.Point(xy) for xy in zip(lon, lat)])
        pts = cast("gpd.GeoSeries", pts.set_crs(4326))
        self._points = self.__validate(pts, self.__box_geo(self.bounds))

    @property
    def points(self) -> gpd.GeoSeries:
        """Get validate coordinate as a ``geopandas.GeoSeries``."""
        return self._points


def validate_crs(crs: CRSTYPE) -> str:
    """Validate a CRS.

    Parameters
    ----------
    crs : str, int, or pyproj.CRS
        Input CRS.

    Returns
    -------
    str
        Validated CRS as a string.
    """
    try:
        return pyproj.CRS(crs).to_string()  # type: ignore
    except ProjCRSError as ex:
        raise InputTypeError("crs", "a valid CRS") from ex


@dataclass
class Spline:
    """Provide attributes of an interpolated B-spline.

    Attributes
    ----------
    x : numpy.ndarray
        The x-coordinates of the interpolated points.
    y : numpy.ndarray
        The y-coordinates of the interpolated points.
    phi : numpy.ndarray
        Curvature of the B-spline in radians.
    radius : numpy.ndarray
        Radius of curvature of the B-spline.
    distance : numpy.ndarray
        Total distance of each point along the B-spline from the start point.
    """

    x: npt.NDArray[np.float64]
    y: npt.NDArray[np.float64]
    phi: npt.NDArray[np.float64]
    radius: npt.NDArray[np.float64]
    distance: npt.NDArray[np.float64]


class GeoBSpline:
    """Create B-spline from a geo-dataframe of points.

    Parameters
    ----------
    points : geopandas.GeoDataFrame or geopandas.GeoSeries
        Input points as a ``GeoDataFrame`` or ``GeoSeries`` in a projected CRS.
    npts_sp : int
        Number of points in the output spline curve.
    degree : int, optional
        Degree of the spline. Should be less than the number of points and
        greater than 1. Default is 3.

    Examples
    --------
    >>> from pygeoutils import GeoBSpline
    >>> import geopandas as gpd
    >>> xl, yl = zip(
    ...     *[
    ...         (-97.06138, 32.837),
    ...         (-97.06133, 32.836),
    ...         (-97.06124, 32.834),
    ...         (-97.06127, 32.832),
    ...     ]
    ... )
    >>> pts = gpd.GeoSeries(gpd.points_from_xy(xl, yl, crs=4326))
    >>> sp = GeoBSpline(pts.to_crs("epsg:3857"), 5).spline
    >>> pts_sp = gpd.GeoSeries(gpd.points_from_xy(sp.x, sp.y, crs="epsg:3857"))
    >>> pts_sp = pts_sp.to_crs("epsg:4326")
    >>> list(zip(pts_sp.x, pts_sp.y))
    [(-97.06138, 32.837),
    (-97.06135, 32.83629),
    (-97.06131, 32.83538),
    (-97.06128, 32.83434),
    (-97.06127, 32.83319)]
    """

    @staticmethod
    def __curvature(
        xs: npt.NDArray[np.float64], ys: npt.NDArray[np.float64], l_tot: float
    ) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """Compute the curvature of a B-spline curve.

        Notes
        -----
        This function is based on `nldi-xstool <https://code.usgs.gov/wma/nhgf/toolsteam/nldi-xstool>`__.

        Parameters
        ----------
        xs : array_like
            x coordinates of the points.
        ys : array_like
            y coordinates of the points.
        l_tot : float
            Total distance of points along the B-spline from the start point.

        Returns
        -------
        tuple of array_like
            Curvature and radius of curvature.
        """
        size = len(xs)
        dx = np.diff(xs, prepend=xs[0])
        dy = np.diff(ys, prepend=ys[0])
        phi = np.zeros(size) + np.pi * 0.5 * np.sign(dy)
        nonzero = np.nonzero(dx)

        phi[nonzero] = np.arctan2(dy[nonzero], dx[nonzero])
        phi[0] = (2.0 * phi[1]) - phi[2]

        rad = np.zeros(size) + 1.0e8
        scals = l_tot / (dx.size - 1)

        dphi = np.diff(np.abs(phi), prepend=np.abs(phi[0]))
        non_small = np.where(dphi > 1e-4)[0]
        rad[non_small] = scals / dphi[non_small]
        return phi, rad

    def __spline(self, npts_sp: int, degree: int = 3) -> Spline:
        """Create a B-spline curve from a set of points.

        Notes
        -----
        This function is based on https://stackoverflow.com/a/45928473/5797702.

        Parameters
        ----------
        npts_sp : int
            Number of points in the output spline curve.
        degree : int, optional
            Degree of the spline. Should be less than the number of points and
            greater than 1. Default is 3.

        Returns
        -------
        Spline
            A Spline object with ``x``, ``y``, ``phi``, ``radius``,
            and ``distance`` attributes.
        """
        degree = np.clip(degree, 1, self.npts_ln - 1)
        konts = np.clip(np.arange(self.npts_ln + degree + 1) - degree, 0, self.npts_ln - degree)
        spl = BSpline(konts, np.column_stack([self.x_ln, self.y_ln]), degree)

        x_sp, y_sp = spl(np.linspace(0, self.npts_ln - degree, max(npts_sp, 3), endpoint=False)).T
        x_sp = cast("npt.NDArray[np.float64]", x_sp)
        y_sp = cast("npt.NDArray[np.float64]", y_sp)
        phi_sp, rad_sp = self.__curvature(x_sp, y_sp, self.l_ln)
        geom = (
            LineString([(x1, y1), (x2, y2)])
            for x1, y1, x2, y2 in zip(x_sp[:-1], y_sp[:-1], x_sp[1:], y_sp[1:])
        )
        d_sp = gpd.GeoSeries(geom).set_crs(self.crs).length.cumsum().values
        if npts_sp < 3:
            idx = np.r_[:npts_sp]
            return Spline(x_sp[idx], y_sp[idx], phi_sp[idx], rad_sp[idx], d_sp[idx])

        return Spline(x_sp, y_sp, phi_sp, rad_sp, d_sp)

    def __init__(self, points: GDF, npts_sp: int, degree: int = 3) -> None:
        self.degree = degree
        self.crs = points.crs
        if self.crs is None:
            raise MissingCRSError

        if not self.crs.is_projected:
            raise InputTypeError("points.crs", "projected CRS")

        if any(points.geom_type != "Point"):
            raise InputTypeError("points.geom_type", "Point")
        self.points = points

        if npts_sp < 1:
            raise InputRangeError("npts_sp", ">= 1")
        self.npts_sp = npts_sp

        tx, ty = zip(*(g.xy for g in points.geometry))
        self.x_ln = np.array(tx, dtype="f8").squeeze()
        self.y_ln = np.array(ty, dtype="f8").squeeze()
        self.npts_ln = self.x_ln.size
        self.l_ln = LineString(points.geometry).length
        self._spline = self.__spline(npts_sp, degree)

    @property
    def spline(self) -> Spline:
        """Get the spline as a ``Spline`` object."""
        return self._spline


def snap2nearest(lines: GDF, points: GDF, tol: float) -> GDF:
    """Find the nearest points on a line to a set of points.

    Parameters
    ----------
    lines : geopandas.GeoDataFrame or geopandas.GeoSeries
        Lines.
    points : geopandas.GeoDataFrame or geopandas.GeoSeries
        Points to snap to lines.
    tol : float, optional
        Tolerance for snapping points to the nearest lines in meters.
        It must be greater than 0.0.

    Returns
    -------
    geopandas.GeoDataFrame or geopandas.GeoSeries
        Points snapped to lines.
    """
    if lines.crs is None or points.crs is None:
        raise MissingCRSError

    if not lines.crs.is_projected or not points.crs.is_projected:
        raise UnprojectedCRSError

    if isinstance(points, gpd.GeoSeries):
        pts = points.to_frame("geometry").reset_index()
    else:
        pts = points.copy()

    pts = cast("gpd.GeoDataFrame", pts)
    cols = list(pts.columns)
    cols.remove("geometry")
    pts_idx, ln_idx = lines.sindex.query_bulk(pts.buffer(tol))
    merged_idx = tlz.merge_with(list, ({p: f} for p, f in zip(pts_idx, ln_idx)))
    _pts = {
        pi: (
            *pts.iloc[pi][cols],
            ops.nearest_points(lines.iloc[fi].geometry.unary_union, pts.iloc[pi].geometry)[0],
        )
        for pi, fi in merged_idx.items()
    }
    pts = gpd.GeoDataFrame.from_dict(_pts, orient="index")
    pts.columns = cols + ["geometry"]
    pts = pts.set_geometry("geometry", crs=points.crs)
    pts = cast("gpd.GeoDataFrame", pts)

    if isinstance(points, gpd.GeoSeries):
        return pts.geometry
    return pts


def break_lines(lines: GDF, points: gpd.GeoDataFrame, tol: float = 0.0) -> GDF:
    """Break lines at specified points at given direction.

    Parameters
    ----------
    lines : geopandas.GeoDataFrame
        Lines to break at intersection points.
    points : geopandas.GeoDataFrame
        Points to break lines at. It must contain a column named ``direction``
        with values ``up`` or ``down``. This column is used to determine which
        part of the lines to keep, i.e., upstream or downstream of points.
    tol : float, optional
        Tolerance for snapping points to the nearest lines in meters.
        The default is 0.0.

    Returns
    -------
    geopandas.GeoDataFrame
        Original lines except for the parts that have been broken at the specified
        points.
    """
    if lines.crs is None or points.crs is None:
        raise MissingCRSError

    if lines.crs != points.crs or not lines.crs.is_projected or not points.crs.is_projected:
        raise UnprojectedCRSError

    if "direction" not in points.columns:
        raise MissingColumnError(["direction"])

    if (points.direction == "up").sum() + (points.direction == "down").sum() != len(points):
        raise InputValueError("direction", ["up", "down"])

    if not lines.geom_type.isin(["LineString", "MultiLineString"]).all():
        raise InputTypeError("geometry", "LineString or MultiLineString")

    crs_proj = lines.crs
    if tol > 0.0:
        points = snap2nearest(lines, points, tol)

    mlines = lines.geom_type == "MultiLineString"
    if mlines.any():
        lines.loc[mlines, "geometry"] = lines.loc[mlines, "geometry"].apply(lambda g: list(g.geoms))
        lines = lines.explode("geometry").set_crs(crs_proj)

    pts_idx, flw_idx = lines.sindex.query_bulk(points.geometry)
    if len(pts_idx) == 0:
        raise ValueError("No intersection between lines and points")  # noqa: TC003

    flw_geom = lines.iloc[flw_idx].geometry
    pts_geom = points.iloc[pts_idx].geometry
    pts_dir = points.iloc[pts_idx].direction
    idx = lines.iloc[flw_idx].index
    broken_lines = gpd.GeoSeries(
        [
            ops.substring(fl, *((0, fl.project(pt)) if d == "up" else (fl.project(pt), fl.length)))
            for fl, pt, d in zip(flw_geom, pts_geom, pts_dir)
        ],
        crs=crs_proj,
        index=idx,
    )
    out = lines.loc[idx].drop(columns="geometry")
    out = gpd.GeoDataFrame(out, geometry=broken_lines, crs=crs_proj)
    return out.to_crs(lines.crs)


def geometry_list(
    geometry: GTYPE | sgeom.Point | sgeom.MultiPoint | sgeom.LineString | sgeom.MultiLineString,
) -> list[sgeom.Polygon | sgeom.Point | sgeom.LineString]:
    """Get a list of polygons, points, and lines from a geometry."""
    if isinstance(geometry, (sgeom.Polygon, sgeom.LineString, sgeom.Point)):
        return [geometry]

    if isinstance(geometry, (sgeom.MultiPolygon, sgeom.MultiLineString, sgeom.MultiPoint)):
        return list(geometry.geoms)  # type: ignore

    if isinstance(geometry, (tuple, list)) and len(geometry) == 4:
        return [sgeom.box(*geometry)]
    valid_geoms = (
        "Polygon",
        "MultiPolygon",
        "tuple/list of length 4",
        "Point",
        "MultiPoint",
        "LineString",
        "MultiLineString",
    )
    raise InputTypeError("geometry", ", ".join(valid_geoms))


def query_indices(
    tree_gdf: gpd.GeoDataFrame | gpd.GeoSeries,
    input_gdf: gpd.GeoDataFrame | gpd.GeoSeries,
    predicate: str = "intersects",
) -> dict[Any, list[Any]]:
    """Find the indices of the input_geo that intersect with the tree_geo.

    Parameters
    ----------
    tree_gdf : geopandas.GeoDataFrame or geopandas.GeoSeries
        The tree geodataframe.
    input_gdf : geopandas.GeoDataFrame or geopandas.GeoSeries
        The input geodataframe.
    predicate : str, optional
        The predicate to use for the query operation, defaults to ``intesects``.

    Returns
    -------
    dict
        A dictionary of the indices of the ``input_gdf`` that intersect with the
        ``tree_gdf``. Keys are the index of ``input_gdf`` and values are a list
        of indices of the intersecting ``tree_gdf``.
    """
    if input_gdf.crs != tree_gdf.crs:
        raise MatchingCRSError

    in_iloc, tr_iloc = tree_gdf.sindex.query_bulk(input_gdf.geometry, predicate=predicate)
    idx_dict = defaultdict(set)
    for ii, it in zip(input_gdf.iloc[in_iloc].index, tree_gdf.iloc[tr_iloc].index):
        idx_dict[ii].add(it)
    return {k: list(v) for k, v in idx_dict.items()}


def nested_polygons(gdf: gpd.GeoDataFrame | gpd.GeoSeries) -> dict[int | str, list[int | str]]:
    """Get nested polygons in a GeoDataFrame.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame or geopandas.GeoSeries
        A GeoDataFrame or GeoSeries with (multi)polygons.

    Returns
    -------
    dict
        A dictionary where keys are indices of larger ploygons and
        values are a list of indices of smaller polygons that are
        contained within the larger polygons.
    """
    if not gdf.geom_type.str.contains("Polygon").all():
        raise InputTypeError("gdf", "dataframe with (Multi)Polygons")

    if gdf.crs is None or not gdf.crs.is_projected:
        raise UnprojectedCRSError

    centroid = gdf.centroid
    nested_idx = query_indices(centroid, gdf, "contains")
    nested_idx = {k: list(set(v).difference({k})) for k, v in nested_idx.items()}
    nested_idx = {k: v for k, v in nested_idx.items() if v}
    nidx = {tuple(set(v + [k])) for k, v in nested_idx.items()}
    area = gdf.area
    nested_keys = [area.loc[list(i)].idxmax() for i in nidx]
    nested_idx = {k: v for k, v in nested_idx.items() if k in nested_keys}
    return nested_idx
