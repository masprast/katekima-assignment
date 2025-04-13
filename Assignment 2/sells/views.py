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
# class SellListView(generics.ListAPIView):
#     queryset = SellHeader.objects.filter(is_deleted=False)
#     serializer_class = SellHeaderSerializer


# class SellDetailView(generics.RetrieveAPIView):
#     queryset = SellDetail.objects.all()
#     serializer_class = SellHeaderSerializer
#     lookup_field = "code"


# class SellCreateView(generics.CreateAPIView):
#     queryset = SellHeader.objects.all()
#     serializer_class = SellHeaderModifySerializer


# class SellUpdateView(generics.UpdateAPIView):
#     queryset = SellHeader.objects.filter(is_deleted=False)
#     serializer_class = SellHeaderModifySerializer
#     lookup_field = "code"


# class SellDeleteView(generics.DestroyAPIView):
#     queryset = SellHeader.objects.filter(is_deleted=False)
#     lookup_field = "code"

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.is_deleted = True
#         instance.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class SellDetailListByHeader(generics.ListAPIView):
#     serializer_class = SellDetailSerializer

#     def get_queryset(self):
#         header_code = self.kwargs.get("header_code")
#         header = get_object_or_404(SellHeader, code=header_code, is_deleted=False)
#         return SellDetail.objects.filter(header_code=header)


# class SellDetailModify(generics.CreateAPIView):
#     serializer_class = SellDetailModifySerializer

#     def perform_create(self, serializer):
#         header_code = self.kwargs.get("header_code")
#         header = get_object_or_404(SellHeader, code=header_code, is_deleted=False)
#         item_code = serializer.validated_data["item_code"]
#         quantity = serializer.validated_data["quantity"]

#         with transaction.atomic():
#             sell_detail = serializer.save(header_code=header)
#             try:
#                 item = Item.objects.get(code=item_code, is_deleted=False)
#                 if item.stock >= quantity:
#                     # Find the purchasing stock to decrease balance
#                     # This requires tracking purchase history per item
#                     # For simplicity, we'll just decrease the overall balance
#                     # A more robust solution would track FIFO/LIFO for accurate COGS
#                     purchases = PurchaseDetail.objects.filter(
#                         item_code=item_code
#                     ).order_by("header_code__date")
#                     sold_price = 0
#                     qty_to_sell = quantity
#                     for purchase in purchases:
#                         if qty_to_sell > 0:
#                             sell_qty = min(qty_to_sell, purchase.quantity)
#                             sold_price += sell_qty * purchase.unit_price
#                             qty_to_sell -= sell_qty

#                     item.stock -= quantity
#                     item.balance -= sold_price  # Simplified balance decrease
#                     item.save()
#                 else:
#                     raise serializer.ValidationError(
#                         f"Not enough stock for item '{item_code}'. Available stock: {item.stock}"
#                     )
#             except Item.DoesNotExist:
#                 raise serializer.ValidationError(
#                     f"Item with code '{item_code}' does not exist."
#                 )


#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return self.perform_create(serializer)
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], url_path="details")
    def details(self, request, code=None):
        header = self.get_object()
        details = SellDetail.objects.filter(header_code=header)
        serializer = SellDetailSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="details")
    def create_detail(self, request, code=None):
        header = self.get_object()
        serializer = SellDetailModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_code = serializer.validated_data["item_code"]
        quantity = serializer.validated_data["quantity"]

        with transaction.atomic():
            sell_detail = serializer.save(header_code=header)
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
