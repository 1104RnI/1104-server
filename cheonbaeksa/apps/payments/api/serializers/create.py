# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.payments.models import Payment


# Main Section
class PaymentCreateSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('imp_uid',)
