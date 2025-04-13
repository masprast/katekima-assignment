from django.db import models
from items.models import Item
from stock_warehouse.models import BaseModel
from django.core.validators import MaxLengthValidator, MinLengthValidator


# Create your models here.
class SellHeader(BaseModel):
    code = models.CharField(
        max_length=5,
        unique=True,
        validators=[MaxLengthValidator(5), MinLengthValidator(5)],
    )
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.code}/{self.date}"


class SellDetail(models.Model):
    header_code = models.ForeignKey(
        SellHeader,
        related_name="details",
        on_delete=models.CASCADE,
    )
    item_code = models.ForeignKey(Item, to_field="code", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.header_code} - {self.item_code}"
