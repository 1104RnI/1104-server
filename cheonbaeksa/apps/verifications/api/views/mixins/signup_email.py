# Settings
from config.settings.base import EMAIL_HOST_USER

# Django
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema, no_body

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Models
from cheonbaeksa.apps.verifications.models import EmailVerification


# Main Section
class EmailVerificationSignupEmailViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='이메일 인증',
                                             id='회원가입 이메일 인증 생성',
                                             description="""

                                             회원가입을 위한 이메일 인증 코드를 생성하여 사용자에게 전송합니다.
                                             요청 시 헤더에 유효한 토큰을 포함해야 합니다. 이메일 인증의 유효시간은 객체 생성 후 5분 이내입니다.
                                             인증 코드는 1분 후에 다시 생성할 수 있습니다.

                                             """,
                                             request=no_body,
                                             response={201: 'ok'}
                                             ))
    @action(detail=False, methods=['post'], url_path='signup')
    def signup_email(self, request, *args, **kwargs):
        user = request.user

        # 이메일 인증이 이미 완료된 경우
        if user.is_email_verified:
            raise ValidationError(_('이미 이메일 인증이 완료되었습니다.'))

        email = user.email
        purpose = 'SIGNUP'

        email_verification = EmailVerification.create_or_get_valid_code(user=user, email=email, purpose=purpose)

        # 이메일 전송 로직
        subject = '1104 R&I 회원가입 이메일 인증 코드'
        html_message = render_to_string('email_template.html',
                                        {'user': user, 'verification_code': email_verification.code})
        plain_message = strip_tags(html_message)
        from_email = EMAIL_HOST_USER
        to_email = email

        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        return Response(
            status=status.HTTP_201_CREATED,
            code=201,
            message=_('ok'),
        )
