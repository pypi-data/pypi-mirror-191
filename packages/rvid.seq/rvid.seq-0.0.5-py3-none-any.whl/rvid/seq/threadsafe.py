from threading import RLock

from rvid.seq.basic import RIDMaker
from rvid.seq.common import RIDType


class RIDMakerThreadSafe(RIDMaker):
    """Private class that issues new RID:s"""

    def __init__(self) -> None:
        RIDMaker.__init__(self)
        self.lock = RLock()

    def adjust_top_from_rid(self, rid: RIDType) -> None:
        with self.lock:
            RIDMaker.adjust_top_from_rid(self, rid)

    def next(self) -> str:
        with self.lock:
            return RIDMaker.next(self)

    def reset(self) -> None:
        with self.lock:
            RIDMaker.reset(self)
