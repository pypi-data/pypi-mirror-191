from typing_extensions import Self
from ..math import Vec2
from ..template import Node
from .types import ASCIISurface


class ASCIINode(Node):
    cell_transparant = " " # type used to indicate that a cell is transparent in `content`
    cell_default = " " # the default look of an empty cell
    # per instance
    visible: bool = False

    def __init__(self, owner: Self | None = None, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(owner, x, y, z_index)
        if force_sort:
            Node._request_sort = True # requests the Engine to sort every frame a new node is created
        self.content = [] # 2D array
    
    def _render(self, surface: ASCIISurface) -> None:
        return
    
    def _resize(self, size: Vec2) -> None:
        return
