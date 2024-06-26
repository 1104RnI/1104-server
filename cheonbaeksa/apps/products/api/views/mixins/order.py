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
from cheonbaeksa.apps.orders.api.serializers import OrderCreateSerializer, OrderRetrieveSerializer

# Models
from cheonbaeksa.apps.orders.models import Order
from cheonbaeksa.apps.coupons.models import Coupon


# Main Section
class ProductOrderViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='상품',
                                             id='상품 주문',
                                             description='상품을 주문합니다. 적용할 쿠폰 코드가 없으면 빈 객체를 보냅니다.',
                                             request=OrderCreateSerializer,
                                             response={201: OrderRetrieveSerializer},
                                             ))
    @action(methods=['post'], detail=True, url_path='order', url_name='product_order')
    def product_order(self, request, pk=None):
        product = self.get_object()
        user = request.user
        coupon_code = request.data.get('coupon_code')
        coupon_id = None

        if coupon_code:
            coupon = Coupon.validate_code(coupon_code)
            coupon.is_used = True
            coupon_id = coupon.id
            coupon.save()
            total_price = coupon.get_discounted_price(original_price=product.price)
        else:
            total_price = product.price

        instance = Order.objects.create(user_id=user.id, product_id=product.id, coupon_id=coupon_id,
                                        total_price=total_price,
                                        status='PENDING')

        return Response(
            status=status.HTTP_201_CREATED,
            code=201,
            message=_('ok'),
            data=OrderRetrieveSerializer(instance=instance).data
        )
