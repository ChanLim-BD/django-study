from rest_framework import serializers
from .models import Product
from datetime import date

class ProductSerializer(serializers.ModelSerializer):
    account = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'category': {'required': False},
            'barcode': {'required': False},
            'size': {'required': False},
            'name': {'required': False},
        }

    def validate(self, data):
        if data.get('expiration_date') is None:
            data['expiration_date'] = date.max # expiration_date가 null일 경우 max로 변환
        if data.get('description') is None:
            data['description'] = ''  # description이 null일 경우 빈 문자열로 변환
        if data.get('category') is None:
            data['category'] = ''  # category가 null일 경우 빈 문자열로 변환
        if data.get('barcode') is None:
            data['barcode'] = ''  # barcode가 null일 경우 빈 문자열로 변환
        if data.get('size') is None:
            data['size'] = ''  # size가 null일 경우 빈 문자열로 변환
        return data

