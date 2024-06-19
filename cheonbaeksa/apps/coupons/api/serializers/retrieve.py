# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.coupons.models import Coupon


# Main Section
class CouponRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'discount_price', 'discount_percentage',)
