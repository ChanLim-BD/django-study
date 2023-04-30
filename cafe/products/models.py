from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)                                                     # 상품 이름
    description = models.TextField(null=True)                                                   # 상품 설명
    category = models.CharField(max_length=255)                                                 # 카테고리
    barcode = models.CharField(max_length=255)                                                  # 바코드
    price = models.IntegerField(default=0)                                                      # 가격
    cost = models.IntegerField(default=0)                                                       # 비용
    expiration_date = models.DateField(null=True)                                               # 유통기한
    size = models.CharField(choices=[('small', 'Small'), ('large', 'Large')], max_length=10)    # 상품 크기
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)                   # 계정

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-id"]

