import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "charcoallog.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils.text import slugify
from mixer.backend.django import mixer
from charcoallog.core.models import Extract


mixer.cycle(5).blend(Extract)
