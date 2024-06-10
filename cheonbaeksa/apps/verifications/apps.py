from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VerificationsConfig(AppConfig):
    name = "cheonbaeksa.apps.verifications"
    verbose_name = _('인증')

    def ready(self):
        try:
            import cheonbaeksa.apps.verifications.signals
        except ImportError:
            pass
