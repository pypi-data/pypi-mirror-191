"""
File manager.

Optional requirement for Samba/Windows shares: pip install smbprotocol
"""
from __future__ import annotations
import os, ntpath, sys, logging
from pathlib import Path

try:
    import smbclient
except ImportError:
    smbclient = None

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


def _use_smbclient(path: str):
    if not path:
        return False
    
    if isinstance(path, Path):
        path = str(path)
    
    if not path.startswith(r'\\'):
        return False

    if sys.platform == 'win32' and not _cache['smb_credentials']:
        # Python is natively compatible with Samba shares on Windows
        return False

    if not smbclient:
        raise ModuleNotFoundError(f'cannot use smbclient: package `smbprotocol` not available')

    return True


def exists(path: str):
    if _use_smbclient(path):
        return smbclient.path.exists(path)
    else:
        return os.path.exists(path)


def dirname(path: str):
    if _use_smbclient(path):
        return ntpath.dirname(path)
    else:
        return os.path.dirname(path)


def basename(path: str):
    if _use_smbclient(path):
        return ntpath.basename(path)
    else:
        return os.path.basename(path)


def makedirs(path: str, exist_ok: bool = False):
    if _use_smbclient(path):
        smbclient.makedirs(path, exist_ok=exist_ok)
    else:
        os.makedirs(path, exist_ok=exist_ok)


def open_file(path: str, mode="r", buffering=-1, encoding=None, errors=None, newline=None, **kwargs):
    if _use_smbclient(path):
        return smbclient.open_file(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)
    else:
        return open(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)


def remove(path: str):
    if _use_smbclient(path):
        smbclient.remove(path)
    else:
        os.remove(path)
