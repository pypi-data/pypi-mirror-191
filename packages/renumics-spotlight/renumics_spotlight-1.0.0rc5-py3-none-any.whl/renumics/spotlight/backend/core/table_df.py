"""
access pandas DataFrame table data
"""
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Type, cast

import numpy as np
import pandas as pd
import trimesh
from loguru import logger

from renumics.spotlight.dataset import _get_current_datetime
from renumics.spotlight.dtypes import (
    Category,
    Embedding,
    Mesh,
    Window,
)
from renumics.spotlight.dtypes.exceptions import InvalidFile
from renumics.spotlight.dtypes.typing import (
    ColumnType,
    ColumnTypeMapping,
    get_column_type,
    get_column_type_name,
    is_array_based_column_type,
    is_column_type,
    is_file_based_column_type,
    is_scalar_column_type,
)
from renumics.spotlight.io.pandas import (
    infer_dtype,
    is_empty,
    prepare_column,
    try_literal_eval,
)
from renumics.spotlight.licensing import username
from .table_base import (
    sanitize_values,
    CellsUpdate,
    Column,
    ConversionFailed,
    TableBase,
    read_external_value,
)
from ..settings import Settings


class UnsupportedDType(Exception):
    """
    Data type is not supported.
    """


class TableDf(TableBase):
    """
    access pandas DataFrame table data
    """

    _settings: Settings
    _generation_id: int
    _uid: str
    _df: pd.DataFrame
    _dtype: ColumnTypeMapping
    _inferred_dtype: ColumnTypeMapping

    @property
    def column_names(self) -> List[str]:
        return self._df.columns.to_list()

    @property
    def df(self) -> pd.DataFrame:
        """
        Get **a copy** of the served `DataFrame`.
        """
        return self._df.copy()

    @property
    def dtype(self) -> Optional[ColumnTypeMapping]:
        """
        Get **a copy** of dict with the desired data types.
        """
        if self._dtype is None:
            return None
        return self._dtype.copy()

    def __init__(
        self,
        settings: Settings,
        df: pd.DataFrame,
        dtype: Optional[ColumnTypeMapping] = None,
    ):
        self._settings = settings
        self._generation_id = 0
        self._uid = str(id(df))
        self._df = df.copy()
        self._dtype = dtype.copy() if dtype else {}
        for column_name, dtype_ in self._dtype.items():
            if not is_column_type(dtype_):
                raise UnsupportedDType(
                    f"Desired column type {dtype_} (for the column "
                    f"'{column_name}') is not a valid Spotlight data type."
                )
        self._inferred_dtype = self._dtype.copy()
        for column_name in df:
            if column_name not in self._inferred_dtype:
                try:
                    dtype_ = infer_dtype(df[column_name])
                except ValueError:
                    dtype_ = str
                self._inferred_dtype[column_name] = dtype_

    def __len__(self) -> int:
        return len(self._df)

    def get_generation_id(self) -> int:
        return self._generation_id

    def get_uid(self) -> str:
        return self._uid

    def get_name(self) -> str:
        if self._settings.table_file is None:
            return ""
        return str(Path(self._settings.table_file).name)

    def get_columns(self, column_names: Optional[List[str]] = None) -> List[Column]:
        if column_names is None:
            column_names = self._df.columns.to_list()
        columns = []
        for column_name in column_names:
            try:
                column = self.get_column(column_name, None)
            except Exception as e:  # pylint: disable=broad-except
                if column_name in self._dtype:
                    raise e
                logger.warning(str(e))
            else:
                columns.append(column)

        return columns

    def get_column(self, column_name: str, indices: Optional[List[int]]) -> Column:
        try:
            column = self._convert_pandas_column(column_name, indices)
            return column
        except Exception as e:
            raise ValueError(
                f"Cannot convert column '{column_name}' to the type "
                f"`{self._dtype[column_name].__name__}`."
            ) from e

    def get_cell_data(self, column_name: str, row_index: int) -> Any:
        """
        Return the value of a single cell, warn if not possible.
        """
        # pylint: disable=too-many-return-statements, too-many-branches
        self._assert_column_exists(column_name)
        self._assert_index_exists(row_index)

        column_index = self._df.columns.get_loc(column_name)
        raw_value = self._df.iloc[row_index, column_index]
        dtype = self._inferred_dtype[column_name]

        if dtype is Category:
            if pd.isna(raw_value):
                return -1
            categories = self._get_column_categories(column_name)
            return categories.get(raw_value, -1)
        if dtype is datetime:
            value = pd.to_datetime(raw_value).to_numpy("datetime64[us]").tolist()
            # `tolist()` returns `None` for all `NaT`s, `datetime` otherwise.
            if value is None:
                return ""
            return value.isoformat()
        if dtype is str:
            if pd.isna(raw_value):
                return ""
            return str(raw_value)
        if is_scalar_column_type(dtype):
            # `dtype` is `bool`, `int` or `float`.
            dtype = cast(Type[Union[bool, int, float]], dtype)
            try:
                return dtype(raw_value)
            except (TypeError, ValueError) as e:
                raise ConversionFailed(dtype, raw_value) from e
        if dtype is np.ndarray:
            if isinstance(raw_value, str):
                raw_value = try_literal_eval(raw_value)
            if is_empty(raw_value):
                return None
            return np.asarray(raw_value)
        if dtype is Window:
            if isinstance(raw_value, str):
                raw_value = try_literal_eval(raw_value)
            if is_empty(raw_value):
                return np.full(2, np.nan)
            try:
                value = np.asarray(raw_value, dtype=float)
            except (TypeError, ValueError) as e:
                raise ConversionFailed(dtype, raw_value) from e
            if value.ndim != 1 or len(value) != 2:
                raise ValueError(
                    f"Window column cells should be sequences of shape (2,), "
                    f"but a sequence of shape {value.shape} received for the "
                    f"column '{column_name}'."
                )
        if is_empty(raw_value):
            return None
        if isinstance(raw_value, str):
            raw_value = try_literal_eval(raw_value)
        if isinstance(raw_value, trimesh.Trimesh) and dtype is Mesh:
            value = Mesh.from_trimesh(raw_value)
            return value.encode()
        if isinstance(raw_value, str) and is_file_based_column_type(dtype):
            try:
                return read_external_value(str(raw_value), dtype)
            except Exception as e:
                raise ConversionFailed(dtype, raw_value) from e
        if not isinstance(raw_value, dtype) and is_array_based_column_type(dtype):
            try:
                value = dtype(raw_value)
            except (InvalidFile, TypeError, ValueError) as e:
                raise ConversionFailed(dtype, raw_value) from e
            return value.encode()
        if isinstance(raw_value, dtype):
            return raw_value.encode()
        raise ConversionFailed(dtype, raw_value)

    def replace_cells(
        self, column_name: str, indices: List[int], value: Any
    ) -> CellsUpdate:
        """
        replace multiple cell's value
        """
        self._generation_id += 1
        self._assert_column_exists(column_name)
        self._assert_indices_exist(indices)

        column_index = self._df.columns.get_loc(column_name)
        old_values = self._df.iloc[indices, column_index]
        dtype = self._inferred_dtype[column_name]

        categories = None
        if dtype is Category:
            # Convert category code to category.
            categories = self._get_column_categories(column_name)
            value = next((cat for cat, i in categories.items() if i == value), np.nan)
        elif value is None:
            value = self._get_default_value(dtype)

        try:
            self._df.iloc[indices, column_index] = pd.Series([value] * len(indices))
        except Exception as e:
            self._df.iloc[indices, column_index] = old_values
            raise e

        new_value = self._df.iloc[indices[0], column_index]
        if dtype is Category:
            # Back-project category onto its code.
            new_value = -1 if categories is None else categories.get(new_value, -1)

        return CellsUpdate(
            value=sanitize_values(new_value),
            author=username,
            edited_at=_get_current_datetime().isoformat(),
        )

    def delete_column(self, name: str) -> None:
        """
        remove a column from the table
        """
        self._generation_id += 1
        self._assert_column_exists(name)
        del self._df[name]
        del self._inferred_dtype[name]

    def delete_row(self, index: int) -> None:
        """
        remove a row from the table
        """
        self._generation_id += 1
        self._assert_index_exists(index)
        self._df = self._df.drop(index=self._df.index[index], axis=0)

    def duplicate_row(self, index: int) -> int:
        """
        duplicate a row in the table
        """
        self._generation_id += 1
        self._assert_index_exists(index)
        self._df = pd.concat(
            [
                self._df.iloc[:index],
                self._df.iloc[index : index + 1],
                self._df.iloc[index:],
            ]
        )
        return index + 1

    def append_column(self, name: str, dtype_name: str) -> Column:
        """
        add a column to the table
        """
        self._generation_id += 1
        self._assert_column_not_exists(name)
        dtype = get_column_type(dtype_name)

        value = self._get_default_value(dtype)
        if dtype is Window:
            self._df[name] = [value] * len(self)
            self._dtype[name] = Window
        else:
            self._df[name] = value
            inferred_dtype = infer_dtype(self._df[name])
            if inferred_dtype is not dtype:
                logger.warning(
                    f"Newly added column {name} has type {dtype}, but "
                    f"automatically inferred type would be {inferred_dtype}."
                )
        self._inferred_dtype[name] = dtype
        try:
            return self._convert_pandas_column(name)
        except Exception as e:
            del self._df[name]
            self._dtype.pop(name, None)
            del self._inferred_dtype[name]
            raise e

    def _get_default_value(self, dtype: Type[ColumnType]) -> Any:
        if dtype is int:
            return 0
        if dtype is bool:
            return False
        if dtype is str:
            return ""
        if dtype is Window:
            return [float("nan"), float("nan")]
        # `dtype` is `float`, `datetime`, `np.ndarray`, or a custom data type.
        return np.nan

    @lru_cache()
    def _get_column_categories(self, column_name: str) -> Dict[str, int]:
        """
        Get categories of a categorical column.

        At the moment, there is no way to add a new category in Spotlight, so we
        rely on the previously cached ones.
        """
        self._assert_column_exists(column_name)
        dtype = self._inferred_dtype[column_name]
        if dtype is not Category:
            raise UnsupportedDType(
                f"Column categories exist for categorical columns only, but "
                f"column '{column_name}' of type {dtype} received."
            )
        column = self._convert_pandas_column(column_name)
        if column.categories is None:
            return {}
        return column.categories

    def _convert_pandas_column(
        self, column_name: str, indices: Optional[List[int]] = None
    ) -> Column:
        # pylint: disable=too-many-branches, too-many-statements
        self._assert_column_exists(column_name)

        dtype = self._inferred_dtype[column_name]
        column = self._df[column_name]
        if indices is not None:
            column = column.iloc[indices]
        column = prepare_column(column, dtype)

        categories = None
        embedding_length = None
        references = None

        if dtype is Category:
            # `NaN` category is listed neither in `pandas`, not in our format.
            categories = {
                category: i for i, category in enumerate(column.cat.categories)
            }
            column = column.cat.codes
            values = column.to_numpy()
        elif dtype is datetime:
            # We expect datetimes as ISO strings; empty strings instead of `NaT`s.
            column = column.dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            column = column.mask(column.isna(), "")
            values = column.to_numpy()
        elif dtype is str:
            # Replace `NA`s with empty strings.
            column = column.mask(column.isna(), "")
            values = column.to_numpy()
        elif is_scalar_column_type(dtype):
            values = column.to_numpy()
        elif dtype is Window:
            # Replace all `NA` values with `[NaN, NaN]`.
            na_mask = column.isna()
            column.iloc[na_mask] = pd.Series(
                [[float("nan"), float("nan")]] * na_mask.sum()
            )
            # This will fail, if arrays in column cells aren't aligned.
            try:
                values = np.asarray(column.to_list(), dtype=float)
            except ValueError as e:
                raise ValueError(
                    f"For the window column '{column_name}', column cells "
                    f"should be sequences of shape (2,) or `NA`s, but "
                    f"unaligned sequences received."
                ) from e
            if values.ndim != 2 or values.shape[1] != 2:
                raise ValueError(
                    f"For the window column '{column_name}', column cells "
                    f"should be sequences of shape (2,) or `NA`s, but "
                    f"sequences of shape {values.shape[1:]} received."
                )
        elif dtype is Embedding:
            na_mask = column.isna()
            # This will fail, if arrays in column cells aren't aligned.
            try:
                embeddings = np.asarray(column[~na_mask].to_list(), dtype=float)
            except ValueError as e:
                raise ValueError(
                    f"For the window column '{column_name}', column cells "
                    f"should be sequences of the same shape (n,) or `NA`s, but "
                    f"unaligned sequences received."
                ) from e
            if embeddings.ndim != 2 or embeddings.shape[1] == 0:
                raise ValueError(
                    f"For the window column '{column_name}', column cells "
                    f"should be sequences of the same shape (n,) or `NA`s, but "
                    f"sequences of shape {values.shape[1:]} received."
                )
            if na_mask.any():
                values = np.empty(len(column), dtype=object)
                values[np.where(~na_mask)[0]] = list(embeddings)
            embedding_length = embeddings.shape[1]
        else:
            # A reference column. `dtype` is one of `np.ndarray`, `Audio`,
            # `Image`, `Mesh`, `Sequence1D` or `Video`. Don't try to check or
            # convert values at the moment.
            na_mask = column.isna()
            references = na_mask.to_numpy()
            if is_file_based_column_type(dtype):
                # Strings are paths or URLs, let them inplace. Replace
                # non-strings with empty strings.
                column = column.mask(~(column.map(type) == str), "")
                values = column.to_numpy()
            else:
                values = np.full(len(column), "")
        return Column(
            type_name=get_column_type_name(dtype),
            type=dtype,
            order=None,
            hidden=column_name.startswith("_"),
            optional=True,
            description=None,
            tags=[],
            editable=dtype in (bool, int, float, str, Category, Window),
            categories=categories,
            x_label=None,
            y_label=None,
            embedding_length=embedding_length,
            has_lookup=False,
            is_external=False,
            name=column_name,
            values=values,
            references=references,
        )
