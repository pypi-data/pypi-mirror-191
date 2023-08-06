import abc
from ctypes import *

from libp2p import PeerStore
from libp2p.utils import *


lib = load_library()


class Validator(abc.ABC):
    lib.validator_delete.argtypes = [c_size_t, ]
    _FREE = lib.validator_delete
    _VALIDATE_FUNC = CFUNCTYPE(c_size_t, c_size_t, POINTER(c_char), )
    _SELECT_FUNC = _VALIDATE_FUNC
    lib.validator_new.argtypes = [_VALIDATE_FUNC, _SELECT_FUNC, ]
    lib.validator_new.restype = c_size_t
    _INIT = lib.validator_new

    def __init__(self):
        def _v(length: int, ptr: POINTER(c_char)):
            mp = MsgpackBody()
            mp.set_members(length, ptr)
            key, value = mp.bytes[0], mp.bytes[1]
            strings = list()
            try:
                self.validate(key=key, value=value)
            except Exception as e:
                err = str(e)
                strings.append(err)
            resp = {
                "Strings": strings,
            }
            return MsgpackBody.callback_return(resp)

        def _s(length: int, ptr: POINTER(c_char)):
            mp = MsgpackBody()
            mp.set_members(length, ptr)
            key, values = mp.bytes[0], mp.bytes[1:]
            strings = list()
            integers = list()
            try:
                idx = self.select(key=key, values=values)
                if idx < 0 or idx >= len(values):
                    raise IndexError
                integers.append(idx)
            except Exception as e:
                err = str(e)
                strings.append(err)
            resp = {
                "Integers": integers,
                "Strings": strings,
            }
            return MsgpackBody.callback_return(resp)

        self._v_fp = self._VALIDATE_FUNC(_v)
        self._s_fp = self._SELECT_FUNC(_s)
        self.handle = self._INIT(self._v_fp, self._s_fp)
        super().__init__()

    @abc.abstractmethod
    def validate(self, key: bytes, value: bytes):
        raise NotImplementedError

    @abc.abstractmethod
    def select(self, key: bytes, values: list[bytes]) -> int:
        raise NotImplementedError


class PublicKeyValidator(SimpleFreeMixin):
    lib.validator_delete.argtypes = [c_size_t, ]
    _FREE = lib.validator_delete
    lib.validator_publicKeyValidator.restype = c_size_t
    _INIT = lib.validator_publicKeyValidator

    def __init__(self):
        self.handle = self._INIT()
        super().__init__()
    

class IpnsValidator(SimpleFreeMixin):
    lib.validator_delete.argtypes = [c_size_t, ]
    _FREE = lib.validator_delete
    lib.validator_ipnsValidator.argtypes = [c_size_t, ]
    lib.validator_ipnsValidator.restype = c_size_t
    _INIT = lib.validator_ipnsValidator

    def __init__(self, peer_store: PeerStore):
        self.handle = self._INIT(peer_store.handle)
        super().__init__()


__all__ = [
    'Validator',
    'PublicKeyValidator',
    'IpnsValidator',
]
