from __future__ import annotations
import asyncclick as ac
from .group import xoa_utils
from .. import click_backend as cb
from ...exceptions import *
from ...cmds import CmdContext
from xoa_driver.hlfuncs import anlt_ll_debug as debug_utils


@xoa_utils.group(cls=cb.XenaGroup)
def debug():
    """
    To enter debug context.\n

    """


# --------------------------
# command: init
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def init(context: ac.Context, lane: int) -> str:
    """
    Debug init

        LANE INT: Specifies the transceiver lane index.\n
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    inf = await debug_utils.init(port_obj, lane)
    storage.store_anlt_low(lane, inf)
    return str(inf)


async def _help_get(func: t.Callable, context: ac.Context, lane: int) -> str:
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_lane() == lane or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, lane)
        storage.store_anlt_low(lane, inf)
    return str(await func(port_obj, lane, inf=inf))


async def _help_set(
    func: t.Callable, context: ac.Context, lane: int, value: int
) -> str:
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_lane() == lane or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, lane)
        storage.store_anlt_low(lane, inf)
    await func(port_obj, lane, value=value, inf=inf)
    return ""


# --------------------------
# command: lane-reset
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lane_reset(context: ac.Context, lane: int) -> str:
    """
    Debug lane-reset

        LANE INT: Specifies the transceiver lane index.\n
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_lane() == lane or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, lane)
        storage.store_anlt_low(lane, inf)
    await debug_utils.lane_reset(port_obj, lane, inf=inf)
    return ""


# --------------------------
# command: mode-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def mode_get(context: ac.Context, lane: int) -> str:
    """
    Debug mode-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.mode_get, context, lane)


# --------------------------
# command: mode-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def mode_set(context: ac.Context, lane: int, value: int) -> str:
    """
    Debug mode-set

        LANE INT: Specifies the transceiver lane index.\n
        VALUE INT: Specifies the value.\n
    """

    return await _help_set(debug_utils.mode_get, context, lane, value)


# --------------------------
# command: lt-tx-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_tx_config_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-tx-config-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_tx_config_get, context, lane)


# --------------------------
# command: lt-tx-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_tx_config_set(context: ac.Context, lane: int, value: int) -> str:
    """
    Debug lt-tx-config-set

        LANE INT: Specifies the transceiver lane index.\n
        VALUE INT: Specifies the value.\n
    """
    return await _help_set(debug_utils.lt_tx_config_set, context, lane, value)


# --------------------------
# command: lt-rx-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_config_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-config-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_config_get, context, lane)


# --------------------------
# command: lt-rx-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_config_set(context: ac.Context, lane: int, value: int) -> str:
    """
    Debug lt-rx-config-set

        LANE INT: Specifies the transceiver lane index.\n
        VALUE INT: Specifies the value.\n
    """
    return await _help_set(debug_utils.lt_rx_config_set, context, lane, value)


# --------------------------
# command: lt-tx-tf-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_tx_tf_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-tx-tf-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_tx_tf_get, context, lane)


# --------------------------
# command: lt-rx-error-stat0-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_error_stat0_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-error-stat0-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_error_stat0_get, context, lane)


# --------------------------
# command: lt-rx-error-stat1-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_error_stat1_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-error-stat1-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_error_stat1_get, context, lane)


# --------------------------
# command: lt-rx-analyzer-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_config_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-analyzer-config-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_analyzer_config_get, context, lane)


# --------------------------
# command: lt-rx-analyzer-trig-mask-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_trig_mask_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-analyzer-trig-mask-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_analyzer_trig_mask_get, context, lane)


# --------------------------
# command: lt-rx-analyzer-status-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_status_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-analyzer-status-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_analyzer_status_get, context, lane)


# --------------------------
# command: lt-rx-analyzer-rd-addr-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_addr_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-analyzer-rd-addr-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_analyzer_rd_addr_get, context, lane)


# --------------------------
# command: lt-rx-analyzer-rd-page-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_page_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-analyzer-rd-page-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_analyzer_rd_page_get, context, lane)


# --------------------------
# command: lt-rx-analyzer-rd-data-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_data_get(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-analyzer-rd-data-get

        LANE INT: Specifies the transceiver lane index.\n
    """
    return await _help_get(debug_utils.lt_rx_analyzer_rd_data_get, context, lane)


# --------------------------
# command: lt-rx-analyzer-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_config_set(context: ac.Context, lane: int, value: int) -> str:
    """
    Debug lt-rx-analyzer-config-set

        LANE INT: Specifies the transceiver lane index.\n
        VALUE INT: Specifies the value.\n
    """
    await _help_set(debug_utils.lt_rx_analyzer_config_set, context, lane, value)
    return ""


# --------------------------
# command: lt-rx-analyzer-trig-mask-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_trig_mask_set(
    context: ac.Context, lane: int, value: int
) -> str:
    """
    Debug lt-rx-analyzer-trig-mask-set

        LANE INT: Specifies the transceiver lane index.\n
        VALUE INT: Specifies the value.\n
    """
    await _help_set(debug_utils.lt_rx_analyzer_trig_mask_set, context, lane, value)
    return ""


# --------------------------
# command: lt-rx-analyzer-rd-addr-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_addr_set(context: ac.Context, lane: int, value: int) -> str:
    """
    Debug lt-rx-analyzer-rd-addr-set

        LANE INT: Specifies the transceiver lane index.\n
        VALUE INT: Specifies the value.\n
    """
    await _help_set(debug_utils.lt_rx_analyzer_rd_addr_set, context, lane, value)
    return ""


# --------------------------
# command: lt-rx-analyzer-rd-page-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_page_set(context: ac.Context, lane: int, value: int) -> str:
    """
    Debug lt-rx-analyzer-rd-page-set

        LANE INT: Specifies the transceiver lane index.\n
        VALUE INT: Specifies the value.\n
    """
    await _help_set(debug_utils.lt_rx_analyzer_rd_page_set, context, lane, value)
    return ""


# --------------------------
# command: lt-status
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_status(context: ac.Context, lane: int, value: int) -> str:
    """
    Debug lt-status

        LANE INT: Specifies the transceiver lane index.\n
        VALUE INT: Specifies the value.\n
    """
    await _help_set(debug_utils.lt_status, context, lane, value)
    return ""


# --------------------------
# command: lt-prbs
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_prbs(context: ac.Context, lane: int) -> str:
    """
    Debug lt-prbs

        LANE INT: Specifies the transceiver lane index.\n
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_lane() == lane or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, lane)
        storage.store_anlt_low(lane, inf)
    return str(await debug_utils.lt_prbs(port_obj, lane, inf=inf))


# --------------------------
# command: lt-rx-analyzer-dump
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("lane", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_dump(context: ac.Context, lane: int) -> str:
    """
    Debug lt-rx-analyzer-dump

        LANE INT: Specifies the transceiver lane index.\n
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_lane() == lane or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, lane)
        storage.store_anlt_low(lane, inf)
    return str(await debug_utils.lt_rx_analyzer_dump(port_obj, lane, inf=inf))
