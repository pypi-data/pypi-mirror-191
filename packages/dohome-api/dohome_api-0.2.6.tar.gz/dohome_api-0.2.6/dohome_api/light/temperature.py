"""Temperature helpers"""

class TemperatureConverter:
    """Temperature to/from uint8 converter"""
    # pylint: disable=invalid-name
    _MIN = 0
    _MAX = 0
    _RANGE = 0

    def __init__(self, mireds_min: int, mireds_max: int):
        self._MIN = mireds_min
        self._MAX = mireds_max
        self._RANGE = mireds_max - mireds_min

    def to_uint8(self, mireds: int) -> int:
        """Converts mireds to uint8"""
        percent = (mireds - self._MIN) / self._RANGE
        return int(255 * percent)

    def to_mireds(self, uint8_temp: int) -> int:
        """Converts uint8 to mireds"""
        percent = uint8_temp / 255
        return int(percent * self._RANGE) + self._MIN
