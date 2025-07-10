from django.contrib import admin
from .models import Tax

# Register your models here.
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_type', 'percent', 'is_default', 'is_active')
    ordering = ('-is_default',)
    search_fields = ('name',)
    list_filter = ('tax_type', 'is_default', 'is_active')


admin.site.register(Tax, TaxAdmin)
