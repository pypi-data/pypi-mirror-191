from __future__ import annotations
import configparser
import os
import typing as t
import asyncclick as ac
from xoa_driver import enums

if t.TYPE_CHECKING:
    from xoa_driver.ports import GenericL23Port
    from ..cmds.cmd_context import CmdContext


class ReadConfig:
    EXAMPLE = """[Connection]
port = 66
sshkeypath = ~/.ssh/id_rsa

[Hub]
enable = false
port = 10000
"""

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        self.config = config
        self._read_or_write_ini()
        self.connection_host = config["Connection"].get("host", "localhost")
        self.connection_port = int(config["Connection"].get("port", "5000"))
        self.connection_host_keys = config["Connection"].get(
            "sshkeypath", "~/.ssh/id_rsa"
        )
        self.hub_enabled = (
            True
            if str(config["Hub"].get("enable", "false")).lower() == "true"
            else False
        )
        self.hub_host = config["Hub"].get("host", "localhost")
        self.hub_port = int(config["Hub"].get("port", "10000"))
        self.hub_pid_path = config["Hub"].get("pid_path", "hub.pid")
        self.hub_pid = self._read_hub_pid()

    def _read_or_write_ini(self) -> None:
        folder = os.path.join(os.path.expanduser("~"), "XenaNetworks", "XOA-UTILITIES")
        realpath = os.path.join(folder, "config.ini")
        if not os.path.isfile(realpath):
            self._write_ini(realpath)
        try:
            self.config.read(realpath)
            for i in ("Hub", "Connection"):
                assert i in self.config
        except Exception:
            self._write_ini(realpath)
            self.config.read(realpath)

    def _touch(self, realpath: str) -> None:
        realpath = os.path.abspath(realpath)
        folder = os.path.dirname(realpath)
        if not os.path.isfile(realpath):
            try:
                os.remove(realpath)
            except Exception:
                pass
            os.makedirs(folder, exist_ok=True)
            with open(realpath, "w") as f:
                pass

    def _write_ini(self, realpath: str) -> None:
        self._touch(realpath)
        with open(realpath, "w") as f:
            f.write(type(self).EXAMPLE)

    def _read_hub_pid(self) -> int:
        pid = 0
        self._touch(self.hub_pid_path)
        with open(self.hub_pid_path, "r") as f:
            content = f.read().strip()
            try:
                pid = int(content)
            except ValueError:
                pass
        return pid


def run_coroutine_as_sync(coro: t.Coroutine) -> t.Any:
    while True:
        try:
            next(coro.__await__())
        except StopIteration as done:
            return done.value


def format_error(error: ac.UsageError) -> str:
    hint = ""
    result = ""
    if (
        error.ctx is not None
        and error.ctx.command.get_help_option(error.ctx) is not None
    ):
        hint = f"Try '{error.ctx.command_path} {error.ctx.help_option_names[0]}' for help.\n\n"
    if error.ctx is not None:
        result += f"{error.ctx.get_usage()}\n{hint}"
    result += f"Error: {error.format_message()}\n"
    result = result.replace("python -m entry", "")
    return result


def _port_dic_status(current_id: str, port_dic: dict[str, GenericL23Port]) -> str:
    string = f"Port      Sync      Owner     \n"
    for name, port in port_dic.items():
        new_name = f"*{name}" if current_id == name else name
        owner = "You" if port.is_reserved_by_me() else "Others"
        sync_status = str(port.info.sync_status.name)
        string += f"{new_name:10}{sync_status:10}{owner:10}\n"

    return string


def format_tester_status(storage: "CmdContext") -> str:
    serial_number = storage.retrieve_tester_serial()
    con_info = storage.retrieve_tester_con_info()
    username = storage.retrieve_tester_username()
    result_str = f"\nTester  :      {serial_number}\nConInfo :      {con_info}\nUsername:      {username}\n\n"
    result_str += _port_dic_status(
        storage.retrieve_port_str(), storage.retrieve_ports()
    )
    return result_str


def format_ports_status(storage: "CmdContext", all: bool) -> str:
    if all:
        port_dic = storage.get_all_ports()
    else:
        port_dic = storage.retrieve_ports()
    result_str = _port_dic_status(storage.retrieve_port_str(), port_dic)
    return result_str


def format_port_status(port_id: str, status: dict) -> str:
    return f"""
Port {port_id}
Auto-negotiation      : {status['autoneg_enabled']}
Link training         : {status['link_training_mode']}
Link training timeout : {status['link_training_timeout']}
Link recovery         : {status['link_recovery']}
Lane (serdes) count   : {status['serdes_count']}
"""


