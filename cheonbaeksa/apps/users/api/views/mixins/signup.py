# Django
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.utils import timezone

# DRF
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Serializers
from cheonbaeksa.apps.users.api.serializers import UserSignupSerializer, UserLoginSuccessSerializer

# Models
from cheonbaeksa.apps.users.models import User


# Main Section
class UserSignupViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='회원가입',
                                             description='',
                                             request=UserSignupSerializer,
                                             response={200: UserLoginSuccessSerializer},
                                             ))
    @action(detail=False, methods=['post'])
    def signup(self, request):
        email = request.data.get('email')

        # Validate Email
        self.validate_email_re_signup(email)

        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Email Signup
            user = User.objects.create_user(**request.data)
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('ok'),
                data=UserLoginSuccessSerializer(instance=user).data
            )

    def validate_email_re_signup(self, email):
        user_withdraw = User.objects.filter(email=email, is_deleted=True).first()
        if user_withdraw:
            current_time = now()
            re_signup_deadline = user_withdraw.deleted + timezone.timedelta(days=30)
            if current_time < re_signup_deadline:
                raise ValidationError('탈퇴 후 30일이 지나지 않아 재가입이 불가능합니다.')
