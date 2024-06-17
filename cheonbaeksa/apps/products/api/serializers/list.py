# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.products.models import Product


# Main Section
class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'subscription_price', 'description')
