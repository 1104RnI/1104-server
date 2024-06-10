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
class EmailVerificationSignupEmailVerifyViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='이메일 인증',
                                             id='회원가입 이메일 인증 검증',
                                             description='이메일로 받은 인증 코드를 검증합니다.',
                                             request=EmailVerificationUpdateSerializer,
                                             response={200: UserLoginSuccessSerializer, 400: 'Invalid code'}
                                             ))
    @action(detail=False, methods=['post'], url_path='signup/verify')
    def signup_email_verify(self, request, *args, **kwargs):
        user = request.user

        # 이메일 인증이 이미 완료된 경우
        if user.is_email_verified:
            raise ValidationError(_('이미 이메일 인증이 완료되었습니다.'))

        serializer = EmailVerificationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            email = user.email
            code = serializer.validated_data['code']
            purpose = 'SIGNUP'

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

                    # 유저 테이블의 is_email_verified 필드를 True로 설정
                    user.is_email_verified = True
                    user.save(update_fields=['is_email_verified'])

                    return Response(
                        status=status.HTTP_200_OK,
                        code=200,
                        message=_('ok'),
                        data=UserLoginSuccessSerializer(instance=user).data
                    )
                else:
                    raise ValidationError(_('Invalid code'))
            except EmailVerification.DoesNotExist:
                raise ValidationError(_('Invalid code'))
