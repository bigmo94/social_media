from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Post
        fields = ['id', 'body', 'image', 'user']
