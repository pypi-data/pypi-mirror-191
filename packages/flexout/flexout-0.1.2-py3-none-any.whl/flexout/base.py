from __future__ import annotations
import sys
from io import IOBase
from typing import Any, Callable
from enum import Enum
from datetime import datetime, timezone

if sys.version_info[0:2] < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

from . import filemgr


class IFlexout(Protocol):
    file: IOBase
    target: str
    target_is_path: bool
    split_path_target: Callable[[],tuple[str,str]]


class Format:
    flexout: IFlexout
    opened_by_me: bool

    def __init__(self, flexout: IFlexout, append: bool = False, newline: str = None, encoding: str = None, dialect: str = None, timezone: timezone = None):
        self.headers: list[str] = None
        self.rows: list[list] = []

        self.flexout = flexout

        self.append = append
        self.newline = newline
        self.encoding = encoding
        self.dialect = dialect
        self.timezone = timezone


    def open_file(self):
        return filemgr.open_file(self.flexout.target, mode='a' if self.append else 'w', newline=self.newline, encoding=self.encoding, mkdir=True)


    def before_end(self):
        pass


    def after_end(self):
        pass


    def append_headers(self, headers: list[str]):
        self.headers = headers
        return self.headers


    def append_row(self, row: list):
        row = self.format_row(row)
        self.rows.append(row)
        return row


    def format_row(self, row: list):
        if self.headers is not None:
            while len(row) < len(self.headers):
                row.append(None)

        for i, value in enumerate(row):
            row[i] = self.format_value(value)

        return row


    def format_value(self, value: Any) -> str:
        if value is None:
            return None
        elif isinstance(value, Enum):
            return value.name
        elif isinstance(value, list):
            return '|'.join(value)
        else:
            return value
