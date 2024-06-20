# DRF
from rest_framework import serializers

# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.orders.models import Order
from cheonbaeksa.apps.products.models import Product
from cheonbaeksa.apps.payments.models import Payment


# Main Section
class PaymentListSerializer(ModelSerializer):
    product_title = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('id', 'product_title', 'total_price', 'status',
                  'prepared_at', 'failed_at', 'paid_at', 'partial_cancelled_at', 'cancelled_at')

    def get_product_title(self, obj):
        try:
            order = Order.objects.get(id=obj.order_id)
            product = Product.objects.get(id=order.product_id)
            return product.title
        except (Order.DoesNotExist, Product.DoesNotExist):
            return None
