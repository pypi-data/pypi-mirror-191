"""DoHome lights broadcast"""

from typing import List
from ..transport import DoHomeBroadcastTransport
from .light import DoHomeLight, parse_response
from .exceptions import BadCommandException, NotEnoughException

class DoHomeLightsBroadcast(DoHomeLight):
    """DoHome broadcast light controller class"""
    _transport: DoHomeBroadcastTransport
    _timeout: float

    def __init__(self, sids: List[str], transport: DoHomeBroadcastTransport, timeout = 1.0):
        super().__init__(sids, transport)
        self._sids = sids
        self._timeout = timeout

    async def _send_request(self, request: str):
        response_data = await self._transport.send_request(
            request, self._timeout, len(self._sids)
        )
        responses = list(map(parse_response, response_data))
        if len(responses) < len(self._sids):
            raise NotEnoughException
        for response in responses:
            if response["res"] != 0:
                raise BadCommandException
        return responses[0]
