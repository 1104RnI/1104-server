# Django
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator
from cheonbaeksa.utils.portone import get_portone_access_token

# Modules
from cheonbaeksa.modules.gateways.portone import gateway as gateway_portone

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
    @action(methods=['post'], detail=True, url_path='payment', url_name='order_payment')
    def order_payment(self, request, pk=None):
        order = self.get_object()
        user = request.user
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(user_id=user.id, order_id=order.id, total_price=order.total_price,
                                       order_number=order.number)

            # PG Payment 요청 전에, Payment 위,변조를 막기 위한 사전 검증이 필요함.
            # GET PortOne Access Token
            portone_access_token = get_portone_access_token()

            # API GATEWAY
            response = gateway_portone.check_payment(portone_access_token=portone_access_token,
                                                     order_number=instance.order_number,
                                                     total_price=instance.total_price)
            print('response : ', response)

            if response['code'] != 0:
                raise AuthenticationFailed(response['message'])

            return Response(
                status=status.HTTP_201_CREATED,
                code=201,
                message=_('ok'),
            )
