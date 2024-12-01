import datetime
import importlib
from abc import ABC
from copy import deepcopy
from dataclasses import Field, dataclass, fields
from types import GenericAlias, NoneType, UnionType
from typing import Any, Literal, Self

from klaatu_python.utils import getitem0_nullable

from zoho.utils import get_timezone


@dataclass
class AbstractRecord(ABC):
    @classmethod
    def attrname_to_dict_key(cls, attrname: str) -> str:
        return attrname

    @classmethod
    def dict_keys(cls) -> list[str]:
        return [cls.attrname_to_dict_key(f.name) for f in fields(cls)]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Self":
        """
        Converts a dict into a record object, in a nested manner (i.e. also
        converts fields that are annotated as records or lists of records).
        """
        record_fields = fields(cls)
        field_names = [f.name for f in record_fields]

        for field in record_fields:
            dict_key = cls.attrname_to_dict_key(field.name)
            if dict_key in data:
                if isinstance(field.type, GenericAlias) and field.type.__origin__ == list:
                    _type = cls.type_or_none(field.type.__args__[0])
                    if (
                        _type is not None and
                        issubclass(_type, AbstractRecord) and
                        isinstance(data[dict_key], list)
                    ):
                        data[field.name] = [_type.from_dict(row) for row in data[dict_key]]
                else:
                    try:
                        data[field.name] = cls.handle_input_field(field, data[dict_key])
                    except (ValueError, TypeError):
                        del data[dict_key]

        return cls(**{k: v for k, v in data.items() if k in field_names})

    @classmethod
    def handle_input_field(cls, field: Field, value: Any) -> Any:
        if value is None:
            return value

        _type = cls.type_or_none(field.type)

        if _type is not None:
            if issubclass(_type, AbstractRecord) and isinstance(value, dict):
                return _type.from_dict(value)
            if issubclass(_type, datetime.date):
                return _type.fromisoformat(value)
            try:
                return _type(value)  # type: ignore
            except TypeError:
                pass

        return value

    @classmethod
    def type_or_none(cls, arg: Any) -> type | None:
        if isinstance(arg, str):
            module_name, _, type_name = arg.rpartition(".")
            module_name = module_name or cls.__module__
            try:
                module = importlib.import_module(module_name)
                arg_type = getattr(module, type_name)
            except (ModuleNotFoundError, AttributeError):
                return None
            if isinstance(arg_type, type):
                return arg_type
        elif isinstance(arg, UnionType):
            return getitem0_nullable(arg.__args__, cond=lambda t: t is not NoneType)
        elif isinstance(arg, type):
            return arg
        elif hasattr(arg, "__origin__") and arg.__origin__ is Literal and arg.__args__:
            return arg.__args__[0].__class__
        return None

    def copy(self, **kwargs) -> "Self":
        record_fields = [f.name for f in fields(self)]
        record_copy = deepcopy(self)
        for key, value in kwargs.items():
            if key in record_fields:
                setattr(record_copy, key, value)
        return record_copy

    # pylint: disable=unused-argument
    def handle_output_field(self, attrname: str, value: Any) -> Any:
        """Hook to do stuff with an outgoing field value."""
        return value

    def to_dict(self) -> dict:
        record_fields = [f for f in fields(self) if f.init]
        data: dict[str, Any] = {}

        for f in record_fields:
            key = self.attrname_to_dict_key(f.name)
            attr = self.__dict__[f.name]

            # Let's not fuck around with Owner just now.
            if key == "Owner":
                continue

            if isinstance(f.type, GenericAlias) and f.type.__origin__ == list:
                _type = self.type_or_none(f.type.__args__[0])
                if _type is not None and issubclass(_type, AbstractRecord) and isinstance(attr, list):
                    data[key] = [row.to_dict() for row in attr if isinstance(row, AbstractRecord)]
                else:
                    data[key] = self.handle_output_field(f.name, attr)
            else:
                if isinstance(attr, AbstractRecord):
                    data[key] = attr.to_dict()
                elif isinstance(attr, datetime.datetime):
                    data[key] = attr.replace(microsecond=0).astimezone(get_timezone()).isoformat()
                elif isinstance(attr, datetime.date):
                    data[key] = attr.isoformat()
                elif attr is not None:
                    data[key] = self.handle_output_field(f.name, attr)

        return data


@dataclass
class AbstractIDRecord(AbstractRecord, ABC):
    id: str | None

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, self.__class__) and
            __value.id is not None and
            self.id is not None and
            __value.id == self.id
        )

    def with_id(self, _id: str):
        self.id = _id
        return self
