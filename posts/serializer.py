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
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ('body', 'writer', 'pub_time', 'post', 'id')

        extra_kwargs = {
            'post': {'read_only': True},
        }

    def get_writer(self, obj):
        return obj.writer.username

    def create(self, validated_data):
        body = validated_data.get('body')
        post = Post.objects.filter(id=validated_data.get('id'))[0]
        instance = Comment.objects.create(writer=self.context['request'].user, post=post, body=body)
        return instance


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PostLike
        fields = ('post', 'liked_by', 'id')
        extra_kwargs = {
            'post': {'read_only': True},
            'liked_by': {'read_only': True},
        }

    def create(self, validated_data):
        post = Post.objects.filter(id=validated_data.get('id'))[0]
        instance = PostLike.objects.create(liked_by=self.context['request'].user, post=post)
        return instance
