from __future__ import annotations
import csv, _csv, os, locale, logging
from datetime import datetime
from typing import Any

from . import filemgr
from .base import Format


logger = logging.getLogger(__name__)


class CsvFormat(Format):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # For CSV files:
        # - Set newline to '', otherwise newlines embedded inside quoted fields will not be interpreted correctly. See footnote of: https://docs.python.org/3/library/csv.html
        # - Set encoding to utf-8-sig (UTF8 with BOM): CSV is for exchanges, encoding should not depend on the exporting operating system. BOM is necessary for correct display with Excel.
        if self.newline is None:
            self.newline = ''
        if self.encoding is None:
            self.encoding = 'utf-8-sig'

        self.dialect = get_dialect(self.dialect)
        dialect_str = (self.dialect if isinstance(self.dialect, str) else (self.dialect.__name__ if isinstance(self.dialect, type) else type(self.dialect).__name__)).replace('_', '-')

        if dialect_str == 'excel':
            self.excel_dialect = 'default'
        elif dialect_str.startswith('excel-'):
            self.excel_dialect = dialect_str[6:]
        else:
            self.excel_dialect = None
        
        self.headers_mapping: dict[int,int] = None


    def open_file(self):
        self.read_existing_file_if_any()
        return super().open_file()

    
    def read_existing_file_if_any(self):
        if hasattr(self, 'previous_headers'):
            return
        
        # Determine headers of existing file
        self.previous_headers: list[str] = None
        if self.append and self.flexout.target_is_path and filemgr.exists(self.flexout.target):
            with filemgr.open_file(self.flexout.target, 'r', newline='') as f:
                reader = csv.reader(f, dialect=self.dialect)
                try:
                    self.previous_headers = next(reader)
                except StopIteration:
                    self.previous_headers = None


    @property
    def writer(self) -> _csv._writer:
        try:
            return getattr(self, '_writer')
        except AttributeError:
            self._writer = csv.writer(self.flexout.file, dialect=self.dialect)
            return self._writer


    headers_mapping_actual_len: int

    def append_headers(self, headers: list[str]):
        headers = super().append_headers(headers)
        
        self.read_existing_file_if_any()
        if self.previous_headers:
            # Determine mapping
            additional_headers = []
            for pos, header in enumerate(headers):
                try:
                    previous_pos = self.previous_headers.index(header)
                except ValueError:
                    additional_headers.append(header)
                    previous_pos = len(self.previous_headers) + len(additional_headers) - 1

                if previous_pos != pos:
                    if self.headers_mapping is None:
                        self.headers_mapping = {}
                    self.headers_mapping[pos] = previous_pos

            if additional_headers:
                logger.warning(f"header missing in existing file: {', '.join(additional_headers)} - corresponding data will be appended without the header name")

            self.headers_mapping_actual_len = len(headers) + len(additional_headers)

        else:
            self.writer.writerow(headers)
            self.flexout.file.flush()


    def append_row(self, row: list):
        row = super().append_row(row)

        if self.headers_mapping:
            # Apply mapping
            reordered_row = [None] * self.headers_mapping_actual_len
            pos = 0
            while pos < len(row):
                reordered_row[self.headers_mapping.get(pos, pos)] = row[pos]
                pos += 1
            row = reordered_row

        self.writer.writerow(row)
        self.flexout.file.flush()


    def format_value(self, value: Any) -> str:
        if value is None:
            return None
        elif isinstance(value, datetime):
            # If output is expected in a given timezone, we make this datetime naive in the target timezone and display it in a format understandable by Excel
            if value.tzinfo:
                if self.timezone:
                    value: datetime = value.astimezone(None if self.timezone == 'local' else self.timezone)
                    use_tzinfo = False
                else:
                    use_tzinfo = True
            else:
                use_tzinfo = False

            # Format microseconds. For excel, remove it if we can make Excel interprete the value as datetime
            if self.excel_dialect or value.microsecond == 0:
                mspart = ''
            else:
                mspart = '.' + value.strftime('%f')
            
            # Format tzinfo and microseconds
            if use_tzinfo:
                tzpart = value.strftime('%z')
                if len(tzpart) == 5:
                    tzpart = tzpart[0:3] + ':' + tzpart[3:]
            else:
                tzpart = ''

            return value.strftime("%Y-%m-%d %H:%M:%S") + mspart + tzpart
        elif isinstance(value, float) and self.excel_dialect == 'fr':
            return str(value).replace('.', ',')
        elif hasattr(value, 'value'): # example: ValueString
            return getattr(value, 'value')
        else:
            return super().format_value(value)


class excel_fr(csv.excel):
    """ Dialect for French version of Excel. """
    delimiter = ";"


def get_dialect(name: str|csv.Dialect|type[csv.Dialect] = None, default: str|csv.Dialect|type[csv.Dialect] = None) -> str|csv.Dialect|type[csv.Dialect]:
    # Register my own dialects
    available_dialects = csv.list_dialects()

    if 'excel-fr' not in available_dialects:
        csv.register_dialect('excel-fr', excel_fr())
        available_dialects.append('excel-fr')

    # Return if name or default given
    if name:
        return name
    
    if default:
        return default
    
    default = os.environ.get("CSV_DIALECT", None)
    if default:
        return default

    # If nothing provided, try to detect language
    language_code, _ = locale.getlocale()
    lang = language_code[0:2]
    dialect = f"excel-{lang}"
    if dialect in available_dialects:
        return dialect

    return 'excel'
