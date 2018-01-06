from django.contrib import admin
from .models import Extract


@admin.register(Extract)
class ExtractAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'description', 'money', 'date')
