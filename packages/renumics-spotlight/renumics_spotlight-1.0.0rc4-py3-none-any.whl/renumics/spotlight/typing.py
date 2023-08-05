"""
Common types and type guards.
"""
import os
from typing import Any, Iterable, List, Union

import numpy as np
from typing_extensions import TypeGuard


BoolType = Union[bool, np.bool_]
IntType = Union[int, np.integer]
FloatType = Union[float, np.floating]
NumberType = Union[IntType, FloatType]

PathType = Union[str, os.PathLike]
PathOrURLType = Union[str, os.PathLike]

IndexType = Union[int, np.integer]
Indices1DType = Union[
    slice, List[int], List[np.integer], List[bool], List[np.bool_], np.ndarray
]


def is_bool(x: Any) -> TypeGuard[Union[bool, np.bool_]]:
    """
    Check whether `x` is boolean.
    """
    if isinstance(x, (bool, np.bool_)):
        return True
    return False


def is_integer(x: Any) -> TypeGuard[Union[int, np.integer]]:
    """
    Check whether `x` is integer.
    """
    if isinstance(x, (int, np.integer)):
        return True
    return False


def is_iterable(x: Any) -> TypeGuard[Iterable]:
    """
    Check whether `x` is iterable. Strings and bytes are considered as
    non-iterable.
    """
    if isinstance(x, (str, bytes)):
        return False
    try:
        iter(x)
    except TypeError:
        return False
    return True
