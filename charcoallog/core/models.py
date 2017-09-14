from django.db import models
from .manager import ExtractManager


class Extract(models.Model):
    user_name = models.CharField('Name', max_length=30)
    date = models.DateField('Date')
    money = models.DecimalField('Money', max_digits=12, decimal_places=2, null=False, blank=False)
    description = models.CharField('Description', max_length=70)
    category = models.CharField('Category', max_length=70)
    payment = models.CharField('Payment', max_length=70)

    objects = ExtractManager()

    def save(self, *args, **kwargs):
        if Extract.objects.filter(user_name=self.user_name, date=self.date, money=self.money,
                                  description=self.description, category=self.category,
                                  payment=self.payment).exists():
            pass
            #   return
        else:
            super(Extract, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
