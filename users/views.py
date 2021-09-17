from django.shortcuts import render

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Profile
from .permissions import IsProfileOwner
from .serializer import (ProfileSerializer,
                         ProfileRegisterSerializer,
                         ProfileLoginSerializer,
                         ProfileVerifySerializer)


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
