# DRF
from rest_framework.permissions import BasePermission


# Main Section
class OrderPermission(BasePermission):

    def has_permission(self, request, view):
        # 로그인하지 않은 사용자는 접근을 제한합니다.
        if view.action in [
            'order_payment',
        ] and request.user.is_anonymous:
            return False

        return True
