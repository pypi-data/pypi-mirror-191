# Displaylib

## Submodules
- `template`
- `ascii` (default)
- `pygame`
---

Example using `displaylib` in `ascii` mode:
```python 
import displaylib.ascii as dl
# mode selected   ^^^^^


class Square(dl.Node):
    def __init__(self, owner=None, x: int = 0, y: int = 0) -> None:
        super().__init__(owner, x, y) # the most important args to pass down
        self.content = [ # you can use this style to define its visual
            [*"OO+OO"], # the '+' represents transparancy
            [*"O+++O"], # see dl.Node.cell_transparancy (ascii mode)
            [*"OO+OO"]
        ]


class App(dl.Engine):
    def _on_ready(self) -> None: # use this instead of __init__
        dl.Node.cell_transparent = "+" # represents transparancy
        dl.Node.cell_default = "." # changes background default
        self.my_square = Square(x=5, y=3)
    
    def _update(self, delta: float) -> None:
        ... # called every frame


if __name__ == "__main__":
    # autorun on instance creation
    app = App(tps=4, width=24, height=8)

```