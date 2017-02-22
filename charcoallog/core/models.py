from django.db import models
# from django.utils import timezone

class ExtractManager(models.Manager):
    def search(self,query):
        return self.get_queryset().filter(models.Q(user_name__contains=query))

class Extract(models.Model):
    user_name = models.CharField('Name', max_length=30)
    date = models.DateField('Date', null=False, blank=False)
    money = models.FloatField('Money', null=False, blank=False)
    description = models.CharField('Description', max_length=70)
    category = models.CharField('Category', max_length=70)
    payment = models.CharField('Payment', max_length=70)

    objects = ExtractManager()

    class Meta:
        ordering = ['date']
