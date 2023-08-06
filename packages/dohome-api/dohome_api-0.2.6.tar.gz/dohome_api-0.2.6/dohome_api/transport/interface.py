"""DoHome transport interface"""

from typing import List

class DoHomeApiTransport:
    """DoHome API transport interface"""

    @property
    def connected(self):
        """Indicates whether the transport is connected."""

    async def send_request(self, request: str) -> List[str]:
        """Sends request to DoHome device"""
