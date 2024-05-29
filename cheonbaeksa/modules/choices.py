from model_utils import Choices
from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = Choices(
    ('MALE', _('남성')),
    ('FEMALE', _('여성')),
)
