from __future__ import annotations

from xoa_driver.ports import GenericAnyPort
import typing as t


class ConfigError(Exception):
    def __init__(self) -> None:
        self.name = ""
        self.msg = ""

    def __repr__(self) -> str:
        return self.msg

    def __str__(self) -> str:
        return self.msg


class NotConnectedError(ConfigError):
    def __init__(self) -> None:
        self.name = "Not Connected Error"
        self.msg = "No tester is connected!"


class NoSuchModuleError(ConfigError):
    def __init__(self, module_id: int) -> None:
        self.name = "No Such Module Error"
        self.msg = f"No such module {module_id}!"


class NoSuchIDError(ConfigError):
    def __init__(self, general_id: str) -> None:
        self.name = "No Such ID Error"
        self.msg = f"No such ID {general_id}!"


class NotInStoreError(ConfigError):
    def __init__(self, general_id: str) -> None:
        self.name = "Not in store Error"
        self.msg = f"Not in store {general_id}!"


class NotCorrectLaneError(ConfigError):
    def __init__(self, port_id: str, lane: int) -> None:
        self.name = "Not Correct Lane Error"
        self.msg = f"No lane {lane} in port {port_id}!"


class NoSuchPortError(ConfigError):
    def __init__(self, port_id: int) -> None:
        self.name = "No Such Port Error"
        self.msg = f"No such port {port_id}!"


class NoWorkingPort(ConfigError):
    def __init__(self) -> None:
        self.name = "No Working Port Error"
        self.msg = (
            f"There is no working port, please use 'port' command to specify one!"
        )


class NotSupportPcsPmaError(ConfigError):
    def __init__(self, port: GenericAnyPort) -> None:
        module_id, port_id = port.kind.module_id, port.kind.port_id
        self.name = "Not Support Pcs Pma Error"
        self.msg = f"This port {module_id}/{port_id} does not support pcs_pma!"


class NotSupportAutoNegError(ConfigError):
    def __init__(self, port: GenericAnyPort) -> None:
        module_id, port_id = port.kind.module_id, port.kind.port_id
        self.name = "Not Support Autoneg Error"
        self.msg = f"This port {module_id}/{port_id} does not support auto negotiation!"


class NotSupportLinkTrainError(ConfigError):
    def __init__(self, port: GenericAnyPort) -> None:
        module_id, port_id = port.kind.module_id, port.kind.port_id
        self.name = "Not Support Link Train Error"
        self.msg = f"This port {module_id}/{port_id} does not support link training!"


class NotRightLaneLengthError(ConfigError):
    def __init__(self, lane: list[int]) -> None:
        self.name = "Not Right Lane Length Error"
        self.msg = f"Lane {lane} should be length of 4!"


class NotRightLaneValueError(ConfigError):
    def __init__(self, lane: list[int]) -> None:
        self.name = "Not Right Lane Value Error"
        self.msg = f"Lane {lane} should be a list of 4 integers ranges from 0 to 255!"


# class NotInChoicesError(ConfigError):
#     def __init__(self, string: str, choices: list[str]) -> None:
#         self.name = "Not In Choices Error"
#         self.msg = f"{string} is not in the choices {choices}!"


class CannotConvertError(ConfigError):
    def __init__(self, e: Exception) -> None:
        self.name = "Cannot Convert Error"
        self.msg = f"{e}!"


class NotSameLengthError(ConfigError):
    def __init__(self, a: t.Iterable, b: t.Iterable) -> None:
        self.name = "Zip Error"
        self.msg = f"{a} {b} are not of the same length!"
