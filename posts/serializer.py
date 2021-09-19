from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from posts.models import Post, Comment, PostLike


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Post
        fields = ['id', 'body', 'image', 'user']


class CommentSerializer(serializers.ModelSerializer):
    writer = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('body', 'writer', 'pub_time', 'post')

    def get_writer(self, obj):
        return obj.writer.username


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('post', 'liked_by')
