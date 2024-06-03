# Django
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator
from cheonbaeksa.utils.validators import validator_password

# Serializers
from cheonbaeksa.apps.users.api.serializers import UserMeSerializer, UserUpdateSerializer, UserLoginSuccessSerializer


# Main Section
class UserMeViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='내 정보 조회',
                                             description='',
                                             response={200: UserMeSerializer},
                                             method='get'
                                             ))
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='내 정보 수정',
                                             description='',
                                             request=UserUpdateSerializer,
                                             response={200: UserLoginSuccessSerializer},
                                             method='patch'
                                             ))
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('ok'),
                data=UserMeSerializer(instance=request.user).data
            )
        elif request.method == 'PATCH':
            password = request.data['password']

            # 비밀번호 유효성 검사
            validator_password(password)

            request.user.set_password(password)
            request.user.save(update_fields=['password'])
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('ok'),
                data=UserLoginSuccessSerializer(instance=request.user).data
            )
