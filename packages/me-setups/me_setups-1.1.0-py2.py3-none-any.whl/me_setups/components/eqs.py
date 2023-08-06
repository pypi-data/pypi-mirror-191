from __future__ import annotations

import pathlib
import subprocess
from enum import Enum
from io import TextIOWrapper
from typing import Any

from me_setups.components import tools
from me_setups.components.comp import Component
from me_setups.components.tools import OSType

PCD_WRITE_COMPLETE = b"##################### CAUTION P-COREDUMP TO  EMMC COMPLETE !! ######################"  # noqa: E501
FCD_WRITE_COMPLETE = b"OK"
LINUX_BOOT_MSG = b"Welcome to EyeQ5"
NO_KEY_CHECK = ["-o", "StrictHostKeyChecking=no"]
NO_SSH_ERROR = ["-E", "/dev/null"]
PROMPTS = {
    OSType.LINUX: b"# ",
    OSType.VOIS: b"VOiS>>",
    OSType.UBOOT: b"EyeQ5 # ",
}


class CoreType(Enum):
    PCD = "pcd"
    FCD = "fcd"


class EyeQ5(Component):
    def __init__(
        self,
        name: str,
        port: str,
        os_type: OSType = OSType.LINUX,
        log_file: TextIOWrapper | None = None,
    ) -> None:
        super().__init__(name, port, log_file)
        self.os_type = os_type

    @property
    def chip(self) -> int:
        return int(self.name[-2])

    @property
    def mid(self) -> int:
        return int(self.name[-1])

    @property
    def prompt(self) -> bytes:
        return PROMPTS[self.os_type]

    @property
    def ip(self) -> str:
        ip = tools.get_eq_ip(self.name, self.os_type)
        assert ip
        return ip

    @property
    def _ssh_root(self) -> str:
        return f"root@{self.ip}"

    def _scp(
        self,
        _from: str,
        _to: str,
        timeout: float = 5,
    ) -> subprocess.CompletedProcess[str]:
        cmd = ["scp"] + NO_KEY_CHECK
        cmd += [_from]
        cmd += [_to]
        return self._sp_cmd(cmd, timeout)

    def copy_from(
        self,
        src: pathlib.Path | str,
        dst: pathlib.Path | str,
        timeout: float = 5,
    ) -> subprocess.CompletedProcess[str]:
        return self._scp(f"{self._ssh_root}:{src}", str(dst), timeout)

    def copy_to(
        self,
        src: pathlib.Path | str,
        dst: pathlib.Path | str,
        timeout: float = 5,
    ) -> subprocess.CompletedProcess[str]:
        return self._scp(str(src), f"{self._ssh_root}:{dst}", timeout)

    def wait_for_linux_boot(self) -> bool:
        boot_msg = b"Welcome to EyeQ5"
        return boot_msg in self.wait_for_msg(boot_msg, 120)

    def run_ssh_cmd(
        self,
        cmd: str,
        timeout: float = 5,
        **kwargs: Any,
    ) -> subprocess.CompletedProcess[str]:
        assert self.os_type == OSType.LINUX
        ssh_cmd = ["ssh"] + NO_KEY_CHECK + NO_SSH_ERROR + [self._ssh_root]
        ssh_cmd.append(cmd)
        return self._sp_cmd(ssh_cmd, timeout, **kwargs)

    def _sp_cmd(
        self,
        cmd: list[str],
        timeout: float,
        **kwargs: Any,
    ) -> subprocess.CompletedProcess[str]:
        self.logger.debug(f"[ssh] running cmd: {' '.join(cmd)!r}")
        res = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            text=True,
            **kwargs,
        )
        self.logger.debug(res)
        return res

    def path_exists(self, path: pathlib.Path | str) -> bool:
        return self.run_ssh_cmd(f"ls {path}").returncode == 0

    def ssh_cmd_stdout(self, cmd: str, **kwargs: Any) -> str:
        return self.run_ssh_cmd(cmd, **kwargs).stdout

    def list_dir(self, _dir: pathlib.Path | str) -> list[str]:
        ls_cmd = self.run_ssh_cmd(f"ls -1 {_dir}")
        if ls_cmd.returncode == 0:
            return ls_cmd.stdout.splitlines()
        elif "No such file or directory" in ls_cmd.stderr:
            raise FileNotFoundError(ls_cmd.stderr)
        else:
            raise Exception(ls_cmd.stderr)

    def wait_for_core_write(self, core_type: CoreType) -> bool:
        self.logger.debug(f"Waiting for {core_type.name} write completion")
        if core_type == CoreType.PCD:
            core_complete_msg = PCD_WRITE_COMPLETE
            timeout = 90
        elif core_type == CoreType.FCD:
            core_complete_msg = FCD_WRITE_COMPLETE
            timeout = 180
        else:
            raise NotImplementedError
        return core_complete_msg in self.wait_for_msg(
            core_complete_msg,
            timeout,
        )
