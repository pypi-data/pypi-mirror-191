from typing import List

from datetime import datetime

from keap.REST.V1.mixins import ModelMixin, DeleteMixin, RetrieveMixin, CreateCustomFieldMixin
from keap.REST.models import Address, CustomField, PhoneNumber, SocialAccount, EmailAddress, DuplicateOption


class ContactService(ModelMixin, DeleteMixin, RetrieveMixin, CreateCustomFieldMixin):
    api_url = "contacts"
    return_key = "contacts"
    update_verb = "patch"

    def __init__(self, keap):
        super().__init__(keap)

    def create(self,
               addresses: List[Address] = None,
               anniversary: datetime = None,
               birthday: datetime = None,
               company: int = None,
               contact_type: str = None,
               custom_fields: List[CustomField] = None,
               duplicate_option: DuplicateOption = None,
               email_addresses: List[EmailAddress] = None,
               family_name: str = None,
               fax_numbers: list = None,
               given_name: str = None,
               lead_source_id: int = None,
               middle_name: str = None,
               opt_in_reason: str = None,
               origin: dict = None,
               owner_id: int = None,
               phone_numbers: List[PhoneNumber] = None,
               preferred_locale: str = None,
               preferred_name: str = None,
               prefix: str = None,
               social_accounts: List[SocialAccount] = None,
               source_type: str = None,
               spouse_name: str = None,
               suffix: str = None,
               time_zone: str = None,
               website: str = None,
               **kwargs):
        data = locals() | kwargs
        if data.get(self.primary_key) or data.get('duplicate_option'):
            return self._put(f"{self.api_url}", data=data)
        return self._post(f"{self.api_url}", data=data)

    def list(self,
             limit: int = 1000,
             offset: int = 0,
             order: str = "id",
             ascending: bool = False,
             email: str = None,
             family_name: str = None,
             given_name: str = None,
             since: datetime = None,
             until: datetime = None,
             optional_properties: list = None
             ):
        params = locals()
        return self._get(f"{self.api_url}", params=params)

    def update(self,
               id: int,
               update_mask: list = None,
               addresses: List[Address] = None,
               anniversary: datetime = None,
               birthday: datetime = None,
               company: int = None,
               contact_type: str = None,
               custom_fields: List[CustomField] = None,
               email_addresses: List[EmailAddress] = None,
               family_name: str = None,
               fax_numbers: list = None,
               given_name: str = None,
               lead_source_id: int = None,
               middle_name: str = None,
               opt_in_reason: str = None,
               origin: dict = None,
               owner_id: int = None,
               phone_numbers: List[PhoneNumber] = None,
               preferred_locale: str = None,
               preferred_name: str = None,
               prefix: str = None,
               social_accounts: List[SocialAccount] = None,
               source_type: str = None,
               spouse_name: str = None,
               suffix: str = None,
               time_zone: str = None,
               website: str = None,
               **kwargs
               ):
        data = locals() | kwargs
        del data['update_mask']

        params = {}
        if update_mask:
            params['update_mask'] = update_mask

        return self._patch(f"{self.api_url}/{id}", data=data, params=params)

    def get_credit_cards(self, id: int):
        return self._get(f"{self.api_url}/{id}/creditCards")

    def create_credit_card(self,
                           id: int,
                           address: Address,
                           card_number: str,
                           card_type: str,
                           email_address: str,
                           expiration_month: str,
                           expiration_year: str,
                           maestro_issue_number: str,
                           maestro_start_date_month: str,
                           maestro_start_date_year: str,
                           name_on_card: str,
                           verification_code: str):
        data = locals()
        return self._post(f"{self.api_url}/{id}/creditCards", data=data)

    def list_emails(self, id: int, email: str = None, limit: int = 1000, offset: int = 0):
        params = {
            'limit': limit,
            'offset': offset,
        }
        if email:
            params['email'] = email
        return self._get(f"{self.api_url}/{id}/emails", params=params)

    def get_tags(self, id: int, limit: int = 1000, offset: int = 0):
        params = {
            'limit': limit,
            'offset': offset,
        }
        return self._get(f"{self.api_url}/{id}/tags", params=params)

    def add_tags(self, id: int, tags: list):
        data = {
            'tagIds': tags,
        }
        return self._post(f"{self.api_url}/{id}/tags", data=data)

    def remove_tags(self, id: int, tags: list):
        params = {
            'ids': tags,
        }
        return self._delete(f"{self.api_url}/{id}/tags", params=params)

    def remove_tag(self, id: int, tag: int):
        return self._delete(f"{self.api_url}/{id}/tags/{tag}")
