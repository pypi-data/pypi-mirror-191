import time
from time import sleep

from rvid.netseq.client import RIDMakerProxy
from rvid.netseq.server import RIDHandler
from rvid.networknumbers.server import GenericTCPServer


def main() -> None:
    import sys

    if len(sys.argv) != 2:
        print("Must specify client, server or benchmark")
        print("client and benchmark commands assume server is already running on localhost")
        sys.exit(1)

    if sys.argv[1] == "benchmark":
        times = 100 * 1000
        r = RIDMakerProxy()
        print(f"Calling .next() {times} times with no sleep inbetween")
        updates = 0
        prev_fetch = -1
        ts = time.time()
        for _ in range(times):
            r.next()
            if r.last_fetch != prev_fetch:
                updates += 1
                prev_fetch = r.last_fetch

        duration = time.time() - ts
        rate = round(times / duration)

        print(
            f"Completed in {duration:.2f} seconds ({rate} id:s/second) with {updates} server-updates requested."
        )

    if sys.argv[1] == "client":
        r = RIDMakerProxy()
        print("Running .next() 12 times with 0.1s sleep between")
        for _ in range(12):
            sleep(0.1)
            print(
                f"{r.next()} with last fetch at {r.last_fetch} and {len(r.cached_ids)} ID:s remaining"
            )

    elif sys.argv[1] == "server":
        s = GenericTCPServer(handler_class=RIDHandler)
        s.serve_forever()


if __name__ == "__main__":
    main()
