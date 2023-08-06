"""
access h5 table data
"""
from hashlib import sha1
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from renumics.spotlight.dataset import INTERNAL_COLUMN_NAMES
from renumics.spotlight.dataset.exceptions import InvalidIndexError
from renumics.spotlight.dtypes import Category
from renumics.spotlight.dtypes.typing import get_column_type
from renumics.spotlight.licensing import FeatureNotLicensed
from renumics.spotlight.typing import PathType
from .table_base import (
    CellsUpdate,
    NoTableFileFound,
    CouldNotOpenTableFile,
    InvalidLicense,
    NoRowFound,
    ColumnNotEditable,
    InvalidCategory,
    Column,
    TableBase,
)
from ..settings import Settings
from .dataset import H5Dataset


class TableH5(TableBase):
    """
    access h5 table data
    """

    def __init__(
        self,
        settings: Settings,
        table_file: PathType,
    ):
        self._settings = settings
        self._table_file = Path(table_file)

    @property
    def column_names(self) -> List[str]:
        with self._open_table() as dataset:
            return dataset.keys()

    def __len__(self) -> int:
        with self._open_table() as dataset:
            return len(dataset)

    def get_generation_id(self) -> int:
        with self._open_table() as dataset:
            return dataset.get_generation_id()

    def get_uid(self) -> str:
        return sha1(str(self._table_file.absolute()).encode("utf-8")).hexdigest()

    def get_name(self) -> str:
        return str(self._table_file.name)

    def get_columns(self, column_names: Optional[List[str]] = None) -> List[Column]:
        with self._open_table() as dataset:
            if column_names is None:
                column_names = dataset.keys()
            return [dataset.read_column(column_name) for column_name in column_names]

    def get_internal_columns(self) -> List[Column]:
        with self._open_table() as dataset:
            return [
                dataset.read_column(column_name)
                for column_name in INTERNAL_COLUMN_NAMES
            ]

    def get_column(self, column_name: str, indices: Optional[List[int]]) -> Column:
        with self._open_table() as dataset:
            return dataset.read_column(column_name, indices=indices)

    def get_cell_data(self, column_name: str, row_index: int) -> Any:
        """
        return the value of a single cell
        """
        with self._open_table() as dataset:
            try:
                return dataset.read_value(column_name, row_index)
            except IndexError as e:
                raise NoRowFound(str(e)) from e

    def replace_cells(
        self, column_name: str, indices: List[int], value: Any
    ) -> CellsUpdate:
        """
        replace multiple cell's value
        """

        with self._open_table("r+") as dataset:
            # we can't assign an int value to a float cell in spotlight atm
            # but json numbers don't have distinct float and int types,
            # so we convert ints to float values for now
            attrs = dataset.read_attrs(column_name)
            if not attrs.editable:
                raise ColumnNotEditable(f"Column {column_name} is not editable.")
            if value is not None:
                if attrs.type is float:
                    value = float(value)
                elif attrs.type is Category:
                    categories = cast(Dict, attrs.categories)
                    if value == -1:
                        value = None
                    else:
                        try:
                            value = list(categories.keys())[
                                list(categories.values()).index(value)
                            ]
                        except ValueError as e:
                            raise InvalidCategory() from e

            try:
                dataset[column_name, indices] = value
                new_value = dataset.read_value(column_name, indices[0])
            except IndexError as e:
                raise NoRowFound(str(e)) from e

            edited_at = dataset.read_value("__last_edited_at__", indices[0])
            author = dataset.read_value("__last_edited_by__", indices[0])

            author = cast(str, author)
            edited_at = cast(str, edited_at)
            return CellsUpdate(value=new_value, author=author, edited_at=edited_at)

    def delete_column(self, name: str) -> None:
        """
        remove a column from the table
        """
        with self._open_table("r+") as dataset:
            del dataset[name]

    def delete_row(self, index: int) -> None:
        """
        remove a row from the table
        """

        with self._open_table("r+") as dataset:
            try:
                del dataset[index]
            except InvalidIndexError as e:
                raise NoRowFound from e

    def duplicate_row(self, index: int) -> int:
        """
        duplicate a row in the table
        """

        with self._open_table("r+") as dataset:
            try:
                dataset.duplicate_row(index, index + 1)
                return index + 1
            except InvalidIndexError as e:
                raise NoRowFound from e

    def append_column(self, name: str, dtype_name: str) -> Column:
        """
        add a column to the table
        """

        with self._open_table("r+") as dataset:
            dtype = get_column_type(dtype_name)
            order = dataset.min_order() - 1

            if dtype is int:
                dataset.append_column(
                    name,
                    dtype,
                    optional=True,
                    editable=True,
                    default=0,
                    order=order,
                )
            elif dtype is bool:
                dataset.append_column(
                    name,
                    dtype,
                    optional=True,
                    editable=True,
                    default=False,
                    order=order,
                )
            else:
                dataset.append_column(
                    name, dtype, optional=True, editable=True, order=order
                )

            return dataset.read_column(name)

    def _open_table(self, mode: str = "r") -> H5Dataset:
        try:
            return H5Dataset(self._table_file, mode)
        except FileNotFoundError as e:
            raise NoTableFileFound(str(e)) from e
        except OSError as e:
            raise CouldNotOpenTableFile(str(e)) from e
        except FeatureNotLicensed as e:
            raise InvalidLicense(str(e)) from e
