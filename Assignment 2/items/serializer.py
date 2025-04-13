from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        max_length=5,
        min_length=5,
        validators=[MinLengthValidator(5), MaxLengthValidator(5)],
    )

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


class ItemModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["code", "name", "unit", "description"]
