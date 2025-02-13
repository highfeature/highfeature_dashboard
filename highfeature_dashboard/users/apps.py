from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "highfeature_dashboard.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import highfeature_dashboard.users.signals  # noqa: F401
        except ImportError:
            pass
