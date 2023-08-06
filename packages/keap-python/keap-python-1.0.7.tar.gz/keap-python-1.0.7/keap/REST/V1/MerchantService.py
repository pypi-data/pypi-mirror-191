from keap.REST.V1.mixins import ListMixin


class MerchantService(ListMixin):
    api_url = "merchants"

    def __init__(self, keap):
        super().__init__(keap)
