from django.urls import path
from .views import (PostListCreateAPIView,
                    PostRetrieveAPIView,
                    PostRetrieveUpdateDestroyAPIView,
                    CommentListAPIView,
                    CommentRetrieveUpdateDestroyAPIView,
                    LikeListCreateAPIView, )

app_name = "posts"

urlpatterns = [
    path('create/', PostListCreateAPIView.as_view(), name='post_create'),
    path('<int:pk>/', PostRetrieveAPIView.as_view(), name='post_detail'),
    path('edit/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post_edit'),
    path('comments/', CommentListAPIView.as_view(), name='post_comments'),
    path('comments/edit/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment_edit'),
    path('<int:pk>/like/', LikeListCreateAPIView.as_view(), name='post_likes'),

]
