"""DoHome light controller"""

from typing import Final, List, Tuple
from logging import getLogger
from ..commands import (
    CMD_GET_STATE,
    CMD_GET_TIME,
    format_request,
    parse_response,
)
from ..transport import DoHomeApiTransport
from .brightness import apply_brightness
from .temperature import TemperatureConverter
from .request import format_light_request
from .exceptions import BadCommandException
from .uint8 import (
    uint8_to_dohome,
    dohome_state_to_uint8,
)

_LOGGER = getLogger(__name__)

class DoHomeLight():
    """DoHome light controller class"""
    MIREDS_MIN: Final = 166
    MIREDS_MAX: Final = 400

    _temp = None
    _sids: List[str] = []
    _transport: DoHomeApiTransport = None

    def __init__(self, sid: str, transport: DoHomeApiTransport):
        self._sids = [sid]
        self._transport = transport
        self._temp = TemperatureConverter(self.MIREDS_MIN, self.MIREDS_MAX)

    @property
    def connected(self):
        """Indicates whether the socket is connected."""
        return self._transport.connected

    async def get_state(self) -> dict:
        """Reads high-level state from the device"""
        raw_state = await self.get_raw_state()
        uint8_state = dohome_state_to_uint8(raw_state)
        summ = 0
        state = {
            "enabled": False,
            "mode": "none", # none, rgb, white
            "rgb": [0, 0, 0],
            "mireds": 0,
            "brightness": 0
        }
        for color in ["r", "g", "b"]:
            summ += uint8_state[color]
        if summ > 0:
            state["enabled"] = True
            state["mode"] = "rgb"
            state["rgb"] = [
                uint8_state["r"], uint8_state["g"], uint8_state["b"]
            ]
            # Unfortunately, I have not found a way
            # to reliably determine brightness from RGB
            state["brightness"] = 255
            return state
        for temp in ["w", "m"]:
            summ += uint8_state[temp]
        if summ > 0:
            state["enabled"] = True
            state["mode"] = "white"
            state["brightness"] = summ
            brightness_percent = state["brightness"] / 255
            warm_amount = uint8_state["m"]
            if brightness_percent < 1.0:
                warm_amount = warm_amount / brightness_percent
            state["mireds"] = self._temp.to_mireds(warm_amount)
        return state

    async def get_raw_state(self):
        """Reads color from the device"""
        return await self._send_request(
            format_request(self._sids, CMD_GET_STATE)
        )

    async def get_time(self):
        """Reads time from the device"""
        await self._send_request(
            format_request(self._sids, CMD_GET_TIME)
        )

    async def turn_off(self):
        """Turns the device off"""
        return await self._send_request(
            format_light_request(self._sids)
        )

    async def set_white(self, mireds: int, brightness = 255):
        """Sets white temperature to the device"""
        white_percent = self._temp.to_uint8(mireds) / 255
        warm_white = 5000 * white_percent
        return await self._send_request(
            format_light_request(
                self._sids,
                w=apply_brightness(5000 - warm_white, brightness),
                m=apply_brightness(warm_white, brightness)
            )
        )

    async def set_rgb(self, color: Tuple[int, int, int], brightness = 255):
        """Sets RGB color to the device"""
        # pylint: disable-next=invalid-name
        (r, g, b) = color
        return await self._send_request(
            format_light_request(
                self._sids,
                apply_brightness(uint8_to_dohome(r), brightness),
                apply_brightness(uint8_to_dohome(g), brightness),
                apply_brightness(uint8_to_dohome(b), brightness)
            )
        )

    async def _send_request(self, request: str):
        response_data = await self._transport.send_request(request)
        response = parse_response(response_data[0])
        if response["res"] != 0:
            raise BadCommandException()
        return response
    