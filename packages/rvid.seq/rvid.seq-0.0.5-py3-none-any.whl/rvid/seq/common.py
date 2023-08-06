import re
import time
from typing import NewType

_allowed_letters = "A-HJ-NP-Y0-9*#"  # No India or Oscar
RID_REGEXP = re.compile(
    "^([%s]{3})-([%s]{3})-([%s]{3})$" % ((_allowed_letters,) * 3), re.IGNORECASE
)
BASE35_CHARS = "0123456789ABCDEFGH*JKLMN#PQRSTUVWXY"
RIDType = NewType("RIDType", str)  # String like ABC-DEF-GHI, see _rid_regexp.


def encode_base35(number: int) -> str:
    if not isinstance(number, int):
        raise TypeError("Number must be an integer")

    if number == 0:
        return "0"

    if number < 0:
        raise Exception("Timestamp cannot be negative")

    if number < 35:
        return BASE35_CHARS[number]

    base35 = ""
    while number != 0:
        number, i = divmod(number, 35)
        base35 = BASE35_CHARS[i] + base35

    return base35


def rid2epoch_ms(rid: RIDType) -> int:
    """
    Convert a RID to milliseconds since epoch
    """
    mo = RID_REGEXP.match(rid)
    if mo:
        # * and # replace letters easy to confuse with digits. The dashes are just flair.
        plain_rid = rid.replace("*", "I").replace("#", "O").replace("-", "")
        return int(plain_rid, 35)
    else:
        raise ValueError(f"Cannot convert invalid RID to epoch: '{rid}'")


def epoch_ms2rid(epoch_ms: int) -> RIDType:
    """
    Convert milliseconds since epoch to RID

    (n.b time.time() gives you seconds, don't forget to multiply by 1000 before casting to int)
    """
    plain_rid = encode_base35(epoch_ms)
    plain_rid = plain_rid.rjust(9, "0")
    return RIDType(plain_rid[0:3] + "-" + plain_rid[3:6] + "-" + plain_rid[6:9])


def epoch_ms_now() -> int:
    """
    Milliseconds since epoch.

    time.time() returns seconds since epoch start as a floating-point number with
    varying accuracy between platforms. Just multiply by 1000 and round to int.

    We really don't care too much about the accuracy since collisions are detected
    and handled.
    """
    return round(time.time() * 1000)
