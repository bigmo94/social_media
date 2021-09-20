from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if obj == request.user:
            return True

        return False


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.username == request.data.get('receiver') or request.data.get('sender'):
            return True
        return False
