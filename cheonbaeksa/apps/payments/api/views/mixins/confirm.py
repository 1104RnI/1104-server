# Django
from django.db import transaction
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Serializer
from cheonbaeksa.apps.payments.api.serializers import PaymentConfirmSerializer


# Main Section
class PaymentConfirmViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='결제',
                                             id='결제 승인',
                                             description='',
                                             request=PaymentConfirmSerializer,
                                             response={200: 'ok'}))
    @action(detail=False, methods=['POST'], url_path='confirm', url_name='payment_confirm')
    @transaction.atomic()
    def payment_confirm(self, request):
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok')
        )
