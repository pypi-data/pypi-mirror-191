from keap.REST.V1.mixins import RetrieveMixin, UpdateMixin
import requests


class HookService(RetrieveMixin, UpdateMixin):
    api_url = "hooks"

    def __init__(self, keap):
        super().__init__(keap)

    def create(self,
               eventKey: str = None,
               hookUrl: str = None,
               ):
        data = locals()
        return self._post(f"{self.api_url}", data=data)
        # return self._post(f"{self.api_url}", data=data)

    def list(self):
        return self._get(f"{self.api_url}")

    def delete(self,
               key: str = None):
        return self._delete(f"{self.api_url}/{key}")

    def verify(self,
               key: int = None):
        return self._post(f'{self.api_url}/{key}')

    def list_event_keys(self):
        return self._get(f"{self.api_url}/event_keys")

    def delete_hooks(self,
                     hook_keys: list = None):
        for key in hook_keys:
            self._delete(key=key)


