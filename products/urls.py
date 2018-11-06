from django.urls import path, include

from products.views import sub_categories
from . import views

app_name = 'start'

urlpatterns = [
    path('category/<int:pk>/', sub_categories, name='category')
]