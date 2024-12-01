import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING

from zoho.records.modules.base import AbstractModuleRecord
from zoho.records.ref import RecordRef, UserRef


if TYPE_CHECKING:
    from zoho.records.tag import Tag


@dataclass
class BaseCampaign(AbstractModuleRecord):
    Campaign_Name: str

    Actual_Cost: Decimal | None = None
    Budgeted_Cost: Decimal | None = None
    Created_By: UserRef | None = None
    Created_Time: datetime.datetime | None = None
    Description: str | None = None
    End_Date: datetime.date | None = None
    Expected_Response: str | None = None
    Expected_Revenue: Decimal | None = None
    Layout: RecordRef | None = None
    Modified_By: UserRef | None = None
    Modified_Time: datetime.datetime | None = None
    Num_sent: str | None = None
    Owner: UserRef | None = None
    Parent_Campaign: RecordRef | None = None
    Start_Date: datetime.date | None = None
    Status: str | None = None
    Tag: list["Tag"] = field(default_factory=list)
    Type: str | None = None

    module: str = field(init=False, default="Campaigns")


@dataclass
class Campaign(BaseCampaign):
    ...
