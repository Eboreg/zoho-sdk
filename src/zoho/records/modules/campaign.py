import datetime
from dataclasses import dataclass, field
from decimal import Decimal

from zoho.records.modules.base import AbstractTaggedModuleRecord
from zoho.records.ref import RecordRef, UserRef


@dataclass
class BaseCampaign(AbstractTaggedModuleRecord):
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
    Type: str | None = None

    module: str = field(init=False, default="Campaigns")


@dataclass
class Campaign(BaseCampaign):
    ...
