import enum
import asyncio
from ctypes import *
from typing import Self
from libp2p import Host
from libp2p.cid import Cid
from libp2p.data_store import MutexDataStore
from libp2p.peer import AddrInfo, Peer
from libp2p.utils import *
from libp2p.validator import *


lib = load_library()


class DhtOption(Option):
    load_library().dhtOption_delete.argtypes = [c_size_t, ]
    _FREE = load_library().dhtOption_delete


class DhtModeEnum(AutoInt):
    ModeAuto = enum.auto()
    ModeClient = enum.auto()
    ModeServer = enum.auto()
    ModeAutoServer = enum.auto()


class Mode(DhtOption):
    lib.dhtOption_mode.argtypes = [c_size_t, ]
    lib.dhtOption_mode.restype = c_size_t
    _INIT = lib.dhtOption_mode

    def __init__(self, mode: DhtModeEnum) -> None:
        handle = self._INIT(mode.value)
        super(Mode, self).__init__(handle)


class DataStore(DhtOption):
    lib.dhtOption_datastore.argtypes = [c_size_t, ]
    lib.dhtOption_datastore.restype = c_size_t
    _INIT = lib.dhtOption_datastore

    def __init__(self, ds: MutexDataStore) -> None:
        handle = self._INIT(ds.handle)
        super(DataStore, self).__init__(handle)
        self.ds = ds


class NamespacedValidator(DhtOption):
    lib.dhtOption_namespacedValidator.argtypes = [c_size_t, GoString, ]
    lib.dhtOption_namespacedValidator.restype = c_size_t
    _INIT = lib.dhtOption_namespacedValidator

    def __init__(self, namespace: str, validator: Validator | PublicKeyValidator | IpnsValidator):
        handle = self._INIT(validator.handle, GoString.new(namespace))
        super(NamespacedValidator, self).__init__(handle)
        self.validator = validator


class BootstrapPeers(DhtOption):
    lib.dhtOption_bootstrapPeers.argtypes = [MsgpackArg, ]
    lib.dhtOption_bootstrapPeers.restype = c_size_t
    _INIT = lib.dhtOption_bootstrapPeers

    def __init__(self, *addrs: AddrInfo):
        arg = {
            "Handles": [addr.handle for addr in addrs],
        }
        handle = self._INIT(MsgpackArg.from_dict(arg))
        super(BootstrapPeers, self).__init__(handle)


class ProtocolPrefix(DhtOption):
    lib.dht_protocolPrefix.argtypes = [GoString, ]
    lib.dht_protocolPrefix.restype = c_size_t
    _INIT = lib.dht_protocolPrefix

    def __init__(self, protocol_id: str):
        handle = self._INIT(GoString.new(protocol_id))
        super(ProtocolPrefix, self).__init__(handle)


class ProtocolExtension(DhtOption):
    lib.dht_protocolExtension.argtypes = [GoString, ]
    lib.dht_protocolExtension.restype = c_size_t
    _INIT = lib.dht_protocolExtension

    def __init__(self, protocol_id: str):
        handle = self._INIT(GoString.new(protocol_id))
        super(ProtocolExtension, self).__init__(handle)


class V1ProtocolOverride(DhtOption):
    lib.dht_v1ProtocolOverride.argtypes = [GoString, ]
    lib.dht_v1ProtocolOverride.restype = c_size_t
    _INIT = lib.dht_v1ProtocolOverride

    def __init__(self, protocol_id: str):
        handle = self._INIT(GoString.new(protocol_id))
        super(V1ProtocolOverride, self).__init__(handle)


class DisableAutoRefresh(DhtOption):
    lib.dhtOption_disableAutoRefresh.restype = c_size_t
    _INIT = lib.dhtOption_disableAutoRefresh

    def __init__(self):
        handle = self._INIT()
        super(DisableAutoRefresh, self).__init__(handle)


class DisableProviders(DhtOption):
    lib.dhtOption_disableProviders.restype = c_size_t
    _INIT = lib.dhtOption_disableProviders

    def __init__(self):
        handle = self._INIT()
        super(DisableProviders, self).__init__(handle)


class DisableValues(DhtOption):
    lib.dhtOption_disableValues.restype = c_size_t
    _INIT = lib.dhtOption_disableValues

    def __init__(self):
        handle = self._INIT()
        super(DisableValues, self).__init__(handle)


class BucketSize(DhtOption):
    lib.dht_bucketSize.argtypes = [c_size_t, ]
    lib.dht_bucketSize.restype = c_size_t
    _INIT = lib.dht_bucketSize

    def __init__(self, bucket_size: int):
        handle = self._INIT(bucket_size)
        super(BucketSize, self).__init__(handle)


class Concurrency(DhtOption):
    lib.dht_concurrency.argtypes = [c_size_t, ]
    lib.dht_concurrency.restype = c_size_t
    _INIT = lib.dht_concurrency

    def __init__(self, alpha: int):
        handle = self._INIT(alpha)
        super(Concurrency, self).__init__(handle)


