"read json from endpoint"


from typing import Any
import requests
from jsonschema import validate


def get_json_from_url(url: str, schema: Any = None) -> Any:
    """
    returns json encoded content from url
    optionally validates against json schema
    """
    obj = requests.get(url, timeout=20).json()
    if schema is not None:
        validate(obj, schema=schema)
    return obj
