import os
import socket
from array import array
from typing import List

from rvid.networknumbers.request import RequestForNumbers


class GenericNumbersSocketClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 65432) -> None:
        self.host = host
        self.port = port

    def get_with_mandatory_params(self, request: RequestForNumbers, array_type: str) -> List[int]:
        array_chunks = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(request.to_binary())
            while True:
                data = s.recv(1024)
                if data:
                    array_chunks.append(data)
                else:
                    break

        if not array_chunks:
            return []

        rid_array = array(array_type)
        rid_array.frombytes(b"".join(array_chunks))
        return rid_array.tolist()


class ExampleIntsClient(GenericNumbersSocketClient):
    """
    A socket client that requests lists of integers.
    """

    def __init__(self, name: str = "test-client"):
        self.name = name
        GenericNumbersSocketClient.__init__(self)

    def get(self) -> List[int]:
        request = RequestForNumbers(
            client_name=self.name,
            client_host=socket.gethostname(),
            client_pid=os.getpid(),
        )

        array_type = "L"

        return GenericNumbersSocketClient.get_with_mandatory_params(self, request, array_type)
