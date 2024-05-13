from rest_framework.permissions import BasePermission
from users.models import TokenBlacklist


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1]
        is_allowed_user = True
        try:
            is_blackListed = TokenBlacklist.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except TokenBlacklist.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
