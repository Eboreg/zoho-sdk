import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING

from zoho.records.modules.base import AbstractModuleRecord
from zoho.records.ref import RecordRef, TerritoryRef, UserRef
from zoho.types import LanguageFieldType


if TYPE_CHECKING:
    from zoho.records.tag import Tag


@dataclass
class BaseContact(AbstractModuleRecord):
    Last_Name: str

    Account_Name: RecordRef | None = None
    Assistant: str | None = None
    Asst_Phone: str | None = None
    Average_Time_Spent_Minutes: Decimal | None = None
    Created_By: UserRef | None = None
    Created_Time: datetime.datetime | None = None
    Date_of_Birth: datetime.date | None = None
    Days_Visited: int | None = None
    Department: str | None = None
    Description: str | None = None
    Email_Opt_Out: bool | None = None
    Email: str | None = None
    Fax: str | None = None
    First_Name: str | None = None
    First_Visited_Time: datetime.datetime | None = None
    First_Visited_URL: str | None = None
    Full_Name: str | None = None
    Home_Phone: str | None = None
    Last_Activity_Time: datetime.datetime | None = None
    Last_Visited_Time: datetime.datetime | None = None
    Lead_Source: str | None = None
    Mailing_City: str | None = None
    Mailing_Country: str | None = None
    Mailing_State: str | None = None
    Mailing_Street: str | None = None
    Mailing_Zip: str | None = None
    Mobile: str | None = None
    Modified_By: UserRef | None = None
    Modified_Time: datetime.datetime | None = None
    Number_Of_Chats: int | None = None
    Other_City: str | None = None
    Other_Country: str | None = None
    Other_Phone: str | None = None
    Other_State: str | None = None
    Other_Street: str | None = None
    Other_Zip: str | None = None
    Owner: UserRef | None = None
    Phone: str | None = None
    Record_Image: str | None = None
    Referrer: str | None = None
    Reporting_To: RecordRef | None = None
    Salutation: str | None = None
    Secondary_Email: str | None = None
    Skype_ID: str | None = None
    Tag: list["Tag"] = field(default_factory=list)
    Territories: list[TerritoryRef] = field(default_factory=list)
    Title: str | None = None
    Twitter: str | None = None
    Unsubscribed_Mode: str | None = None
    Unsubscribed_Time: datetime.datetime | None = None
    Vendor_Name: RecordRef | None = None
    Visitor_Score: str | None = None

    module: str = field(init=False, default="Contacts")


@dataclass
class Contact(BaseContact):
    City: str | None = None
    Country: str | None = None
    Grow_Planet_admin_URL: str | None = None
    Grow_Planet_licence_end: datetime.date | None = None
    Grow_Planet_licence_start: datetime.date | None = None
    Grow_Planet_reg_date: datetime.datetime | None = None
    Grow_Planet_user_ID: int | None = None
    Language: LanguageFieldType | None = None
    Latest_sync_date: datetime.datetime | None = None
    organization: str | None = None
    Type_of_school: str | None = None
