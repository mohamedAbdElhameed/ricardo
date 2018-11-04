from rest_framework import serializers

from news.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['image', 'title', 'details', 'modified_at']