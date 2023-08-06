from keap.REST.V1.mixins import (CreateMixin, CreateCustomFieldMixin, DeleteMixin, ListMixin, ModelMixin, ReplaceMixin,
                                 RetrieveMixin, UpdateMixin)


class ProductService(CreateMixin, DeleteMixin, ListMixin, ReplaceMixin,
                     RetrieveMixin, UpdateMixin):
    api_url = "products"

    def __init__(self, keap):
        super().__init__(keap)

    def upload_product_image(self, product_id: int, **kwargs):
        return self._post(f"{self.api_url}/{product_id}/image", data=kwargs)

    def delete_product_image(self, product_id: int):
        return self._delete(f"{self.api_url}/{product_id}/image")

    def create_product_subscription(self, product_id: int, **kwargs):
        return self._post(f"{self.api_url}/{product_id}/subscriptions", data=kwargs)

    def get_product_subscription(self, product_id: int, subscription_id: int):
        return self._get(f"{self.api_url}/{product_id}/subscriptions/{subscription_id}")

    def delete_product_subscription(self, product_id: int, subscription_id: int):
        return self._get(f"{self.api_url}/{product_id}/subscriptions/{subscription_id}")
