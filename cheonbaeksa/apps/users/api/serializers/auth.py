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
        access = str(token.access_token)
        refresh = str(token)

        return {'access': access, 'refresh': refresh}
