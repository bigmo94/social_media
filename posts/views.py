from rest_framework import generics

from .models import Post
from .serializer import PostSerializer


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)
