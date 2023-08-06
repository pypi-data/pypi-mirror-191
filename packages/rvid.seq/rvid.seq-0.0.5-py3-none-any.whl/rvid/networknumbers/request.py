"""
Right now the request only contains sender info.

TODO: Add a field for specifying a command.

"""
import struct

NUMBER_REQ_STRUCT_FORMAT = "255s255sL"


class RequestForNumbers:
    def __init__(self, client_name: str, client_host: str, client_pid: int) -> None:
        for name, value in [("client_host", client_host), ("client_name", client_name)]:
            if 1 > len(value) > 255:
                raise ValueError(f"{name} must be 2-255 chars long")
            if not all(31 < ord(c) < 127 for c in value):
                raise ValueError("f{name} may only contain ASCII codes 32-126")

        if not isinstance(client_pid, int) or client_pid < 1:
            raise ValueError("client_pid must be a positive, non-zero integer")

        self.client_name: bytes = client_name.encode("ascii")
        self.client_host: bytes = client_host.encode("ascii")
        self.client_pid: int = client_pid

    def key(self) -> str:
        return "%r-%r-%i" % (self.client_name, self.client_host, self.client_pid)

    @classmethod
    def from_binary(cls, data: bytes) -> "RequestForNumbers":
        name, host, pid = struct.unpack(NUMBER_REQ_STRUCT_FORMAT, data)
        return cls(
            client_name=name.strip(b"\0").decode("ascii"),
            client_host=host.strip(b"\0").decode("ascii"),
            client_pid=pid,
        )

    def to_binary(self) -> bytes:
        return struct.pack(
            NUMBER_REQ_STRUCT_FORMAT, self.client_name, self.client_host, self.client_pid
        )
