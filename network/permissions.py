from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """
    Разрешает доступ только активным staff-пользователям.
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)
