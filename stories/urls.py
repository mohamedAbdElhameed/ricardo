from django.urls import path, include

from products.views import sub_categories, products_view, product_view
from stories.views import masters_view, tales_view
from . import views

app_name = 'stories'

urlpatterns = [
    path('masters/', masters_view, name='masters'),
    path('tales/', tales_view, name='tales'),
]
