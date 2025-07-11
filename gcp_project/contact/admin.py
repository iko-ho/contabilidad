from django.contrib import admin

from .models import Group, Client, Provider


# Register your models here.
admin.site.register(Group)

# 1. Creamos una BaseClass con toda la configuración compartida
class BaseContactAdmin(admin.ModelAdmin):
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

    # Escondemos el campo 'user' en la edición para no cambiarlo por error y lo asignamos automaticamente al crear.
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)


# 2. Los ModelAdmin finales ahora son súper limpios. Solo heredan.
@admin.register(Client)
class ClientAdmin(BaseContactAdmin):
    # Podríamos añadir aquí fieldsets o list_display específicos para Cliente si los hubiera
    pass

@admin.register(Provider)
class ProviderAdmin(BaseContactAdmin):
    # Ídem para Proveedor
    pass
