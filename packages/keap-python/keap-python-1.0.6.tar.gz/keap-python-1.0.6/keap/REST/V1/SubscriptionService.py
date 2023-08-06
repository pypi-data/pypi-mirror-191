from keap.REST.V1.mixins import CreateMixin, ListMixin, ModelMixin


class SubscriptionService(CreateMixin, ListMixin, ModelMixin):
    api_url = "subscriptions"

    def __init__(self, keap):
        super().__init__(keap)
