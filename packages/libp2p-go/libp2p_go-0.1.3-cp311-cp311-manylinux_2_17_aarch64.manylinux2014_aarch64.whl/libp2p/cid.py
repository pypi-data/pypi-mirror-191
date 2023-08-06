from ctypes import *
from typing import Self
from functools import cached_property
from libp2p.utils import *


lib = load_library()


class Cid(SimpleFreeMixin):
    lib.cid_delete.argtypes = [c_size_t, ]
    _FREE = lib.cid_delete
    lib.cid_newCidV1.argtypes = [c_ulonglong, c_size_t, POINTER(c_ubyte), ]
    lib.cid_newCidV1.restype = MsgpackBody
    _NEW_CID_V1 = lib.cid_newCidV1
    lib.cid_defined.argtypes = [c_size_t, ]
    lib.cid_defined.restype = c_bool
    _DEFINED = lib.cid_defined
    lib.varint_toUvarint.argtypes = [c_ulonglong, ]
    lib.varint_toUvarint.restype = MsgpackBody
    _TO_UVARINT = lib.varint_toUvarint
    lib.cid_bytes.argtypes = [c_size_t, ]
    lib.cid_bytes.restype = MsgpackBody
    _BYTES = lib.cid_bytes
    lib.cid_fromBytes.argtypes = [c_size_t, POINTER(c_ubyte), ]
    lib.cid_fromBytes.restype = MsgpackBody
    _FROM_BYTES = lib.cid_fromBytes
    lib.cid_decode.argtypes = [GoString, ]
    lib.cid_decode.restype = MsgpackBody
    _DECODE = lib.cid_decode
    lib.cid_version.argtypes = [c_size_t, ]
    lib.cid_version.restype = c_uint64
    _VERSION = lib.cid_version
    lib.cid_type.argtypes = [c_size_t, ]
    lib.cid_type.restype = c_uint64
    _TYPE = lib.cid_type
    lib.cid_string.argtypes = [c_size_t, ]
    lib.cid_string.restype = MsgpackBody
    _STRING = lib.cid_string

    def __init__(self, codec_type: int = None, key: bytes = None, _handle: int = None):
        if _handle is not None:
            self.handle = _handle
        else:
            codec_result: MsgpackBody = self._TO_UVARINT(codec_type)
            codec: bytes = codec_result.bytes.first()
            length_result: MsgpackBody = self._TO_UVARINT(len(key))
            length: bytes = length_result.bytes.first()
            full_key = codec + length + key
            buffer = c_buffer(full_key)
            result: MsgpackBody = self._NEW_CID_V1(codec_type, len(full_key), buffer)
            result.raise_error()
            self.handle = result.handles.first()

    def __str__(self):
        return f'{self.__class__}({self.string})'

    @classmethod
    def from_bytes(cls, cid_bytes: bytes) -> Self:
        buffer = c_buffer(cid_bytes)
        result: MsgpackBody = cls._FROM_BYTES(len(cid_bytes), buffer)
        result.raise_error()
        return Cid(_handle=result.handles.first())

    @classmethod
    def decode(cls, s: str) -> Self:
        result: MsgpackBody = Cid._DECODE(GoString.new(s))
        result.raise_error()
        return Cid(_handle=result.handles.first())

    @cached_property
    def defined(self) -> bool:
        return self._DEFINED(self.handle)

    @cached_property
    def bytes(self) -> bytes:
        result: MsgpackBody = self._BYTES(self.handle)
        return result.bytes.first()

    @cached_property
    def version(self) -> int:
        return self._VERSION(self.handle)

    @cached_property
    def type(self) -> int:
        return self._TYPE(self.handle)

    @cached_property
    def string(self) -> str:
        result: MsgpackBody = self._STRING(self.handle)
        result.raise_error()
        return result.strings.first()


__all__ = ['Cid', ]