def format_an_status(dic: dict) -> str:
    return f"""
Loopback              : {dic['loopback']}
Duration              : {dic['duration']:,} µs
Successful runs       : {dic['successes']}
Timeouts              : {dic['timeouts']}
Loss of sync          : {dic['loss_of_sync']}
FEC negotiation fails : {dic['fec_negotiation_fails']}
HCD negotiation fails : {dic['hcd_negotiation_fails']}
                             RX    TX
Link codewords        : {dic['link_codewords']['rx']:6}{dic['link_codewords']['tx']:6}
Next-page messages    : {dic['next_page_messages']['rx']:6}{dic['next_page_messages']['tx']:6}
Unformatted pages     : {dic['unformatted_pages']['rx']:6}{dic['unformatted_pages']['tx']:6}
    """


def format_lt_config(storage: CmdContext) -> str:
    return f"""
Port {storage.retrieve_port_str()}
Link training : {'on' if storage.retrieve_lt_enable() else 'off'}
Mode          : {'interactive' if storage.retrieve_lt_interactive() else 'auto'}
Preset0       : {'standard tap' if storage.retrieve_lt_preset0_std() else 'existing tap'} values 
"""


def format_lt_im(storage: CmdContext, lane: int) -> str:
    return f"Port {storage.retrieve_port_str()}: initial modulation {storage.retrieve_lt_initial_mod_lane(lane).name} on Lane {lane}\n"


def format_an_config(storage: CmdContext, on: bool, loopback: bool) -> str:
    om = "on" if on else "off"
    lo = "allowed" if loopback else "not allowed"
    return (
        f"Port {storage.retrieve_port_str()} auto-negotiation: {om}, loopback: {lo}\n"
    )


def format_recovery(storage: CmdContext, on: bool) -> str:
    enable = "on" if on else "off"
    return f"Port {storage.retrieve_port_str()} link recovery: {enable}\n"


def format_lt_inc_dec(
    storage: CmdContext, lane: int, emphasis: str, increase: bool
) -> str:
    change = {
        "pre3": "c(-3)",
        "pre2": "c(-2)",
        "pre": "c(-1)",
        "main": "c(0)",
        "post": "c(1)",
    }[emphasis]
    action = "increase" if increase else "decrease"
    return (
        f"Port {storage.retrieve_port_str()}: {action} {change} by 1 on Lane {lane}\n"
    )


def format_lt_encoding(storage: CmdContext, lane: int, encoding: str) -> str:
    e = enums.LinkTrainEncoding[
        {"pam4pre": "PAM4_WITH_PRECODING"}.get(encoding, encoding).upper()
    ]
    return f"Port {storage.retrieve_port_str()}: use {e.name} on Lane {lane}\n"


def format_lt_preset(storage: CmdContext, lane: int, preset: int) -> str:
    return f"Port {storage.retrieve_port_str()}: use preset {preset} on Lane {lane}.\n"


def format_lt_trained(storage: CmdContext, lane: int) -> str:
    return f"Port {storage.retrieve_port_str()} requests: Lane {lane} is trained.\n"


def format_txtap_get(lane: int, dic: dict) -> str:
    return f"""
Local Coefficient Lane({lane})   :           c(-3)       c(-2)       c(-1)        c(0)        c(1)
    Current level           :              {dic['c(-3)']}           {dic['c(-2)']}           {dic['c(-1)']}           {dic['c(0)']}           {dic['c(1)']}
"""


def format_txtap_set(
    lane: int, pre3: int, pre2: int, pre: int, main: int, post: int
) -> str:
    return format_txtap_get(
        lane, {"c(-3)": pre3, "c(-2)": pre2, "c(-1)": pre, "c(0)": main, "c(1)": post}
    )


