from rest_framework import generics

from news.apis.serializers import PostSerializer
from news.models import Post


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created_at')
    permission_classes = ()

