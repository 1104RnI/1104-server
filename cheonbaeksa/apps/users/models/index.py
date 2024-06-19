# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.models import Model

# Fields
from cheonbaeksa.apps.users.models.fields.phone_number import PhoneNumberField

# Models
from cheonbaeksa.apps.users.models.managers.objects import UserMainManager


# Main Section
class User(AbstractUser,
           Model):
    # FK
    advisor_id = models.IntegerField(verbose_name=_('담당 어드바이저 ID'), null=True, blank=True)

    # Main
    email = models.EmailField(verbose_name=_('이메일'), unique=True,
                              error_messages={'unique': _('이미 사용중인 이메일 입니다.')})

    # Boolean
    is_email_verified = models.BooleanField(verbose_name=_('회원가입 이메일 인증 여부'), default=False)

    # Not use
    trading_view_username = models.CharField(verbose_name=_('트레이딩뷰 닉네임'), max_length=100, blank=True)
    exchange_title = models.CharField(verbose_name=_('거래소 타이틀'), max_length=100, blank=True)
    exchange_uid = models.CharField(verbose_name=_('거래소 UID'), max_length=100, blank=True)
    phone = PhoneNumberField(verbose_name=_('전화'), max_length=20, blank=True)
    username = models.CharField(verbose_name=_('닉네임'), max_length=20, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserMainManager()

    class Meta:
        verbose_name = verbose_name_plural = _('유저')
        ordering = ['-created']

        # 빈 스트링이 아닐 때, unique=True
        constraints = [
            models.UniqueConstraint(
                fields=['username'],
                name='unique_username',
                condition=~Q(username=''),
            ),
            models.UniqueConstraint(
                fields=['trading_view_username'],
                name='unique_trading_view_username',
                condition=~Q(trading_view_username=''),
            ),

            # exchange_uid 필드가 빈 문자열이 아닐 때, exchange_title, exchange_uid unique=True
            models.UniqueConstraint(
                fields=['exchange_title', 'exchange_uid'],
                name='unique_exchange_title_uid',
                condition=~Q(exchange_uid=''),
            )
        ]
