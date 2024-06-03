# Django
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Serializers
from cheonbaeksa.apps.users.api.serializers import UserEmailCheckSerializer

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator


# Main Section
class UserValidateViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='이메일 유효성 검사',
                                             description='',
                                             request=UserEmailCheckSerializer,
                                             response={200: 'ok'},
                                             ))
    @action(methods=['post'], detail=False, url_path='email/check', url_name='email_check')
    def email_check(self, request):
        serializer = UserEmailCheckSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('ok'),
            )
