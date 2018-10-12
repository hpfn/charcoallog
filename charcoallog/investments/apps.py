from django.apps import AppConfig


class InvestmentsConfig(AppConfig):
    name = 'charcoallog.investments'

    def ready(self):
        # using @receiver decorator
        # do not optimize import !!!
        import charcoallog.investments.signals  # noqa: F401
