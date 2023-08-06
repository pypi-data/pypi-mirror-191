from keap.REST.V1.mixins import (CreateMixin, CreateCustomFieldMixin, DeleteMixin, ListMixin, ModelMixin, ReplaceMixin,
                                 RetrieveMixin, UpdateMixin)


class NoteService(CreateMixin, CreateCustomFieldMixin, DeleteMixin, ListMixin, ModelMixin, ReplaceMixin,
                  RetrieveMixin, UpdateMixin):
    api_url = "notes"

    def __init__(self, keap):
        super().__init__(keap)

    def get_contact_notes(self,
                          contact_id: int = None):
        params = locals()
        return self._get(f"{self.api_url}", params=params)
