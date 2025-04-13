from django.urls import include, path
from .views import PurchaseViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"purchase", PurchaseViewSet, basename="purchase")

purchase = PurchaseViewSet.as_view({"get": "details", "post": "create_detail"})

urlpatterns = [
    path("", include(router.urls)),
    path(r"purchase/<str:code>/details/$", purchase, name="purchase-detail"),
]
