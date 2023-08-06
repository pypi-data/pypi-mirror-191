"""provides access to different data sources (h5, pandas, etc.)"""

import os
from pathlib import Path
from typing import Optional, Dict, Type

import pandas as pd
from loguru import logger

from renumics.spotlight import Dataset
from renumics.spotlight.dtypes.typing import ColumnType
from .table_base import TableBase, InvalidPath
from .table_df import TableDf
from .table_h5 import TableH5
from ..settings import Settings


class DataSource:
    """provides access to different data sources (h5, pandas, etc.)"""

    _settings: Settings
    _data_source: Optional[TableBase]

    def __init__(self, settings: Settings):
        self._settings = settings
        self._data_source = None

    def open_dataframe(
        self, df: pd.DataFrame, dtype: Optional[Dict[str, Type[ColumnType]]]
    ) -> None:
        """open dataframe"""
        self._data_source = TableDf(self._settings, df=df, dtype=dtype)

    def open_table(
        self, path: str, dtype: Optional[Dict[str, Type[ColumnType]]] = None
    ) -> None:
        """
        open the specified table file

        :raises InvalidPath: if the supplied path is outside the project root
                             or points to an incompatible file
        """
        # Reject any files outside the project folder
        # once we rely on python 3.9 or newer this check can be replaced with:
        # Path(...).is_relative_to(...)
        file_path = os.path.abspath(Path(self._settings.project_root) / path)
        root_path = os.path.abspath(self._settings.project_root)

        if os.path.commonpath([root_path]) != os.path.commonpath(
            [root_path, file_path]
        ):
            raise InvalidPath()

        if Path(file_path).suffix == ".h5":
            self._data_source = TableH5(self._settings, Path(file_path))
        elif Path(file_path).suffix == ".csv":
            # For csv files:
            # 1. Create a corresponding table with suffix .h5
            #    next to the .csv file
            #    (add (#) to the name if the file already exists)
            # 2. Import the data
            # 3. Set this file as the current table_file

            table_path = Path(file_path).with_suffix(".h5")
            idx = 1
            while table_path.is_file():
                table_path = table_path.with_name(
                    Path(file_path).stem + f"({idx})"
                ).with_suffix(".h5")
                idx += 1

            logger.info(f"Importing csv (as {table_path})")
            with Dataset(table_path, "w") as dataset:
                dataset.from_csv(file_path, dtype=dtype)

            self._data_source = TableH5(self._settings, table_path)

        else:
            # reject any filetypes we don't explicitly handle above
            raise InvalidPath()

    def current_data_source(self) -> Optional[TableBase]:
        """get current (opened) table data source"""
        if self._data_source is None:
            if self._settings.table_file is not None:
                self.open_table(self._settings.table_file)
        return self._data_source
