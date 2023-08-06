"""DoHome light request helpers"""

from typing import List
from ..commands import CMD_SET_STATE, format_request

# pylint: disable-next=invalid-name, too-many-arguments
def format_light_request(sids: List[str], r = 0, g = 0, b = 0, w = 0, m = 0):
    """Formats DoHome light set command"""
    return format_request(sids, CMD_SET_STATE, {
        'r': r,
        'g': g,
        'b': b,
        'w': w,
        'm': m
    })
