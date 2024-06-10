from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "cheonbaeksa.apps.users"
    verbose_name = _('유저')

    def ready(self):
        try:
            import cheonbaeksa.apps.users.signals
        except ImportError:
            pass
