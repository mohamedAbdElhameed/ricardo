from django.urls import path, include

from news.apis.views import PostListView
from . import views

app_name = 'news'

urlpatterns = [
   path('api/postlist/', PostListView.as_view(), name='ads'),
]
