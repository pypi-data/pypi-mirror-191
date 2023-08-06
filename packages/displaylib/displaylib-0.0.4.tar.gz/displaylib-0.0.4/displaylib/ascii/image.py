import io
import os
from ..math import Vec2
from .types import FilePath
from .surface import ASCIISurface


class _ASCIINodeStruct:
    def __init__(self, content: list[list]) -> None:
        self.visible = True
        self.content = content
        self.position = Vec2(0, 0)
        self.global_position = Vec2(0, 0)


class ASCIIImage:
    extension = ".txt"
    _cache = {}

    @classmethod
    def load(cls, file_path: FilePath, /, cache: bool = True) -> ASCIISurface:
        if not isinstance(file_path, str):
            TypeError("argument 'file_path' is required to be of type 'str'. '" + type(file_path).__name__ + "' found")
        fpath = os.path.normpath(file_path)
        if fpath in cls._cache and cache:
            return cls._cache[fpath]
        if not fpath.endswith(cls.extension):
            raise ValueError("argument 'file_path' needs to end with the current extension of '" + cls.extension + "'")
        file: io.TextIOWrapper = open(fpath, "r")
        content = list(map(list, file.readlines()))
        file.close()
        node = _ASCIINodeStruct(content)
        cls._cache[fpath] = node
        width = len(max(content, key=len))
        height = len(content)
        return ASCIISurface(nodes=[node], width=width, height=height)
