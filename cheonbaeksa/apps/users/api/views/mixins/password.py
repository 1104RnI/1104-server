# Django
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator
from cheonbaeksa.utils.validators import validator_password

# Serializers
from cheonbaeksa.apps.users.api.serializers import UserLoginSuccessSerializer, UserPasswordUpdateSerializer

# Models
from cheonbaeksa.apps.users.models import User
from cheonbaeksa.apps.tokens.models import PasswordResetToken


# Main Section
class UserPasswordViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='비밀번호 수정',
                                             description='',
                                             request=UserPasswordUpdateSerializer,
                                             response={200: UserLoginSuccessSerializer},
                                             method='patch'
                                             ))
    @action(detail=False, methods=['patch'], url_path='password')
    def update_password(self, request):
        password = request.data['password']
        password_reset_token = request.data['password_reset_token']
        user = request.user

        # 비밀번호 유효성 검사
        validator_password(password)

        # 토큰 검증
        user_id = PasswordResetToken.verify_reset_token(password_reset_token)
        get_object_or_404(User, id=user_id)

        if user.id != user_id:
            raise ValidationError('Invalid token')

        user.set_password(password)
        user.save(update_fields=['password'])

        # 토큰 삭제
        PasswordResetToken.objects.filter(token=password_reset_token).soft_delete()

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
            data=UserLoginSuccessSerializer(instance=request.user).data
        )
