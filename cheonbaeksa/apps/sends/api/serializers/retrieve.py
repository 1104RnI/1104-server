# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.sends.models import EmailSend


# Main Section
class EmailSendRetrieveSerializer(ModelSerializer):
    class Meta:
        model = EmailSend
        fields = ('id', 'from_email', 'to_email', 'title', 'content', 'purpose', 'status', 'created')
