# DRF
from phonenumber_field.modelfields import PhoneNumberField

# Utils
from cheonbaeksa.utils.validators import validate_international_phonenumber


# Main Section
class PhoneNumberField(PhoneNumberField):
    default_validators = [validate_international_phonenumber]
