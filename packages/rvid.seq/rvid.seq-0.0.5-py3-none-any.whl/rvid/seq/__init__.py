from typing import Union

from .basic import RIDMaker
from .common import RIDType, epoch_ms2rid, rid2epoch_ms
from .threadsafe import RIDMakerThreadSafe

RID = RIDMaker()
RID_ThreadSafe = RIDMakerThreadSafe()


def rid2epoch(rid_value: RIDType) -> int:
    return round(rid2epoch_ms(rid_value) / 1000)


def epoch2rid(epoch: Union[int, float]) -> str:
    """
    Convert a standard epoch value in seconds to a RID
    """
    return epoch_ms2rid(round(epoch * 1000))
