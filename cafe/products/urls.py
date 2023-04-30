from django.urls import path
from .views import ProductList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete

urlpatterns = [
    path('', ProductList.as_view(), name='product-list'),
    path('create/', ProductCreate.as_view(), name='product-create'),
    path('<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
]
