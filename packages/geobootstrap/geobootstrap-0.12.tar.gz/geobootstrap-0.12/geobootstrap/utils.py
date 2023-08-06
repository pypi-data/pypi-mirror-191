import math
import warnings
import numpy as np
import geopandas as gpd
from scipy.spatial import cKDTree


def _get_coords(gdf, method="random", size=1, batch_size=1000):
    """
    Get array containing x,y coordinates from GeoDataFrame

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame to return coordinates from
    method : str
        what method to use to sample polygons
    size : int (default: 1)
        number of random points to generate within polygon (default 1)
    batch_size : int (default: 1000)
        number of random points to generate within bounds

    Returns
    -------
    type : np.array
        array containing x and y values
    """

    geom_type = gdf.type.values

    if "x" and "y" in gdf:
        return gdf[["x", "y"]].values

    else:
        if geom_type.any() == "Point":
            x, y = gdf.geometry.x, gdf.geometry.y
            return np.array([x, y]).T

        elif geom_type.any() in ("Polygon", "MultiPolygon"):
            if method == "random":
                return sample_points(gdf, size, batch_size)
            else:
                x_mids, y_mids = _calculate_mid_points(gdf.bounds)
                return np.array([x_mids, y_mids]).T

        elif geom_type.any() in ("LineString", "MultiLineString"):
            raise ValueError("Not suppported")


def sample_points(gdf, size, batch_size):
    """
    Get array containing x,y coordinates from GeoDataFrame

    Parameters
    ----------
    gdf : gpd.GeoDataFrame

    size : int (default: 1)
        number of random points to generate within polygon (default 1)
    batch_size : int (default: 1000)
        number of random points to generate within bounds

    Returns
    -------
    type : np.array
        array containing x and y values
    """

    geoms = gdf.geometry.apply(_uniform_polygon, size=size)

    g = gpd.GeoDataFrame(geometry=geoms, crs=gdf.crs)

    g["x"] = g.geometry.x
    g["y"] = g.geometry.y

    return g[["x", "y"]].values


def _uniform_polygon(geom, size=1, batch_size=None):
    """
    Return n points contained within a polygon

    Parameters
    ----------
    geom : gpd.GeoDataFrame.geometry
        geometry for a gpd.GeoDataFrame
    size : int (default: 1)
        number of random points to generate within polygon (default 1)
    batch_size : int (default: 1000)
        number of random points to generate within bounds

    Returns
    -------
    type : gpd.GeoSeries
        GeoSeries containing n points contained within a polygon
    """
    from geopandas.array import points_from_xy
    from geopandas.geoseries import GeoSeries

    n_points = size

    if batch_size is None:
        batch_size = n_points

    xmin, ymin, xmax, ymax = geom.bounds

    candidates = []

    while len(candidates) < n_points:
        batch = points_from_xy(
            x=np.random.uniform(xmin, xmax, size=batch_size),
            y=np.random.uniform(ymin, ymax, size=batch_size),
        )
        valid_samples = batch[batch.sindex.query(geom, predicate="contains")]
        candidates.extend(valid_samples)

    return GeoSeries(candidates[:n_points]).unary_union


def _calculate_mid_points(bounds):
    """
    Calculate middle points based on the geometry bounds

    Parameters
    ----------
    bounds : array_like
        array containing xmin, ymin, xmax, ymax

    Returns
    -------
    type: np.array
        x_mids : mid points of x values
        y_mids : mid points of y values
    """

    # Calculate mid points for x and y bound coords
    x_mids = (bounds[:, 0] + bounds[:, 2]) / 2.0
    y_mids = (bounds[:, 1] + bounds[:, 3]) / 2.0

    return x_mids, y_mids


def _check_bandwidth(coords1, coords2, bandwidth):

    """A function that checks whether the bandwidth set
    allows for pooling from at least 1 neighbour

    Parameters
    ----------
    coords1: np.array
        array containing x,y coordinate pairs
    coords2: np.array
        array containing x,y coordinate pairs
    bandwidth: int
        fixed distance for finding neighbours

    Returns
    -------
    int: (optional)
        bandwidth

    """

    # Create KD-tree
    tree = cKDTree(coords1)
    # Get number of neighbours within bandwidth
    k = tree.query_ball_point(coords2, r=bandwidth, return_length=True)
    # If any observation has less than 1 neighbour,
    # then calculate the minimum distance for each to have neighbours
    if np.any(k <= 1) is True:
        d, i = tree.query(coords2, k=1)
        max_d = math.ceil(d.max())

        warnings.warn(
            f"The bandwidth: {bandwidth} will result in the indexes:"
            f"{i} not having any values pooled. If this is not desired, use"
            f"a bandwidth greater than {max_d}"
        )
