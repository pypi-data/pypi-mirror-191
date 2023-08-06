from ..template import Node
from .types import Event, Surface


class PygameNode(Node):
    visible: bool = False
    
    def _input(event: Event) -> None:
        return
    
    def _render(self, surface: Surface) -> None:
        return
