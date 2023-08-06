import pygame
from pygame.constants import *
from ..template import Node, Engine
from .constants import DEFAULT, MILLISECOND
from .types import Event, Surface


class PygameEngine(Engine):
    bg_color = (255, 255, 255) # white

    def __init__(self, window_name: str = "DisplayLib Window", tps: int = 60, width: int = 512, height: int = 256, icon_path: str | None = None, flags: int = DEFAULT) -> None:
        self._window_name = window_name # TODO: add setter
        self.tps = tps
        self._width = width # TODO: add setter
        self._height = height # TODO: add setter
        self.icon_img: None | Surface = None
        if icon_path:
            pygame.image.load(icon_path)
            pygame.display.set_icon(self.icon_img)
        self.flags = flags
        self.screen = pygame.display.set_mode(size=(width, height), flags=flags)
        self.display = pygame.Surface(size=(width, height))
        self._on_start()
        
        self.is_running = True
        self._main_loop()
    
    @property
    def height(self) -> int:
        return self._height
    
    @property
    def height(self, value: int) -> None: # TODO: queue this action
        self._height = value
        self.screen = pygame.display.set_mode(size=(self.width, self.height), flags=self.flags)
    
    @property
    def width(self) -> int:
        return self._width
    
    @property
    def width(self, value: int) -> None: # TODO: queue this action
        self._width = value
        self.screen = pygame.display.set_mode(size=(self.width, self.height), flags=self.flags)

    @property
    def icon(self) -> None:
        return self.icon_img
    
    @property
    def icon(self, icon_path: str) -> None:
        self.icon_img = pygame.image.load(icon_path)
        pygame.display.set_icon(self.icon_img)

    def _input(self, event: Event) -> None:
        if event.type == QUIT:
            self.is_running = False
    
    def _main_loop(self) -> None:
        def sort_fn(element):
            return element[1].z_index

        clock = pygame.time.Clock()
        delta = 1.0 / self.tps
        # update one time at the very start
        self.screen.fill(self.bg_color)
        pygame.display.flip()

        while self.is_running:
            self._update(delta)
            nodes = tuple(Node.nodes.values())
            for event in pygame.event.get():
                self._input(event)
                for node in nodes:
                    node._input(event)
            for node in nodes:
                node._update(delta)
            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            
            self.display.fill(self.bg_color)
            for node in nodes: # render nodes onto the display
                node._render(self.display)
            # TODO: implement camera
            self.screen.blit(self.display, (0, 0)) # render display onto the main screen
            
            pygame.display.flip()
            delta = clock.tick(self.tps) / MILLISECOND # milliseconds -> seconds
        self._on_exit()
