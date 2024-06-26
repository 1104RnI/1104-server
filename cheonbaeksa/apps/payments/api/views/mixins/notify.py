# Settings
from config.settings.base import EMAIL_HOST_USER

# Django
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

# DRF
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

# Third Party
from drf_yasg.utils import swagger_auto_schema, no_body

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Serializers
from cheonbaeksa.apps.sends.api.serializers import EmailSendRetrieveSerializer

# Models
from cheonbaeksa.apps.products.models import Product
from cheonbaeksa.apps.sends.models import EmailSend
from cheonbaeksa.apps.orders.models import Order


# Main Section
class PaymentNotifyViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='결제',
                                             id='결제 완료 알림',
                                             description="""
                                             유저가 특정 상품을 결제하면, 관리자에게 결제 내역을 이메일로 전송하는 API입니다.
                                             성공 시 status=SENT, 실패 시 status=FAILED 반환됩니다.
                                             """,
                                             request=no_body,
                                             response={201: EmailSendRetrieveSerializer}
                                             ))
    @action(detail=True, methods=['post'], url_path='notify', url_name='payment_notify')
    def payment_notify(self, request, pk=None):
        payment = self.get_object()
        user = request.user

        order = get_object_or_404(Order, id=payment.order_id)
        product = get_object_or_404(Product, id=order.product_id)

        title = f'[결제완료] {product.title} | {user.id}, {user.email}'

        # 이메일 전송 로직
        subject = title
        plain_message = title
        from_email = EMAIL_HOST_USER
        to_email = EMAIL_HOST_USER

        try:
            send_mail(subject, plain_message, from_email, [to_email])
            email_send_status = 'SENT'
        except Exception as e:
            email_send_status = 'FAILED'
            raise ValidationError(_('이메일 전송에 실패했습니다.'))

        instance = EmailSend.objects.create(title=title,
                                            content=title,
                                            from_email=EMAIL_HOST_USER,
                                            to_email=EMAIL_HOST_USER,
                                            status=email_send_status,
                                            purpose='PAYMENT_NOTIFY'
                                            )
        return Response(
            status=status.HTTP_201_CREATED,
            code=201,
            message=_('ok'),
            data=EmailSendRetrieveSerializer(instance=instance).data
        )
