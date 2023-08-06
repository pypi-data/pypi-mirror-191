from __future__ import annotations
import asyncclick as ac
import asyncio
from .. import click_backend as cb
from xoa_driver.hlfuncs import anlt as anlt_utils
from xoa_driver.hlfuncs import mgmt as mgmt_utils
from xoa_driver.testers import L23Tester
from ...exceptions import *
import asyncclick as ac
from ...clis import (
    format_tester_status,
    format_ports_status,
    format_port_status,
)
from .group import xoa_utils
from .. import click_help as h
from ...cmds import CmdContext


# --------------------------
# command: connect
# --------------------------
@xoa_utils.command(cls=cb.XenaCommand)
@ac.argument("device", type=ac.STRING)
@ac.argument("username", type=ac.STRING)
@ac.option("-p", "--ports", type=ac.STRING, help=h.HELP_CONNECT_PORT_LIST, default="")
@ac.option("--reset/--no-reset", type=ac.BOOL, help=h.HELP_CONNECT_RESET, default=True)
@ac.option("--force/--no-force", type=ac.BOOL, help=h.HELP_CONNECT_FORCE, default=True)
@ac.option("-P", "--password", type=ac.STRING, help=h.HELP_CONNECT_PWD, default="xena")
@ac.option("-t", "--tcp", type=ac.INT, help=h.HELP_CONNECT_TCP_PORT, default=22606)
@ac.pass_context
async def connect(
    context: ac.Context,
    device: str,
    username: str,
    ports: str,
    reset: bool,
    force: bool,
    password: str,
    tcp: int,
) -> str:
    """
    To connect to a tester for the current session.

        DEVICE TEXT: Specifies the chassis address for connection. You can specify the IP addresses in IPv4 format, or a host name, e.g. 10.10.10.10 or demo.xenanetworks.com\n

        USERNAME TEXT: Specifies the name of the user.\n

    """
    storage: CmdContext = context.obj
    real_port_list = [i.strip() for i in ports.split(",")] if ports else []
    tester = await L23Tester(device, username, password, tcp, debug=True)
    con_info = f"{device}:{tcp}"
    storage.store_current_tester(username, con_info, tester)
    count = 0
    first_id = ""
    for id_str in real_port_list:
        this_port_dic = storage.obtain_physical_ports(id_str)
        for port_id, port_obj in this_port_dic.items():
            if force:
                await mgmt_utils.reserve_port(port_obj, force)
            if reset:
                await mgmt_utils.reset_port(port_obj)
            port_lane_num = (await anlt_utils.anlt_status(port_obj))["serdes_count"]
            storage.store_port(port_id, port_obj, port_lane_num)
            if count == 0:
                first_id = port_id
            count += 1

    if real_port_list:
        storage.store_current_port_str(first_id)
    if force or reset:
        await asyncio.sleep(3)
        # status will change when you reserve_port or reset_port, need to wait
    return format_tester_status(storage)


# --------------------------
# command: exit
# --------------------------
@xoa_utils.command(cls=cb.XenaCommand)
@ac.option("--reset/--no-reset", type=ac.BOOL, help=h.HELP_CONNECT_RESET, default=True)
@ac.option(
    "--release/--no-release", type=ac.BOOL, help=h.HELP_EXIT_RELEASE, default=True
)
@ac.pass_context
async def exit(context: ac.Context, reset: bool, release: bool) -> str:
    """
    To exit the session by terminating port reservations, disconnecting from the chassis, releasing system resources, and removing the specified port configurations. This command works in all context.
    """
    storage: CmdContext = context.obj
    for port_id, port_obj in storage.retrieve_ports().copy().items():
        if reset:
            await mgmt_utils.reset_port(port_obj)
        if release:
            await mgmt_utils.free_port(port_obj)
        storage.remove_port(port_id)
    return ""


# --------------------------
# command: port
# --------------------------
@xoa_utils.command(cls=cb.XenaCommand)
@ac.argument("port", type=ac.STRING)
@ac.option("--reset/--no-reset", type=ac.BOOL, help=h.HELP_CONNECT_RESET, default=False)
@ac.option("--force/--no-force", type=ac.BOOL, help=h.HELP_CONNECT_FORCE, default=True)
@ac.pass_context
async def port(context: ac.Context, port: str, reset: bool, force: bool) -> str:
    """
    Switch the working port. If the port is not yet reserved, reserve the port. Update the working port in the cache.

        PORT TEXT: Specifies the port on the specified device host. Specify a port using the format slot/port, e.g. 0/0\n
    """
    storage: CmdContext = context.obj
    try:
        storage.store_current_port_str(port)
        p_obj = storage.retrieve_port()
        port_lane_num = (await anlt_utils.anlt_status(p_obj))["serdes_count"]
        storage.store_port(port, p_obj, port_lane_num)
    except NotInStoreError:
        port_dic = storage.obtain_physical_ports(port)
        for p_id, p_obj in port_dic.items():
            port_lane_num = (await anlt_utils.anlt_status(p_obj))["serdes_count"]
            storage.store_port(p_id, p_obj, port_lane_num)
            storage.store_current_port_str(p_id)
    port_obj = storage.retrieve_port()
    port_id = storage.retrieve_port_str()
    if force:
        await mgmt_utils.reserve_port(port_obj, force)
    if reset:
        await mgmt_utils.reset_port(port_obj)
    if force or reset:
        await asyncio.sleep(3)
        # status will change when you reserve_port or reset_port, need to wait
    status_dic = await anlt_utils.anlt_status(port_obj)
    return f"{format_ports_status(storage, False)}{format_port_status(port_id, status_dic)}"


# --------------------------
# command: ports
# --------------------------
@xoa_utils.command(cls=cb.XenaCommand)
@ac.option("--all/--no-all", type=ac.BOOL, help=h.HELP_PORTS_ALL, default=False)
@ac.pass_context
async def ports(context: ac.Context, all: bool) -> str:
    """
    To list all the ports reserved by the current session.\n

    """
    storage: CmdContext = context.obj
    return format_ports_status(storage, all)
