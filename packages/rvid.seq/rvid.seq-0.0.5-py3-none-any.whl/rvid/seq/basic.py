from rvid.seq.common import RIDType, epoch_ms2rid, epoch_ms_now, rid2epoch_ms


class RIDMaker:
    """Private class that issues new RID:s"""

    def __init__(self) -> None:
        self._top = epoch_ms_now()
        self.collisions = 0

    def adjust_top_from_rid(self, rid: RIDType) -> None:
        """
        Adjust top-RID IFF argument is higher than current top-RID
        """
        suggested_new_top = rid2epoch_ms(rid)
        if suggested_new_top > self._top:
            self._top = suggested_new_top

    def next(self) -> str:
        now = epoch_ms_now()
        if now <= self._top:
            now = self._top + 1
            self.collisions += 1

        self._top = now
        return epoch_ms2rid(now)

    def reset(self) -> None:
        self._top = epoch_ms_now()
