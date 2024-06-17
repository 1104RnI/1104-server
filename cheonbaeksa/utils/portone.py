# Django
from django.conf import settings

# DRF
from rest_framework.exceptions import AuthenticationFailed

# Modules
from cheonbaeksa.modules.gateways.portone import gateway as gateway_portone


# Main Section
def get_portone_access_token():
    imp_key = settings.PORTONE_IMP_KEY
    imp_secret = settings.PORTONE_IMP_SECRET

    # API GATEWAY
    response = gateway_portone.get_access_token(imp_key=imp_key, imp_secret=imp_secret)
    response_data = response['response']

    if not response_data:
        raise AuthenticationFailed(response_data['message'])

    access_token = response_data['access_token']
    return access_token
