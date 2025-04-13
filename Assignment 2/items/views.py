from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Item
from .serializer import ItemModifySerializer, ItemSerializer


# Create your views here.


# Menggunakan viewsets karena kita akan menggunakan CRUD
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(is_deleted=False)
    serializer_class = ItemSerializer
    lookup_field = "code"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_value = self.kwargs.get(self.lookup_field)
        try:
            return get_object_or_404(
                queryset, **{f"{self.lookup_field}__iexact": lookup_value}
            )
        except Item.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Mendapatkan serializer apakah untuk menampilkan atau membuat dan mengubah data
    # jika untuk menampilkan data maka menggunakan ItemSerializer
    # jika untuk membuat atau mengubah data maka menggunakan ItemModifySerializer
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ItemModifySerializer
        return ItemSerializer

    # Untuk menghapus data menggunakan pendekatan Soft delete dengan mengubah nilai 'is_deleted' menjadi 'True'
    # sehingga data tidak terhapus dan masih tersimpan di database
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     if getattr(instance, "_prefetched_objects_cache", None):
    #         instance._prefetched_objects_cache = {}
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     if getattr(instance, "_prefetched_objects_cache", None):
    #         instance._prefetched_objects_cache = {}
    #     return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if instance.is_deleted:
    #         return Response(
    #             {"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND
    #         )
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
