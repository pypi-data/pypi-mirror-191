from __future__ import annotations

import contextlib
import logging
import pathlib
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from subprocess import CompletedProcess
from typing import Generator

import me_setups.components.const as C
from me_setups.components.eqs import EyeQ5
from me_setups.components.eqs import OSType
from me_setups.components.mcu import Mcu
from me_setups.components.mcu import McuType


class BoardType(Enum):
    GAS52 = "GAS52"
    EVO = "EVO"
    EOL = "End Of Line"
    EVO_EOL = "EVO End Of Line"


class Gas52Board:
    log_folder: pathlib.Path | None
    eqs: list[EyeQ5]
    mcus: list[Mcu]

    def __init__(
        self,
        eqs: dict[str, str] = C.GAS52_EQS,
        mcus: dict[str, str] = C.GAS52_MCU,
        board_type: BoardType = BoardType.GAS52,
        os_type: OSType | None = None,
        mcu_type: McuType | None = None,
    ) -> None:
        self.log_folder = None
        self.board_type = board_type
        self.logger = logging.getLogger("Gas52Board")
        self.eqs = self.generate_eqs(eqs, os_type)
        self.mcus = self.generate_mcus(mcus, mcu_type)
        self.mcs = None

    def generate_eq(
        self,
        eq_name: str,
        eq_port: str,
        os_type: OSType | None = None,
    ) -> EyeQ5:
        self.logger.debug(f"generating eyeq {eq_name}")
        if os_type is not None:
            eq = EyeQ5(eq_name, eq_port, os_type)
        elif self.board_type in (BoardType.GAS52, BoardType.EVO):
            eq = EyeQ5(eq_name, eq_port, OSType.LINUX)
        elif self.board_type in (BoardType.EOL, BoardType.EVO_EOL):
            eq = EyeQ5(eq_name, eq_port, OSType.VOIS)
        else:
            raise NotImplementedError
        return eq

    def generate_eqs(
        self,
        eqs: dict[str, str],
        os_type: OSType | None = None,
    ) -> list[EyeQ5]:
        return [
            self.generate_eq(eq_name, eq_port, os_type)
            for eq_name, eq_port in eqs.items()  # for black format
        ]

    def generate_mcu(
        self,
        mcu_name: str,
        mcu_port: str,
        mcu_type: McuType | None = None,
    ) -> Mcu:
        self.logger.debug(f"generating mcu {mcu_name}")
        if mcu_type is not None:
            mcu = Mcu(mcu_name, mcu_port, mcu_type)
        elif self.board_type == BoardType.GAS52:
            mcu = Mcu(mcu_name, mcu_port, McuType.ADAM)
        elif self.board_type == BoardType.EVO:
            mcu = Mcu(mcu_name, mcu_port, McuType.ASR)
        elif self.board_type == BoardType.EOL:
            mcu = Mcu(mcu_name, mcu_port, McuType.MEAVES)
        elif self.board_type == BoardType.EVO_EOL:
            mcu = Mcu(mcu_name, mcu_port, McuType.MEAVES_SINGLE_IMG)
        else:
            raise NotImplementedError
        return mcu

    def generate_mcus(
        self,
        mcus: dict[str, str],
        mcu_type: McuType | None = None,
    ) -> list[Mcu]:
        return [
            self.generate_mcu(mcu_name, mcu_port, mcu_type)
            for mcu_name, mcu_port in mcus.items()  # for black format
        ]

    def get_eyeq(self, chip: int, mid: int) -> EyeQ5:
        return self.eqs[chip * 2 + mid]

    def config_log_files(self, log_folder: pathlib.Path | str) -> None:
        self.logger.debug(f"configuring log folder {log_folder}")
        self.log_folder = pathlib.Path(log_folder)
        self.log_folder.mkdir(parents=True, exist_ok=True)
        for conn in self.conns:
            conn.config_serial_log_file(self.log_folder / f"{conn.name}.log")

    @property
    def mcu(self) -> Mcu:
        assert not len(self.mcus) > 1, "More then one MCU in setup!"
        return self.mcus[0]

    @property
    def conns(self) -> list[EyeQ5 | Mcu]:
        return self.eqs + self.mcus

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(eqs={self.eqs}, mcu={self.mcu})"

    @contextlib.contextmanager
    def sniff(
        self,
        log_folder: pathlib.Path,
    ) -> Generator[None, None, None]:
        self.config_log_files(log_folder)
        try:
            for conn in self.conns:
                conn.start_sniffing()
            yield
        finally:
            for conn in self.conns:
                conn.stop_sniffing()

    def close_serials(self) -> None:
        for conn in self.conns:
            conn.logger.debug("closing serial")
            conn.serial.close()

    def open_serials(self) -> None:
        for conn in self.conns:
            if not conn.serial.is_open:
                conn.logger.debug("opening serial")
                conn.serial.open()

    def restart_serials(self) -> None:
        self.close_serials()
        self.open_serials()

    def run_ssh_cmd_all(self, cmd: str) -> list[CompletedProcess[str]]:
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            results = executor.map(
                lambda eq: eq.run_ssh_cmd(cmd),
                self.eqs,
            )
        return list(results)

    def wait_for_msg_all(self, msg: bytes, timeout: float) -> bool:
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            results = executor.map(
                lambda eq: eq.wait_for_msg(msg, timeout),
                self.eqs,
            )
        return all(results)

    def wait_for_linux_boot(self) -> bool:
        with ThreadPoolExecutor(max_workers=len(self.eqs)) as executor:
            results = executor.map(
                lambda eq: eq.wait_for_linux_boot(),
                self.eqs,
            )
        return all(results)

    def reboot(self, *, sleep_after: int = 0) -> None:
        if self.board_type == BoardType.EVO:
            raise NotImplementedError("reboot is not support on EVO")

        self.logger.info("rebooting platform...")

        if self.mcs is not None:
            self.logger.debug("rebooting MCS")
            self.mcs.run_serial_cmd("reboot")

        self.logger.debug("rebooting board")
        self.mcu.run_serial_cmd("reboot")

        if sleep_after > 0:
            self.logger.info(f"sleeping for {sleep_after} seconds.")
            time.sleep(sleep_after)
