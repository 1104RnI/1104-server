# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.verifications.models import EmailVerification


# Main Section
class EmailVerificationUpdateSerializer(ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ('code',)
