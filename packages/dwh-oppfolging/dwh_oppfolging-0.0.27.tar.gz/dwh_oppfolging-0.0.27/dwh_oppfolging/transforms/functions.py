"data transforms"
from typing import Any
from datetime import datetime
import hashlib
import json
import re
import pendulum
from pendulum.datetime import DateTime as PendulumDateTime


def flatten_dict(mapping: dict, separator: str = "_", flatten_lists: bool = False) -> dict[str, Any]:
    """
    recursively flattens dict with specified separator
    optionally flatten lists in it as well
    note: all keys become strings
    >>> flatten_dict({0: {1: 3}, 'z': [1, 2, 3]}, "_", True)
    {'0_1': 3, 'z_0': 1, 'z_1': 2, 'z_2': 3}
    """
    def flatten(mapping: dict, parent_key: str = "") -> dict:
        items: list[Any] = []
        for key, value in mapping.items():
            flat_key = str(key) if not parent_key else str(parent_key) + separator + str(key)
            if isinstance(value, dict):
                items.extend(flatten(value, flat_key).items())
            elif isinstance(value, list) and flatten_lists:
                for it_key, it_value in enumerate(value):
                    items.extend(flatten({str(it_key):it_value}, flat_key).items())
            else:
                items.append((flat_key, value))
        return dict(items)

    return flatten(mapping)


def string_to_naive_norwegian_datetime(
    string: str
) -> datetime:
    """converts string to a naive pendulum datetime, stripping any timezone info if naive is true
    and adjusting time using the utc offset of the tz_name timezone instead.
    >>> string_to_naive_norwegian_datetime("2022-05-05T05:05:05+01:00").isoformat()
    '2022-05-05T06:05:05'
    """
    pdl_dt = pendulum.parser.parse(string)
    assert isinstance(pdl_dt, PendulumDateTime)
    pdl_dt = pdl_dt.in_timezone("Europe/Oslo")
    pdl_dt = pdl_dt.naive()
    return pdl_dt


#def string_to_naive_norwegian_datetime(x: datetime.datetime):  # pylint: disable=invalid-name
#    """returns naive datetime offset by norwegian utc (lifted from dvh-kafka-python)
#    >>> old_dt(datetime.datetime.fromisoformat("2022-05-05T05:05:05+01:00")).isoformat()
#    '2022-05-05T06:05:05'
#    """
#    timezone = pytz.timezone("Europe/Oslo")
#    if x.tzinfo is not None:
#        x = (x - x.utcoffset()).replace(tzinfo=None)  # type: ignore
#    x += timezone.utcoffset(x, is_dst=True)  # type: ignore
#    return x


def datetime_to_naive_norwegian_datetime(dt: datetime):
    """converts datetime to naive norwegian datetime
    >>> datetime_to_naive_norwegian_datetime(datetime.fromisoformat("2022-05-05T05:05:05+01:00")).isoformat()
    '2022-05-05T06:05:05'
    """
    return string_to_naive_norwegian_datetime(dt.isoformat())


def string_to_code(string: str) -> str:
    """converts a string to a code string conforming to dwh standard
    >>> string_to_code("/&$  ØrkEn Rotte# *;-")
    'ORKEN_ROTTE'
    >>> string_to_code(" ??? ")
    'UKJENT'
    """
    code = string.upper().replace("Æ", "A").replace("Ø", "O").replace("Å", "AA")
    code = "_".join(
        word
        for word in re.findall(
            r"(\w*)",
            code,
        )
        if word
    )
    code = "UKJENT" if code == "" else code
    return code


def dict_to_string(dictionary: dict) -> str:
    """Returns a json dump of the dict
    >>> dict_to_string({"x": 2, "y": 3})
    '{"x": 2, "y": 3}'
    """
    string = json.dumps(dictionary, ensure_ascii=False)
    return string


def string_to_sha256_hash(string: str) -> str:
    """Returns the sha256 hash of the utf-8 encoded string as a hex-numerical string
    >>> string_to_sha256_hash("Hello, world!")
    '315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3'
    """
    sha = hashlib.sha256(string.encode("utf-8")).hexdigest()
    return sha
