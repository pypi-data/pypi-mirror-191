from typing import Tuple
from .fastxm import *
import numpy as np


__doc__ = fastxm.__doc__
__all__ = ["intersect_1d"]


def _intersect_1d(a, b, parallel):
    assert isinstance(a, np.ndarray) and isinstance(
        b, np.ndarray
    ), "a and b must be numpy arrays"
    assert a.dtype == b.dtype, "a and b must have the same dtype"
    assert a.ndim == 1 and b.ndim == 1, "a and b must be 1D arrays"
    # if not ints, try to convert to ints
    # if not possible, force conversion to ints using hash
    if a.dtype != np.int64:
        try:
            a = a.astype(np.int64)
            b = b.astype(np.int64)
        except:
            a = a.astype(object)
            b = b.astype(object)
            a = hash_array(a)
            b = hash_array(b)

    if parallel:
        if a.dtype == np.int64:
            return par_i1d_i64(a, b)
        elif a.dtype == np.int32:
            return par_i1d_i32(a, b)
        elif a.dtype == np.int16:
            return par_i1d_i16(a, b)
        elif a.dtype == np.int8:
            return par_i1d_i8(a, b)
        elif a.dtype == np.uint64:
            return par_i1d_u64(a, b)
        elif a.dtype == np.uint32:
            return par_i1d_u32(a, b)
        elif a.dtype == np.uint16:
            return par_i1d_u16(a, b)
        elif a.dtype == np.uint8:
            return par_i1d_u8(a, b)
        raise ValueError("Unsupported dtype: {}".format(a.dtype))
    else:
        if a.dtype == np.int64:
            return i1d_i64(a, b)
        elif a.dtype == np.int32:
            return i1d_i32(a, b)
        elif a.dtype == np.int16:
            return i1d_i16(a, b)
        elif a.dtype == np.int8:
            return i1d_i8(a, b)
        elif a.dtype == np.uint64:
            return i1d_u64(a, b)
        elif a.dtype == np.uint32:
            return i1d_u32(a, b)
        elif a.dtype == np.uint16:
            return i1d_u16(a, b)
        elif a.dtype == np.uint8:
            return i1d_u8(a, b)
        raise ValueError("Unsupported dtype: {}".format(a.dtype))


def intersect_1d(
    a: np.ndarray, b: np.ndarray, parallel: bool = False
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns two arrays containing the indices of the intersection of a and b.

    Parameters
    ----------
    a : numpy.ndarray
        1D array of integers.
    b : numpy.ndarray
        1D array of integers.
    parallel : bool, optional
        If True, the intersection is computed in parallel using Rayon.

    Returns
    -------
    a_idx : numpy.ndarray
        1D array of indices of the intersection of a and b.
    b_idx : numpy.ndarray
        1D array of indices of the intersection of b and a.

    Examples
    --------
    >>> a = np.array([1, 2, 3, 4, 5])
    >>> b = np.array([2, 3, 4, 5, 6])
    >>> a_idx, b_idx = intersect_1d(a, b)
    >>> a_idx
    array([1, 2, 3, 4])
    >>> b_idx
    array([0, 1, 2, 3])
    """
    a_ix, b_ix = _intersect_1d(a, b, parallel)
    return a_ix, b_ix
