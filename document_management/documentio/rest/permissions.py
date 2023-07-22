from rest_framework.permissions import BasePermission

from ..choices import UserRole


class IsAdmin(BasePermission):
    message = "User is not Admin"

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated and user.role != UserRole.ADMIN:
            return False
        return True
