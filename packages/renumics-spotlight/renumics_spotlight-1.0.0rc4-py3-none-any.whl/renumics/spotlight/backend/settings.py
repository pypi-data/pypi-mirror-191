"""
api settings
"""
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Fastapi settings module
    settings will be loaded from env variables or .env file
    """

    project_root: str = str(Path.cwd())
    table_file: Optional[str] = None
    dev: bool = False
    server_name = ""
    license_path = "renumics_license.key"

    class Config:
        """
        settings config
        set env prefix to spotlight_
        """

        env_prefix = "spotlight_"
