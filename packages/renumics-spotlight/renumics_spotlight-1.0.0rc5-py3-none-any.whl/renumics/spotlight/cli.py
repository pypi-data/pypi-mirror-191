#!/usr/bin/env python3
"""
    Command line entrypoint for the renumics-spotlight python package
"""
import multiprocessing
import signal
import sys
from typing import Any, Dict, Optional, Tuple, Type, Union

import click

from renumics.spotlight import __version__
from renumics.spotlight.webbrowser import launch_browser_in_thread
from renumics.spotlight.backend.server import setup
from renumics.spotlight.dtypes.typing import ColumnType, COLUMN_TYPES_BY_NAME


def cli_dtype_callback(
    _ctx: click.Context, _param: click.Option, value: Tuple[str, ...]
) -> Optional[Dict[str, Type[ColumnType]]]:
    """
    Parse column types from multiple strings in format
    `COLUMN_NAME=DTYPE` to a dict.
    """
    if not value:
        return None
    dtype = {}
    for mapping in value:
        try:
            column_name, dtype_name = mapping.split("=")
        except ValueError as e:
            raise click.BadParameter(
                "Column type setting separator '=' not specified or specified "
                "more than once."
            ) from e
        try:
            column_type = COLUMN_TYPES_BY_NAME[dtype_name]
        except KeyError as e:
            raise click.BadParameter(
                f"Column types from {list(COLUMN_TYPES_BY_NAME.keys())} "
                f"expected, but value '{dtype_name}' recived."
            ) from e
        dtype[column_name] = column_type
    return dtype


@click.command()
@click.argument("table-or-folder", type=str, required=False)
@click.option(
    "--host",
    "-h",
    default="localhost",
    help="The host that Spotlight should listen on.",
    show_default=True,
)
@click.option(
    "--port",
    "-p",
    type=str,
    default="auto",
    help="The port that Spotlight should listen on (use 'auto' to use a random free port)",
    show_default=True,
)
@click.option(
    "--layout",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Preconfigured layout to use as default.",
)
@click.option(
    "--dtype",
    type=click.UNPROCESSED,
    callback=cli_dtype_callback,
    multiple=True,
    help="Custom column types setting (use COLUMN_NAME={"
    + "|".join(sorted(COLUMN_TYPES_BY_NAME.keys()))
    + "} notation). Multiple settings allowed.",
)
@click.option(
    "--no-browser",
    is_flag=True,
    default=False,
    help="Do not automatically show Spotlight in browser.",
)
@click.version_option(__version__)
def main(
    table_or_folder: str,
    host: str,
    port: Union[int, str],
    layout: Optional[str],
    dtype: Optional[Dict[str, Type[ColumnType]]],
    no_browser: bool,
) -> None:
    """
    Parse CLI arguments and launch Renumics Spotlight.
    """
    # pylint: disable=too-many-arguments
    server = setup(table_or_folder, dtype, host, port, layout)

    def _sigint_handler(*_args: Any) -> None:
        if server.should_exit:
            sys.tracebacklimit = 0
            processes = multiprocessing.active_children()
            for process in processes:
                process.terminate()
        server.should_exit = True

    signal.signal(signal.SIGINT, _sigint_handler)

    if not no_browser:
        launch_browser_in_thread(server.config.host, server.config.port)
    server.run()
