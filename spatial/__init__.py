"""Top-level package for spatial."""
__author__ = """Fabrice Normandin"""
__email__ = """normandf@mila.quebec"""
__version__ = """0.0.1"""
__version_info__ = tuple(int(n) for n in __version__.split('.'))

from .space import Space
from .discrete import Discrete

__all__ = ["Space", "Discrete"]