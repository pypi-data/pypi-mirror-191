from scipy.spatial.distance import cdist
from geobootstrap.utils import _get_coords, _check_bandwidth
from geobootstrap.kernel import _kernel


def geobootstrap(
    gdf1,
    gdf2,
    coords1=None,
    coords2=None,
    r=1000,
    kernel="gaussian",
    metric="euclidean",
    bandwidth=1000,
    fixed=True,
):
    """
    Bootstrap a GeoDataFrame using defined kernel weights,
    determined by a distance decay function to another GeoDataFrame

    Parameters
    ----------
    gdf1 : gpd.GeoDataFrame
        GeoDataFrame to calculate distances from
    gdf2 : gpd.GeoDataFrame
        GeoDataFrame to calculate distances to
    coords1: array_like
        two dimensional array containing x, y values for sources
   coords2: array_like
        two dimensional array containing x, y values for gdf2
    r : int
        how many resamples with replacement to return
    kernel : str
        kernel distance-decay function
    metric : str
        how to calculate distances between coordinates
    bandwidth : int
       bandwidth (distance)
    fixed: bool
        whether to apply a fixed or adaptive (knn) kernel

    Returns
    -------
    type : list
        list of GeoPandas.GeoDataFrames
    """

    if fixed is False:
        raise ValueError("Only fixed bandwidths are currently supported")

    if coords1 is None:
        coords1 = _get_coords(gdf1)
    if coords2 is None:
        coords2 = _get_coords(gdf2)

    # Check bw if all observations will have at least 1 neighbour
    _check_bandwidth(coords1, coords2, bandwidth)
    # Compute distances between coords
    dist = cdist(coords2, coords1, metric)
    # Calculate kernel for each gdf2 observation
    ks = _kernel(kernel, dist, bandwidth, fixed)

    return [gdf1.sample(n=r, weights=k, replace=True) for k in ks]
