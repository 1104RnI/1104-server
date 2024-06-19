# Django
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Serializers
from cheonbaeksa.apps.coupons.api.serializers import CouponValidateSerializer, CouponRetrieveSerializer

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Models
from cheonbaeksa.apps.coupons.models import Coupon


# Main Section
class CouponValidateViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='쿠폰',
                                             id='쿠폰 유효성 검사',
                                             description='입력된 쿠폰 코드를 유효성 검사합니다. 유효한 쿠폰 코드인 경우, 쿠폰의 ID를 반환합니다.',
                                             request=CouponValidateSerializer,
                                             response={200: CouponRetrieveSerializer},
                                             ))
    @action(methods=['post'], detail=False, url_path='check', url_name='coupon_check')
    def coupon_check(self, request):
        code = request.data.get('code')
        instance = Coupon.validate_code(code)
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
            data=CouponRetrieveSerializer(instance=instance).data
        )
