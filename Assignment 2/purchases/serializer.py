from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from items.models import Item
from .models import PurchaseHeader, PurchaseDetail


class PurchaseDetailSerializer(serializers.ModelSerializer):
    # Untuk menampilkan item_code dengan slug yang sesuai dengan 'code' pada model Item
    header_code = serializers.SlugRelatedField(
        slug_field="code", queryset=PurchaseHeader.objects.all()
    )

    class Meta:
        model = PurchaseDetail
        fields = ["item_code", "quantity", "unit_price", "header_code"]
        read_only_fields = ["header_code", "created_at", "updated_at", "is_deleted"]


class PurchaseHeaderSerializer(serializers.ModelSerializer):
    details = PurchaseDetailSerializer(many=True, read_only=True)
    code = serializers.CharField(max_length=5, min_length=5)

    class Meta:
        model = PurchaseHeader
        fields = ["code", "date", "description", "details"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]
        extra_kwargs = {
            "code": {"validators": [MinLengthValidator(5), MaxLengthValidator(5)]}
        }


class PurchaseHeaderModifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=5, min_length=5)

    class Meta:
        model = PurchaseHeader
        fields = ["code", "date", "description"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]
        extra_kwargs = {
            "code": {"validators": [MinLengthValidator(5), MaxLengthValidator(5)]}
        }

    def validate_code(self, value):
        # Cek jika purchase code sudah ada
        if self.instance is None:  # Create
            if PurchaseHeader.objects.filter(
                code__iexact=value, is_deleted=False
            ).exists():
                raise serializers.ValidationError(
                    f"Purchase with code {value} already exists."
                )
        else:  # Update
            if (
                value.lower() != self.instance.code.lower()
                and PurchaseHeader.objects.filter(code__iexact=value, is_deleted=False)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise serializers.ValidationError(
                    f"Purchase with code {value} already exists."
                )
        return value


class PurchaseDetailModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = ["item_code", "quantity", "unit_price"]

    def validate_item_code(self, value):
        try:
            Item.objects.get(code=value, is_deleted=False)
        except Item.DoesNotExist:
            raise serializers.ValidationError(f"Item with code {value} does not exist.")
        return value
