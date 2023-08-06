"""DoHome direct transport"""

from typing import Union
from aiodatagram import open_endpoint, Endpoint
from .interface import DoHomeApiTransport
from .constants import API_PORT, API_ENCODING

class DoHomeDirectTransport(DoHomeApiTransport):
    """High-level direct transport for DoHome API devices"""
    _host: str = ''
    _endpoint: Union[Endpoint, type(None)] = None

    def __init__(self, host: str):
        self._host = host

    @property
    def connected(self):
        """Indicates whether the transport is connected."""
        return not (self._endpoint is None or self._endpoint.closed)

    async def send_request(self, request: str) -> list:
        """Sends request to DoHome device"""
        if not self.connected:
            await self._connect()
        self._endpoint.send(
            request.encode(API_ENCODING)
        )
        response = await self._endpoint.receive()
        return [response.decode(API_ENCODING)]

    async def _connect(self):
        self._endpoint = await open_endpoint(
            self._host,
            API_PORT
        )
