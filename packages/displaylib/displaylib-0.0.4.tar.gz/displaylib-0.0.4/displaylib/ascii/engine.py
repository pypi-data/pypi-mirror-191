from ..template import Node, Engine
from .clock import Clock
from .screen import ASCIIScreen
from .surface import ASCIISurface


class ASCIIEngine(Engine):
    """ASCIIEngine for creating a world in ASCII graphics
    """

    def __init__(self, tps: int = 16, width: int = 16, height: int = 8) -> None:
        self.tps = tps
        self.screen = ASCIIScreen(width=width, height=height) # upper level ASCIISurface
        self.display = ASCIISurface(Node.nodes.values()) # sub level ASCIISurface | just above a ASCIISurface
        self._on_start()

        self.is_running = True
        self._main_loop()
    
    def _render(self, surface: ASCIISurface) -> None:
        return
    
    def _main_loop(self) -> None:
        def sort_fn(element):
            return element[1].z_index

        nodes = tuple(Node.nodes.values())
        clock = Clock(self.tps)
        while self.is_running:
            delta = 1.0 / self.tps
            self.screen.clear()
            
            self._update(delta)
            for node in nodes:
                node._update(delta)

            for node in Node._queued_nodes:
                del Node.nodes[id(node)]
            Node._queued_nodes.clear()
            
            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            nodes = tuple(Node.nodes.values())

            # render content of visible nodes onto a surface
            self.display = ASCIISurface(Node.nodes.values(), self.screen.width, self.screen.height) # create a Surface from all the Nodes
            self.screen.blit(self.display, transparent=True)
            
            self._render(self.screen)
            # render nodes onto main screen
            for node in nodes:
                node._render(self.screen)
            
            self.screen.show()
            clock.tick()
        
        # v exit protocol v
        self._on_exit()
        surface = ASCIISurface(Node.nodes.values(), self.screen.width, self.screen.height) # create a Surface from all the Nodes
        self.screen.blit(surface)
        self.screen.show()
