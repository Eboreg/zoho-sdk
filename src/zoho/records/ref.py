from dataclasses import dataclass

from zoho.records.base import AbstractIDRecord


@dataclass
class RecordRef(AbstractIDRecord):
    name: str


@dataclass
class TerritoryRef(AbstractIDRecord):
    Name: str


@dataclass
class UserRef(AbstractIDRecord):
    name: str | None = None
    email: str | None = None
