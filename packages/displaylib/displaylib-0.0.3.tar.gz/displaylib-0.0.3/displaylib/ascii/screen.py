import sys
from .node import ASCIINode
from .surface import ASCIISurface
from .constants import *


class ASCIIScreen(ASCIISurface):
    def show(self) -> None:
        lines = len(self.content)
        for idx, line in enumerate(self.content):
            rendered = "".join(letter if letter != ASCIINode.cell_transparant else ASCIINode.cell_default for letter in (line))
            sys.stdout.write(rendered + " " + ("\n" if idx != lines else ""))
        sys.stdout.write(ANSI_UP * len(self.content) + "\r")
        sys.stdout.flush()
