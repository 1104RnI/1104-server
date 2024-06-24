# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.models import Model


# Main Section
class UserHistory(Model):
    # FK
    user_id = models.IntegerField(verbose_name=_('유저 ID'))

    # Main
    action = models.CharField(verbose_name=_('행동'), max_length=20)
    model_title = models.CharField(verbose_name=_('모델 타이틀'), max_length=100)
    object_id = models.IntegerField(verbose_name=_('객체 ID'))
    description = models.TextField(verbose_name=_('설명'))
    changed_fields = models.TextField(verbose_name=_('변경된 필드'), blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = _('유저 히스토리')
        ordering = ['-created']
