from __future__ import annotations

import contextlib
import functools
import logging
import pathlib
import re
import sys
from datetime import datetime
from io import TextIOWrapper
from time import sleep
from typing import Any
from typing import Generator

from serial import Serial
from serial.threaded import LineReader
from serial.threaded import ReaderThread


logger = logging.getLogger(__name__)


def filter_ansi_escape(line: str) -> str:
    COLOR_ESC = r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
    ESC_CHARS = r"[\x00-\x09]|[\x0B-\x1F]"
    ansi_escape = re.compile(f"{COLOR_ESC}|{ESC_CHARS}")
    return ansi_escape.sub("", line)


def add_line_timestamp(line: str) -> str:
    def timestamp() -> str:
        return datetime.now().strftime("[%H:%M:%S.%f]")

    return f"{timestamp()} {line}"


class Sniffer(LineReader):
    TERMINATOR = b"\n"

    def __init__(
        self,
        log_file: TextIOWrapper | None = None,
        clean_line: bool = True,
        add_timestamp: bool = True,
    ) -> None:
        super().__init__()
        self.log_file = log_file
        self.clean_line = clean_line
        self.add_timestamp = add_timestamp

    def handle_line(self, data: str) -> None:
        if self.log_file is not None:
            if self.clean_line:
                data = filter_ansi_escape(data)
            if self.add_timestamp:
                data = add_line_timestamp(data)
            self.log_file.write(f"{data}\n")


class SerialSniffer(Serial):
    def __init__(
        self,
        *args: Any,
        log_file: TextIOWrapper | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._log_file = log_file
        self.protocol = Sniffer()

    @property
    def log_file(self) -> TextIOWrapper | None:
        if self._log_file is None:
            raise UnboundLocalError("the log file need to be assigned.")
        return self._log_file

    @log_file.setter
    def log_file(self, log_file: TextIOWrapper | None) -> None:
        self.protocol.log_file = log_file
        self._log_file = log_file

    def read(self, size: int = 1) -> bytes:
        data = super().read(size)
        if self._log_file is not None:
            self.protocol.data_received(data)
        return data


class Component:
    def __init__(
        self,
        name: str,
        port: str,
        log_file: TextIOWrapper | None = None,
    ) -> None:
        self.name = name
        self.serial = SerialSniffer(
            port=port,
            baudrate=115200,
            timeout=5,
            log_file=log_file,
        )
        self._log_file = log_file
        self.sniff_thread: ReaderThread | None = None
        self.logger = logging.getLogger(name)

    @property
    def prompt(self) -> bytes:
        raise NotImplementedError

    @property
    def log_file(self) -> TextIOWrapper | None:
        return self._log_file

    @log_file.setter
    def log_file(self, log_file: TextIOWrapper) -> None:
        self.serial.log_file = log_file
        self._log_file = log_file

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

    def start_sniffing(self) -> ReaderThread:
        if not self.log_file:
            log = sys.stdout
        else:
            log = self.log_file
        self.serial.log_file = None
        self.sniff_thread = ReaderThread(
            self.serial,
            functools.partial(
                Sniffer,
                log_file=log,
            ),
        )
        self.sniff_thread.start()
        return self.sniff_thread

    def stop_sniffing(self) -> None:
        assert isinstance(self.sniff_thread, ReaderThread)
        self.sniff_thread.stop()
        self.sniff_thread = None
        self.serial.log_file = self.log_file

    def config_serial_log_file(self, log_file: pathlib.Path | str) -> None:
        self.logger.debug(f"configuring log file for serial: {log_file}")
        log_file = pathlib.Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        s_log_file = open(log_file, "w", buffering=1)
        self.log_file = s_log_file

    def wait_for_msg(self, msg: bytes, timeout: float) -> bytes:
        self.logger.debug(f"waiting for msg {msg.decode()!r}")
        with self.change_timeout_ctx(timeout):
            if not self.serial.is_open:
                self.serial.open()
            return self.serial.read_until(msg)
