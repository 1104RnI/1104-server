# DRF
from rest_framework.permissions import BasePermission


# Main Section
class UserPermission(BasePermission):

    def has_permission(self, request, view):
        # 로그인하지 않은 사용자는 접근을 제한합니다.
        if view.action in [
            'me', 'update_password', 'update_trading_view_username',
        ] and request.user.is_anonymous:
            return False

        # 이메일 인증이 완료되지 않은 사용자는 접근을 제한합니다.
        if request.user.is_authenticated and not request.user.is_email_verified:
            return False

        return True
