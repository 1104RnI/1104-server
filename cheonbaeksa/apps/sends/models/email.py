# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Bases
from cheonbaeksa.bases.models import Model

# Modules
from cheonbaeksa.modules.choices import PURPOSE_CHOICES


# Main Section
class EmailSend(Model):
    # Main
    sender_email = models.EmailField(verbose_name=_('보낸 사람 이메일'))
    recipient_email = models.EmailField(verbose_name=_('받는 사람 이메일'))
    title = models.CharField(verbose_name=_('타이틀'), max_length=100)
    content = models.TextField(verbose_name=_('본문'))
    purpose = models.CharField(verbose_name=_('이메일 전송 목적'), choices=PURPOSE_CHOICES, max_length=20)

    # Status
    status = models.CharField(verbose_name=_('상태'), max_length=100, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = _('이메일 전송')
        ordering = ['-created']
