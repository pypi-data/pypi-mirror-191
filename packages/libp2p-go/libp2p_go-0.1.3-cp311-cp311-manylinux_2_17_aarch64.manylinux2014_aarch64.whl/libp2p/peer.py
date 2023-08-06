import asyncio
import dataclasses
from ctypes import *
from typing import Self
from functools import cached_property
from libp2p.cid import Cid
from libp2p.crypto import *
from libp2p.utils import *


lib = load_library()


class Peer(SimpleFreeMixin):
    lib.peer_delete.argtypes = [c_size_t, ]
    _FREE = lib.peer_delete
    lib.peer_string.argtypes = [c_size_t, ]
    lib.peer_string.restype = MsgpackBody
    _STRING = lib.peer_string
    lib.peer_decode.argtypes = [GoString, ]
    lib.peer_decode.restype = MsgpackBody
    _DECODE = lib.peer_decode
    lib.peer_fromBytes.argtypes = [c_size_t, POINTER(c_ubyte), ]
    lib.peer_fromBytes.restype = MsgpackBody
    _FROM_BYTES = lib.peer_fromBytes
    lib.peer_fromCid.argtypes = [c_size_t, ]
    lib.peer_fromCid.restype = MsgpackBody
    _FROM_CID = lib.peer_fromCid
    lib.peer_fromPublicKey.argtypes = [c_size_t, ]
    lib.peer_fromPublicKey.restype = MsgpackBody
    _FROM_PK = lib.peer_fromPublicKey
    lib.peer_fromPrivateKey.argtypes = [c_size_t, ]
    lib.peer_fromPrivateKey.restype = MsgpackBody
    _FROM_SK = lib.peer_fromPrivateKey
    lib.peer_toCid.argtypes = [c_size_t, ]
    lib.peer_toCid.restype = c_size_t
    _TO_CID = lib.peer_toCid
    lib.peer_toPublicKey.argtypes = [c_size_t, ]
    lib.peer_toPublicKey.restype = MsgpackBody
    _TO_PK = lib.peer_toPublicKey
    lib.peer_matchesPublicKey.argtypes = [c_size_t, c_size_t, ]
    lib.peer_matchesPublicKey.restype = c_bool
    _MATCHES_PK = lib.peer_matchesPublicKey
    lib.peer_matchesPrivateKey.argtypes = [c_size_t, c_size_t, ]
    lib.peer_matchesPrivateKey.restype = c_bool
    _MATCHES_SK = lib.peer_matchesPrivateKey
    lib.peer_bytes.argtypes = [c_size_t, ]
    lib.peer_bytes.restype = MsgpackBody
    _BYTES = lib.peer_bytes

    def __init__(self, handle: int):
        self.handle = handle

    def __eq__(self, other):
        return self.string == other.string

    def __hash__(self):
        return self.string.__hash__()

    def __str__(self):
        return f'{self.__class__}({self.string})'

    @cached_property
    def string(self) -> str:
        result: MsgpackBody = self._STRING(self.handle)
        result.raise_error()
        return result.strings.first()

    @cached_property
    def bytes(self) -> bytes:
        result: MsgpackBody = self._BYTES(self.handle)
        result.raise_error()
        return result.bytes.first()

    @classmethod
    def decode(cls, s: str) -> Self:
        result: MsgpackBody = Peer._DECODE(GoString.new(s))
        result.raise_error()
        return Peer(handle=result.handles.first())

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        buffer = c_buffer(data)
        result: MsgpackBody = Peer._FROM_BYTES(len(data), buffer)
        result.raise_error()
        return Peer(handle=result.handles.first())

    @classmethod
    def from_cid(cls, cid: Cid) -> Self:
        result: MsgpackBody = Peer._FROM_CID(cid.handle)
        result.raise_error()
        return Peer(handle=result.handles.first())

    @classmethod
    def from_public_key(cls, pk: PubKey) -> Self:
        result: MsgpackBody = Peer._FROM_PK(pk.handle)
        result.raise_error()
        return Peer(handle=result.handles.first())

    @classmethod
    def from_private_key(cls, sk: PrivKey) -> Self:
        result: MsgpackBody = Peer._FROM_SK(sk.handle)
        result.raise_error()
        return Peer(handle=result.handles.first())

    def to_cid(self) -> Cid:
        handle = self._TO_CID(self.handle)
        return Cid(_handle=handle)

    def to_public_key(self) -> PubKey:
        result: MsgpackBody = self._TO_PK(self.handle)
        result.raise_error()
        return PubKey(handle=result.handles.first())

    def matches_public_key(self, pk: PubKey) -> bool:
        return self._MATCHES_PK(self.handle, pk.handle)

    def matches_private_key(self, sk: PrivKey) -> bool:
        return self._MATCHES_SK(self.handle, sk.handle)


