# Django
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.exceptions import ValidationError

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from cheonbaeksa.bases.api.viewsets import GenericViewSet
from cheonbaeksa.bases.api import mixins

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Serializers
from cheonbaeksa.apps.sends.api.serializers import EmailSendCreateSerializer

# Models
from cheonbaeksa.apps.sends.models import EmailSend


# Main Section
class EmailSendsViewSet(mixins.CreateModelMixin,
                        GenericViewSet):
    serializers = {
        'default': EmailSendCreateSerializer,
    }
    queryset = EmailSend.available.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(**swagger_decorator(tag='이메일',
                                             id='이메일 전송',
                                             description='',
                                             request=EmailSendCreateSerializer,
                                             response={201: 'ok'}
                                             ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_send = serializer.save()

        # 이메일 전송 로직
        subject = email_send.title
        plain_message = email_send.content
        from_email = email_send.from_email
        to_email = email_send.to_email

        try:
            send_mail(subject, plain_message, from_email, [to_email])
            email_send.status = 'SENT'
        except Exception as e:
            email_send.status = 'FAILED'
            raise ValidationError(_('이메일 전송에 실패했습니다.'))

        email_send.save()

        return Response(
            status=status.HTTP_201_CREATED,
            code=201,
            message=_('ok'),
            data=EmailSendCreateSerializer(instance=email_send).data
        )
