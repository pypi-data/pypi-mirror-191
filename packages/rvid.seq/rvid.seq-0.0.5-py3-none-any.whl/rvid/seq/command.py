import sys
from datetime import datetime
from typing import cast

from rvid.seq.basic import RIDMaker
from rvid.seq.common import RID_REGEXP, epoch_ms2rid, rid2epoch_ms, RIDType


def command() -> None:
    if len(sys.argv) == 1:
        print(RIDMaker().next())
        return
    elif len(sys.argv) > 2:
        print("Syntax: rid [epoch|RID]")
        return

    arg = sys.argv[1]

    if RID_REGEXP.match(arg):
        rid = cast(RIDType, arg)
        epoch = rid2epoch_ms(rid) // 1000
        date_str = datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{rid} corresponds to {date_str}")

    elif arg.isnumeric():
        rid = epoch_ms2rid(int(arg) * 1000)
        print(f"{arg} corresponds to {rid}")

    else:
        print(f"No one has taught me to parse this input: '{arg}'")
