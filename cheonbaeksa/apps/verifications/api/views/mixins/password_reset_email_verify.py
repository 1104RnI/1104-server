# Settings
from rest_framework.exceptions import ValidationError

# Django
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Serializers
from cheonbaeksa.apps.users.api.serializers import UserLoginSuccessSerializer
from cheonbaeksa.apps.verifications.api.serializers import EmailVerificationUpdateSerializer

# Models
from cheonbaeksa.apps.verifications.models import EmailVerification


# Main Section
class EmailVerificationPasswordResetVerifyViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='이메일',
                                             id='비밀번호 변경 인증 이메일 검증',
                                             description='이메일로 받은 인증 코드를 검증합니다.',
                                             request=EmailVerificationUpdateSerializer,
                                             response={200: UserLoginSuccessSerializer}
                                             ))
    @action(detail=False, methods=['post'], url_path='password-reset-verification/verify',
            url_name='password_reset_email_verify')
    def password_reset_email_verify(self, request, *args, **kwargs):
        user = request.user

        # 이메일 인증이 이미 완료된 경우
        if not user.is_email_verified:
            raise ValidationError(_('회원가입이 완료된 유저가 아닙니다.'))

        serializer = EmailVerificationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            email = user.email
            code = serializer.validated_data['code']
            purpose = 'PASSWORD_RESET'

            try:
                # 가장 최근에 생성된 유효한 인증 코드를 가져옴
                email_verification = EmailVerification.objects.filter(
                    user=user,
                    email=email,
                    purpose=purpose,
                    is_verified=False,
                    expired__gt=now()
                ).latest('created')

                if email_verification.code == code:
                    email_verification.is_verified = True
                    email_verification.save(update_fields=['is_verified'])

                    return Response(
                        status=status.HTTP_200_OK,
                        code=200,
                        message=_('ok'),
                    )
                else:
                    raise ValidationError(_('잘못된 코드이거나 코드가 만료되었습니다.'))
            except EmailVerification.DoesNotExist:
                raise ValidationError(_('잘못된 코드이거나 코드가 만료되었습니다.'))
