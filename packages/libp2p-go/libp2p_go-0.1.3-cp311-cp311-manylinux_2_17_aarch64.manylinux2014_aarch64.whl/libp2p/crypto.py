import enum
from typing import Self
from ctypes import *
from functools import cached_property
from libp2p.utils import *


lib = load_library()


class KeyType(AutoInt):
    RSA = enum.auto()
    Ed25519 = enum.auto()
    Secp256k1 = enum.auto()
    ECDSA = enum.auto()


class PubKey(SimpleFreeMixin):
    lib.pubkey_delete.argtypes = [c_size_t, ]
    _FREE = lib.pubkey_delete
    lib.crypto_marshalPublicKey.argtypes = [c_size_t, ]
    lib.crypto_marshalPublicKey.restype = MsgpackBody
    _MARSHAL = lib.crypto_marshalPublicKey
    lib.crypto_unmarshalPublicKey.argtypes = [c_size_t, POINTER(c_ubyte), ]
    lib.crypto_unmarshalPublicKey.restype = MsgpackBody
    _UNMARSHAL = lib.crypto_unmarshalPublicKey
    lib.peer_idFromPublicKey.argtypes = [c_size_t, ]
    lib.peer_idFromPublicKey.restype = MsgpackBody
    _ID_FROM_PUBLIC_KEY = lib.peer_idFromPublicKey
    lib.crypto_publicKeyType.argtypes = [c_size_t, ]
    lib.crypto_publicKeyType.restype = c_int64
    _KEY_TYPE = lib.crypto_publicKeyType
    lib.crypto_publicKeyRaw.argtypes = [c_size_t, ]
    lib.crypto_publicKeyRaw.restype = MsgpackBody
    _RAW = lib.crypto_publicKeyRaw
    lib.crypto_publicKeyVerify.argtypes = [c_size_t, c_size_t, POINTER(c_ubyte), c_size_t, POINTER(c_ubyte), ]
    lib.crypto_publicKeyVerify.restype = MsgpackBody
    _VERIFY = lib.crypto_publicKeyVerify

    def __init__(self, handle: int):
        self.handle = handle

    def __str__(self):
        return f'{self.__class__}({self.type}@{self.handle})'

    def marshal(self) -> bytes:
        result: MsgpackBody = self._MARSHAL(self.handle)
        result.raise_error()
        return result.bytes.first()

    @classmethod
    def unmarshal(cls, data: bytes) -> Self:
        buffer = c_buffer(data)
        result: MsgpackBody = cls._UNMARSHAL(len(data), buffer)
        result.raise_error()
        return PubKey(result.handles.first())

    @cached_property
    def type(self) -> KeyType:
        return KeyType(self._KEY_TYPE(self.handle))

    def raw(self) -> bytes:
        result: MsgpackBody = self._RAW(self.handle)
        result.raise_error()
        return result.bytes.first()

    def verify(self, data: bytes, sig: bytes) -> bool:
        data_buffer = c_buffer(data)
        sig_buffer = c_buffer(sig)
        result: MsgpackBody = self._VERIFY(self.handle, len(data), data_buffer, len(sig), sig_buffer)
        result.raise_error()
        return bool(result.bytes.first())


class PrivKey(SimpleFreeMixin):
    lib.privkey_delete.argtypes = [c_size_t, ]
    _FREE = lib.privkey_delete
    lib.crypto_marshalPrivateKey.argtypes = [c_size_t, ]
    lib.crypto_marshalPrivateKey.restype = MsgpackBody
    _MARSHAL = lib.crypto_marshalPrivateKey
    lib.crypto_unmarshalPrivateKey.argtypes = [c_size_t, POINTER(c_ubyte), ]
    lib.crypto_unmarshalPrivateKey.restype = MsgpackBody
    _UNMARSHAL = lib.crypto_unmarshalPrivateKey
    lib.peer_idFromPrivateKey.argtypes = [c_size_t, ]
    lib.peer_idFromPrivateKey.restype = MsgpackBody
    _ID_FROM_PRIVATE_KEY = lib.peer_idFromPrivateKey
    lib.crypto_privateKeyType.argtypes = [c_size_t, ]
    lib.crypto_privateKeyType.restype = c_int64
    _KEY_TYPE = lib.crypto_privateKeyType
    lib.crypto_privateKeyRaw.argtypes = [c_size_t, ]
    lib.crypto_privateKeyRaw.restype = MsgpackBody
    _RAW = lib.crypto_privateKeyRaw
    lib.crypto_privateKeyGetPublic.argtypes = [c_size_t, ]
    lib.crypto_privateKeyGetPublic.restype = c_size_t
    _GET_PUBLIC = lib.crypto_privateKeyGetPublic
    lib.crypto_privateKeySign.argtypes = [c_size_t, c_size_t, POINTER(c_ubyte), ]
    lib.crypto_privateKeySign.restype = MsgpackBody
    _SIGN = lib.crypto_privateKeySign

    def __init__(self, handle: int):
        self.handle = handle

    def __str__(self):
        return f'{self.__class__}({self.type}@{self.handle})'

    def marshal(self) -> bytes:
        result: MsgpackBody = self._MARSHAL(self.handle)
        result.raise_error()
        return result.bytes.first()

    @classmethod
    def unmarshal(cls, data: bytes) -> Self:
        buffer = c_buffer(data)
        result: MsgpackBody = cls._UNMARSHAL(len(data), buffer)
        result.raise_error()
        return PrivKey(result.handles.first())

    @cached_property
    def type(self) -> KeyType:
        return KeyType(self._KEY_TYPE(self.handle))

    def raw(self) -> bytes:
        result: MsgpackBody = self._RAW(self.handle)
        result.raise_error()
        return result.bytes.first()

    @cached_property
    def get_public(self) -> PubKey:
        handle = self._GET_PUBLIC(self.handle)
        return PubKey(handle)

    def sign(self, data: bytes) -> bytes:
        buffer = c_buffer(data)
        result: MsgpackBody = self._SIGN(self.handle, len(data), buffer)
        result.raise_error()
        return result.bytes.first()


lib.crypto_generateKeyPairWithReader.argtypes = [c_longlong, c_longlong, c_longlong, ]
lib.crypto_generateKeyPairWithReader.restype = MsgpackBody
_GENERATE_KEYPAIR_WITH_READER = lib.crypto_generateKeyPairWithReader
lib.crypto_generateKeyPair.argtypes = [c_longlong, c_longlong, ]
lib.crypto_generateKeyPair.restype = MsgpackBody
_GENERATE_KEYPAIR = lib.crypto_generateKeyPair


def crypto_generate_keypair_with_reader(typ: KeyType, bits: int, randseed: int) -> tuple[PrivKey, PubKey]:
    result: MsgpackBody = _GENERATE_KEYPAIR_WITH_READER(typ.value, bits, randseed)
    result.raise_error()
    handles = result.handles
    priv, pub = handles.take(2)
    return PrivKey(priv), PubKey(pub)


def crypto_generate_keypair(typ: KeyType, bits: int) -> tuple[PrivKey, PubKey]:
    result: MsgpackBody = _GENERATE_KEYPAIR(typ.value, bits)
    result.raise_error()
    handles = result.handles
    priv, pub = handles.take(2)
    return PrivKey(priv), PubKey(pub)


__all__ = [
    'KeyType',
    'PrivKey',
    'PubKey',
    'crypto_generate_keypair_with_reader',
    'crypto_generate_keypair',
]
