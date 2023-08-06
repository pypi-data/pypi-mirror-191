import time
import socket
import selectors
from ..template import Node, Client
from .surface import ASCIISurface


class ASCIIClient(Client):
    _BUFF_SIZE = 4096
    _DELIMITER = b"$"
    _ARGUMENT_DELIMITER = ":"
    _NEGATIVE_INF = float("-inf")

    def __init__(self, host: str, port: int) -> None:
        self._address = (host, port)
        self._sel = selectors.DefaultSelector()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sel.register(self._sock, selectors.EVENT_READ)
        self._sock.connect(self._address)
        self._sock.setblocking(False)
        self._buffer = bytes()

    def send(self, request: str) -> None:
        encoded = request.encode(encoding="utf-8") + self._DELIMITER
        self._sock.send(encoded)

    def _on_request(self, data: str) -> None:
        return
    
    def _update_socket(self) -> None:
        for key, mask in self._sel.select(timeout=self._NEGATIVE_INF):
            connection = key.fileobj
            if mask & selectors.EVENT_READ:
                data = connection.recv(self._BUFF_SIZE)
                if data: # a readable client socket that has data.
                    if self._DELIMITER in data:
                        head, *rest = data.split(self._DELIMITER)
                        self._buffer += head
                        data = self._buffer.decode()
                        request, *args = data.split(self._ARGUMENT_DELIMITER)
                        self._buffer = bytes()
                        self._on_request(request, list(args))
                        for content in rest[:-1]:
                            data = content.decode()
                            request, *args = data.split(self._ARGUMENT_DELIMITER)
                            self._on_request(request, list(args))
                        self._buffer += rest[-1]
                    else:
                        self._buffer += data
                    # print('  received {!r}'.format(data))
    
    def _main_loop(self) -> None:
        def sort_fn(element):
            return element[1].z_index

        while self.is_running:
            delta = 1.0 / self.tps
            if Node._request_sort: # only sort once per frame if needed
                Node.nodes = {k: v for k, v in sorted(Node.nodes.items(), key=sort_fn)}
            self._update_socket() # <--- updates socket
            self.screen.clear()
            self._update(delta)
            nodes = tuple(Node.nodes.values())
            for node in nodes:
                node._update(delta)
            # render nodes onto main screen
            surface = ASCIISurface(nodes, self.display.width, self.display.height) # create a Surface from all the Nodes
            self.screen.blit(surface)
            self.screen.display()
            
            time.sleep(delta) # TODO: implement clock
        self._on_exit()
        surface = ASCIISurface(nodes, self.display.width, self.display.height) # create a Surface from all the Nodes
        self.screen.blit(surface)
        self.screen.display()
