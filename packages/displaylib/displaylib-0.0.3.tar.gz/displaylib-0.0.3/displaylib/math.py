from math import sqrt
from typing_extensions import Self


__all__ = ["Vec2"]


class Vec2:
    """2-dimensional Vector class

    Usefull for storing position or direction
    """
    def __init__(self, x: int | float = 0, y: int | float = 0) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"
    
    def __add__(self, other: Self) -> Self:
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Self) -> Self:
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Self) -> Self:
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
    
    def __floordiv__(self, other: Self) -> Self:
        if isinstance(other, Vec2):
            return Vec2(self.x // other.x, self.y // other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x // other, self.y // other)
    
    def __truediv__(self, other: Self) -> Self:
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x / other, self.y / other)
    
    def __mod__(self, other: int | float) -> Self:
        return Vec2(self.x % other, self.y % other)
    
    def __eq__(self, other: Self) -> bool:
        return (self.x == other.x) and (self.y == other.y)
    
    def __ne__(self, other: Self) -> bool:
        return (self.x != other.x) or (self.y != other.y)
    
    def __gt__(self, other: Self) -> bool:
        return self.x > other.x and self.y > other.y
    
    def __lt__(self, other: Self) -> bool:
        return self.x < other.x and self.y < other.y
    
    def __ge__(self, other: Self) -> bool:
        return self.x >= other.x and self.y >= other.y

    def __le__(self, other: Self) -> bool:
        return self.x <= other.x and self.y <= other.y

    def length(self) -> float:
        if self.x == 0 and self.y == 0:
            return 0.0
        return sqrt(self.x*self.x + self.y*self.y)
    
    def normalized(self) -> Self:
        return self / self.length()
