from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """
    Пускаем в API только активных сотрудников.
    """

    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.is_active and u.is_staff)
