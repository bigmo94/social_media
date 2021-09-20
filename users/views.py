from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

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
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
