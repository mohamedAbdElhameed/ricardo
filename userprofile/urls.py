from django.urls import path, include

from products.views import sub_categories, products_view, product_view
from userprofile.views import sellers_view, vendor_view, we_view, contact_view

from userprofile.apis.views import SellerDetailView
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('api/seller/<int:pk>/', SellerDetailView.as_view(), name='seller_endpoint_detail'),
    path('sellers/', sellers_view, name='sellers'),
    path('vendor/<int:pk>/', vendor_view, name='vendor'),
    path('we/', we_view, name='we'),
    path('contact/', contact_view, name='contact'),
]