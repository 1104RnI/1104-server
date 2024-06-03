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
                                             description='',
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

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=UserLoginSuccessSerializer(instance=user).data
        )
