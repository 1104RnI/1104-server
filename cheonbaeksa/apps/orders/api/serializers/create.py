# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# DRF
from rest_framework import serializers

# Models
from cheonbaeksa.apps.orders.models import Order


# Main Section
class OrderCreateSerializer(ModelSerializer):
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = ('coupon_code',)
