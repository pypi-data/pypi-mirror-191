"""
Renumics Spotlight
"""

from .__version__ import __version__
from ._build_variant import __build_variant__
from .dataset import Dataset
from .dtypes import (
    Audio,
    Category,
    Embedding,
    Image,
    Mesh,
    Sequence1D,
    Video,
    Window,
)
from .viewer import Viewer, close, instances, show
from .plugin_loader import load_plugins

load_plugins()

__all__ = [
    "show",
    "close",
    "instances",
    "Viewer",
]
