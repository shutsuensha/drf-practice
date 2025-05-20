from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактировать объявления только их владельцу.
    Чтение — всем.
    """

    def has_object_permission(self, request, view, obj):
        # безопасные методы — разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # на запись — только владелец объявления
        return obj.user == request.user
