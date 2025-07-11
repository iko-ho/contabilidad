from django import forms
from accounting.models import Tax
from .models import InvoiceItem


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # "Pescamos" el objeto request que nos pasó el InvoiceAdmin
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Si estamos creando un item nuevo (no editando uno existente)
        # y tenemos el request, buscamos los impuestos por defecto.
        if not self.instance.pk and request:
            default_vat = Tax.objects.filter(user=request.user, tax_type=Tax.TaxType.IVA, is_default=True).first()
            default_irpf = Tax.objects.filter(user=request.user, tax_type=Tax.TaxType.IRPF, is_default=True).first()
            
            if default_vat:
                self.fields['iva_tax'].initial = default_vat
            if default_irpf:
                self.fields['irpf_tax'].initial = default_irpf