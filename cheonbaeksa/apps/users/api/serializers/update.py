# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.users.models.index import User


# Main Section
class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
