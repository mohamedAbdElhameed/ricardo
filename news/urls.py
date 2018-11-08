from django.urls import path, include

from news.apis.views import PostListView
from news.views import news_view
from . import views

app_name = 'news'

urlpatterns = [
   path('api/postlist/', PostListView.as_view(), name='ads'),
   path('', news_view, name='posts')
]
