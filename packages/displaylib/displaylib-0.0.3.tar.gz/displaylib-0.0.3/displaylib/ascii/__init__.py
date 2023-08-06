"""ASCII submodule from DisplayLib
"""

__all__ = [
    "Vec2",
    "overload",
    "OverloadUnmatched",
    "Node",
    "Engine",
    "Camera",
    "Screen",
    "Surface",
    "Image",
    "Client",
    "Clock"
]

from ..math import Vec2
from ..overload import overload, OverloadUnmatched
from .node import ASCIINode as Node
from .engine import ASCIIEngine as Engine
from .camera import ASCIICamera as Camera
from .surface import ASCIISurface as Surface
from .screen import ASCIIScreen as Screen
from .image import ASCIIImage as Image
from .client import ASCIIClient as Client
from .clock import Clock
# from .constants import * # TODO: find out whether to include this

# activate ANSI escape codes
import os as _os
_os.system("")
# _os.system("cls") # used when developing
del _os
