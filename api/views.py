from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AllProducts(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related("reviews").order_by("-id")
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @method_decorator(cache_page(60 * 15))  # Caching for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all().prefetch_related("reviews")
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @method_decorator(cache_page(60 * 15))  # Caching for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all().order_by("id")
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):

        product_id = request.data.get("product") or kwargs.get("pk")

        # Checking the existence of the product
        if not Product.objects.filter(pk=product_id).exists():
            return Response(
                {"error": "Product does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Adding product_id to review data
        request.data["product"] = product_id

        # Create a serializer with the transferred data
        serializer = self.get_serializer(data=request.data)
        # Data validation
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        # Saving the review
        self.perform_create(serializer)
        # Generating a successful response
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
