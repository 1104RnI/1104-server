# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.models import Model


# Main Section
class Product(Model):
    # FK
    user_id = models.IntegerField(verbose_name=_('상품을 생성한 유저의 ID'), null=True, blank=True)

    # Main
    title = models.CharField(verbose_name=_('타이틀'), max_length=100)
    price = models.DecimalField(verbose_name=_('가격'), max_digits=10, decimal_places=2)
    subscription_price = models.DecimalField(verbose_name=_('월 구독료'), max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name=_('설명'), blank=True)

    class Meta:
        verbose_name = verbose_name_plural = _('상품')
        ordering = ['-created']
