"""Pygame submodule from DisplayLib

Raises:
    ModuleNotFoundError: `pygame` was not found
"""

__all__ = [
    "Vec2",
    "overload",
    "OverloadUnmatched",
    "Node",
    "Engine"
]

try: # check if pygame is installed
    import pygame as _pygame
    import os as _os
    _os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
    del _os
    _pygame.init() # init without displaying message
    del _pygame
except ModuleNotFoundError as error:
    raise ModuleNotFoundError("pygame is required to import this submodule") from error

from ..math import Vec2
from ..overload import overload, OverloadUnmatched
from .node import PygameNode as Node
from .engine import PygameEngine as Engine
