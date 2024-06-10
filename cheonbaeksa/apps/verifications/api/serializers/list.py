# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.verifications.models import EmailVerification


# Main Section
class EmailVerificationListSerializer(ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ('id', 'user', 'email', 'code', 'purpose', 'is_verified', 'created', 'expired')
