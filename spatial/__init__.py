# -*- coding: utf-8 -*-
"""Top-level package for spatial."""

__author__ = """Fabrice Normandin"""
__email__ = """normandf@mila.quebec"""
__version__ = """0.0.1"""
__version_info__ = tuple(int(n) for n in __version__.split('.'))

from .spatial import Discrete
def __contains__(self: Discrete, val):
    if not isinstance(val, int):
        return False
    try:
        int_val = int(val)
    except TypeError:
        return False
    else:
        if int_val != val:
            return False
    return self.contains(val)

Discrete.__contains__ = __contains__

__all__ = ["Discrete"]
