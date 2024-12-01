import datetime
from dataclasses import dataclass, field
from decimal import Decimal

from zoho.records.modules.base import AbstractModuleRecord
from zoho.records.ref import RecordRef, TerritoryRef, UserRef
from zoho.records.tag import Tag


@dataclass
class BaseAccount(AbstractModuleRecord):
    Account_Name: str

    Account_Number: str | None = None
    Account_Site: str | None = None
    Account_Type: str | None = None
    Annual_Revenue: Decimal | None = None
    Billing_City: str | None = None
    Billing_Code: str | None = None
    Billing_Country: str | None = None
    Billing_State: str | None = None
    Billing_Street: str | None = None
    Created_By: UserRef | None = None
    Created_Time: datetime.datetime | None = None
    Description: str | None = None
    Employees: int | None = None
    Fax: str | None = None
    Industry: str | None = None
    Last_Activity_Time: datetime.datetime | None = None
    Modified_By: UserRef | None = None
    Modified_Time: datetime.datetime | None = None
    Owner: UserRef | None = None
    Ownership: str | None = None
    Parent_Account: RecordRef | None = None
    Phone: str | None = None
    Rating: str | None = None
    Record_Image: str | None = None
    Shipping_City: str | None = None
    Shipping_Code: str | None = None
    Shipping_Country: str | None = None
    Shipping_State: str | None = None
    Shipping_Street: str | None = None
    SIC_Code: int | None = None
    Tag: list["Tag"] = field(default_factory=list)
    Territories: list[TerritoryRef] = field(default_factory=list)
    Ticker_Symbol: str | None = None
    Website: str | None = None

    module: str = field(init=False, default="Accounts")


@dataclass
class Account(BaseAccount):
    Admin_URL: str | None = None
    Country: str | None = None
    Language: str | None = None
    Latest_sync_date: datetime.datetime | None = None
    Licence_end: datetime.date | None = None
    Licence_start: datetime.date | None = None
    Number_of_classes: int | None = None
    School_ID: int | None = None
    Type_of_school: str | None = None
