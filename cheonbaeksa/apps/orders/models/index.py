# Python
import random
import string

# Django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField

# Bases
from cheonbaeksa.bases.models import Model


# Function Section
def create_random_number():
    return ''.join(random.choices(string.digits, k=6))  # 6자리 숫자 난수


def generate_unique_number():
    while True:
        date_str = timezone.now().strftime('%Y%m%d')  # 날짜 형식
        random_number = create_random_number()
        number = f'{date_str}-{random_number}'
        if not Order.objects.filter(number=number).exists():
            return number


# Main Section
class Order(Model):
    STATUS = Choices(
        ('PENDING', '진행'),
        ('APPROVED', '승인'),
        ('REFUSED', '거절'),
    )

    # FK
    user_id = models.IntegerField(verbose_name=_('유저 ID'))
    product_id = models.IntegerField(verbose_name=_('상품 ID'))
    coupon_id = models.IntegerField(verbose_name=_('쿠폰 ID'), null=True, blank=True)

    # Main
    number = models.CharField(verbose_name=_('주문 번호'), unique=True, max_length=20, default=generate_unique_number)
    total_price = models.DecimalField(verbose_name=_('총 가격'), max_digits=10, decimal_places=2)

    # Status
    status = StatusField(_('상태'), null=True, default=None)
    pending_at = MonitorField(_('진행 시간'), monitor='status', when=['PENDING'], default=None, null=True)
    approved_at = MonitorField(_('승인 시간'), monitor='status', when=['APPROVED'], default=None, null=True)
    refused_at = MonitorField(_('거절 시간'), monitor='status', when=['REFUSED'], default=None, null=True)

    class Meta:
        verbose_name = verbose_name_plural = _('주문')
        ordering = ['-created']

    def save(self, *args, **kwargs):
        # 상태가 PENDING인 경우 pending_at 필드를 수동으로 설정
        if self.status == 'PENDING' and not self.pending_at:
            self.pending_at = timezone.now()
        super().save(*args, **kwargs)
