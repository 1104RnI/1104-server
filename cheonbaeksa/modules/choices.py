# Django
from model_utils import Choices
from django.utils.translation import gettext_lazy as _

# Main Section
PURPOSE_CHOICES = Choices(
    ('SIGNUP', _('회원가입')),
    ('PASSWORD_RESET', _('비밀번호 변경')),
    ('PASSWORD_RECOVERY', _('비밀번호 찾기')),
)
