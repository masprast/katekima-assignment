from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from .models import SellHeader, SellDetail
from items.models import Item


class SellDetailSerializer(serializers.ModelSerializer):
    header_code = serializers.SlugRelatedField(
        slug_field="code", queryset=SellHeader.objects.all()
    )

    class Meta:
        model = SellDetail
        fields = ["item_code", "quantity", "header_code"]
        read_only_fields = ["header_code", "created_at", "updated_at", "is_deleted"]


class SellHeaderSerializer(serializers.ModelSerializer):
    details = SellDetailSerializer(many=True, read_only=True)
    code = serializers.CharField(max_length=5, min_length=5)

    class Meta:
        model = SellHeader
        fields = ["code", "date", "description", "details"]
        read_only_fields = ["created_at", "updated_at", "is_deleted", "details"]
        extra_kwargs = {
            "code": {"validators": [MinLengthValidator(5), MaxLengthValidator(5)]}
        }


class SellHeaderModifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=5, min_length=5)

    class Meta:
        model = SellHeader
        fields = ["code", "date", "description"]
        extra_kwargs = {
            "code": {"validators": [MinLengthValidator(5), MaxLengthValidator(5)]}
        }

    def validate_code(self, value):
        # Cek jika sell code sudah ada
        if self.instance is None:  # Create
            if SellHeader.objects.filter(code__iexact=value, is_deleted=False).exists():
                raise serializers.ValidationError(
                    f"Sell with code {value} already exists."
                )
        else:  # Update
            if (
                value.lower() != self.instance.code.lower()
                and SellHeader.objects.filter(code__iexact=value, is_deleted=False)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise serializers.ValidationError(
                    f"Sell with code {value} already exists."
                )
        return value


class SellDetailModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetail
        fields = ["item_code", "quantity"]

    def validate_item_code(self, value):
        try:
            Item.objects.get(code=value, is_deleted=False)
        except Item.DoesNotExist:
            raise serializers.ValidationError(f"Item with code {value} does not exist.")
        return value

    def validate(self, data):
        item_code = data.get("item_code")
        quantity = data.get("quantity")
        if item_code and quantity is not None and quantity <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if item_code:
            try:
                item = Item.objects.get(code=item_code, is_deleted=False)
                if item.stock < quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for item {item_code}. Available: {item.quantity}, Requested: {quantity}"
                    )
            except Item.DoesNotExist:
                pass
        return data
