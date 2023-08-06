from keap.REST import BaseService
from keap.REST.models import CustomFieldType


class BaseServiceMixin(BaseService):
    primary_key = "id"
    update_verb = "PUT"


class ModelMixin(BaseServiceMixin):
    def model(self):
        return self._get(f"{self.api_url}/model")


class CreateMixin(BaseServiceMixin):
    def create(self, **kwargs):
        return self._post(f"{self.api_url}", data=kwargs)


class DeleteMixin(BaseServiceMixin):
    def delete(self, id: int, params: dict = None):
        return self._delete(f"{self.api_url}/{id}", params=params)


class RetrieveMixin(BaseServiceMixin):
    def get(self, id: int, **kwargs):
        return self._get(f"{self.api_url}/{id}", params=kwargs)


class SearchMixin(BaseServiceMixin):
    def search(self, **kwargs):
        return self._get(f"{self.api_url}/search", params=kwargs)


class UpdateMixin(BaseServiceMixin):
    def update(self, id: int, data: dict = None, params: dict = None):
        return self._put(f"{self.api_url}/{id}", data=data, params=params)


class ReplaceMixin(BaseServiceMixin):
    def replace(self, id: int, data: dict = None, params: dict = None):
        return self._patch(f"{self.api_url}/{id}", data=data, params=params)


class ListMixin(BaseServiceMixin):
    def list(self, **kwargs):
        return self._get(f"{self.api_url}", params=kwargs)


class CreateCustomFieldMixin(BaseServiceMixin):
    def create_custom_field(self,
                            field_type: CustomFieldType,
                            label: str,
                            options: list = None,
                            group_id: int = 0,
                            user_group_id: int = None
                            ):
        data = locals()
        data['field_type'] = field_type.value
        return self._post(f"{self.api_url}/model/customFields", data=data)
