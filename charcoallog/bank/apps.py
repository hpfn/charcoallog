from django.apps import AppConfig


class BankConfig(AppConfig):
    name = 'charcoallog.bank'

    def ready(self):
        # using @receiver decorator
        # do not optimize import !!!
        import charcoallog.bank.signals  # noqa: F401
