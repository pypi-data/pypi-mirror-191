import numpy as np
import warnings


def _kernel(function, dist, bandwidth, fixed=True):
    """
    Creates distanced-based kernel weights for geobootstrap

    In general, a fixed bandwidth suits more regular sample configurations,
    whereas an adaptive bandwidth suits irregular sample configurations

    Parameters
    ----------
    function : str
        Kernel function specified
    dist : array_like
        Distance vector
    bandwidth : int
        fixed bandwidth in metres
    fixed : bool
        whether to return a fixed or adaptive bandwidth

    Returns
    -------
    type: array_like
        distance-based kernel weights
    """

    if fixed is True:
        return _kernel_funcs(function, zs=dist / bandwidth)


def _kernel_funcs(function, zs):
    """
    modified from
    https://github.com/pysal/mgwr/blob/eef4f707fc2d34245c6cf0afeb85d742fdb90af5/mgwr/kernels.py#L65

    Parameters
    ----------
    function : str
        kernel function name
    zs : int
        distance / bandwidth

    Returns
    -------
    type: array_like
        kernel weights
    """

    functions = [
        "triangular",
        "uniform",
        "quadratic",
        "quartic",
        "gaussian",
        "bisquare",
        "exponential",
    ]

    if function != "gaussian":
        warnings.warn("Only Gaussian kernels have been tested")

    if function == "triangular":
        return 1 - zs
    elif function == "uniform":
        return np.ones(zs.shape) * 0.5
    elif function == "quadratic":
        return (3.0 / 4) * (1 - zs ** 2)
    elif function == "quartic":
        return (15.0 / 16) * (1 - zs ** 2) ** 2
    elif function == "gaussian":
        return np.exp(-0.5 * (zs) ** 2)
    elif function == "bisquare":
        return (1 - (zs) ** 2) ** 2
    elif function == "exponential":
        return np.exp(-zs)
    else:
        raise ValueError(
            f"Only the following kernels are supported: \
            {functions}"
        )
