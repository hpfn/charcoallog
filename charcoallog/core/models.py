from django.db import models
from django.utils import timezone

class Extract(models.Model):
    username = models.ForeignKey('auth.User')
