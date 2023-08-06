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
               key: str = None,
               secret_key: str = None):
        params = dict()
        params["access_token"] = self.token.access_token
        print(secret_key)
        headers = {
            'Content-Type': 'application/json',
            'X-Hook-Secret': secret_key
        }
        url = f'https://api.infusionsoft.com/crm/rest/v1/hooks/{key}/verify'
        response = requests.request("POST", url, headers=headers, params=params)
        print(response.json())
        print('is ver')
        return response

    def list_event_keys(self):
        return self._get(f"{self.api_url}/event_keys")

    def delete_hooks(self,
                     hook_keys: list = None):
        for key in hook_keys:
            self._delete(key=key)


