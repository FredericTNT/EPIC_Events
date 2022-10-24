from django.contrib import admin
from events.models import Client, Contract, Event, EventStatus


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'client')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract')


class EventStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventStatus, EventStatusAdmin)
