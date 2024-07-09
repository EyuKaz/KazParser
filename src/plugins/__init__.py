"""
KazParser Plugins Subpackage

This subpackage contains various plugins for data transformation and processing.
"""

# Expose key components at the subpackage level
from .transformers import EmailNormalizer, TimestampAdder

__all__ = [
    "EmailNormalizer",
    "TimestampAdder"
]

# Optional: Add plugin registration logic
_PLUGINS = {
    "email_normalizer": EmailNormalizer,
    "timestamp_adder": TimestampAdder,
}

def get_plugin(plugin_name, *args, **kwargs):
    """
    Retrieve a plugin by name.

    Args:
        plugin_name (str): Name of the plugin to retrieve.
        *args, **kwargs: Arguments to pass to the plugin constructor.

    Returns:
        An instance of the requested plugin.

    Raises:
        ValueError: If the plugin name is not recognized.
    """
    if plugin_name not in _PLUGINS:
        raise ValueError(f"Unknown plugin: {plugin_name}")
    return _PLUGINS[plugin_name](*args, **kwargs)