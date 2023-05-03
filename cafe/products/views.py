from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CustomResponse(Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        if status is not None:
            data = {'meta': {'code': status, 'message': data}, 'data': None}
        super().__init__(data, status, template_name, headers, exception, content_type, **kwargs)

class ProductList(APIView):
    permission_classes = [IsAuthenticated]

    """
    모든 상품을 나열
    """
    def get(self, request, format=None):
        name_query = request.query_params.get('name')
        if name_query:
            products = ProductFilter(request.query_params, queryset=Product.objects.all()).qs
        else:
            products = Product.objects.all()
        
        paginator = Paginator(products, 10)
        cursor = request.query_params.get('cursor')

        if cursor is not None:
            try:
                products = paginator.page(cursor)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
        else:
            products = paginator.page(1)

        serializer = ProductSerializer(products, many=True)
        data = {
            'meta': {
                'code': 200,
                'message': "OK"
            },
            'data': {
                'count': paginator.count,
                'next_cursor': str(products.next_page_number()) if products.has_next() else None,
                'prev_cursor': str(products.previous_page_number()) if products.has_previous() else None,
                'results': serializer.data
            }
        }
        return CustomResponse(data)
    


class ProductDetail(APIView):
    permission_classes = [IsAuthenticated]
    """
    상품 상세 보기
    """
    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            if product.account != self.request.user:
                raise Http404
            return product
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        res_data = {
                    "meta": {
                        "code": 200,
                        "message": "OK"
                    },
                    "data": {
                        "products": serializer.data
                    }
                }
        return CustomResponse(res_data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            res_data = {
                    "meta": {
                        "code": 200,
                        "message": "OK"
                    },
                    "data": {
                        "products": serializer.data
                    }
                }
            return CustomResponse(res_data)
        res_data = {
                    "meta": {
                        "code": 400,
                        "message": "유효한 데이터가 아님"
                    },
                    "data": {
                        "products": None
                    }
                }
        return CustomResponse(res_data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return CustomResponse(status=status.HTTP_204_NO_CONTENT)


class ProductCreate(APIView):
    permission_classes = [IsAuthenticated]
    """
    상품 생성
    """

    def post(self, request, format=None):
        data = request.data.copy()
        data['account'] = request.user.id
        serializer = ProductSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            res_data = {
                    "meta": {
                        "code": 201,
                        "message": "CREATE"
                    },
                    "data": {
                        "products": serializer.data
                    }
                }
            return CustomResponse(res_data, status=status.HTTP_201_CREATED)
        res_data = {
                    "meta": {
                        "code": 400,
                        "message": "상품 생성 실패힙니다."
                    },
                    "data": {
                        "products": None
                    }
                }
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductUpdate(APIView):
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PATCH']
    """
    상품 업데이트
    """
    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            if product.account != self.request.user:
                raise Http404
            return product
        except Product.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res_data = {
                    "meta": {
                        "code": 200,
                        "message": "OK"
                    },
                    "data": {
                        "products": serializer.data
                    }
                }
            return CustomResponse(res_data)
        res_data = {
                    "meta": {
                        "code": 400,
                        "message": "유효한 데이터가 아님"
                    },
                    "data": {
                        "products": None
                    }
                }
        return CustomResponse(res_data, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDelete(APIView):
    permission_classes = [IsAuthenticated]
    """
    상품 제거
    """

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        if not request.user == product.account:
            raise PermissionDenied
        product.delete()
        return CustomResponse(status=status.HTTP_204_NO_CONTENT)
