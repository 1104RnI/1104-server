# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField

# Bases
from cheonbaeksa.bases.models import Model


# Main Section
class Payment(Model):
    STATUS = Choices(
        ('PREPARED', _('결제 예정')),
        ('FAILED', _('결제 실패')),
        ('PAID', _('결제 완료')),
        ('PARTIAL_CANCELLED', _('부분 취소')),
        ('CANCELLED', _('전체 취소')),
    )

    # FK
    user_id = models.IntegerField(verbose_name=_('유저 ID'))
    order_id = models.IntegerField(verbose_name=_('주문 ID'))

    # Main
    imp_uid = models.CharField(_('포트원 결제 UID'), max_length=20, null=True, blank=True)
    total_price = models.DecimalField(verbose_name=_('총 가격'), max_digits=10, decimal_places=2)

    # Status
    status = StatusField(verbose_name=_('상태'), default=None, null=True)
    prepared_at = MonitorField(verbose_name=_('결제 예정 시간'), monitor='status', when=['PREPARED'], default=None, null=True)
    failed_at = MonitorField(verbose_name=_('결제 실패 시간'), monitor='status', when=['FAILED'], default=None, null=True)
    paid_at = MonitorField(verbose_name=_('결제 완료 시간'), monitor='status', when=['PAID'], default=None, null=True)
    partial_cancelled_at = MonitorField(verbose_name=_('부분 취소 시간'), monitor='status', when=['PARTIAL_CANCELLED'],
                                        default=None, null=True)
    cancelled_at = MonitorField(verbose_name=_('전체 취소 시간'), monitor='status', when=['CANCELLED'], default=None,
                                null=True)

    # Data
    pg_data = models.JSONField(verbose_name=_('PG 데이터'), null=True)

    class Meta:
        verbose_name = verbose_name_plural = _('결제')
        ordering = ['-created']
