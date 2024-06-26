from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SendsConfig(AppConfig):
    name = "cheonbaeksa.apps.sends"
    verbose_name = _('전송')

    def ready(self):
        try:
            import cheonbaeksa.apps.sends.signals
        except ImportError:
            pass
