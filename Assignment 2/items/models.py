from django.db import models
from stock_warehouse.models import BaseModel


# Create your models here.
class Item(BaseModel):
    code = models.CharField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit = models.CharField(max_length=10)
    stock = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.code}"
