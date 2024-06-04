# Django
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework.exceptions import ValidationError

# Bases
from cheonbaeksa.bases.api.serializers import ModelSerializer

# Models
from cheonbaeksa.apps.users.models.index import User


# Main Section
class UserPasswordUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)


class UserTradingViewUsernameUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('trading_view_username',)

    def update(self, instance, validated_data):
        try:
            instance.trading_view_username = validated_data.get('trading_view_username', instance.trading_view_username)
            instance.save()
            return instance
        except IntegrityError as e:
            if 'unique_trading_view_username' in str(e):
                raise ValidationError(_('이미 사용중인 트레이딩뷰 닉네임입니다.'))
            raise e
