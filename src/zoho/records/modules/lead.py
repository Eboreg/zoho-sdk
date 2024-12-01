import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Self

from zoho.records.modules.base import AbstractTaggedModuleRecord
from zoho.records.ref import RecordRef, UserRef
from zoho.types import LanguageFieldType, SchoolYearType


@dataclass
class BaseLead(AbstractTaggedModuleRecord):
    Last_Name: str

    Annual_Revenue: Decimal | None = None
    Average_Time_Spent_Minutes: Decimal | None = None
    City: str | None = None
    Company: str | None = None
    Converted_Account: RecordRef | None = None
    Converted_Contact: RecordRef | None = None
    Converted_Date_Time: datetime.datetime | None = None
    Converted_Deal: RecordRef | None = None
    Country: str | None = None
    Created_By: UserRef | None = None
    Created_Time: datetime.datetime | None = None
    Days_Visited: int | None = None
    Description: str | None = None
    Designation: str | None = None
    Email_Opt_Out: bool = False
    Email: str | None = None
    Fax: str | None = None
    First_Name: str | None = None
    First_Visited_Time: datetime.datetime | None = None
    First_Visited_URL: str | None = None
    Full_Name: str | None = None
    Industry: str | None = None
    Last_Activity_Time: datetime.datetime | None = None
    Last_Visited_Time: datetime.datetime | None = None
    Lead_Conversion_Time: int | None = None
    Lead_Source: str | None = None
    Lead_Status: str | None = None
    Mobile: str | None = None
    Modified_By: UserRef | None = None
    Modified_Time: datetime.datetime | None = None
    No_of_Employees: int | None = None
    Number_Of_Chats: int | None = None
    Owner: UserRef | None = None
    Phone: str | None = None
    Rating: str | None = None
    Record_Image: str | None = None
    Referrer: str | None = None
    Salutation: str | None = None
    Secondary_Email: str | None = None
    Skype_ID: str | None = None
    State: str | None = None
    Street: str | None = None
    Twitter: str | None = None
    Unsubscribed_Mode: str | None = None
    Unsubscribed_Time: datetime.datetime | None = None
    Visitor_Score: str | None = None
    Website: str | None = None
    Zip_Code: str | None = None

    module: str = field(init=False, default="Leads")


@dataclass
class Lead(BaseLead):
    Country2: str | None = None
    Duplicate_Email: bool | None = None
    Email_Bounced: bool | None = None
    Headmaster: str | None = None
    Juridisk_form: str | None = None
    Language: LanguageFieldType | None = None
    Latest_email_campaign_send_date: datetime.datetime | None = None
    Lead_Type: str | None = None
    Linkedin_profile: str | None = None
    Organization_number: str | None = None
    School_District: str | None = None
    School_unit_name: str | None = None
    School_unit_type: str | None = None
    School_years: list[SchoolYearType] = field(default_factory=list)
    Sent_welcome_email: bool | None = None
    Set_up_the_task: bool | None = None
    Title: str | None = None
    Type_of_school: str | None = None

    @property
    def lead_status_prio(self) -> int:
        prios = [
            "New lead",
            "E-mail sent",
            "E-mail responded",
            "Not interested",
            "Call & discussion",
            "Converted",
        ]
        if self.Lead_Status is None:
            return -1
        try:
            return prios.index(self.Lead_Status)
        except ValueError:
            return -1

    @property
    def mergeable_fields(self):
        return [
            "City",
            "Company",
            "Country2",
            "Description",
            "First_Name",
            "Headmaster",
            "Juridisk_form",
            "Language",
            "Linkedin_profile",
            "Mobile",
            "Organization_number",
            "Phone",
            "School_District",
            "School_unit_name",
            "School_unit_type",
            "State",
            "Street",
            "Title",
            "Type_of_school",
            "Unsubscribed_Time",
            "Website",
            "Zip_Code",
        ]

    def merge_with(self, other: Self):
        for f in self.mergeable_fields:
            if getattr(other, f) and not getattr(self, f):
                setattr(self, f, getattr(other, f))
        if other.lead_status_prio > self.lead_status_prio:
            self.Lead_Status = other.Lead_Status
        if other.Sent_welcome_email:
            self.Sent_welcome_email = True
        if other.Set_up_the_task:
            self.Set_up_the_task = True
        if other.Email_Bounced:
            self.Email_Bounced = True
        if other.School_years:
            self.School_years = list(set((self.School_years or []) + other.School_years))
        for other_tag in other.Tag:
            if other_tag not in self.Tag:
                self.Tag.append(other_tag)
