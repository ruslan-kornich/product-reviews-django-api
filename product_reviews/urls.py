from django.contrib import admin
from django.urls import path, include
from api.views import AllProducts

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("", AllProducts.as_view(), name="home"),
]
