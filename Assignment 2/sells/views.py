from email import header
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from items import serializer
from purchases.models import PurchaseDetail
from .models import SellHeader, SellDetail
from .serializer import (
    SellHeaderModifySerializer,
    SellHeaderSerializer,
    SellDetailSerializer,
    SellDetailModifySerializer,
)
from items.models import Item


# Create your views here.


class SellViewSet(viewsets.ModelViewSet):
    queryset = SellHeader.objects.filter(is_deleted=False)
    serializer_class = SellHeaderSerializer
    lookup_field = "code"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SellHeaderModifySerializer
        return SellHeaderSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_value = self.kwargs.get(self.lookup_field)
        try:
            return get_object_or_404(
                queryset, **{f"{self.lookup_field}__iexact": lookup_value}
            )
        except SellHeader.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], url_path="details")
    def details(self, request, code=None):
        sell_header = self.get_object()
        details = SellDetail.objects.filter(header_code=sell_header)
        serializer = SellDetailSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="details")
    def create_detail(self, request, code=None):
        sell_header = self.get_object()
        serializer = SellDetailModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_code = serializer.validated_data["item_code"]
        quantity = serializer.validated_data["quantity"]

        with transaction.atomic():
            sell_detail = serializer.save(header_code=sell_header)
            try:
                item = Item.objects.get(code=item_code, is_deleted=False)
                if item.stock >= quantity:
                    purchases = PurchaseDetail.objects.filter(
                        item_code=item_code
                    ).order_by("header_code__date")
                    sold_price = 0
                    qty_to_sell = quantity
                    for purchase in purchases:
                        if qty_to_sell > 0:
                            sell_qty = min(qty_to_sell, purchase.quantity)
                            sold_price += sell_qty * purchase.unit_price
                            qty_to_sell -= sell_qty

                    # Selling adalah menjual sehingga stock berkurang
                    item.stock -= quantity
                    item.balance -= sold_price
                    item.save()
                    return Response(
                        SellDetailSerializer(sell_detail).data,
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {
                            "error": f"Not enough stock for item '{item_code}'. Available stock: {item.stock}"
                        }
                    )
            except Item.DoesNotExist:
                return Response(
                    {"error": f"Item with code '{item_code}' does not exist."}
                )
