import sys
from time import sleep

from rvid.networknumbers.client import ExampleIntsClient
from rvid.networknumbers.server import ExampleIntHandler, GenericTCPServer


def main() -> None:
    if len(sys.argv) != 2:
        print("Must specify client or server")
        sys.exit(1)

    elif sys.argv[1] == "server":
        s = GenericTCPServer(handler_class=ExampleIntHandler)
        s.serve_forever()

    if sys.argv[1] == "client":
        client = ExampleIntsClient()
        print("Running .get() 3 times with 0.1s sleep between")
        for _ in range(3):
            sleep(0.1)
            print(client.get())


if __name__ == "__main__":
    main()
