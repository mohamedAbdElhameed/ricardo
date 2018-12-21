from django.urls import path, include
from products.views import sub_categories, products_view, product_view, cart_view, delete_cart_element, add_to_cart, \
    total_price_and_items, payment_confirmation, order_view
from rest_framework.routers import DefaultRouter
from products.apis.views import *
from . import views

app_name = 'products'

urlpatterns = [
    path('api/productlist/', ProductViewSet.as_view({'get': 'list'})),
    path('api/addtocart/', CartView.as_view(), name='cart'),
    path('api/cartlist/', CartListView.as_view(), name='cat_list'),
    path('api/product/<int:pk>/', ProductDetailViewSet.as_view()),
    path('api/subcategorylist/', SubCategoryList.as_view()),
    path('api/subcategoryproducts/<int:pk>/', ProductsInSubCategoryList.as_view()),
    path('api/categories/', CategoriesView.as_view()),
    path('api/subcatincat/<int:pk>/', SubCatInCat.as_view()),
    path('api/orders/', OrderView.as_view()),
    path('category/<int:pk>/', sub_categories, name='category'),
    path('subcategory/<int:pk>/', products_view, name='subcategory'),
    path('product/<int:pk>/', product_view, name='product'),
    path('cart/', cart_view, name='cart'),
    path('cart/delete/<int:pk>/', delete_cart_element, name='delete_cart_element'),
    path('cart/add/<int:product>/<int:quantity>/', add_to_cart, name='add_to_cart'),
    path('cart/total/', total_price_and_items, name='total_price'),
    path('payment_confirmation/', payment_confirmation, name='payment_confirmation'),
    path('orders/', order_view, name='orders')
]
