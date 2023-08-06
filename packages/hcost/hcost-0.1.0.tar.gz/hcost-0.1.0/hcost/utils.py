from datetime import datetime
from decimal import Decimal
from json import load, JSONEncoder
from random import Random
from sys import byteorder
from typing import Dict
from uuid import UUID

from dateutil.parser import parse

CONVERTERS = {
    'datetime': parse,
    'decimal': Decimal,
}


class SmartJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime,)):
            return {"val": obj.isoformat(), "_spec_type": "datetime"}
        elif isinstance(obj, (Decimal,)):
            return {"val": str(obj), "_spec_type": "decimal"}
        else:
            return super().default(obj)


def object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj

    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))


def read(path: str) -> str:
    with open(path) as file:
        return file.read()


def readj(path: str) -> Dict:
    with open(path) as file:
        return load(file, object_hook=object_hook)


def rand_bytes(rng: Random, length: int) -> bytes:
    if length == 0:
        return b''
    return rng.getrandbits(length * 8).to_bytes(length, byteorder)


def deterministic_uuid(r: Random) -> UUID:
    return UUID(bytes=rand_bytes(r, 16), version=4)


def get_first_of_year(year: int):
    return datetime(year, 1, 1, 0, 0, 0)


def get_next_year(now: datetime):
    return get_first_of_year(now.year + 1)


def format_decimal(number: Decimal | float) -> str:
    return f"{number:.2f}"
