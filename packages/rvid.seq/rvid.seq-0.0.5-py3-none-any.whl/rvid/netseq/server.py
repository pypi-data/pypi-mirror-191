from logging import getLogger
from typing import Callable, Dict, Sequence

from rvid.networknumbers.request import RequestForNumbers
from rvid.networknumbers.server import NumberRequestTCPHandler
from rvid.seq.common import epoch_ms_now

log = getLogger(__name__)


class TranchKeeper:
    """
    TODO: Split out generic server functionality to the networknumbers module and inherit/mix
          that into this RID-specific class.
    """

    def __init__(self) -> None:
        self.tranches: Dict[str, Sequence[int]] = dict()
        self.client_last_seen: Dict[str, int] = dict()
        self.resolution = 3333  # Milliseconds of tranche length
        self.top = -1  # Millisecond epoch

    def get_tranche_for(self, request: RequestForNumbers) -> Sequence[int]:
        client_id = request.key()

        self.client_last_seen[client_id] = epoch_ms_now()
        self._age_out_clients()

        # Check if client is new
        if client_id not in self.tranches:
            self.tranches[client_id] = []
            self._make_new_tranches()

        # Check if client has already asked for its currently allocated tranche
        if not self.tranches[client_id]:
            self._make_new_tranches()

        # Check if current tranches are too old
        for tranche in self.tranches.values():
            if epoch_ms_now() - tranche[0] > self.resolution // 2:
                self._make_new_tranches()
            break

        return_tranch = self.tranches[client_id]
        self.tranches[client_id] = []  # Make sure we don't return same tranche twice
        return return_tranch

    def _make_new_tranches(self) -> None:
        now = epoch_ms_now()
        client_count = len(self.tranches.keys())
        log.info("Making new tranches for %i clients at ms-epoch %i" % (client_count, now))

        # Set current top to now, if now is higher than top
        self.top = now if now > self.top else self.top + 1

        rid_range = range(self.top, self.top + self.resolution)
        for idx, client in enumerate(self.tranches.keys()):
            self.tranches[client] = rid_range[idx::client_count]

        # Set top to the highest awarded RID + 1
        self.top += self.resolution + 1

    def _age_out_clients(self) -> None:
        now = epoch_ms_now()
        to_forget = list()

        for client, last_seen in self.client_last_seen.items():
            if now - last_seen > self.resolution * 10:
                to_forget.append(client)

        for client in to_forget:
            log.info(f"Forgetting client {client} due to not having asked for anything in a while")
            del self.tranches[client]
            del self.client_last_seen[client]


TK = TranchKeeper()


class RIDHandler(NumberRequestTCPHandler):
    """
    The Handler class will get instantiated for each connection to the server, so
    any persistent state needs to live outside the instance.
    """

    def number_getter(self) -> Callable[[RequestForNumbers], Sequence[int]]:
        return TK.get_tranche_for

    def array_type(self) -> str:
        return "L"
