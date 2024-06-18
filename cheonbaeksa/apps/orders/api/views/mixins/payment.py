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
from cheonbaeksa.apps.payments.api.serializers import PaymentCreateSerializer


# Main Section
class OrderPaymentViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='주문',
                                             id='주문 결제',
                                             description='주문한 상품을 결제합니다.',
                                             request=PaymentCreateSerializer,
                                             response={201: 'ok'},
                                             ))
    @action(methods=['post'], detail=True, url_path='order', url_name='product_order')
    def order_payment(self, request, pk=None):
        order = self.get_object()
        user = request.user
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=user.id, order_id=order.id, total_price=order.total_price,
                            order_number=order.number)
            return Response(
                status=status.HTTP_201_CREATED,
                code=201,
                message=_('ok'),
            )
