from keap.REST.V1.mixins import ListMixin, CreateMixin, ModelMixin, RetrieveMixin


class AffiliateService(CreateMixin, ListMixin, ModelMixin, RetrieveMixin):
    api_url = "affiliates"

    def __init__(self, keap):
        super().__init__(keap)

    def get_commissions(self, **kwargs):
        return self._get(f"{self.api_url}/commissions", params=kwargs)

    def get_programs(self, **kwargs):
        return self._get(f"{self.api_url}/programs", params=kwargs)

    def get_redirects(self, **kwargs):
        return self._get(f"{self.api_url}/redirectlinks", params=kwargs)

    def get_summaries(self, **kwargs):
        return self._get(f"{self.api_url}/summaries", params=kwargs)

    def get_affilliate_clawbacks(self, id: int, **kwargs):
        return self._get(f"{self.api_url}/{id}/clawbacks", params=kwargs)

    def get_affilliate_payments(self, id: int, **kwargs):
        return self._get(f"{self.api_url}/{id}/payments", params=kwargs)
