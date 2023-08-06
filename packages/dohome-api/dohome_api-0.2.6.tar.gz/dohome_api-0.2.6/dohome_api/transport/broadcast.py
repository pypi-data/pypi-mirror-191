"""DoHome broadcast transport"""

from typing import Union, List
from aiodatagram import open_broadcast, Broadcast
from .interface import DoHomeApiTransport
from .util import get_discovery_host
from .constants import API_PORT

class DoHomeBroadcastTransport(DoHomeApiTransport):
    """High-level broadcast transport for DoHome API devices"""
    _host: str = ''
    _broadcast: Union[type(Broadcast), type(None)] = None

    def __init__(self, host: str = None):
        self._host = host if host is not None else get_discovery_host()
        self._broadcast: Broadcast = None

    @property
    def connected(self):
        """Indicates whether the transport is connected."""
        return not (self._broadcast is None or self._broadcast.closed)

    async def receive(self, timeout = 1.0, count = 0) -> List[str]:
        """Receives messages from broadcast"""
        responses = await self._broadcast.receive(timeout, count)
        bodies = []
        for response in responses:
            (body, _) = response
            bodies.append(body.decode("utf-8"))
        return bodies

    # pylint: disable-next=arguments-differ
    async def send_request(self, request: str, timeout=0.2, count=0, receive=True) -> List[str]:
        """Sends broadcast request to DoHome device"""
        if not self.connected:
            await self._connect()
        self._broadcast.send(
            request.encode()
        )
        if not receive:
            return []
        return await self.receive(timeout, count)

    async def _connect(self) -> None:
        self._broadcast = await open_broadcast((self._host, API_PORT))
