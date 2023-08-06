import logging

from .zplconfig import ZplConfig
from .zplwriter import ZplWriter

try:
    # Python 3.8+
    import importlib.metadata as importlib_metadata
except ImportError:
    # <Python 3.7 and lower
    import importlib_metadata  # type: ignore

logger = logging.getLogger()

__version__ = importlib_metadata.version(__name__)

__all__ = [
    "__version__",
    "ZplWriter",
    "ZplConfig",
]
