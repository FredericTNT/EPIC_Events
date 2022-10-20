from django.contrib import admin
from events.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')


admin.site.register(Client, ClientAdmin)
