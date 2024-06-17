# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.coupons.models import Coupon


# Main Section
class CouponValidateSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('code',)

    def validate_code(self, value):
        return Coupon.validate_code(value)
