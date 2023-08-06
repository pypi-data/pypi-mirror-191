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
    import smbclient.path as smbclient_path
    import smbclient.shutil as smbclient_shutil
except ImportError:
    smbclient = None
    smbclient_path = None
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


def _smb_available():
    if sys.platform == 'win32' and not _cache['smb_credentials']:
        # Python is natively compatible with Samba shares on Windows
        return True

    if not smbclient:
        return False

    return True


class _UseSmb(Enum):
    NATIVE = 1
    SMBCLIENT = 2


def _usage(path: str) -> tuple[str,_UseSmb|None]:
    if not path:
        return path, False
    
    if isinstance(path, Path):
        path = str(path)

    path = os.path.expanduser(path)
    
    if not (path.startswith("\\\\") or path.startswith("//")):
        return path, False  # not a remote path

    if sys.platform == 'win32' and not _cache['smb_credentials']:
        # Python is natively compatible with Samba shares on Windows
        return path, _UseSmb.NATIVE

    if not smbclient:
        raise ModuleNotFoundError(f'cannot use smbclient: package `smbprotocol` not available')

    return path, _UseSmb.SMBCLIENT


def exists(path: str):
    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
        return smbclient_path.exists(path)
    elif use_smb == _UseSmb.NATIVE:    
        return ntpath.exists(path)
    else:    
        return os.path.exists(path)


def stat(path: str):
    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
        return smbclient.stat(path)
    else:
        return os.stat(path)


def dirname(path: str):
    path, use_smb = _usage(path)
    if use_smb:
        return ntpath.dirname(path)
    else:
        return os.path.dirname(path)


def basename(path: str):
    path, use_smb = _usage(path)
    if use_smb:
        return ntpath.basename(path)
    else:
        return os.path.basename(path)


def splitext(path: str):
    path, use_smb = _usage(path)
    if use_smb:
        return ntpath.splitext(path)
    else:
        return os.path.splitext(path)


def makedirs(path: str, exist_ok: bool = False):
    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
        smbclient.makedirs(path, exist_ok=exist_ok)
    else:
        os.makedirs(path, exist_ok=exist_ok)


def remove(path: str):
    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
        smbclient.remove(path)
    else:
        os.remove(path)


def open_file(path: str, mode="r", buffering: int = -1, encoding: str = None, errors: str = None, newline: str = None, mkdir: bool = False, **kwargs):
    if mkdir:
        dir_path = dirname(path)
        if dir_path:
            makedirs(dir_path, exist_ok=True)

    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
        return smbclient.open_file(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)
    else:
        return open(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)


def read_bytes(path: str):
    """
    Open the file in bytes mode, read it, and close the file.
    """
    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
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
    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
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
    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
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
    path, use_smb = _usage(path)
    if use_smb == _UseSmb.SMBCLIENT:
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
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)
    return smbclient_shutil.copy(src, dst, follow_symlinks=follow_symlinks)


def copy2(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)
    return smbclient_shutil.copy2(src, dst, follow_symlinks=follow_symlinks)


def copyfile(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)
    return smbclient_shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)


def copystat(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)
    return smbclient_shutil.copystat(src, dst, follow_symlinks=follow_symlinks)


def copymode(src: str, dst: str, follow_symlinks=True):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)
    return smbclient_shutil.copymode(src, dst, follow_symlinks=follow_symlinks)


def copytree(src: str, dst: str, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=False):
    if isinstance(src, Path):
        src = str(src)
    if isinstance(dst, Path):
        dst = str(dst)
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)
    return smbclient_shutil.copytree(src, dst, symlinks=symlinks, ignore=ignore, ignore_dangling_symlinks=ignore_dangling_symlinks, dirs_exist_ok=dirs_exist_ok)


def rmtree(path: str, ignore_errors=False, onerror=None):
    if isinstance(path, Path):
        path = str(path)
    path = os.path.expanduser(path)
    return smbclient_shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)
