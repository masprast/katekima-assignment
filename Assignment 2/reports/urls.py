from django.urls import path
from .views import StockReport

urlpatterns = [
    path(r"report/<str:item_code>/", StockReport.as_view(), name="stock-report"),
]