class Resiliency(DhtOption):
    lib.dht_resiliency.argtypes = [c_size_t, ]
    lib.dht_resiliency.restype = c_size_t
    _INIT = lib.dht_resiliency

    def __init__(self, beta: int):
        handle = self._INIT(beta)
        super(Resiliency, self).__init__(handle)


class DHT(SimpleFreeMixin):
    lib.dht_new.argtypes = [c_size_t, MsgpackArg, ]
    lib.dht_new.restype = MsgpackBody
    _INIT = lib.dht_new
    lib.dht_newDHT.argtypes = [c_size_t, c_size_t, ]
    lib.dht_newDHT.restype = c_size_t
    _NEW_DHT = lib.dht_newDHT
    lib.dht_delete.argtypes = [c_size_t, ]
    _FREE = lib.dht_delete
    lib.dht_bootstrap.argtypes = [c_size_t, ]
    lib.dht_bootstrap.restype = MsgpackBody
    _BOOTSTRAP = lib.dht_bootstrap
    lib.dht_defaultBootstrapPeers.restype = MsgpackBody
    _DEFAULT_BOOTSTRAP_PEERS = lib.dht_defaultBootstrapPeers
    lib.dht_ping.argtypes = [c_size_t, c_size_t, ]
    lib.dht_ping.restype = MsgpackBody
    _PING = lib.dht_ping
    lib.dht_putValue.argtypes = [c_size_t, MsgpackArg, ]
    lib.dht_putValue.restype = MsgpackBody
    _PUT_VALUE = lib.dht_putValue
    lib.dht_getValue.argtypes = [c_size_t, MsgpackArg, ]
    lib.dht_getValue.restype = MsgpackBody
    _GET_VALUE = lib.dht_getValue
    lib.dht_provide.argtypes = [c_size_t, c_size_t, c_bool, ]
    lib.dht_provide.restype = MsgpackBody
    _PROVIDE = lib.dht_provide
    lib.dht_findProviders.argtypes = [c_size_t, c_size_t, ]
    lib.dht_findProviders.restype = MsgpackBody
    _FIND_PROVIDERS = lib.dht_findProviders

    def __init__(self, handle: int, loop: asyncio.AbstractEventLoop, opts: tuple[DhtOption] = None):
        self.handle = handle
        self.loop: asyncio.AbstractEventLoop = loop
        self.opts = opts

    @classmethod
    async def new(cls, host: Host, *opts: DhtOption) -> Self:
        args = {
            'Handles': [opt.handle for opt in opts]
        }
        fut = c_wrap(host.io_loop, cls._INIT, host.handle, MsgpackArg.from_dict(args))
        result: MsgpackBody = await fut
        result.raise_error()
        return DHT(result.handles.first(), host.io_loop, opts=opts)

    @classmethod
    def new_dht(cls, host: Host, mutex_data_store: MutexDataStore) -> Self:
        handle = cls._NEW_DHT(host.handle, mutex_data_store.handle)
        return DHT(handle, host.io_loop)

    async def bootstrap(self):
        result: MsgpackBody = self._BOOTSTRAP(self.handle)
        result.raise_error()

    @classmethod
    def default_bootstrap_peers(cls) -> list[str]:
        result: MsgpackBody = cls._DEFAULT_BOOTSTRAP_PEERS()
        result.raise_error()
        return result.strings

    async def ping(self, peer: Peer) -> bool:
        result: MsgpackBody = self._PING(self.handle, peer.handle)
        result.raise_error()
        return True

    async def get_value(self, key: bytes) -> None | bytes:
        args = {
            "Bytes": [key, ],
            "Handles": [],
        }
        fut = c_wrap(self.loop, self._GET_VALUE, self.handle, MsgpackArg.from_dict(args))
        result: MsgpackBody = await fut
        try:
            result.raise_error()
        except LibP2PError as e:
            if "routing: not found" in str(e):
                return None
        return result.bytes.first()

    async def put_value(self, key: bytes, value: bytes):
        args = {
            "Bytes": [key, value, ],
            "Handles": [],
        }
        fut = c_wrap(self.loop, self._PUT_VALUE, self.handle, MsgpackArg.from_dict(args))
        result: MsgpackBody = await fut
        result.raise_error()

    async def provide(self, cid: Cid, brdcst: bool):
        fut = c_wrap(self.loop, self._PROVIDE, self.handle, cid.handle, brdcst)
        result: MsgpackBody = await fut
        result.raise_error()

    async def find_providers(self, cid: Cid) -> list[AddrInfo]:
        fut = c_wrap(self.loop, self._FIND_PROVIDERS, self.handle, cid.handle)
        result: MsgpackBody = await fut
        result.raise_error()
        addrs = [AddrInfo(_handle=handle) for handle in result.handles]
        return addrs


__all__ = [
    'DhtModeEnum',
    'DhtOption',
    'Mode',
    'DataStore',
    'NamespacedValidator',
    'BootstrapPeers',
    'ProtocolPrefix',
    'ProtocolExtension',
    'V1ProtocolOverride',
    'DisableAutoRefresh',
    'DisableProviders',
    'DisableValues',
    'DHT',
]
