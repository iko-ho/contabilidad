from django.contrib import admin
from accounting.models import Tax
from .forms import InvoiceItemForm
from .models import Invoice, InvoiceItem


# Register your models here.
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    form = InvoiceItemForm
    extra = 1
    exclude = ('iva_percent', 'irpf_percent')
    readonly_fields = ('line_subtotal', 'iva_amount', 'irpf_amount', 'line_total')
    autocomplete_fields = ('iva_tax', 'irpf_tax')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('status', 'client', 'concept', ('issue_date', 'due_date')),
        }),
        ('Totales', {
            # 'classes': ('collapse',), # Opcional: para que empiece colapsado
            'fields': ('invoice_number', 'subtotal', 'total_iva', 'total_irpf', 'total'),
        }),
    )
    list_display = ('client','concept','invoice_number', 'issue_date', 'total', 'status')
    list_filter = ('status', 'issue_date', 'client')
    search_fields = ('invoice_number', 'client__razon_social')
    date_hierarchy = 'issue_date'
    ordering = ('-issue_date',)
    autocomplete_fields = ('client',)
    # Hacemos readonly los campos que se calculan o asignan automáticamente
    readonly_fields = ('invoice_number', 'subtotal', 'total_iva', 'total_irpf', 'total')
    inlines = [InvoiceItemInline]
    
    # ---- MÉTODO PARA ASIGNAR EL USUARIO ----
    def save_model(self, request, obj, form, change):
        # Usamos `if not obj.pk:` que es la forma estándar de saber si es un objeto nuevo.
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    # ---- MÉTODO PARA PASAR DATOS AL INLINE ----
    # Queremos pasarle los impuestos por defecto al InlineFormSet
    def get_formset_kwargs(self, request, obj, inline, prefix):
        kwargs = super().get_formset_kwargs(request, obj, inline, prefix)
        kwargs['form_kwargs'] = {'request': request}
        return kwargs

    # Con la clase Media, le decimos a Django qué archivos JS y CSS
    # debe cargar en la página de este modelo.
    class Media:
        js = ('admin/js/invoice_recalculate.js',)
