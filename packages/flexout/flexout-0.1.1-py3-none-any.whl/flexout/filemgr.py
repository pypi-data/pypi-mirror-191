"""
File manager.

Optional requirement for Samba/Windows shares: pip install smbprotocol
"""
from __future__ import annotations
import os, ntpath, sys, logging
from pathlib import Path
from enum import Enum

try:
    import smbclient
    import smbclient.shutil as smbclient_shutil
except ImportError:
    smbclient = None
    smbclient_shutil = None

_cache = {
    'smb_credentials': False
}

logger = logging.getLogger('__name__')



def configure_smb_credentials(user: str = None, password: str = None):
    if user or password:
        if not smbclient:
            logger.warning(f'ignore smb credentials: package `smbprotocol` not available')
        else:
            smbclient.ClientConfig(username=user, password=password)
            _cache['smb_credentials'] = True


def smb_available():
    if sys.platform == 'win32' and not _cache['smb_credentials']:
        # Python is natively compatible with Samba shares on Windows
        return True

    if not smbclient:
        return False

    return True


def _is_remote_path(path: str):
    if not path:
        return False
    
    if isinstance(path, Path):
        path = str(path)
    
    if not (path.startswith("\\\\") or path.startswith("//")):
        return False

    return True


class Specific(Enum):
    NATIVE = 1
    SMBCLIENT = 2


def _use_specific(path: str) -> Specific|None:
    if not _is_remote_path(path):
        return False

    if sys.platform == 'win32' and not _cache['smb_credentials']:
        # Python is natively compatible with Samba shares on Windows
        return Specific.NATIVE

    if not smbclient:
        raise ModuleNotFoundError(f'cannot use smbclient: package `smbprotocol` not available')

    return Specific.SMBCLIENT


def exists(path: str):
    specific = _use_specific(path)
    if specific == Specific.SMBCLIENT:
        return smbclient.path.exists(path)
    elif specific == Specific.NATIVE:    
        return ntpath.exists(path)
    else:    
        return os.path.exists(path)


def stat(path: str):
    if _use_specific(path) == Specific.SMBCLIENT:
        return smbclient.stat(path)
    else:
        return os.stat(path)


def dirname(path: str):
    if _is_remote_path(path):
        return ntpath.dirname(path)
    else:
        return os.path.dirname(path)


def basename(path: str):
    if _is_remote_path(path):
        return ntpath.basename(path)
    else:
        return os.path.basename(path)


def splitext(path: str):
    if _is_remote_path(path):
        return ntpath.splitext(path)
    else:
        return os.path.splitext(path)


def makedirs(path: str, exist_ok: bool = False):
    if _use_specific(path) == Specific.SMBCLIENT:
        smbclient.makedirs(path, exist_ok=exist_ok)
    else:
        os.makedirs(path, exist_ok=exist_ok)


def remove(path: str):
    if _use_specific(path) == Specific.SMBCLIENT:
        smbclient.remove(path)
    else:
        os.remove(path)


def open_file(path: str, mode="r", buffering: int = -1, encoding: str = None, errors: str = None, newline: str = None, **kwargs):
    if _use_specific(path) == Specific.SMBCLIENT:
        return smbclient.open_file(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)
    else:
        return open(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)


def read_bytes(path: str):
    """
    Open the file in bytes mode, read it, and close the file.
    """
    if _use_specific(path) == Specific.SMBCLIENT:
        with smbclient.open_file(mode='rb') as f:
            return f.read()
    else:
        if not isinstance(path, Path):
            path = Path(path)
        return path.read_bytes()
    

def read_text(path: str, encoding: str = None, errors: str = None):
    """
    Open the file in text mode, read it, and close the file.
    """
    if _use_specific(path) == Specific.SMBCLIENT:
        with smbclient.open_file(mode='r', encoding=encoding, errors=errors) as f:
            return f.read()
    else:
        if not isinstance(path, Path):
            path = Path(path)
        return path.read_text(encoding=encoding, errors=errors)


def write_bytes(path: str, data):
    """
    Open the file in bytes mode, write to it, and close the file.
    """
    if _use_specific(path) == Specific.SMBCLIENT:
        with smbclient.open_file(mode='wb') as f:
            return f.write(data)
    else:
        if not isinstance(path, Path):
            path = Path(path)
        return path.write_bytes(data)
    

def write_text(path: str, data: str, encoding: str = None, errors: str = None, newline: str = None):
    """
    Open the file in text mode, write to it, and close the file.
    """
    if _use_specific(path) == Specific.SMBCLIENT:
        with smbclient.open_file(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
            return f.write(data)
    else:
        if not isinstance(path, Path):
            path = Path(path)
        return path.write_text(data, encoding=encoding, errors=errors, newline=newline)


def copy(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    return smbclient_shutil.copy(src, dst, follow_symlinks=follow_symlinks)


def copy2(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    return smbclient_shutil.copy2(src, dst, follow_symlinks=follow_symlinks)


def copyfile(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    return smbclient_shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)


def copystat(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    return smbclient_shutil.copystat(src, dst, follow_symlinks=follow_symlinks)


def copymode(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    return smbclient_shutil.copymode(src, dst, follow_symlinks=follow_symlinks)


def copytree(src: str, dst: str, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=False):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    return smbclient_shutil.copytree(src, dst, symlinks=symlinks, ignore=ignore, ignore_dangling_symlinks=ignore_dangling_symlinks, dirs_exist_ok=dirs_exist_ok)


def rmtree(path: str, ignore_errors=False, onerror=None):
    if isinstance(path, Path):
        path = str(path)
    return smbclient_shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)
