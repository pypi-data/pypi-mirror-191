from keap.REST.V1.mixins import (CreateMixin, CreateCustomFieldMixin,  ListMixin, ModelMixin, ReplaceMixin,
                                 RetrieveMixin, UpdateMixin)


class OpportunityService(CreateMixin, CreateCustomFieldMixin, ListMixin, ModelMixin, ReplaceMixin, RetrieveMixin,
                         UpdateMixin):
    api_url = "opportunities"

    def __init__(self, keap):
        super().__init__(keap)
