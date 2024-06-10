# DRF
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'is_email_verified', 'token')

    def get_token(self, obj):
        token = TokenObtainPairSerializer.get_token(obj)
        refresh_token = str(token)
        access_token = str(token.access_token)

        return {'refresh_token': refresh_token, 'access_token': access_token}
