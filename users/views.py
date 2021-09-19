from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Profile, Message, Follow
from .permissions import IsProfileOwner
from .serializer import (ProfileSerializer,
                         ProfileRegisterSerializer,
                         ProfileLoginSerializer,
                         ProfileVerifySerializer, MessageSerializer, FollowSerializer)


class ProfileRegisterAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileRegisterSerializer


class ProfileVerifyAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileVerifySerializer


class ProfileLoginAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileLoginSerializer


class ProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwner, ]
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


def message_view(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
