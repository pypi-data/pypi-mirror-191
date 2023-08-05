"""
    Facilities for plugin loading and registration.
"""

import importlib
import pkgutil

import renumics.spotlight.plugins as plugins_namespace


def load_plugins() -> dict:
    """
    Automatically load and register plugins
    inside the renumics.spotlight.plugins namespace package.
    """
    plugins = {}

    for _, name, _ in pkgutil.iter_modules(plugins_namespace.__path__):
        plugin = importlib.import_module(plugins_namespace.__name__ + "." + name)
        plugins[name] = plugin

    return plugins
