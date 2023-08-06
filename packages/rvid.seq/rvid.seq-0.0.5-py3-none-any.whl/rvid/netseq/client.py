from typing import List, Tuple

from rvid.networknumbers.client import ExampleIntsClient
from rvid.seq.basic import RIDMaker
from rvid.seq.common import RIDType, epoch_ms2rid, epoch_ms_now


class RIDMakerProxy(RIDMaker):
    def __init__(self) -> None:
        super().__init__()
        self.client = ExampleIntsClient(name="netseq-client")
        self.resolution = 3333  # TODO: Fetch value from server
        self.cached_ids: List[int] = list()
        self.last_fetch = 0
        self.drift = 0
        self.top = epoch_ms_now()

    def next(self) -> str:
        now = epoch_ms_now() - self.drift
        if now - self.last_fetch > self.resolution:
            self._update()
        elif not self.cached_ids:
            self._update()

        best_match, match_at_idx = self._search(now)
        del self.cached_ids[: match_at_idx + 1]
        return epoch_ms2rid(best_match)

    def _search(self, now: int) -> Tuple[int, int]:
        """
        Find the earliest acceptable ID among the ones we have stored. Since we prune on
        each search, this should usually be close to the start. We also don't want to
        waste usable ID:s.

        A binary search for the first value at the left edge of acceptability would perhaps
        be better.
        """
        step = 1
        offset = 0
        while (step + offset) < len(self.cached_ids):
            diff = abs(now - self.cached_ids[offset])
            # If we are within half of the resolution from "now", that is good enough
            if diff < self.resolution // 2:
                break

            step += 1
            offset += step

        offset = min(offset, len(self.cached_ids) - 1)
        return self.cached_ids[offset], offset

    def _update(self) -> None:
        self.cached_ids = self.client.get()
        self.last_fetch = max(self.cached_ids)
        self.drift = epoch_ms_now() - self.last_fetch

    def adjust_top_from_rid(self, rid: RIDType) -> None:
        raise NotImplementedError("Can't adjust top from client-side yet.")

    def reset(self) -> None:
        raise NotImplementedError("Can't reset top from client-side yet.")
