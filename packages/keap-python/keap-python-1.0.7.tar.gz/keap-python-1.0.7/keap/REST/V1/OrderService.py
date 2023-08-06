from keap.REST.V1.mixins import (CreateMixin, DeleteMixin, ListMixin, ModelMixin, RetrieveMixin)


class OrderService(CreateMixin, DeleteMixin, ListMixin, ModelMixin, RetrieveMixin):
    api_url = "orders"

    def __init__(self, keap):
        super().__init__(keap)

    def create_order_item(self, order_id: int, **kwargs):
        return self._get(f"{self.api_url}/{order_id}/items", params=kwargs)

    def delete_order_item(self, order_id: int, order_item_id: int):
        return self._delete(f"{self.api_url}/{order_id}/items/{order_item_id}")

    def replace_order_payplan(self, order_id: int, **kwargs):
        return self._delete(f"{self.api_url}/{order_id}/paymentPlan", data=kwargs)

    def get_order_payments(self, order_id: int):
        return self._get(f"{self.api_url}/{order_id}/payments")

    def create_order_payments(self, order_id: int, **kwargs):
        return self._post(f"{self.api_url}/{order_id}/payments", data=kwargs)

    def get_order_transactions(self, order_id: int, **kwargs):
        return self._get(f"{self.api_url}/{order_id}/transactions", params=kwargs)
