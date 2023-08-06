from __future__ import annotations
import asyncclick as ac
from .. import click_backend as cb
from xoa_driver.hlfuncs import anlt as anlt_utils
import asyncclick as ac
from ...clis import (
    format_an_status,
    format_an_config,
)
from .group import xoa_utils
from .. import click_help as h
from ...cmds import CmdContext

# --------------------------
# command: an
# --------------------------
@xoa_utils.group(cls=cb.XenaGroup)
def an():
    """
    To enter auto-negotiation context.\n
    """


# **************************
# Type: Config
# **************************
# **************************
# sub-command: an config
# **************************
@an.command(cls=cb.XenaCommand, name="config")
@ac.option("--on/--off", type=ac.BOOL, help=h.HELP_AN_CONFIG_ON, default=True)
@ac.option(
    "--loopback/--no-loopback",
    type=ac.BOOL,
    help=h.HELP_AN_CONFIG_LOOPBACK,
    default=False,
)
@ac.pass_context
async def an_config(context: ac.Context, on: bool, loopback: bool) -> str:
    """
    Configure auto-negotiation for the working port.\n
    """
    storage: CmdContext = context.obj
    storage.retrieve_port()
    storage.store_an_allow_loopback(loopback)
    storage.store_should_do_an(on)
    return format_an_config(storage, on, loopback)


# **************************
# Type: Statistics
# **************************
# **************************
# sub-command: an status
# **************************
@an.command(cls=cb.XenaCommand, name="status")
@ac.pass_context
async def an_status(context: ac.Context) -> str:
    """
    Show the auto-negotiation status.\n
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    status_dic = await anlt_utils.autoneg_status(port_obj)
    return format_an_status(status_dic)
