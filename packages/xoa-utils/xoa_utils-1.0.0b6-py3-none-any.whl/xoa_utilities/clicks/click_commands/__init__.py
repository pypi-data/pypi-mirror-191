from __future__ import annotations
import typing as t
from ...cmds import CmdContext
from . import an
from . import lt
from . import management
from . import anlt
from . import debug
from .group import xoa_utils


async def cmd_main(context: CmdContext, cmd_str: str) -> t.Any:
    context.clear_error()
    args = cmd_str.split()
    result = await xoa_utils.main(args=args, standalone_mode=False, obj=context)
    return result 
