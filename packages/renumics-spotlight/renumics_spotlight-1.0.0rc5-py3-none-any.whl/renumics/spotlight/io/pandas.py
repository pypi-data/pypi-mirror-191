"""
This module contains helpers for importing `pandas.DataFrame`s.
"""

import ast
import os.path
from contextlib import suppress
from datetime import datetime
from typing import Any, Optional, Type

import pandas as pd
import validators

from renumics.spotlight.dtypes import Category
from renumics.spotlight.dtypes.exceptions import NotADType
from renumics.spotlight.dtypes.typing import (
    COLUMN_TYPES_BY_NAME,
    ColumnType,
    is_column_type,
    is_file_based_column_type,
    is_scalar_column_type,
)
from renumics.spotlight.typing import PathOrURLType, PathType


def is_empty(value: Any) -> bool:
    """
    Check if value is `NA` or an empty string.
    """
    # We need to check for a string type before checking for an empty string
    # because of arrays.
    return pd.isna(value) or (isinstance(value, str) and value == "")


def try_literal_eval(x: str) -> Any:
    """
    Try to evaluate a literal expression, otherwise return value as is.
    """
    with suppress(Exception):
        return ast.literal_eval(x)
    return x


def prepare_path_or_url(path_or_url: PathOrURLType, workdir: PathType) -> str:
    """
    For a relative path, prefix it with the `workdir`.
    For an absolute path or an URL, do nothing.
    """
    path_or_url_str = str(path_or_url)
    if validators.url(path_or_url_str):
        return path_or_url_str
    return os.path.join(workdir, path_or_url_str)


def infer_dtype(column: pd.Series) -> Type[ColumnType]:
    """
    Get an equivalent Spotlight data type for a `pandas` column, if possible.

    At the moment, only scalar data types can be inferred.

    Nullable boolean and integer `pandas` dtypes have no equivalent Spotlight
    data type and will be read as strings.

    Float, string, and category data types are allowed to have `NaN`s.

    Args:
        column: A `pandas` column to infer dtype from.

    Returns:
        Inferred dtype.

    Reises:
        ValueError: If dtype cannot be inferred automatically.
    """
    if pd.api.types.is_bool_dtype(column) and not column.hasnans:
        return bool
    if pd.api.types.is_categorical_dtype(column):
        return Category
    if pd.api.types.is_integer_dtype(column) and not column.hasnans:
        return int
    if pd.api.types.is_float_dtype(column):
        return float
    if pd.api.types.is_datetime64_any_dtype(column):
        return datetime
    # `is_string_dtype` only checks `object` dtype, it's not enough.
    if (
        pd.api.types.is_string_dtype(column)
        and ((column.map(type) == str) | (column.isna())).all()
    ):
        return str
    raise ValueError("Column dtype cannot be inferred automatically.")


def is_string_mask(column: pd.Series) -> pd.Series:
    """
    Return mask of column's elements of type string.
    """
    return column.map(type) == str


def prepare_column(
    column: pd.Series, dtype: Type[ColumnType], workdir: Optional[PathType] = None
) -> pd.Series:
    """
    Convert a `pandas` column to the desired `dtype` and prepare some values,
    but still as `pandas` column.

    Args:
        column: A `pandas` column to prepare.
        dtype: Target data type.
        workdir: Directory to prefix relative paths. For file-based data only.

    Returns:
        Prepared `pandas` column.

    Raises:
        TypeError: If `dtype` is not a Spotlight data type.
    """
    column = column.copy()

    if dtype is Category:
        column = column.mask(column.isna(), None).astype("category")
        # We only support string/`NA` categories, but `pandas` can more, so
        # force categories to be strings (does not affect `NA`s).
        return column.cat.rename_categories(column.cat.categories.astype(str))

    if dtype is datetime:
        # `errors="coerce"` will produce `NaT`s instead of fail.
        return pd.to_datetime(column, errors="coerce")

    if dtype is str:
        # Allow `NA`s, convert all other elements to strings.
        return column.astype(str).mask(column.isna(), None)

    if is_scalar_column_type(dtype):
        # `dtype` is `bool`, `int` or `float`.
        return column.astype(dtype)

    if not is_column_type(dtype):
        raise NotADType(
            "`dtype` should be one of Spotlight data types ("
            + ", ".join(COLUMN_TYPES_BY_NAME.keys())
            + f"), but {dtype} received."
        )

    # We consider empty strings as `NA`s.
    str_mask = is_string_mask(column)
    column[str_mask] = column[str_mask].replace("", None)
    na_mask = column.isna()

    # When `pandas` reads a csv, arrays and lists are read as literal strings,
    # try to interpret them.
    str_mask = is_string_mask(column)
    column[str_mask] = column[str_mask].apply(try_literal_eval)

    if workdir is not None and is_file_based_column_type(dtype):
        # For file-based data types, relative paths should be resolved.
        str_mask = is_string_mask(column)
        column[str_mask] = column[str_mask].apply(prepare_path_or_url)

    return column.mask(na_mask, None)
