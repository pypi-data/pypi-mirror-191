"""
The DoHome bulb protocol from DoIT uses a 0 to 5000 measurement system.
It contains auxiliary functions that convert these values.
"""

def dohome_to_uint8(value: int):
    """Converts DoHome value to uint8"""
    return int(255 * (value / 5000))

def uint8_to_dohome(value: int):
    """Converts uint8 value to DoHome"""
    return int(5000 * (value / 255))

def dohome_state_to_uint8(raw_state: dict) -> dict:
    """Converts all values of dict from dohome to uint8"""
    for key in raw_state:
        raw_state[key] = dohome_to_uint8(raw_state[key])
    return raw_state
