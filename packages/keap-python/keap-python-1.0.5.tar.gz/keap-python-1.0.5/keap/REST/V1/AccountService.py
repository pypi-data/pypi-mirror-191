from keap.REST.V1.mixins import RetrieveMixin, UpdateMixin


class AccountService(RetrieveMixin, UpdateMixin):
    api_url = "account/profile"

    def __init__(self, keap):
        super().__init__(keap)
