from django.urls import path, include

from news.apis.views import PostListView
from . import views

app_name = 'start'

urlpatterns = [
   path('', views.index, name='index'),
]
