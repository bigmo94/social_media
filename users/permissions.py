from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response


class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.profile != request.profile:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return True
