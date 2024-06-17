# Django
from django.conf import settings

# Bases
from cheonbaeksa.bases.modules.gateways import Gateway as BaseGateway


# Main Section
class Gateway(BaseGateway):
    def __init__(self):
        super().__init__(base_url=settings.PORTONE_SERVER_HOST)

    def get_access_token(self, imp_key: str, imp_secret: str):
        path = '/users/getToken'

        body = {
            'imp_key': imp_key,
            'imp_secret': imp_secret
        }

        return self.request(method="POST", path=path, json=body)

    def check_payment(self, portone_access_token: str, order_number: str, total_price: int):
        path = '/payments/prepare'

        headers = {
            'Authorization': f'Bearer {portone_access_token}'
        }

        body = {
            'merchant_uid': str(order_number),
            'amount': total_price
        }

        return self.request(method="POST", path=path, headers=headers, json=body)

    def get_payment(self, portone_access_token: str, imp_uid: str):
        path = f'/payments/{imp_uid}'

        headers = {
            'Authorization': f'Bearer {portone_access_token}'
        }

        return self.request(method="GET", path=path, headers=headers)


gateway = Gateway()
