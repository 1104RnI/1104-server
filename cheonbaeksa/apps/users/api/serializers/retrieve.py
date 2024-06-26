# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.users.models.index import User


# Main Section
class UserMeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_email_verified', 'trading_view_username')
