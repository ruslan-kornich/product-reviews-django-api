from django.urls import path
from .views import ProductDetail, ReviewCreate

urlpatterns = [
    path("products/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("reviews/create/", ReviewCreate.as_view(), name="review-create"),
]
