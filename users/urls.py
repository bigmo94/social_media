from django.urls import path

from .views import (ProfileRegisterAPIView,
                    ProfileLoginAPIView,
                    ProfileVerifyAPIView,
                    ProfileRetrieveUpdateDestroyAPIView,
                    MessageListCreateAPIView,
                    FollowCreateListAPIView, )

app_name = 'users'

urlpatterns = [
    path('register/', ProfileRegisterAPIView.as_view(), name='register'),
    path('verify/', ProfileVerifyAPIView.as_view(), name='verify'),
    path('login/', ProfileLoginAPIView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateDestroyAPIView.as_view(), name='profile'),
    path('message/', MessageListCreateAPIView.as_view(), name='message'),
    path('follow/', FollowCreateListAPIView.as_view())

]
