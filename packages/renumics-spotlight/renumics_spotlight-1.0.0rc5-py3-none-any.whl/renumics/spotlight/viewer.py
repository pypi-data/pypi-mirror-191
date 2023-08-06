"""
This module allows user to start Spotlight from a python script/notebook.

Example:
    >>> import time
    >>> from renumics import spotlight
    >>> with spotlight.Dataset("docs/example.h5", "w") as dataset:
    ...     pass  # Create empty dataset
    >>> spotlight.instances()
    []
    >>> spotlight.show("docs/example.h5", "127.0.0.1", port=5001, no_browser=True, wait=False)
    Spotlight is running on http://127.0.0.1:5001/
    http://127.0.0.1:5001/
    >>> spotlight.instances()
    [http://127.0.0.1:5001/]
    >>> spotlight.close()
    >>> spotlight.instances()
    []

Example:
    >>> import time
    >>> from renumics import spotlight
    >>> with spotlight.Dataset("docs/example.h5", "w") as dataset:
    ...     pass  # Create empty dataset
    >>> viewer = spotlight.show(
    ...     "docs/example.h5",
    ...     "127.0.0.1", port=5001,
    ...     no_browser=True,
    ...     wait=False
    ... )
    Spotlight is running on http://127.0.0.1:5001/
    >>> viewer
    http://127.0.0.1:5001/
    >>> spotlight.close()

Example:
    >>> import time
    >>> import pandas as pd
    >>> from renumics import spotlight
    >>> df = pd.DataFrame({"a":[0, 1, 2], "b":["x", "y", "z"]})
    >>> viewer = spotlight.show(df, "127.0.0.1", port=5001, no_browser=True, wait=False)
    Spotlight is running on http://127.0.0.1:5001/
    >>> viewer
    http://127.0.0.1:5001/
    >>> viewer.get_df()["a"].to_list()
    [0, 1, 2]
    >>> spotlight.close()

"""

import dataclasses
import os
import threading
from contextlib import suppress
from typing import List, Union, Optional, Dict, Type

import pandas as pd
from loguru import logger
from typing_extensions import Literal
import ipywidgets as widgets
import IPython.display

import __main__
from renumics.spotlight.webbrowser import launch_browser_in_thread
from renumics.spotlight.dataset import ColumnType
from renumics.spotlight.backend.core.table_df import TableDf
from renumics.spotlight.layout import _LayoutLike
from renumics.spotlight.backend.server import setup, Server
from renumics.spotlight.backend.websockets import RefreshMessage


class ViewerNotFoundError(Exception):
    """
    Raised if a Spotlight viewer is not found.
    """


@dataclasses.dataclass(frozen=True)
class Viewer:
    """
    A Spotlight viewer. It corresponds to a single running Spotlight instance.

    Viewer can be created using the :func:`show` function.

    Attributes:
        host: host at which Spotlight is running
        port: port at which Spotlight is running
    """

    host: str
    port: int
    _thread: threading.Thread
    _server: Server

    def close(self, wait: bool = False) -> None:
        """
        Shutdown the corresponding Spotlight instance.
        """
        if wait:
            wait_event = threading.Event()
            timer: Optional[threading.Timer] = None

            def stop() -> None:
                wait_event.set()

            def on_connect(_: int) -> None:
                nonlocal timer
                if timer:
                    timer.cancel()
                    timer = None

            def on_disconnect(active_connections: int) -> None:
                if not active_connections:
                    ## create timer
                    nonlocal timer
                    timer = threading.Timer(3, stop)
                    timer.start()

            self._server.config.app.websocket_manager.add_disconnect_callback(  # type: ignore
                on_disconnect
            )
            self._server.config.app.websocket_manager.add_connect_callback(  # type: ignore
                on_connect
            )
            try:
                wait_event.wait()
            except KeyboardInterrupt as e:
                # cleanup on KeyboarInterrupt to prevent zombie processes
                self.close(wait=False)
                raise e

        self._server.should_exit = True
        self._thread.join()
        _VIEWERS.remove(self)

    def show(self) -> None:
        """
        Open the corresponding Spotlight instance in a browser.
        """
        launch_browser_in_thread(self.host, self.port)

    def refresh(self) -> None:
        """
        Refresh the corresponding Spotlight instance in a browser.
        """
        config = self._server.config
        config.app.websocket_manager.broadcast(RefreshMessage())  # type: ignore

    def get_df(self) -> Optional[pd.DataFrame]:
        """
        Get served `DataFrame` if a `DataFrame` is served, `None` otherwise.
        """
        config = self._server.config
        if hasattr(config.app, "data_source"):
            current_data_source = config.app.data_source.current_data_source()  # type: ignore
            if isinstance(current_data_source, TableDf):
                return current_data_source.df.copy()
        return None

    def update_df(
        self,
        df: Optional[pd.DataFrame] = None,
        dtype: Optional[Dict[str, Type[ColumnType]]] = None,
    ) -> None:
        """
        Replace `df` and/or its `dtype` if a `DataFrame` is served, do nothing
        otherwise.
        """
        config = self._server.config
        if not hasattr(config.app, "data_source"):
            logger.warning("App has no data source attached.")
            return
        if df is None and dtype is None:
            logger.warning("Neither `df` nor `dtype` is set, nothing to update.")
            return
        current_data_source = config.app.data_source.current_data_source()  # type: ignore
        if not isinstance(current_data_source, TableDf):
            logger.warning("Current data source is not a `DataFrame`.")
            return
        if df is None:
            df = current_data_source.df
        elif dtype is None:
            dtype = current_data_source.dtype
        config.app.data_source.open_dataframe(df, dtype)  # type: ignore
        self.refresh()

    def __repr__(self) -> str:
        return f"http://{self.host}:{self.port}/"

    def _ipython_display_(self) -> None:
        if self._server.should_exit:
            return

        # pylint: disable=undefined-variable
        if get_ipython().__class__.__name__ == "ZMQInteractiveShell":  # type: ignore
            # in notebooks display a rich html widget

            label = widgets.Label(
                f"Spotlight running on http://{self.host}:{self.port}/"
            )
            open_button = widgets.Button(
                description="open", tooltip="Open spotlight viewer"
            )
            close_button = widgets.Button(description="stop", tooltip="Stop spotlight")

            def on_click_open(_: widgets.Button) -> None:
                self.show()

            open_button.on_click(on_click_open)

            def on_click_close(_: widgets.Button) -> None:
                open_button.disabled = True
                close_button.disabled = True
                label.value = "Spotlight stopped"
                self.close()

            close_button.on_click(on_click_close)

            IPython.display.display(
                widgets.VBox([label, widgets.HBox([open_button, close_button])])
            )
        else:
            print(self)


