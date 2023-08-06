from keap.REST.V1.mixins import RetrieveMixin, DeleteMixin


class TagService(DeleteMixin, RetrieveMixin):
    api_url = "tags"
    return_key = "tags"

    def __init__(self, keap):
        super().__init__(keap)

    def list(self,
             category: int = None,
             name: str = None,  # This is a full string match, no wildcard
             limit: int = 1000,
             offset: int = 0,
             ):
        params = {
            'limit': limit,
            'offset': offset,
        }
        if category:
            params['category'] = category
        if name:
            params['name'] = name

        return self._get(f"{self.api_url}", params=params)

    def create(self, category: int, name: str, description: str = None):
        data = {
            'category': {
                'id': category
            },
            'name': name
        }
        if description:
            data['description'] = description
        return self._post(f"{self.api_url}", data=data)

    def create_category(self, name: str, description: str = None):
        data = {
            'name': name
        }
        if description:
            data['description'] = description
        return self._post(f"{self.api_url}/categories", data=data)

    def get_tagged_companies(self, id: int, limit: int = 1000, offset: int = 0):
        params = {
            'tagId': id,
            'limit': limit,
            'offset': offset,
        }
        return self._get(f"{self.api_url}/{id}/companies", params=params)

    def get_tagged_contacts(self, id: int, limit: int = 1000, offset: int = 0):
        params = {
            'tagId': id,
            'limit': limit,
            'offset': offset,
        }
        return self._get(f"{self.api_url}/{id}/contacts", params=params)

    def add_contacts(self, id: int, contact_ids: list):
        data = {
            'ids': contact_ids,
        }
        return self._post(f"{self.api_url}/{id}/contacts", data=data)

    def remove_contacts(self, id: int, contact_ids: list):
        params = {
            'ids': ','.join([str(cid) for cid in contact_ids]),
        }
        return self._delete(f"{self.api_url}/{id}/contacts", params=params)

    def remove_contact(self, id: int, contact_id: int):
        return self._delete(f"{self.api_url}/{id}/contacts/{contact_id}")
