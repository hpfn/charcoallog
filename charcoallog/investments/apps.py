from django.apps import AppConfig

# from django.db.models.signals import post_save

# from charcoallog.bank.models import Extract
# from charcoallog.investments.signals import populate_investments


class InvestmentConfig(AppConfig):
    name = 'charcoallog.investments'

    def ready(self):
        # using @receiver decorator
        import charcoallog.investments.signals  # noqa: F401

        # post_save.connect(populate_investments, sender=Extract)
