from keap.REST.V1.mixins import BaseServiceMixin


class SettingService(BaseServiceMixin):
    api_url = "setting"

    def __init__(self, keap):
        super().__init__(keap)

    def get_application_configuration(self):
        return self._get(f"{self.api_url}/application/configuration")

    def get_application_status(self):
        return self._get(f"{self.api_url}/application/enabled")
