# Python
import re

# Django
from django.utils.translation import ugettext_lazy as _

# DRF
from rest_framework.exceptions import ValidationError

# Fields
from phonenumber_field.phonenumber import to_python


# Main Section
def validate_international_phonenumber(value):
    phone_number = to_python(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(
            _("연락처를 정확히 입력해 주세요."), code="invalid_phone_number"
        )


def validator_password(password):
    errors = []

    if len(password) < 8 or len(password) > 25:
        errors.append(_('비밀번호는 최소 8자리, 최대 25자리여야 합니다.'))

    if not re.search(r'[0-9]', password):
        errors.append(_('비밀번호에는 적어도 하나의 숫자가 포함되어야 합니다.'))

    if not re.search(r'[A-Z]', password):
        errors.append(_('비밀번호에는 적어도 하나의 영문 대문자가 포함되어야 합니다.'))

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append(_('비밀번호에는 적어도 하나의 특수문자가 포함되어야 합니다.'))

    if not re.match(r'^[a-zA-Z0-9!@#$%^&*(),.?":{}|<>]+$', password):
        errors.append(_('비밀번호는 숫자, 영문 소문자, 영문 대문자, 특수문자만 사용할 수 있습니다.'))

    if errors:
        raise ValidationError(errors)


def validator_name(name):
    validator = re.compile(r'^[a-z가-힣]{1,20}$')
    if not validator.match(name):
        raise ValidationError(_('한글 / 영어(소문자)로만 입력해주세요.'))


def validator_username(username):
    if len(username) < 2:
        raise ValidationError(_('닉네임은 최소 두글자 부터 입력 가능합니다.'))
    validator = re.compile(r'^[a-z가-힣0-9]{2,20}$')
    if not validator.match(username):
        raise ValidationError(_('한글 / 영어(소문자) / 숫자만 입력 가능합니다.'))


def validator_content(content):
    if len(content) < 20:
        raise ValidationError(_('내용은 최소 20자 부터 입력 가능합니다.'))
