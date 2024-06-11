# DRF
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


# Main Section
class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs['refresh']
        try:
            refresh_token = RefreshToken(refresh)
            data = {
                'access': str(refresh_token.access_token),
            }
            return data
        except Exception as e:
            raise serializers.ValidationError('유효하지 않은 토큰입니다: ' + str(e))
