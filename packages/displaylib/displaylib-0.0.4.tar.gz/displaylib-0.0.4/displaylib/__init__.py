"""DisplayLib

Submodules:
- template
- ascii (default)
- pygame
"""

__version__ = "0.0.4"
__author__ = "FloatingInt"
__all__ = [
    "Vec2",
    "overload",
    "OverloadUnmatched",
    "ASCIINode",
    "ASCIIEngine",
    "ASCIICamera",
    "ASCIISurface",
    "ASCIIScreen",
    "ASCIIImage",
    "ASCIIClient",
    "Clock"
]

# utility
from .overload import overload, OverloadUnmatched
from .math import Vec2
# default module
from .ascii import (
    Node as ASCIINode,
    Engine as ASCIIEngine,
    Camera as ASCIICamera,
    Surface as ASCIISurface,
    Screen as ASCIIScreen,
    Image as ASCIIImage,
    Client as ASCIIClient,
    Frame as Frame,
    Animation as Animation,
    EmptyAnimation as EmptyAnimation,
    AnimationPlayer as AnimationPlayer,
    Clock as Clock
)