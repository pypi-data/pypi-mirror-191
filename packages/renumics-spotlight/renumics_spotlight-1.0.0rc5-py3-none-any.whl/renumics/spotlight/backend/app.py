"""
start flask development server
"""

import asyncio
import os
from pathlib import Path
from typing import Any, Dict, Optional, Type

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from renumics.spotlight.dtypes.typing import ColumnType
from renumics.spotlight.licensing import spotlight_license
from renumics.spotlight.layout.nodes import Layout
from .apis import (
    table,
    user,
    filebrowser,
    layout as layout_api,
    config as config_api,
    websocket,
)
from .core.data_source import DataSource
from .settings import Settings
from .tasks.task_manager import TaskManager
from .middlewares.timing import add_timing_middleware
from .config import Config
from .websockets import WebsocketManager

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "table",
        "description": "Operations on Table slice and cells.",
    },
]


def create_app(
    settings: Optional[Settings] = None,
    layout: Optional[Layout] = None,
    dtype: Optional[Dict[str, Type[ColumnType]]] = None,
) -> FastAPI:
    """
    create app
    """

    app: Any = FastAPI()
    app.settings = Settings() if settings is None else settings

    app.spotlight_license = spotlight_license
    app.data_source = DataSource(app.settings)

    # if we launch spotlight with a file
    #   set the current file and the project root to the file's parent
    # if we launch it with a folder
    #   set the project_root to folder
    table_or_project_root = os.environ.get("SPOTLIGHT_TABLE_FILE")
    if table_or_project_root:
        if Path(table_or_project_root).is_file():
            app.settings.project_root = str(Path(table_or_project_root).parent)
            app.data_source.open_table(Path(table_or_project_root).name, dtype)
        elif Path(table_or_project_root).is_dir():
            app.settings.project_root = table_or_project_root
            app.settings.table_file = None
        else:
            app.settings.table_file = str(Path(table_or_project_root))

    if app.settings.dev:
        logger.info("Running in dev mode")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        add_timing_middleware(app)

    app.include_router(table.router, prefix="/api/table")
    table.add_error_handlers(app)
    app.include_router(user.router, prefix="/api/user")
    app.include_router(filebrowser.router, prefix="/api/browse")
    app.include_router(websocket.router, prefix="/api")
    app.include_router(layout_api.router, prefix="/api/layout")
    app.include_router(config_api.router, prefix="/api/config")

    app.task_manager = TaskManager()
    app.layout = layout
    app.config = Config()

    @app.on_event("startup")
    def _() -> None:
        loop = asyncio.get_running_loop()
        app.websocket_manager = WebsocketManager(loop)

    @app.on_event("shutdown")
    def _() -> None:
        app.task_manager.shutdown()

    try:
        app.mount(
            "/",
            StaticFiles(packages=["renumics.spotlight.backend"], html=True),
        )
    except AssertionError:
        logger.warning("Frontend folder does not exist. No frontend will be served.")

    return app
