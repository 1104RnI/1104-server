from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    name = "cheonbaeksa.apps.orders"
    verbose_name = _('주문')

    def ready(self):
        try:
            import cheonbaeksa.apps.orders.signals
        except ImportError:
            pass
