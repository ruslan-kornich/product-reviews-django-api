import os
import pytest
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product_reviews.settings")
django.setup()
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Product, Review
from api.serializers import ProductSerializer, ReviewSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestAPI:

    def test_product_creation(self):
        product = Product.objects.create(title="Test Product", asin="123456")
        assert product.title == "Test Product"
        assert product.asin == "123456"

    def test_review_creation(self):
        product = Product.objects.create(title="Test Product", asin="123456")
        review = Review.objects.create(
            product=product, title="Test Review", review="This is a test review"
        )
        assert review.title == "Test Review"
        assert review.review == "This is a test review"

    def test_all_products(self, api_client):
        url = reverse("home")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_product_detail(self, api_client):
        product = Product.objects.create(title="Test Product", asin="123456")
        url = reverse("product-detail", kwargs={"pk": product.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_review_create(self, api_client):
        product = Product.objects.create(title="Test Product", asin="123456")
        url = reverse("review-create")
        data = {
            "product": product.pk,
            "title": "Test Review",
            "review": "This is a test review",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_product_serializer(self):
        product = Product.objects.create(title="Test Product", asin="123456")
        serializer = ProductSerializer(instance=product)
        assert serializer.data["title"] == "Test Product"
        assert serializer.data["asin"] == "123456"

    def test_review_serializer(self):
        product = Product.objects.create(title="Test Product", asin="123456")
        review = Review.objects.create(
            product=product, title="Test Review", review="This is a test review"
        )
        serializer = ReviewSerializer(instance=review)
        assert serializer.data["title"] == "Test Review"
        assert serializer.data["review"] == "This is a test review"

    def test_invalid_product_detail(self, api_client):
        url = reverse("product-detail", kwargs={"pk": 999})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_review_create_invalid_product(self, api_client):
        url = reverse("review-create")
        data = {
            "product": 999,
            "title": "Invalid Review",
            "content": "This review should not be created",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Product does not exist."

    def test_invalid_review_create_invalid_data(self, api_client):
        product = Product.objects.create(title="Test Product", asin="123456")
        url = reverse("review-create")
        # Missing 'content' field
        data = {"product": product.pk, "title": "Invalid Review"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
