from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=5, min_length=5)

    class Meta:
        model = Item
        # Field yang ditampilkan untuk API
        fields = ["code", "name", "unit", "description", "stock", "balance"]
        read_only_fields = [
            "stock",
            "balance",
            "created_at",
            "updated_at",
            "is_deleted",
        ]
        extra_kwargs = {
            "code": {"validators": [MinLengthValidator(5), MaxLengthValidator(5)]}
        }


class ItemModifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=5, min_length=5)

    class Meta:
        model = Item
        fields = ["code", "name", "unit", "description"]
        extra_kwargs = {
            "code": {"validators": [MinLengthValidator(5), MaxLengthValidator(5)]}
        }

    def validate_code(self, value):
        # Cek jika item code sudah ada
        if self.instance is None:  # Create
            if Item.objects.filter(code__iexact=value, is_deleted=False).exists():
                raise serializers.ValidationError(
                    f"Item with code {value} already exists."
                )
        else:  # Update
            if (
                value.lower() != self.instance.code.lower()
                and Item.objects.filter(code__iexact=value, is_deleted=False)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise serializers.ValidationError(
                    f"Item with code {value} already exists."
                )
        return value
