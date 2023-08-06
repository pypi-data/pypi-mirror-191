from __future__ import annotations
import asyncclick as ac
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..cmds import CmdContext


class XenaGroup(ac.Group):
    def get_help(self, ctx: ac.Context) -> str:
        e = super().get_help(ctx)
        e = e.replace("python -m entry ", "")
        storage: CmdContext = ctx.obj
        storage.set_error(f"{e}\n")
        return e


class XenaCommand(ac.Command):
    def get_help(self, ctx: ac.Context) -> str:
        e = super().get_help(ctx)
        e = e.replace("python -m entry ", "")
        storage: CmdContext = ctx.obj
        storage.set_error(f"{e}\n")
        return e
