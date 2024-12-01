import datetime
from dataclasses import dataclass, field
from decimal import Decimal

from zoho.records.modules.base import AbstractModuleRecord
from zoho.records.ref import RecordRef, TerritoryRef, UserRef
from zoho.records.tag import Tag


@dataclass
class BaseDeal(AbstractModuleRecord):
    Deal_Name: str
    Pipeline: str
    Stage: str

    Account_Name: RecordRef | None = None
    Amount: Decimal | None = None
    Campaign_Source: RecordRef | None = None
    Closing_Date: datetime.date | None = None
    Contact_Name: RecordRef | None = None
    Created_By: UserRef | None = None
    Created_Time: datetime.datetime | None = None
    Description: str | None = None
    Expected_Revenue: Decimal | None = None
    Last_Activity_Time: datetime.datetime | None = None
    Lead_Conversion_Time: datetime.datetime | None = None
    Lead_Source: str | None = None
    Modified_By: UserRef | None = None
    Modified_Time: datetime.datetime | None = None
    Next_Step: str | None = None
    Overall_Sales_Duration: int | None = None
    Owner: UserRef | None = None
    Probability: int | None = None
    Record_Image: str | None = None
    Sales_Cycle_Duration: int | None = None
    Tag: list["Tag"] = field(default_factory=list)
    Territory: list[TerritoryRef] = field(default_factory=list)
    Type: str | None = None

    module: str = field(init=False, default="Deals")


@dataclass
class Deal(BaseDeal):
    Country: str | None = None
    Language: str | None = None
    Reason_for_loss: str | None = None
