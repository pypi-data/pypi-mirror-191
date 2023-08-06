from typing_extensions import Self
from ..math import Vec2
from ..template import Node
from .node import ASCIINode
from .types import ASCIISurface, ModeFlags


class ASCIICamera(Node):
    """ASCIICamera for moving the viewport
    """
    FIXED = 1
    CENTERED = 3
    INCLUDE_SIZE = 5
    CENTERED_AND_INCLUDE_SIZE = 8
    current: Self

    def __init__(self, owner: ASCIINode | None = None, x: int = 0, y: int = 0, follow: bool = False, mode: ModeFlags = FIXED) -> None:
        self.owner = owner
        self.position = Vec2(x, y)
        self.mode = mode # `centered` mode only has effect if ´owner´ != None
        self.follow = follow # whether to follow the ´owner´
        self.content = [] # NOTE: attr ´content´ won't be used because ´visible´ will always be False
    
    @property
    def visible(self) -> int:
        return False # static, because it won't be displayed

    @property
    def z_index(self) -> int:
        return 0 # z_index is static, because it's required for the sort algorithm

    @property
    def z_index(self) -> int:
        return 0 # z_index static, because it's required for the sort algorithm
    
    def _update(self, delta: float) -> None:
        if self.follow and self.owner != None:
            self.global_position = self.owner.global_position
    
    def _render(self, surface: ASCIISurface) -> None:
        return

ASCIICamera.current = ASCIICamera() # default camera
