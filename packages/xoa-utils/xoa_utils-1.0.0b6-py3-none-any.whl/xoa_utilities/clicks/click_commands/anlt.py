from __future__ import annotations
import asyncclick as ac
import json
from xoa_driver.hlfuncs import anlt as anlt_utils
from .. import click_backend as cb
from ...exceptions import *
from ...clis import format_recovery, format_port_status
from .group import xoa_utils
from .. import click_help as h
from ...cmds import CmdContext


@xoa_utils.group(cls=cb.XenaGroup)
def anlt():
    """
    To enter anlt context.\n
    """


# --------------------------
# command: recovery
# --------------------------
@anlt.command(cls=cb.XenaCommand)
@ac.option("--on/--off", type=ac.BOOL, help=h.HELP_RECOVERY_ON, default=True)
@ac.pass_context
async def recovery(context: ac.Context, on: bool) -> str:
    """
    Enable/disable link recovery on the specified port. If enable, the port will keep trying ANLT when no link-up signal is detected after five seconds of waiting.
    """
    storage: CmdContext = context.obj

    port_obj = storage.retrieve_port()
    await anlt_utils.anlt_link_recovery(port_obj, on)
    return format_recovery(storage, on)


# --------------------------
# command: status
# --------------------------
@anlt.command(cls=cb.XenaCommand)
@ac.pass_context
async def status(context: ac.Context) -> str:
    """
    Show the overview of ANLT status of the port.\n
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    status_dic = await anlt_utils.anlt_status(port_obj)
    port_id = storage.retrieve_port_str()
    return format_port_status(port_id, status_dic)


# --------------------------
# command: do
# --------------------------
@anlt.command(cls=cb.XenaCommand)
@ac.pass_context
async def do(context: ac.Context) -> str:
    """
    Show the overview of ANLT status of the port.\n
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    an_enable = storage.retrieve_an_enable()
    lt_enable = storage.retrieve_lt_enable()
    an_allow_loopback = storage.retrieve_an_loopback()
    lt_preset0_std = storage.retrieve_lt_preset0_std()
    lt_initial_modulations = storage.retrieve_lt_initial_mod()
    lt_interactive = storage.retrieve_lt_interactive()
    await anlt_utils.anlt_start(
        port_obj,
        an_enable,
        lt_enable,
        an_allow_loopback,
        lt_preset0_std,
        lt_initial_modulations,
        lt_interactive,
    )
    return ""


# **************************
# command: log
# **************************
@anlt.command(cls=cb.XenaCommand, name="log")
@ac.option(
    "-f", "--filename", type=ac.STRING, help=h.HELP_ANLT_LOG_FILENAME, default=""
)
@ac.option(
    "-k",
    "--keep",
    type=ac.Choice(["all", "an", "lt"]),
    help=h.HELP_ANLT_LOG_KEEP,
    default="all",
)
@ac.option("-l", "--lane", type=ac.STRING, help=h.HELP_ANLT_LOG_KEEP, default="")
@ac.pass_context
async def anlt_log(ctx: ac.Context, filename: str, keep: str, lane: str) -> str:
    """
    Show the auto-negotiation log trace.\n
    """

    def filter_log(log: str, keep: str, lane: list[int]) -> list[dict]:
        all_logs = []
        for l in log.split("\n"):
            try:
                content = json.loads(l)
                log_lane = content["lane"]
                module = content["module"]

                lane_in = False
                keep_in = False
                if (lane and log_lane in lane) or not lane:
                    lane_in = True
                if any(
                    (
                        keep == "an" and "AN" in module,
                        keep == "lt" and "LT" in module,
                        keep == "all",
                    )
                ):
                    keep_in = True
                if lane_in and keep_in:
                    all_logs.append(content)

            except Exception:
                pass
        return all_logs

    def beautify(filtered: list[dict]) -> str:
        result = []
        for i in filtered:
            base = (
                json.dumps(i, indent=2)
                .replace("{", "")
                .replace("}", "")
                .replace('"', "")
            ).strip("\n  ")
            space_num = 0
            if i["type"] == "fsm":
                space_num = 26
            elif i["entry"].get("direction", "") == "rx":
                space_num = 52
            real = "\n".join([f"{space_num * ' '}{p}" for p in base.split("\n")])
            result.append(real)

        return (f"\n{'-' * 80}\n").join(result).strip()

    async def log(
        storage: CmdContext, filename: str, keep: str, lane: list[int]
    ) -> str:
        port_obj = storage.retrieve_port()
        log_str = await anlt_utils.anlt_log(port_obj)
        filtered = filter_log(log_str, keep, lane)
        string = beautify(filtered)
        if filename and log_str:
            with open(filename, "a") as f:
                f.write(f"{log_str}\n")
        return string

    real_lane_list = [int(i.strip()) for i in lane.split(",")] if lane else []
    kw = {"filename": filename, "keep": keep, "lane": real_lane_list}
    storage: CmdContext = ctx.obj
    storage.set_loop_coro(log)
    storage.set_loop_coro_kw(kw)
    return ""
