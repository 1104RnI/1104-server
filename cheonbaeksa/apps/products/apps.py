from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    name = "cheonbaeksa.apps.products"
    verbose_name = _('상품')

    def ready(self):
        try:
            import cheonbaeksa.apps.products.signals
        except ImportError:
            pass
