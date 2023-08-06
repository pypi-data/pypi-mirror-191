"Sub-module for data types"

from dataclasses import dataclass
from typing import Callable, Any, Type


@dataclass
class FieldSchema:
    """
    schema for the extraction of a single datafield
    use together with RecordSchema
    """
    name: str
    dtype: Type
    default: Any = None
    transform: Callable | None = None
    rename: str | None = None

    def extract_value(self, mapping: dict) -> Any:
        """
        extracts field value from dict
        >>> FieldSchema('x', int).extract_value({'x': 1})
        1
        >>> FieldSchema('x', int, default='?').extract_value({})
        '?'
        """
        value = mapping.get(self.name)
        if value is None:
            return self.default
        if not isinstance(value, self.dtype) and not value is None:
            raise ValueError(f"{self.name} has {type(value)}, expected {self.dtype}")
        if self.transform is not None:
            return self.transform(value)
        return value


@dataclass
class RecordSchema:
    """
    A schema for extracting a record of datafields
    """
    fields: list[FieldSchema]
    def extract_record(self, mapping: dict):
        """
        extracts record from dict
        >>> RecordSchema([FieldSchema('x', int, rename='y')]).extract_record({'x': 1})
        {'y': 1}
        """
        record = {}
        for field in self.fields:
            record[field.rename or field.name] = field.extract_value(mapping)
        return record
