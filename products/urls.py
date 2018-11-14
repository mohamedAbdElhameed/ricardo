from django.urls import path, include

from products.views import sub_categories, products_view, product_view
from rest_framework.routers import DefaultRouter

from products.apis.views import ProductViewSet, ProductDetailViewSet, SubCategoryList, ProductsInSubCategoryList, \
    CartView
from . import views

app_name = 'products'


urlpatterns = [
    path('api/productlist/', ProductViewSet.as_view({'get': 'list'})),
    path('api/addtocart/', CartView.as_view(), name='cart'),
    path('api/product/<int:pk>/', ProductDetailViewSet.as_view()),
    path('api/subcategorylist/', SubCategoryList.as_view()),
    path('api/subcategoryproducts/<int:pk>/', ProductsInSubCategoryList.as_view()),
    path('category/<int:pk>/', sub_categories, name='category'),
    path('subcategory/<int:pk>/', products_view, name='subcategory'),
    path('product/<int:pk>/', product_view, name='product'),
]