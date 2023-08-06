from rest_framework.permissions import BasePermission, AllowAny


__all__ = [
    "UserHasAccess",
]


class UserHasAccess(BasePermission):
    def user_has_access(self, user) -> bool:
        return True

    def has_permission(self, request, view):
        if getattr(view, "ignore_has_access", False) or (
            AllowAny in view.permission_classes
        ):
            return True
        return bool(request.user) and self.user_has_access(user=request.user)
