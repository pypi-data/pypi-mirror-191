"""
access pandas DataFrame table data
"""
import ast
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Dict, Type, Union, cast

import numpy as np
import pandas as pd

from renumics import spotlight
from renumics.spotlight import dtypes
from renumics.spotlight.licensing import username
from renumics.spotlight.dataset.typing import ColumnType
from .table_base import (
    CellsUpdate,
    InvalidExternalData,
    NoRowFound,
    Column,
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
    _dtype: Dict[str, Type[ColumnType]]
    _inferred_dtype: Dict[str, Type[ColumnType]]

    @property
    def df(self) -> pd.DataFrame:
        """
        Get **a copy** of the served `DataFrame`.
        """
        return self._df.copy()

    @property
    def dtype(self) -> Dict[str, Type[ColumnType]]:
        """
        Get **a copy** of dict with the desired data types.
        """
        return self._dtype.copy()

    def __init__(
        self,
        settings: Settings,
        df: pd.DataFrame,
        dtype: Optional[Dict[str, Type[ColumnType]]] = None,
    ):
        self._settings = settings
        self._generation_id = 0
        self._uid = str(id(df))
        self._df = df.copy()
        self._dtype = dtype if dtype is not None else {}
        self._inferred_dtype = {}

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
            column_names = self._df.keys()
        columns = []
        for column_name in column_names:
            column = self._col_from_df_col(column_name)
            if column is not None:
                columns.append(column)
        return columns

    def get_column(self, column_name: str, indices: Optional[List[int]]) -> Column:
        column = self._col_from_df_col(column_name)
        if column is None:
            raise ValueError(f'Column "{column_name}" is not supported.')
        if indices is not None:
            column.values = column.values[indices]
        return column

    def get_cell_data(self, column_name: str, row_index: int) -> Any:
        """
        return the value of a single cell
        """
        # pylint: disable=too-many-branches, too-many-statements, too-many-return-statements
        try:
            dtype = self._inferred_dtype[column_name]
        except KeyError as e:
            raise spotlight.dataset.exceptions.ColumnNotExistsError(
                f'Column "{column_name}" is not recognized.'
            ) from e
        try:
            raw_value = self._df[column_name].iloc[row_index]
        except IndexError as e:
            raise NoRowFound(str(e)) from e
        if pd.isna(raw_value) or (
            raw_value in ("", b"") and dtype not in (str, spotlight.Category)
        ):
            if dtype is spotlight.Window:
                return np.full(2, np.nan)
            if dtype is spotlight.Category:
                return -1
            return None
        if issubclass(
            dtype, dtypes._BaseFileBasedData  # pylint: disable=protected-access
        ):
            try:
                return read_external_value(str(raw_value), dtype)
            except Exception as e:
                raise InvalidExternalData(
                    f"File {raw_value} does not exist or is not readable by the "
                    f"`spotlight.{dtype.__name__}` class."
                ) from e
        if dtype in (
            np.ndarray,
            spotlight.Window,
            spotlight.Embedding,
            spotlight.Sequence1D,
        ):
            if isinstance(raw_value, str):
                raw_value = ast.literal_eval(raw_value)
            if dtype is spotlight.Sequence1D:
                return spotlight.Sequence1D(raw_value).encode()
            return np.asarray(raw_value, dtype=float)
        if dtype is spotlight.Category:
            column = self._col_from_df_col(column_name)
            if column is None or column.categories is None:
                return -1
            return column.categories.get(raw_value, -1)
        if dtype is datetime:
            value: Optional[datetime] = (
                pd.to_datetime(raw_value).to_numpy().astype("datetime64[us]").tolist()
            )
            if value is not None:
                return value.isoformat()
            return ""
        dtype = cast(Type[Union[bool, int, float, str]], dtype)
        return dtype(raw_value)

    def replace_cells(
        self, column_name: str, indices: List[int], value: Any
    ) -> CellsUpdate:
        """
        replace multiple cell's value
        """
        # pylint: disable=too-many-branches
        self._generation_id += 1
        try:
            column_index = self._df.columns.get_loc(column_name)
        except KeyError as e:
            raise spotlight.dataset.exceptions.ColumnNotExistsError(
                f'Column "{column_name}" does not exist.'
            ) from e
        try:
            old_values = self._df.iloc[indices, column_index]
        except IndexError as e:
            raise NoRowFound(str(e)) from e

        dtype = self._inferred_dtype[column_name]
        attrs: Dict[str, Any] = {}
        if dtype is spotlight.Category:
            column = self._df[column_name]
            (
                _,
                _,
                attrs,
            ) = spotlight.dataset._convert_pandas_column(  # pylint: disable=protected-access
                column, self._dtype.get(column_name)
            )
            if value == -1:
                if "" in column.cat.categories:
                    value = ""
                else:
                    value = np.nan
            else:
                value = attrs["categories"][value]
        elif value is None:
            if dtype is int:
                value = 0
            elif dtype is bool:
                value = False
            elif dtype is float:
                value = np.nan
            elif dtype is str:
                value = ""
            elif dtype is spotlight.Window:
                value = [np.nan, np.nan]
            else:
                raise UnsupportedDType(
                    f"Data type {type(dtype).__name__} does not support editing in df."
                )

        try:
            self._df.iloc[indices, column_index] = pd.Series([value] * len(indices))
        except Exception as e:
            self._df.iloc[indices, column_index] = old_values
            raise e

        if dtype is spotlight.Category:
            try:
                new_value = attrs["categories"].index(value)
            except ValueError:
                new_value = -1
        else:
            new_value = self._df.iloc[indices[0], column_index]

        return CellsUpdate(
            value=new_value,
            author=username,
            edited_at=spotlight.dataset._get_current_datetime().isoformat(),  # pylint: disable=protected-access
        )

    def delete_column(self, name: str) -> None:
        """
        remove a column from the table
        """
        self._generation_id += 1
        try:
            del self._df[name]
        except KeyError as e:
            raise spotlight.dataset.exceptions.ColumnNotExistsError(
                f'Column "{name}" does not exist.'
            ) from e

    def delete_row(self, index: int) -> None:
        """
        remove a row from the table
        """
        self._generation_id += 1
        try:
            index = self._df.index[index]
        except IndexError as e:
            raise NoRowFound(str(e)) from e
        self._df = self._df.drop(index=index, axis=0)

    def duplicate_row(self, index: int) -> int:
        """
        duplicate a row in the table
        """
        self._generation_id += 1
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
        if name in self._df.keys():
            raise spotlight.dataset.exceptions.ColumnExistsError(
                f'Column "{name}" already exists.'
            )
        spotlight.Dataset.check_column_name(name)

        dtype = spotlight.dataset._get_column_type(dtype_name)

        if dtype is int:
            self._df[name] = 0
        elif dtype is bool:
            self._df[name] = False
        elif dtype is float:
            self._df[name] = np.nan
        elif dtype is str:
            self._df[name] = ""
        elif dtype is spotlight.Window:
            self._df[name] = [[np.nan, np.nan]] * len(self._df)
            self._dtype[name] = spotlight.Window
        else:
            raise UnsupportedDType(
                f"Data type {dtype_name} is not supported in df column creation."
            )
        column = self._col_from_df_col(name)
        return cast(Column, column)

    def _col_from_df_col(self, name: str) -> Optional[Column]:
        # pylint: disable=too-many-branches, too-many-statements
        # pylint: disable=too-many-return-statements, too-many-locals
        # pylint: disable=invalid-unary-operand-type, broad-except
        try:
            column = self._df[name]
        except KeyError as e:
            raise spotlight.dataset.exceptions.ColumnNotExistsError(
                f'Column "{name}" does not exist.'
            ) from e
        (
            values,
            dtype,
            convert_attrs,
        ) = spotlight.dataset._convert_pandas_column(  # pylint: disable=protected-access
            column, self._dtype.get(name)
        )
        if values is None or dtype is None:
            return None
        references: Optional[np.ndarray] = None
        is_external = False
        embedding_length = None
        categories = None
        null_mask = pd.isna(values)
        if issubclass(
            dtype, dtypes._BaseFileBasedData  # pylint: disable=protected-access
        ):
            references = ~pd.isna(values)
            is_external = True
        elif dtype is spotlight.Sequence1D:
            try:
                for value in values[~null_mask]:
                    _ = spotlight.Sequence1D(value)
            except Exception:
                return None
            values = np.full(values, "")
            references = ~null_mask
        elif dtype is spotlight.Embedding:
            try:
                data = spotlight.dataset._asarray(  # pylint: disable=protected-access
                    list(values[~null_mask])
                ).astype(float)
            except Exception:
                return None
            if data.ndim != 2 or len(data) != (~null_mask).sum():
                return None
            references = ~null_mask
            embedding_length = data.shape[1]
        elif dtype is np.ndarray:
            try:
                for value in values[~null_mask]:
                    _ = np.asarray(value)
            except Exception:
                return None
            values = np.full(values, "")
            references = ~null_mask
        elif dtype is spotlight.Window:
            default = np.empty(1, dtype=object)
            default[0] = np.array([np.nan, np.nan])
            values[null_mask] = default
            try:
                values = spotlight.dataset._asarray(  # pylint: disable=protected-access
                    values.tolist()
                ).astype(float)
            except Exception:
                return None
            if values.shape != ((~null_mask).sum(), 2):
                return None
        elif dtype is spotlight.Category:
            cat_column = pd.Categorical(values, convert_attrs.get("categories", []))
            values = cat_column.codes
            categories = {
                key: value for value, key in enumerate(cat_column.categories.to_list())
            }
        elif dtype is datetime:
            values = np.array(
                [None if x is None else x.isoformat() for x in values.tolist()]
            )
        elif dtype in (bool, int):
            if null_mask.any():
                return None
        self._inferred_dtype[name] = dtype
        values = cast(np.ndarray, values)
        return Column(
            values=values,
            references=references,
            name=name,
            type_name=spotlight.dataset._get_column_type_name(  # pylint: disable=protected-access
                dtype
            ),
            type=dtype,
            order=None,
            hidden=name[0] == "_",
            optional=True,
            description=None,
            tags=[],
            editable=dtype
            in (bool, int, float, str, spotlight.Category, spotlight.Window),
            categories=categories,
            x_label=None,
            y_label=None,
            embedding_length=embedding_length,
            has_lookup=False,
            is_external=is_external,
        )
