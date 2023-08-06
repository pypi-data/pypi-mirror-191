"""DoHome Gateway utils"""
from typing import Union, List

def _get_records(message: str) -> List[str]:
    return message.split('&')

def _parse_records(records: List[str]) -> List[List[str]]:
    return list(map(lambda x: x.split('='), records))

def parse_pong_sid(message: str) -> Union[str, None]:
    """Parses device sID from pong response"""
    records = _parse_records(_get_records(message))
    for record in records:
        if record[0] == "device_name":
            name = record[1].strip()
            return name[len(name) - 4:]
    return None
