from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics, permissions, status


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()
        name_query = self.request.query_params.get('name')
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        return queryset


class ProductDetail(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class ProductCreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)


class ProductUpdate(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.account == request.user

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsProductOwner]


