# DRF
from rest_framework import serializers

# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.users.models.index import User


# Main Section
class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserLoginSuccessSerializer(ModelSerializer):
    token = serializers.CharField(source='auth_token')

    class Meta:
        model = User
        fields = ('token', 'email')
