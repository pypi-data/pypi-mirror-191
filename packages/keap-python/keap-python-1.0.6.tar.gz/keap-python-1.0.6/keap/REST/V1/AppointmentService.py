from keap.REST.V1.mixins import (CreateMixin, CreateCustomFieldMixin, DeleteMixin, ListMixin, ModelMixin, ReplaceMixin,
                                 RetrieveMixin, UpdateMixin)


class AppointmentService(CreateMixin, CreateCustomFieldMixin, DeleteMixin, ListMixin, ModelMixin, ReplaceMixin,
                         RetrieveMixin, UpdateMixin):
    api_url = "appointments"

    def __init__(self, keap):
        super().__init__(keap)
