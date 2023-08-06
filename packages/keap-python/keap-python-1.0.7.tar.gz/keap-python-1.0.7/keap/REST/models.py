import json
from enum import Enum
from typing import List, Literal


class BaseDataModel(object):
    @property
    def data(self):
        return self.__dict__


class CustomField(BaseDataModel):
    content: any = None
    id: int = None

    def __init__(self, id, content):
        self.content = content
        self.id = id


class EmailAddress(BaseDataModel):
    field: str
    email: str
    slot_min = 1
    slot_max = 3

    def __init__(self, slot: int):
        if slot < self.slot_min or slot > self.slot_max:
            raise ValueError
        self.field = f"EMAIL{slot}"


class PhoneFieldBase(BaseDataModel):
    field: str = None
    number: str = None
    type: str = None
    extension: str = None
    slot_min = 1
    slot_max = 5

    def __init__(self, slot: int):
        if slot < self.slot_min or slot > self.slot_max:
            raise ValueError
        self.field = f"{self.field}{slot}"


class FaxNumber(PhoneFieldBase):
    slot_min = 1
    slot_max = 2

    def __init__(self, slot: int):
        self.field = "FAX"
        super().__init__(slot)


class PhoneNumber(PhoneFieldBase):
    slot_min = 1
    slot_max = 5

    def __init__(self, slot: int):
        self.field = f"PHONE"
        super().__init__(slot)


class SocialAccount(BaseDataModel):
    name: str
    type: str

    def __init__(self,
                 platform: Literal['Facebook', 'Twitter', 'LinkedIn', 'Instagram', 'Snapchat', 'YouTube', 'Pinterest']):
        if platform not in ['Facebook', 'Twitter', 'LinkedIn', 'Instagram', 'Snapchat', 'YouTube', 'Pinterest']:
            raise ValueError
        self.type = platform


class Address(BaseDataModel):
    country_code: str = ""
    field: str = ""
    line1: str = ""
    line2: str = ""
    locality: str = ""
    postal_code: str = ""
    region: str = ""
    zip_code: str = ""
    zip_four: str = ""

    def __str__(self):
        return f"{self.line1} {self.locality}, {self.region} {self.zip_code}"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class BillingAddress(Address):
    def __init__(self):
        self.field = "BILLING"


class ShippingAddress(Address):
    def __init__(self):
        self.field = "SHIPPING"


class OtherAddress(Address):
    def __init__(self):
        self.field = "OTHER"


class DuplicateOption(Enum):
    EMAIL = "Email"
    EMAIL_AND_NAME = "EmailAndName"


class CustomFieldType(Enum):
    CURRENCY = 'Currency'
    DATE = 'Date'
    DATETIME = 'DateTime'
    DAY_OF_WEEK = 'DayOfWeek'
    DRILLDOWN = 'Drilldown'
    EMAIL = 'Email'
    MONTH = 'Month'
    LIST_BOX = 'ListBox'
    NAME = 'Name'
    WHOLE_NUMBER = 'WholeNumber'
    DECIMAL_NUMBER = 'DecimalNumber'
    PERCENT = 'Percent'
    PHONE_NUMBER = 'PhoneNumber'
    RADIO = 'Radio'
    DROPDOWN = 'Dropdown'
    SOCIAL_SECURITYN_UMBER = 'SocialSecurityNumber'
    STATE = 'State'
    TEXT = 'Text'
    TEXT_AREA = 'TextArea'
    USER = 'User'
    USER_LIST_BOX = 'UserListBox'
    WEBSITE = 'Website'
    YEAR = 'Year'
    YES_NO = 'YesNo'
