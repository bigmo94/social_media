from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from .models import Profile, Message, Follow
from .permissions import IsOwnerOrReadOnly, IsOwner
from .serializer import (ProfileSerializer,
                         ProfileRegisterSerializer,
                         ProfileLoginSerializer,
                         ProfileVerifySerializer, MessageSerializer, FollowSerializer)


class ProfileRegisterAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileRegisterSerializer
    permission_classes = [AllowAny, ]


class ProfileVerifyAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileVerifySerializer
    permission_classes = [AllowAny, ]


class ProfileLoginAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileLoginSerializer
    permission_classes = [AllowAny, ]


class ProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsOwner, ]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)


class FollowCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def perform_create(self, serializer):
        following = Profile.objects.filter(username=serializer.validated_data.get('follower'))[0]
        instance = Follow.objects.create(follower=self.request.user, following=following)
        return instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {'username': instance.following.username}
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class UnFollowDestroyAPIView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get_object(self):
        return Follow.objects.filter(follower=self.request.user, following__username=self.request.data.get('follower')).first()
