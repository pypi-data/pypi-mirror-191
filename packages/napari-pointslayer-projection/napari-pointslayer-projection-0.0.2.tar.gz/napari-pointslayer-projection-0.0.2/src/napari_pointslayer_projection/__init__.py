try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
from ._widget import project_points

__all__ = ("project_points",)
