from django.urls import path, include

from products.views import sub_categories, products_view, product_view

from . import views

app_name = 'start'

urlpatterns = [
    path('category/<int:pk>/', sub_categories, name='category'),
    path('subcategory/<int:pk>/', products_view, name='subcategory'),
    path('product/<int:pk>/', product_view, name='product'),
]