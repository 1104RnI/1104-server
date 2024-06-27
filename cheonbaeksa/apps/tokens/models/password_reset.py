# Python
import secrets

# Django
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.models import Model

# Models
from rest_framework.exceptions import ValidationError


# Function Section
def create_token():
    return secrets.token_urlsafe(64)


def generate_unique_token():
    while True:
        token = create_token()
        if not PasswordResetToken.objects.filter(token=token).exists():
            return token


# Main Section
class PasswordResetToken(Model):
    user_id = models.IntegerField(verbose_name=_('유저 ID'))
    token = models.CharField(max_length=128, unique=True)
    expired = models.DateTimeField(verbose_name=_('만료 시간'))

    class Meta:
        verbose_name = verbose_name_plural = _('비밀번호 리셋 토큰')
        ordering = ['-created']

    @classmethod
    def create_token(cls, user):
        token = cls(
            user_id=user.id,
            token=generate_unique_token(),
            expired=timezone.now() + timedelta(minutes=30)
        )
        token.save()
        return token.token

    @staticmethod
    def verify_reset_token(token):
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.expired < timezone.now():
                raise ValidationError('Token has expired')
            return reset_token.user_id
        except PasswordResetToken.DoesNotExist:
            raise ValidationError('Invalid token')
