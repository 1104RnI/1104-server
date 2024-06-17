# Django
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Serializers
from cheonbaeksa.apps.coupons.api.serializers import CouponValidateSerializer

# Utils
from cheonbaeksa.utils.api.response import Response
from cheonbaeksa.utils.decorators import swagger_decorator

# Models
from cheonbaeksa.apps.coupons.models import Coupon


# Main Section
class CouponValidateViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='쿠폰',
                                             id='쿠폰 유효성 검사',
                                             description='',
                                             request=CouponValidateSerializer,
                                             response={200: 'ok'},
                                             ))
    @action(methods=['post'], detail=False, url_path='check', url_name='coupon_check')
    def coupon_check(self, request):
        code = request.data.get('code')

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            raise ValidationError("유효하지 않은 쿠폰 코드입니다.")

        if coupon.is_used:
            raise ValidationError("이미 사용된 쿠폰 코드입니다.")

        if coupon.expired and coupon.expired < timezone.now():
            raise ValidationError("만료된 쿠폰 코드입니다.")

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
            data={'id': coupon.id}
        )
