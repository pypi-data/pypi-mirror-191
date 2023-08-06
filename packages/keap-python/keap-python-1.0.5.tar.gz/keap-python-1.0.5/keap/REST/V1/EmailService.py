from keap.REST.V1.mixins import CreateMixin, DeleteMixin, ListMixin, RetrieveMixin


class EmailService(CreateMixin, DeleteMixin, ListMixin, RetrieveMixin):
    api_url = "emails"

    def __init__(self, keap):
        super().__init__(keap)

    def create_email(self, **kwargs):
        self._post(f"{self.api_url}", data=kwargs)

    def send_email(self, **kwargs):
        self._post(f"{self.api_url}", data=kwargs)

    def sync_email_records(self, **kwargs):
        self._post(f"{self.api_url}/sync", data=kwargs)

    def unsync_email_records(self, **kwargs):
        self._post(f"{self.api_url}/unsync", data=kwargs)

    def update_email_address(self, email: str, opted_in: bool = True, reason: str = "Opted in via API"):
        self._put(f"emailAddresses/{email}", data={'opted_in': opted_in, 'reason': reason})