def format_lt_status(dic: dict) -> str:
    return f"""
Is Enabled        : {str(dic['is_enabled']).lower()}
Is Trained        : {str(dic['is_trained']).lower()}
Failure           : {dic['failure']}

Initial mode      : {dic['init_modulation']}
Preset0           : {dic['preset0']}
Total bits        : {dic['total_bits']:,}
Total err. bits   : {dic['total_errored_bits']:,}
BER               : {dic['ber']}

Duration          : {dic['duration']:,} µs

Lock lost         : {dic['lock_lost']}
Frame lock        : {dic['frame_lock']}
Remote frame lock : {dic['remote_frame_lock']}

Frame errors      : {dic['frame_errors']:,}
Overrun errors    : {dic['overrun_errors']:,}

Last IC received  : {dic['last_ic_received']}
Last IC sent      : {dic['last_ic_sent']}

TX Coefficient              :           c(-3)       c(-2)       c(-1)        c(0)        c(1)
    Current level           :{dic['c(-3)']['current_level']:16}{dic['c(-2)']['current_level']:12}{dic['c(-1)']['current_level']:12}{dic['c(0)']['current_level']:12}{dic['c(1)']['current_level']:12}
                            :         RX  TX      RX  TX      RX  TX      RX  TX      RX  TX
    + req                   :{dic['c(-3)']['+req']['rx']:11}{dic['c(-3)']['+req']['tx']:4}{dic['c(-2)']['+req']['rx']:8}{dic['c(-2)']['+req']['tx']:4}{dic['c(-1)']['+req']['rx']:8}{dic['c(-1)']['+req']['tx']:4}{dic['c(0)']['+req']['rx']:8}{dic['c(0)']['+req']['tx']:4}{dic['c(1)']['+req']['rx']:8}{dic['c(1)']['+req']['tx']:4}
    - req                   :{dic['c(-3)']['-req']['rx']:11}{dic['c(-3)']['-req']['tx']:4}{dic['c(-2)']['-req']['rx']:8}{dic['c(-2)']['-req']['tx']:4}{dic['c(-1)']['-req']['rx']:8}{dic['c(-1)']['-req']['tx']:4}{dic['c(0)']['-req']['rx']:8}{dic['c(0)']['-req']['tx']:4}{dic['c(1)']['-req']['rx']:8}{dic['c(1)']['-req']['tx']:4}
    coeff/eq limit reached  :{dic['c(-3)']['coeff_and_eq_limit_reached']['rx']:11}{dic['c(-3)']['coeff_and_eq_limit_reached']['tx']:4}{dic['c(-2)']['coeff_and_eq_limit_reached']['rx']:8}{dic['c(-2)']['coeff_and_eq_limit_reached']['tx']:4}{dic['c(-1)']['coeff_and_eq_limit_reached']['rx']:8}{dic['c(-1)']['coeff_and_eq_limit_reached']['tx']:4}{dic['c(0)']['coeff_and_eq_limit_reached']['rx']:8}{dic['c(0)']['coeff_and_eq_limit_reached']['tx']:4}{dic['c(1)']['coeff_and_eq_limit_reached']['rx']:8}{dic['c(1)']['coeff_and_eq_limit_reached']['tx']:4}
    eq limit reached        :{dic['c(-3)']['eq_limit_reached']['rx']:11}{dic['c(-3)']['eq_limit_reached']['tx']:4}{dic['c(-2)']['eq_limit_reached']['rx']:8}{dic['c(-2)']['eq_limit_reached']['tx']:4}{dic['c(-1)']['eq_limit_reached']['rx']:8}{dic['c(-1)']['eq_limit_reached']['tx']:4}{dic['c(0)']['eq_limit_reached']['rx']:8}{dic['c(0)']['eq_limit_reached']['tx']:4}{dic['c(1)']['eq_limit_reached']['rx']:8}{dic['c(1)']['eq_limit_reached']['tx']:4}
    coeff not supported     :{dic['c(-3)']['coeff_not_supported']['rx']:11}{dic['c(-3)']['coeff_not_supported']['tx']:4}{dic['c(-2)']['coeff_not_supported']['rx']:8}{dic['c(-2)']['coeff_not_supported']['tx']:4}{dic['c(-1)']['coeff_not_supported']['rx']:8}{dic['c(-1)']['coeff_not_supported']['tx']:4}{dic['c(0)']['coeff_not_supported']['rx']:8}{dic['c(0)']['coeff_not_supported']['tx']:4}{dic['c(1)']['coeff_not_supported']['rx']:8}{dic['c(1)']['coeff_not_supported']['tx']:4}
    coeff at limit          :{dic['c(-3)']['coeff_at_limit']['rx']:11}{dic['c(-3)']['coeff_at_limit']['tx']:4}{dic['c(-2)']['coeff_at_limit']['rx']:8}{dic['c(-2)']['coeff_at_limit']['tx']:4}{dic['c(-1)']['coeff_at_limit']['rx']:8}{dic['c(-1)']['coeff_at_limit']['tx']:4}{dic['c(0)']['coeff_at_limit']['rx']:8}{dic['c(0)']['coeff_at_limit']['tx']:4}{dic['c(1)']['coeff_at_limit']['rx']:8}{dic['c(1)']['coeff_at_limit']['tx']:4}
"""
