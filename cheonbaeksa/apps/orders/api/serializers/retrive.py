# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.orders.models import Order


# Main Section
class OrderRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user_id', 'product_id', 'coupon_id', 'number', 'total_price', 'status', 'created')
