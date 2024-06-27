from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TokensConfig(AppConfig):
    name = "cheonbaeksa.apps.tokens"
    verbose_name = _('토큰')

    def ready(self):
        try:
            import cheonbaeksa.apps.tokens.signals
        except ImportError:
            pass
