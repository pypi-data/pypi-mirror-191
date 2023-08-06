from keap.REST.V1.mixins import BaseServiceMixin


class LocaleService(BaseServiceMixin):
    api_url = "locales"

    def __init__(self, keap):
        super().__init__(keap)

    def list_countries(self):
        return self._get(f"{self.api_url}/countries")

    def list_country_provinces(self, country_code: str):
        return self._get(f"{self.api_url}/countries/{country_code}/provinces")

    def list_dropdown_defaults(self):
        return self._get(f"{self.api_url}/defaultOptions")
