from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HistoriesConfig(AppConfig):
    name = "cheonbaeksa.apps.histories"
    verbose_name = _('히스토리')

    def ready(self):
        try:
            import cheonbaeksa.apps.histories.signals
        except ImportError:
            pass
