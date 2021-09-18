from django.urls import path
from .views import PostListAPIView, PostDetailAPIView, PostRetrieveUpdateDestroyAPIView

app_name = "posts"

urlpatterns = [
    path('create/', PostListAPIView.as_view(), name='post_create'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('edit/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post_edit')
]
