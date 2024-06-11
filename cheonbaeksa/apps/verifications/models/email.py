# Python
import random

# Django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework.exceptions import ValidationError

# Bases
from cheonbaeksa.bases.models import Model

# Choices
from cheonbaeksa.modules.choices import PURPOSE_CHOICES


# Function Section
def create_code():
    return ''.join(random.choices('0123456789', k=6))  # 6자리 숫자


# Main Section
class EmailVerification(Model):
    # FK
    user = models.ForeignKey('users.User', verbose_name=_('유저'), on_delete=models.CASCADE,
                             related_name='email_verifications',
                             null=True, blank=True)  # 인증 코드를 소유하는 사용자와의 외래 키 관계, 비밀번호 찾기 시에는 비워둘 수 있음

    # Main
    email = models.EmailField(verbose_name=_('이메일'))
    code = models.CharField(verbose_name=_('6자리 인증 코드'), max_length=6, default=create_code)
    purpose = models.CharField(verbose_name=_('이메일 전송 목적'), choices=PURPOSE_CHOICES, max_length=20)

    # Boolean
    is_verified = models.BooleanField(verbose_name=_('인증 완료 여부'), default=False)  # 인증 완료 여부

    # Date
    expired = models.DateTimeField(verbose_name=_('만료 시간'))  # 코드가 만료되는 시간

    class Meta:
        verbose_name = verbose_name_plural = _('이메일 인증')
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.expired:
            self.expired = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    @classmethod
    def create_or_get_valid_code(cls, user=None, email=None, purpose=None):
        now = timezone.now()
        one_minute_ago = now - timezone.timedelta(minutes=1)

        # 최근 1분 이내에 생성된 동일한 유형의 전송 시도 횟수 확인
        recent_attempts_count = cls.objects.filter(
            user=user,
            email=email,
            purpose=purpose,
            created__gte=one_minute_ago
        ).count()

        if recent_attempts_count >= 1:  # 1분 내에 생성된 객체가 있으면 예외 발생
            raise ValidationError('1분 후 다시 시도해 주세요.')

        # 새로운 코드를 생성
        new_code = cls(
            user=user,
            email=email,
            purpose=purpose
        )
        new_code.save()
        return new_code
