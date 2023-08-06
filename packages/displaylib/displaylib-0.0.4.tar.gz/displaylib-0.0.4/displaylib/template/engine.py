from typing_extensions import Self
from .node import Node


class Engine:
    """Engine base class
    NOTE: only one Engine instance should exist per script instance
    """
    tps: int = 4
    is_running: bool = False

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        instance = object.__new__(cls)
        Node.root = instance
        return instance

    def __init__(self) -> None: # default implementation
        self._on_start()
        self.is_running = True
        self._main_loop()
        self._on_exit()

    def _on_start(self) -> None:
        return
    
    def _on_exit(self) -> None:
        return
    
    def _update(self, delta: float) -> None:
        return
    
    def _main_loop(self) -> None:
        delta = 1.0 / self.tps
        while self.is_running:
            self._update(delta)
            for node in Node.nodes:
                node._update(delta)
