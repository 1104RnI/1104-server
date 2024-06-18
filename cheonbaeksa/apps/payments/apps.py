from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentsConfig(AppConfig):
    name = "cheonbaeksa.apps.payments"
    verbose_name = _('결제')

    def ready(self):
        try:
            import cheonbaeksa.apps.payments.signals
        except ImportError:
            pass
