from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from posts.models import Post, Comment, PostLike
from users.serializer import ProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['body', 'image', 'user']


class CommentSerializer(serializers.ModelSerializer):
    writer = SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ('body', 'writer', 'pub_time', 'post')

    def get_writer(self, obj):
        return obj.writer.username


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PostLike
        fields = ('post', 'liked_by', 'id')
