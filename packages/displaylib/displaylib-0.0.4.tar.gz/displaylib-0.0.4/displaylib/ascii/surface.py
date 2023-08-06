from typing import Iterable
from typing_extensions import Self
from ..math import Vec2
from .node import ASCIINode
from .camera import ASCIICamera


class ASCIISurface:
    """ASCIISurface for displaying nodes
    """

    def __init__(self, nodes: Iterable[ASCIINode] = [], width: int = 16, height: int = 8) -> None:
        self._width = width
        self._height = height
        self.content = [[ASCIINode.cell_transparant for _ in range(width)] for _ in range(height)] # 2D array

        camera: ASCIICamera = ASCIICamera.current
        half_size = Vec2(self._width, self._height) // 2
        for node in nodes:
            if not node.visible:
                continue
            if not node.content:
                continue
            lines = len(node.content)
            longest = len(max(node.content, key=len))
            position = node.global_position - camera.global_position
            if camera.mode == ASCIICamera.CENTERED:
                position += half_size
            elif camera.mode == ASCIICamera.INCLUDE_SIZE:
                position -= Vec2(longest, lines) // 2
            elif camera.mode == ASCIICamera.CENTERED_AND_INCLUDE_SIZE:
                position += half_size
                position -= Vec2(longest, lines) // 2
            if position.y + lines < 0 or position.y > self._height:
                continue
            if position.x + longest < 0 or position.x > self._width:
                continue
            for h, line in enumerate(node.content):
                if not ((self._height) > (h + position.y) >= 0): # out of screen
                    continue
                for w, char in enumerate(line):
                    if not ((self._width) > (w + position.x) >= 0): # out of screen
                        continue
                    if char != ASCIINode.cell_transparant:
                        self.content[h+position.y][w+position.x] = char

    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self.content = [[ASCIINode.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array

    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, value: int) -> None:
        self._height = value
        self.content = [[ASCIINode.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array

    def clear(self) -> None:
        self.content = [[ASCIINode.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array
    
    def blit(self, surface: Self, position: Vec2 = Vec2(0, 0), transparent: bool = False) -> None:
        lines = len(surface.content)
        longest = len(max(surface.content, key=len))
        if position.x > longest and position.y > lines: # completely out of screen
            return
        for h, line in enumerate(surface.content):
            if self._height < h + position.y or position.y < 0: # line out of screen
                continue
            for w, char in enumerate(line):
                if self._width < w + position.x or position.x < 0: # char out of screen
                    continue

                current = self.content[h+position.y][w+position.x]
                if current == ASCIINode.cell_default: # empty rendered cell
                    if not transparent:
                        self.content[h+position.y][w+position.x] = char
                        continue
                self.content[h+position.y][w+position.x] = char
