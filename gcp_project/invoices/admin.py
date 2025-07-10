from typing import override
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
    list_display = ('description', 'quantity', 'unit_price', 'line_subtotal', 'iva_amount', 'irpf_amount')
    autocomplete_fields = ('iva_tax', 'irpf_tax')

    # Con la clase Media, le decimos a Django qué archivos JS y CSS
    # debe cargar en la página de este modelo.
    class Media:
        js = ('admin/js/invoice_recalculate.js',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'invoice_number',
                'client',
                'status',
                'issue_date',
                'due_date',
            ),
        }),
        ('Totales', {
            # 'classes': ('collapse',), # Opcional: para que empiece colapsado
            'fields': (
                'subtotal',
                'total_iva',
                'total_irpf',
                'total',
            ),
        }),
    )
    list_display = ('client', 'status','invoice_number', 'issue_date', 'due_date', 'subtotal', 'total_iva', 'total_irpf', 'total')
    list_filter = ('client', 'status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'client__name', 'client__razon_social', 'issue_date')
    date_hierarchy = 'issue_date'
    ordering = ('-issue_date',)
    autocomplete_fields = ('client',)
    readonly_fields = ('invoice_number', 'issue_date', 'due_date', 'subtotal', 'total_iva', 'total_irpf', 'total')
    inlines = [InvoiceItemInline]
    
    # ---- MÉTODO PARA ASIGNAR EL USUARIO ----
    def save_model(self, request, obj, form, change):
        """
        Al guardar por primera vez (no al editar), asigna el usuario logueado.
        """
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    # ---- MÉTODO PARA PASAR DATOS AL INLINE ----
    # Queremos pasarle los impuestos por defecto al InlineFormSet
    def get_formset_kwargs(self, request, obj, inline, prefix):
        kwargs = super().get_formset_kwargs(request, obj, inline, prefix)
        # Pass custom kwargs to the form, not the formset.
        kwargs.setdefault('form_kwargs', {})
        kwargs['form_kwargs']['default_iva_tax'] = Tax.objects.filter(user=request.user,tax_type=Tax.TaxType.IVA, is_default=True).first()
        kwargs['form_kwargs']['default_irpf_tax'] = Tax.objects.filter(user=request.user,tax_type=Tax.TaxType.IRPF, is_default=True).first()
        return kwargs


    # Con la clase Media, le decimos a Django qué archivos JS y CSS
    # debe cargar en la página de este modelo.
    class Media:
        js = ('admin/js/invoice_recalculate.js',)


"""@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_type', 'percent', 'is_default', 'is_active')
    ordering = ('-is_default',)"""
