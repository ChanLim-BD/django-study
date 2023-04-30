from django.db import models
from accounts.models import Account

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    price = models.IntegerField()
    cost = models.IntegerField()
    expiration_date = models.DateField()
    size = models.CharField(choices=[('small', 'Small'), ('large', 'Large')], max_length=10)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-id"]
