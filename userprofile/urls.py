from django.urls import path, include

from products.views import sub_categories, products_view, product_view
from userprofile.views import sellers_view, vendor_view
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('sellers/', sellers_view, name='sellers'),
    path('vendor/<int:pk>/', vendor_view, name='vendor'),
]