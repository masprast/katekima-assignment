from django.db import models
from items.models import Item
from stock_warehouse.models import BaseModel


# Create your models here.
class PurchaseHeader(BaseModel):
    code = models.CharField(unique=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Purchase {self.code} - {self.date}"


class PurchaseDetail(models.Model):
    header_code = models.ForeignKey(
        PurchaseHeader,
        related_name="details",
        on_delete=models.CASCADE,
    )
    item_code = models.ForeignKey(Item, to_field="code", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()

    def __str__(self):
        return f"{self.item_code} X{self.quantity} @{self.unit_price}"
