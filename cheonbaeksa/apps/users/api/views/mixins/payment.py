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

# Serializers
from cheonbaeksa.apps.payments.api.serializers import PaymentListSerializer

# Models
from cheonbaeksa.apps.payments.models import Payment


# Main Section
class UserPaymentViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='결제 리스트 조회',
                                             description='내가 결제한 내역을 조회합니다.',
                                             response={200: PaymentListSerializer},
                                             ))
    @action(detail=False, methods=['get'], url_path='me/payments')
    def me_payment(self, request):
        user = request.user
        payments = Payment.objects.filter(user_id=user.id)
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
            data=PaymentListSerializer(instance=payments, many=True).data
        )
