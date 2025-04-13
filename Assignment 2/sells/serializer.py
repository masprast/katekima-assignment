from email import header
import re
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

    class Meta:
        model = SellHeader
        fields = ["code", "date", "description", "details"]
        read_only_fields = ["created_at", "updated_at", "is_deleted", "details"]

    # def create(self, validated_data):
    #     details_data = validated_data.pop("details", [])
    #     header = SellHeader.objects.create(**validated_data)
    #     for detail_data in details_data:
    #         SellDetail.objects.create(header_code=header, **detail_data)
    #     return header

    # def update(self, instance, validated_data):
    #     details_data = validated_data.pop("details", [])
    #     instance.code = validated_data.get("code", instance.code)
    #     instance.date = validated_data.get("date", instance.date)
    #     instance.description = validated_data.get("description", instance.description)
    #     instance.save()

    #     instance.details.all().delete()
    #     for detail_data in details_data:
    #         SellDetail.objects.create(header_code=instance, **detail_data)
    #     return instance


class SellHeaderModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = SellHeader
        fields = ["code", "date", "description"]


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
