from rest_framework import generics
from rest_framework.permissions import AllowAny
from .permissions import IsOwnerOrReadOnly

from .models import Post, Comment, PostLike
from .serializer import PostSerializer, CommentSerializer, PostLikeSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        Post.objects.create(user=self.request.user, **serializer.validated_data)


class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class LikeListCreateAPIView(generics.ListCreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def perform_create(self, serializer):
        post_id = Post.objects.filter(pk=serializer.validated_data.get('id'))
        PostLike.objects.create(user=self.request.user, post__id=post_id)
