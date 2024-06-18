# Python
from datetime import timedelta

# Django
from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, NotFound

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator
from cheonbaeksa.utils.portone import get_portone_access_token

# Modules
from cheonbaeksa.modules.gateways.portone import gateway as gateway_portone

# Serializer
from cheonbaeksa.apps.payments.api.serializers import PaymentConfirmSerializer

# Model
from cheonbaeksa.apps.payments.models import Payment


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
        # GET PortOne Access Token
        portone_access_token = get_portone_access_token()

        # API Gateway
        response = gateway_portone.get_payment(portone_access_token=portone_access_token, **request.data)
        print('response : ', response)

        if response['code'] != 0:
            raise AuthenticationFailed(response['message'])

        # TODO: 결제 이후 로직 구현하기
        # # Payment 유효성 검증을 위한 변수 선언
        # pg_data = response['response']
        #
        # # 필요 데이터
        # imp_uid = pg_data['imp_uid']
        # payment_uuid = pg_data['merchant_uid']
        # total_price = pg_data['amount']
        #
        # payment = Payment.available.filter(uuid=payment_uuid).first()
        # if not payment:
        #     raise NotFound('payment를 찾을 수 없습니다.')
        #
        # if payment.total_price != total_price:
        #     raise ValueError('결제 금액이 상이합니다.')
        #
        # # Payment 상태에 따른 비지니스 로직
        # payment_status = pg_data['status']
        # if payment_status == 'paid':
        #     message = _('ok')
        # else:
        #     message = _('위조된 결제')
        #
        # # Payment 데이터 동기화
        # payment.imp_uid = imp_uid
        # payment.status = payment_status.upper()
        # payment.pg_data = pg_data
        # payment.save()

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok'
        )
