# Expose key components at the package level
from .core import KazParser
from .validators import SchemaValidator
from .exporters import SQLExporter
from .plugins.transformers import EmailNormalizer, TimestampAdder

__all__ = [
    "KazParser",
    "SchemaValidator",
    "SQLExporter",
    "EmailNormalizer",
    "TimestampAdder"
]

__version__ = "0.1.0"