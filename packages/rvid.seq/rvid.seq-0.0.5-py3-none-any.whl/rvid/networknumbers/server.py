from abc import abstractmethod
from array import array
from logging import getLogger
from socketserver import BaseRequestHandler, TCPServer
from threading import Lock
from typing import Callable, List, Sequence, Type

from rvid.networknumbers.request import RequestForNumbers

log = getLogger(__name__)


class GenericTCPServer:
    def __init__(
        self, handler_class: Type[BaseRequestHandler], host: str = "127.0.0.1", port: int = 65432
    ) -> None:
        self.host = host
        self.port = port
        self.HandlerClass = handler_class

    def serve_forever(self) -> None:
        with TCPServer((self.host, self.port), self.HandlerClass) as server:
            log.info("TCP Server is running. Ctrl-C to kill it.")
            log.info(f"Registered handler is: {str(self.HandlerClass)}")
            server.serve_forever()


class NumberRequestTCPHandler(BaseRequestHandler):
    def handle(self) -> None:
        data = self.request.recv(1024)  # Request data could include advise on needs
        request = RequestForNumbers.from_binary(data)
        lock = Lock()
        try:
            lock.acquire()
            retval = array(self.array_type(), self.number_getter()(request))
        finally:
            lock.release()

        self.request.sendall(retval.tobytes())

    @abstractmethod
    def number_getter(self) -> Callable[[RequestForNumbers], Sequence[int]]:
        pass

    @abstractmethod
    def array_type(self) -> str:
        pass


class ExampleIntHandler(NumberRequestTCPHandler):
    def number_getter(self) -> Callable[[RequestForNumbers], List[int]]:
        return lambda x: [123, 345, 567]

    def array_type(self) -> str:
        return "L"
