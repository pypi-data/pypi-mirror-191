from keap.REST.V1.mixins import ListMixin, RetrieveMixin


class TransactionService(ListMixin, RetrieveMixin):
    api_url = "transactions"

    def __init__(self, keap):
        super().__init__(keap)
