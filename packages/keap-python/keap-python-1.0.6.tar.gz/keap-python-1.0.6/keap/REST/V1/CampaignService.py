from keap.REST.V1.mixins import ListMixin, RetrieveMixin


class CampaignService(ListMixin, RetrieveMixin):
    api_url = "campaigns"

    def __init__(self, keap):
        super().__init__(keap)

    def achieve_goal(self, integration: str, call: str, contact_id: int):
        return self._post(f"{self.api_url}/goals/{integration}/{call}", data={'contact_id': contact_id})

    def add_contact_to_campaign(self, campaign_id: int, sequence_id: int, contact_id: int):
        return self._post(f"{self.api_url}/{campaign_id}/sequences/{sequence_id}/contacts/{contact_id}")

    def add_contacts_to_campaign(self, campaign_id: int, sequence_id: int, contacts: list):
        return self._post(f"{self.api_url}/{campaign_id}/sequences/{sequence_id}/contacts",
                          data={'ids': contacts})

    def remove_contact_from_campaign(self, campaign_id: int, sequence_id: int, contact_id: int):
        return self._delete(f"{self.api_url}/{campaign_id}/sequences/{sequence_id}/contacts/{contact_id}")

    def remove_contacts_from_campaign(self, campaign_id: int, sequence_id: int, contacts: list):
        return self._delete(f"{self.api_url}/{campaign_id}/sequences/{sequence_id}/contacts",
                            data={'ids': contacts})
