from django.contrib import admin
from django.db import models

from .models import BaseContact, Group, Client, Provider


# Register your models here.
admin.site.register(Group)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nombre_comercial', 'id_type', 'id_number', 'email', 'phone', 'group')
    search_fields = ('razon_social', 'nombre_comercial', 'id_number', 'email')
    list_filter = ('group', 'id_type')
    fieldsets = (
        (None, {
            'fields': ('user', ('razon_social', 'nombre_comercial'), ('id_type', 'id_number'), 'group')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'province', 'zip_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nombre_comercial', 'id_type', 'id_number', 'email', 'phone', 'group')
    search_fields = ('razon_social', 'nombre_comercial', 'id_number', 'email')
    list_filter = ('group', 'id_type')
    fieldsets = (
        (None, {    
            'fields': ('user', ('razon_social', 'nombre_comercial'), ('id_type', 'id_number'), 'group')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'province', 'zip_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Client, ClientAdmin)
admin.site.register(Provider, ProviderAdmin)
