import socket
import selectors
from typing_extensions import Self


class Client:
    def __new__(cls: type[Self]) -> Self:
        instance = super().__new__(cls)
        return instance
