from django.contrib import admin
from django.contrib.admin import ModelAdmin

from send_email.models import Contact


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    pass