_VIEWERS: List[Viewer] = []


def instances() -> List[Viewer]:
    """
    Get all active Spotlight viewer instances.
    """
    return list(_VIEWERS)


# pylint: disable=too-many-arguments
def show(
    dataset_or_folder: Union[str, os.PathLike, pd.DataFrame],
    host: str = "localhost",
    port: Union[int, Literal["auto"]] = "auto",
    layout: Optional[_LayoutLike] = None,
    no_browser: bool = False,
    wait: Union[bool, Literal["auto"]] = "auto",
    log_level: Union[
        int, Literal["trace", "debug", "info", "warning", "error", "critical"]
    ] = "error",
    dtype: Optional[Dict[str, Type[ColumnType]]] = None,
) -> Optional[Viewer]:
    """
    Start a new Spotlight viewer.

    Args:
        dataset_or_folder: root folder, dataset file or pandas.DataFrame (df) to open.
        host: optional host to run Spotlight at.
        port: optional port to run Spotlight at.
            If "auto" (default), automatically choose a random free port.
        layout: optional Spotlight :mod:`layout <renumics.spotlight.layout>`.
        no_browser: do not show Spotlight in browser.
        wait: If `True`, block code execution until all Spotlight browser tabs are closed.
            If `False`, continue code execution after Spotlight start.
            If "auto" (default), choose the mode automatically: non-blocking for
            `jupyter notebook`, `ipython` and other interactive sessions;
            blocking for scripts.
        log_level: optional log level to use in Spotlight server. In notebooks,
            server's output will be printed in the last visited cell, so low log
            levels can be confusing.
        dtype: Optional dict with mapping `column name -> column type` with
            column types allowed by Spotlight (for dataframes only).
    """
    with suppress(ViewerNotFoundError):
        close(port)  # type: ignore
    server_ = setup(dataset_or_folder, dtype, host, port, layout, log_level)

    try:
        thread = server_.run_in_thread()
    except RuntimeError as e:
        logger.warning(str(e))
        return None
    viewer = Viewer(server_.config.host, server_.config.port, thread, server_)

    in_interactive_session = not hasattr(__main__, "__file__")
    if wait == "auto":
        # `__main__.__file__` is not set in an interactive session, do not wait then.
        wait = not in_interactive_session

    if not in_interactive_session or wait:
        print(f"Spotlight is running on http://{viewer.host}:{viewer.port}/")

    _VIEWERS.append(viewer)
    if not no_browser:
        viewer.show()
    if wait:
        viewer.close(wait=True)

    return viewer


def close(port: Union[int, Literal["last"]] = "last") -> None:
    """
    Close an active Spotlight viewer.

    Args:
        port: optional port number at which the Spotlight viewer is running.
            If "last" (default), close the last started Spotlight viewer.

    Raises:
        ViewNotFoundError: if no Spotlight viewer found at the given `port`.
    """
    if port == "last":
        try:
            _VIEWERS[-1].close()
        except IndexError as e:
            raise ViewerNotFoundError("No active viewers found.") from e
        return
    for index, viewer in enumerate(_VIEWERS):
        if viewer.port == port:
            _VIEWERS[index].close()
            return
    raise ViewerNotFoundError(f"No viewer found at the port {port}.")
