# Django
from django_filters.rest_framework import DjangoFilterBackend

# Bases
from cheonbaeksa.bases.api.viewsets import GenericViewSet

# Mixins
from cheonbaeksa.apps.coupons.api.views.mixins import CouponValidateViewMixin

# Permissions
from cheonbaeksa.apps.coupons.api.views.permissions import CouponPermission

# Models
from cheonbaeksa.apps.coupons.models import Coupon


# Main Section
class CouponsViewSet(CouponValidateViewMixin,
                     GenericViewSet):
    queryset = Coupon.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (CouponPermission,)