@dataclasses.dataclass
class AddrInfo(SimpleFreeMixin):
    lib.addrInfo_delete.argtypes = [c_size_t, ]
    _FREE = lib.addrInfo_delete
    lib.addrInfo_new.argtypes = [c_size_t, MsgpackArg, ]
    lib.addrInfo_new.restype = MsgpackBody
    _INIT = lib.addrInfo_new
    lib.addrInfo_addrs.argtypes = [c_size_t, ]
    lib.addrInfo_addrs.restype = MsgpackBody
    _ADDRS = lib.addrInfo_addrs
    lib.addrInfo_id.argtypes = [c_size_t, ]
    lib.addrInfo_id.restype = MsgpackBody
    _ID = lib.addrInfo_id

    id: Peer = dataclasses.field()
    addrs: list[str] = dataclasses.field(default_factory=list, repr=False)

    def __init__(self, peer_id: Peer = None, addrs: list[str] = None, _handle: int = None):
        if _handle is None:
            args = {
                'Strings': [str(addr) for addr in addrs],
            }
            arg = MsgpackArg.from_dict(args)
            result: MsgpackBody = self._INIT(peer_id.handle, arg)
            result.raise_error()
            _handle = result.handles.first()
        self.handle = _handle
        if peer_id:
            self.id: Peer = peer_id
        else:
            self.id: Peer = self._id()
        if addrs is not None:
            self.addrs: list[str] = addrs
        else:
            self.addrs: list[str] = self._addrs()

    def __str__(self):
        return f'{self.__class__}({self.id} addrs:{len(self.addrs)})'

    def _addrs(self) -> list[str]:
        result: MsgpackBody = self._ADDRS(self.handle)
        result.raise_error()
        addrs = [s for s in result.strings]
        return addrs

    def _id(self) -> Peer:
        result: MsgpackBody = self._ID(self.handle)
        result.raise_error()
        handle = result.handles.first()
        return Peer(handle=handle)


class AddrInfoChan(SimpleFreeMixin):
    lib.addrInfoChan_delete.argtypes = [c_size_t, ]
    _FREE = lib.addrInfoChan_delete
    lib.addrInfoChan_pop.argtypes = [c_size_t, ]
    lib.addrInfoChan_pop.restype = c_size_t
    _POP = lib.addrInfoChan_pop

    def __init__(self, handle: int, loop: asyncio.AbstractEventLoop):
        self.handle = handle
        self.loop = loop

    def __aiter__(self):
        return self

    async def __anext__(self) -> AddrInfo:
        fut = c_wrap(self.loop, self._POP, self.handle)
        handle = await fut
        if not handle:
            raise StopAsyncIteration
        addr = AddrInfo(_handle=handle)
        return addr


lib.peer_addrInfoFromP2pAddr.argtypes = [GoString, ]
lib.peer_addrInfoFromP2pAddr.restype = MsgpackBody
_ADDR_INFO_FROM_P2P_ADDR = lib.peer_addrInfoFromP2pAddr


def addr_info_from_p2p_addr(multi_addr_string: str):
    result: MsgpackBody = _ADDR_INFO_FROM_P2P_ADDR(GoString.new(multi_addr_string))
    result.raise_error()
    handle = result.handles.first()
    return AddrInfo(_handle=handle)


__all__ = [
    'AddrInfo',
    'AddrInfoChan',
    'addr_info_from_p2p_addr',
    'Peer',
]
