# Django
from django.contrib.auth import authenticate

# DRF
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Serializers
from cheonbaeksa.apps.users.api.serializers import UserLoginSuccessSerializer, UserLoginSerializer


# Main Section
class UserLoginViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='이메일 로그인',
                                             description="""

                                             이메일과 비밀번호를 사용하여 로그인합니다. 성공적으로 로그인하면 JWT 토큰을 반환합니다.
                                             응답에서 받은 access 토큰은 모든 보호된 API 요청의 Authorization 헤더에 Bearer prefix와 함께 추가해야 합니다.
                                             예시: Authorization: Bearer <access_token>

                                             """,
                                             request=UserLoginSerializer,
                                             response={200: UserLoginSuccessSerializer},
                                             ))
    @action(detail=False, methods=['post'], url_path='login/email')
    def email_login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('이메일, 또는 비밀번호가 잘못되었습니다.')

        if hasattr(user, 'is_email_verified') and not user.is_email_verified:
            raise AuthenticationFailed('이메일 인증이 완료되지 않았습니다.')

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=UserLoginSuccessSerializer(instance=user).data
        )
