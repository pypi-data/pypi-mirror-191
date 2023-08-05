from __future__ import annotations
from .base import Format

try:
    from tabulate import tabulate
    _import_error = None
except ImportError as err:
    _import_error = str(err)


class TabulateFormat(Format):
    @classmethod
    def is_available(cls):
        return _import_error is None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.is_available():
            raise ValueError(f"cannot use {self.__class__.__name__}: {_import_error}")
    
    
    def before_end(self):
        if not self.rows and not self.headers:
            return
        
        print(tabulate(self.rows, headers=self.headers), file=self.flexout.file)
