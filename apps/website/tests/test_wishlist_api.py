import pytest
from django.urls import reverse
from products.models import Product, ProductStatusType


@pytest.mark.django_db
class TestWishlistAPI:

    # ---------- RETRIEVE ----------

    def test_retrieve_with_anonymous_user_response_401_status(self, api_client):
        url = reverse("website:wishlist")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_retrieve_with_owner_response_200_status(
        self, api_client, normal_user, common_wishlist, common_product
    ):
        api_client.force_authenticate(user=normal_user)
        url = reverse("website:wishlist")
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["user"] == normal_user.username
        assert common_product.title in response.data["products"]

    # ---------- UPDATE ----------

    def test_update_with_anonymous_user_response_401_status(
        self, api_client, common_wishlist
    ):
        url = reverse("website:wishlist")
        response = api_client.put(url, {"products": []})
        assert response.status_code == 401

    def test_update_with_published_product_response_200_status(
        self, api_client, normal_user, common_wishlist
    ):
        published_product = Product.objects.create(
            title="published-product",
            price=10000,
            stock=5,
            status=ProductStatusType.PUBLISH,
        )
        api_client.force_authenticate(user=normal_user)
        url = reverse("website:wishlist")
        response = api_client.put(url, {"products": [published_product.title]})
        assert response.status_code == 200
        assert response.data["products"] == [published_product.title]

    def test_update_with_non_published_product_response_400_status(
        self, api_client, normal_user, common_wishlist
    ):
        draft_product = Product.objects.create(
            title="draft-product",
            price=10000,
            stock=5,
            status=ProductStatusType.DRAFT,
        )
        api_client.force_authenticate(user=normal_user)
        url = reverse("website:wishlist")
        response = api_client.put(url, {"products": [draft_product.title]})
        assert response.status_code == 400

    def test_update_with_invalid_product_title_response_400_status(
        self, api_client, normal_user, common_wishlist
    ):
        api_client.force_authenticate(user=normal_user)
        url = reverse("website:wishlist")
        response = api_client.put(url, {"products": ["nonexistent-product-title"]})
        assert response.status_code == 400

    def test_update_replaces_full_product_list(
        self, api_client, normal_user, common_wishlist, common_product
    ):
        new_product = Product.objects.create(
            title="second-product",
            price=20000,
            stock=3,
            status=ProductStatusType.PUBLISH,
        )
        api_client.force_authenticate(user=normal_user)
        url = reverse("website:wishlist")
        response = api_client.put(url, {"products": [new_product.title]})
        assert response.status_code == 200
        assert response.data["products"] == [new_product.title]
        assert common_product.title not in response.data["products"]

    def test_update_with_other_user_does_not_affect_owner_wishlist(
        self, api_client, admin_user, admin_wishlist, common_wishlist, common_product
    ):
        api_client.force_authenticate(user=admin_user)
        url = reverse("website:wishlist")
        response = api_client.put(url, {"products": []})
        assert response.status_code == 200

        common_wishlist.refresh_from_db()
        assert common_product in common_wishlist.products.all()
