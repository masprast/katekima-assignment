from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from items.models import Item
from .models import PurchaseHeader, PurchaseDetail
from .serializer import (
    PurchaseDetailModifySerializer,
    PurchaseHeaderModifySerializer,
    PurchaseHeaderSerializer,
    PurchaseDetailSerializer,
)


# Create your views here.


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHeader.objects.filter(is_deleted=False)
    serializer_class = PurchaseHeaderSerializer
    lookup_field = "code"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PurchaseHeaderModifySerializer
        return PurchaseHeaderSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_value = self.kwargs.get(self.lookup_field)
        try:
            return get_object_or_404(
                queryset, **{f"{self.lookup_field}__iexact": lookup_value}
            )
        except PurchaseHeader.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], url_path="details")
    def details(self, request, code=None):
        purchase_header = self.get_object()
        details = PurchaseDetail.objects.filter(header_code=purchase_header)
        serializer = PurchaseDetailSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="details")
    def create_detail(self, request, code=None):
        purchase_header = self.get_object()
        serializer = PurchaseDetailModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_code = serializer.validated_data["item_code"]
        quantity = serializer.validated_data["quantity"]
        unit_price = serializer.validated_data["unit_price"]

        with transaction.atomic():
            try:
                item = Item.objects.get(code=item_code, is_deleted=False)
                purchase_detail = PurchaseDetail.objects.create(
                    header_code=purchase_header,
                    item_code=item,
                    quantity=quantity,
                    unit_price=unit_price,
                )

                # Purchasing adalah membeli untuk menambah stock
                item.stock += quantity
                item.balance += quantity * unit_price
                item.save()
                return Response(
                    PurchaseDetailSerializer(purchase_detail).data,
                    status=status.HTTP_201_CREATED,
                )
            except Item.DoesNotExist:
                purchase_detail.delete()
                return Response(
                    {
                        "error": f"Item with code {item_code} does not exist.",
                        "status": status.HTTP_404_NOT_FOUND,
                    },
                )
