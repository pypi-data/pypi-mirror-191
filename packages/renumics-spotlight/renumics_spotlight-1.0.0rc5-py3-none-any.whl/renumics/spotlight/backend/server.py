"""
Setup for Spotlight server and browser.
"""

import contextlib
import inspect
import os
import threading
import time
import socket
from pathlib import Path
from typing import Dict, Iterable, Optional, Type, Union
from urllib.parse import unquote, urlsplit

import click
import pandas as pd
import requests
import uvicorn
import validators
from loguru import logger
from typing_extensions import Literal

from renumics.spotlight.typing import PathOrURLType, PathType
from renumics.spotlight.dtypes.typing import ColumnType
from renumics.spotlight.layout import _LayoutLike, parse
from .app import create_app


def find_free_port() -> int:
    """Find are free port between 1024 and 65535"""
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("", 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock.getsockname()[1]


def is_port_in_use(port: int) -> bool:
    """check if port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("localhost", port)) == 0


class Server(uvicorn.Server):
    """
    Our custom Uvicorn server.
    """

    def run_in_thread(self) -> threading.Thread:
        """
        Run Uvicorn in separate thread.
        """
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        time.sleep(0.1)
        # Wait 2 seconds for server to start.
        for _ in range(20):
            if self.started:
                return thread
            if not thread.is_alive():
                break
            time.sleep(0.1)
        raise RuntimeError("Spotlight not started.")


def download_table(
    url: str,
    supported_extensions: Iterable[str],
    workdir: PathType = ".",
    timeout: int = 30,
) -> str:
    """
    Download a table file with one of the supported extensions form the given
    URL and save it to the `workdir` with the original name.
    If a file with original name already exists, add numeric suffix to its name.

    Returns:
        Path to the downloaded table file.
    """
    filename = unquote(urlsplit(url).path).split("/")[-1]
    if not filename:
        raise ValueError("Cannot parse file name from the given URL.")
    if not any(filename.endswith(ext) for ext in supported_extensions):
        raise ValueError(
            "Invalid file extension parsed from the given URL.\n"
            "Supported are: " + ", ".join(supported_extensions)
        )
    table_folder = Path(workdir)
    # If a file exists at the given path, `FileExistsError` will be raised.
    table_folder.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading '{url}'.")
    response = requests.get(url, timeout=timeout)
    if not response.ok:
        raise ValueError("Given URL could not be reached.")

    table_path = table_folder / filename
    stem = table_path.stem
    idx = 1
    while table_path.is_file():
        table_path = table_path.with_name(stem + f"({idx})").with_suffix(
            table_path.suffix
        )
        idx += 1
    with table_path.open("wb") as f:
        f.write(response.content)
    return str(table_path)


def setup(
    table_or_folder: Optional[PathOrURLType],
    dtype: Optional[Dict[str, Type[ColumnType]]] = None,
    host: str = "localhost",
    port: Union[int, str] = "auto",
    layout: Optional[_LayoutLike] = None,
    log_level: Union[
        int, Literal["trace", "debug", "info", "warning", "error", "critical"]
    ] = "info",
) -> Server:
    """
    Prepare Renumics Spotlight server for launching.
    """
    # pylint: disable=too-many-arguments, too-many-branches
    supported_extensions = (".h5", ".csv")
    df_to_serve = None

    if table_or_folder is None:
        if "SPOTLIGHT_TABLE_FILE" not in os.environ:
            os.environ["SPOTLIGHT_TABLE_FILE"] = str(Path.cwd())

    # dataframe support
    elif isinstance(table_or_folder, pd.DataFrame):
        df_to_serve = table_or_folder
        os.environ["SPOTLIGHT_TABLE_FILE"] = "__df_in_memory__"

    # url support
    elif isinstance(table_or_folder, str) and validators.url(table_or_folder):
        try:
            table_path = download_table(table_or_folder, supported_extensions)
        except Exception as e:
            raise click.BadArgumentUsage(
                f"Spotlight dataset wasn't downloaded from the given URL: "
                f"{table_or_folder}.\n{e}"
            )
        os.environ["SPOTLIGHT_TABLE_FILE"] = table_path

    elif not Path(table_or_folder).exists():
        raise click.BadArgumentUsage(f"Given path '{table_or_folder}' does not exist.")

    # file support
    elif Path(table_or_folder).is_file():
        if Path(table_or_folder).suffix in supported_extensions:
            os.environ["SPOTLIGHT_TABLE_FILE"] = str(table_or_folder)
        else:
            raise click.BadArgumentUsage(
                inspect.cleandoc(
                    f"""
                    Invalid file extension!
                        Supported: {", ".join(supported_extensions)}
                    """
                )
            )

    else:  # folder
        os.environ["SPOTLIGHT_TABLE_FILE"] = str(table_or_folder)

    app = create_app(layout=None if layout is None else parse(layout), dtype=dtype)
    if df_to_serve is not None:
        app.data_source.open_dataframe(df_to_serve, dtype)  # type: ignore

    if port == "auto":
        port_number = find_free_port()
    else:
        port_number = int(port)

    config = uvicorn.Config(
        app,
        host=host,
        port=port_number,
        log_level=log_level,
        http="httptools",
        ws="wsproto",
        workers=4,
        reload=os.environ.get("SPOTLIGHT_DEV") == "true",
    )
    server = Server(config)
    return server
