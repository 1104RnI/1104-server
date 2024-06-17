from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CouponsConfig(AppConfig):
    name = "cheonbaeksa.apps.coupons"
    verbose_name = _('쿠폰')

    def ready(self):
        try:
            import cheonbaeksa.apps.coupons.signals
        except ImportError:
            pass
