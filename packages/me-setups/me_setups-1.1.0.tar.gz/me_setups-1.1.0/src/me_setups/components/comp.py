from __future__ import annotations

import contextlib
import logging
import os
import pathlib
import re
import threading
from datetime import datetime
from io import TextIOWrapper
from time import sleep
from typing import Any
from typing import Generator

import serial


def filter_ansi_escape(line: str) -> str:
    ESC_CHARS = (
        r"(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|[\x00-\x09]|[\x0B-\x1F])"  # noqa: E501
    )
    ansi_escape = re.compile(ESC_CHARS)
    return ansi_escape.sub("", line)


def add_line_timestamp(line: str) -> str:
    def timestamp() -> str:
        return datetime.now().strftime("[%H:%M:%S.%f]")

    return f"{timestamp()} {line}"


class MblySerial(serial.Serial):
    _log_file: TextIOWrapper

    def __init__(
        self,
        log_file: TextIOWrapper | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        if log_file is None:
            self._log_file = open(os.devnull, "w")
        else:
            self._log_file = log_file

    @property
    def log_file(self) -> TextIOWrapper:
        return self._log_file

    @log_file.setter
    def log_file(
        self,
        log_file: TextIOWrapper | None,
    ) -> None:
        if log_file is None:
            return
        if isinstance(log_file, TextIOWrapper):
            self._log_file = log_file

    def _read(self, size: int = 1) -> bytes:
        return super().read(size)

    def read(self, size: int = 1) -> bytes:
        buffer = super().read(size)
        if buffer:
            self.log_file.write(buffer.decode(encoding="latin-1"))
        return buffer


class Component:
    def __init__(
        self,
        name: str,
        port: str,
        log_file: TextIOWrapper | None = None,
    ) -> None:
        self.name = name
        self.serial = MblySerial(
            port=port,
            baudrate=115200,
            timeout=5,
            log_file=log_file,
        )
        self.logger = logging.getLogger(name)

    @property
    def prompt(self) -> bytes:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    @contextlib.contextmanager
    def change_timeout_ctx(
        self,
        timeout: float,
    ) -> Generator[None, None, None]:
        orig_timeout = self.serial.timeout
        try:
            self.serial.timeout = timeout
            yield
        finally:
            self.serial.timeout = orig_timeout

    def run_serial_cmd(self, cmd: str) -> None:
        self.logger.debug(f"[serial] running cmd: {cmd!r}")
        cmd_b = cmd.encode()
        cmd_b += b"\n"
        for b in cmd_b:
            self.serial.write(bytes([b]))
            sleep(0.01)
        sleep(0.4)

    def start_sniffing(self) -> threading.Thread:
        self.event = threading.Event()
        assert isinstance(self.event, threading.Event)
        self.thread = threading.Thread(
            name=self.serial.port,
            target=self._sniff,
            daemon=True,
        )
        self.thread.start()
        return self.thread

    def stop_sniffing(self) -> None:
        assert isinstance(self.event, threading.Event)
        assert isinstance(self.thread, threading.Thread)
        self.event.set()
        self.thread.join(timeout=5)

    def _sniff(self, add_timestamp: bool = True) -> None:
        orig_read = self.serial.read
        setattr(self.serial, "read", self.serial._read)
        while self.event is None or not self.event.is_set():
            line = self.serial.readline()
            if not line.strip():
                continue
            line_s = filter_ansi_escape(line.decode(errors="ignore"))
            if add_timestamp:
                line_s = add_line_timestamp(line_s)
            self.serial.log_file.write(line_s)
        setattr(self.serial, "read", orig_read)

    def config_serial_log_file(self, log_file: pathlib.Path | str) -> None:
        self.logger.debug(f"configuring log file for serial: {log_file}")
        log_file = pathlib.Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        self.serial.log_file = open(
            log_file,
            "w",
            buffering=1,
        )

    def wait_for_msg(self, msg: bytes, timeout: float) -> bytes:
        self.logger.debug(f"waiting for msg {msg.decode()!r}")
        with self.change_timeout_ctx(timeout):
            if not self.serial.is_open:
                self.serial.open()
            return self.serial.read_until(msg)
