# Python
import random
import string

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# DRF
from rest_framework.exceptions import ValidationError

# Bases
from cheonbaeksa.bases.models import Model

# Models
from cheonbaeksa.apps.coupons.models.group import CouponGroup


# Function Section
def create_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))  # 12자리 숫자와 영문 대문자


def generate_unique_code():
    while True:
        code = create_code()
        if not Coupon.objects.filter(code=code).exists():
            return code


# Main Section
class Coupon(Model):
    # FK
    user_id = models.IntegerField(verbose_name=_('쿠폰을 발급한 유저 ID'))
    coupon_group_id = models.IntegerField(verbose_name=_('쿠폰 그룹 ID'), null=True, blank=True)

    # Main
    code = models.CharField(verbose_name=_('코드'), unique=True, max_length=12, default=generate_unique_code)
    discount_price = models.DecimalField(verbose_name=_('할인 금액'), max_digits=10, decimal_places=2, null=True,
                                         blank=True)
    discount_percentage = models.DecimalField(verbose_name=_('할인 비율'), max_digits=5, decimal_places=2, null=True,
                                              blank=True)

    # Boolean
    is_used = models.BooleanField(verbose_name=_('사용 여부'), default=False)

    # Date
    expired = models.DateTimeField(verbose_name=_('만료 시간'), null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = _('쿠폰')
        ordering = ['-created']

    @staticmethod
    def validate_code(value):
        try:
            coupon = Coupon.objects.get(code=value)
        except Coupon.DoesNotExist:
            raise ValidationError("유효하지 않은 쿠폰 코드입니다.")

        if coupon.is_used:
            raise ValidationError("이미 사용된 쿠폰 코드입니다.")

        if coupon.expired and coupon.expired < timezone.now():
            raise ValidationError("만료된 쿠폰 코드입니다.")

        return coupon

    def clean(self):
        if self.coupon_group_id:
            try:
                coupon_group = CouponGroup.objects.get(id=self.coupon_group_id)
                if coupon_group.title == '커스텀':
                    if self.discount_price and self.discount_percentage:
                        raise ValidationError('할인 금액과 할인 비율 중 하나만 설정할 수 있습니다.')
                    if not self.discount_price and not self.discount_percentage:
                        raise ValidationError('할인 금액 또는 할인 비율을 설정해야 합니다.')
                else:
                    self.discount_price = coupon_group.discount_price
                    self.discount_percentage = coupon_group.discount_percentage
            except CouponGroup.DoesNotExist:
                raise ValidationError('유효하지 않은 쿠폰 그룹 ID입니다.')
        else:
            raise ValidationError('쿠폰 그룹을 설정해야 합니다.')

    def save(self, *args, **kwargs):
        if not self.expired:
            try:
                coupon_group = CouponGroup.objects.get(id=self.coupon_group_id)
                self.expired = timezone.now() + timezone.timedelta(days=coupon_group.valid_days)
            except CouponGroup.DoesNotExist:
                raise ValidationError('유효하지 않은 쿠폰 그룹 ID입니다.')
        self.clean()  # Clean method 호출하여 유효성 검사
        super().save(*args, **kwargs)

    def get_discounted_price(self, original_price):
        if self.discount_price:
            return max(original_price - self.discount_price, 0)
        elif self.discount_percentage:
            return max(original_price * (1 - self.discount_percentage / 100), 0)
        return original_price
