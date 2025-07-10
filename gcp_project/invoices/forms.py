from django import forms
from .models import InvoiceItem


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        default_iva_tax = kwargs.pop('default_iva_tax', None)
        default_irpf_tax = kwargs.pop('default_irpf_tax', None)

        super().__init__(*args, **kwargs)
        
        if default_iva_tax:
            self.fields['iva_tax'].initial = default_iva_tax
        if default_irpf_tax:
            self.fields['irpf_tax'].initial = default_irpf_tax
