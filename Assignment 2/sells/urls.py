from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SellViewSet

router = DefaultRouter()
router.register(r"sell", SellViewSet, basename="sell")

sell = SellViewSet.as_view({"get": "details", "post": "create_detail"})

urlpatterns = [
    path("", include(router.urls)),
    path("sell/<str:code>/details", sell, name="sell-detail"),
]
