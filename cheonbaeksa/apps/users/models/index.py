# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.models import Model

# Utils
from cheonbaeksa.utils.validators import validator_username

# Fields
from cheonbaeksa.apps.users.models.fields.phone_number import PhoneNumberField

# Models
from cheonbaeksa.apps.users.models.managers.objects import UserMainManager


# Main Section
class User(AbstractUser,
           Model):
    # Main
    email = models.EmailField(_('이메일'), unique=True,
                              error_messages={'unique': _('이미 사용중인 이메일 입니다.')})
    phone = PhoneNumberField(_('전화'), max_length=20, null=True, blank=True)
    username = models.CharField(_('닉네임'), max_length=20, unique=True,
                                validators=[validator_username],
                                error_messages={'unique': _('이미 사용중인 닉네임 입니다.')})

    # Info
    is_email_verified = models.BooleanField(_('이메일 인증 여부'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserMainManager()

    class Meta:
        verbose_name = verbose_name_plural = _('유저')
        ordering = ['-created']
