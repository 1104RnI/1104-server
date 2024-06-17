# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework.exceptions import ValidationError

# Bases
from cheonbaeksa.bases.models import Model


# Main Section
class CouponGroup(Model):
    # FK
    user_id = models.IntegerField(verbose_name=_('쿠폰 그룹을 생성한 유저의 ID'), null=True, blank=True)

    # Main
    title = models.CharField(verbose_name=_('타이틀'), max_length=100)
    discount_price = models.DecimalField(verbose_name=_('할인 금액'), max_digits=10, decimal_places=2, null=True,
                                         blank=True)
    discount_percentage = models.DecimalField(verbose_name=_('할인 비율'), max_digits=5, decimal_places=2, null=True,
                                              blank=True)

    # Date
    valid_days = models.IntegerField(verbose_name=_('유효 기간 (일)'))

    class Meta:
        verbose_name = verbose_name_plural = _('쿠폰 그룹')
        ordering = ['-created']

    def clean(self):
        if self.title != '커스텀':
            if self.discount_price and self.discount_percentage:
                raise ValidationError('할인 금액과 할인 비율 중 하나만 설정할 수 있습니다.')
            if not self.discount_price and not self.discount_percentage:
                raise ValidationError('할인 금액 또는 할인 비율을 설정해야 합니다.')
