from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment
from .serializer import PostSerializer, CommentSerializer, PostLikeSerializer


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class LikeListCreateAPIView(APIView):

    def get(self, request, pk):
        post = Post.objects.filter(pk=pk)
        like_count = post.likepost.count()
        serializer = PostLikeSerializer(like_count, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        liked_by = request.user
        post = Post.objects.filter(pk=pk)
        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post, liked_by)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
