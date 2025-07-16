from django import forms
from accounting.models import Tax
from .models import Invoice, InvoiceItem

from contact.models import Client

class InvoiceForm(forms.ModelForm):
    """
    Formulario para los datos principales de la Factura.
    """
    # Sobrescribimos el campo 'client' para filtrar por el usuario actual.
    # El queryset se establecerá en la vista.
    client = forms.ModelChoiceField(queryset=Client.objects.none())

    class Meta:
        model = Invoice
        # Especificamos los campos que el usuario rellenará.
        # Los campos calculados o asignados automáticamente se excluyen.
        fields = ['client', 'status', 'issue_date', 'due_date', 'concept']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'concept': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        # "Pescamos" el usuario que nos pasará la vista.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si tenemos un usuario, filtramos el queryset del campo 'client'.
        if user:
            self.fields['client'].queryset = Client.objects.filter(user=user)


class InvoiceItemForm(forms.ModelForm):
    """
    Formulario para cada línea de la Factura.
    """
    class Meta:
        model = InvoiceItem
        # Excluimos los campos que no debe rellenar el usuario directamente.
        exclude = ('invoice', 'iva_percent', 'irpf_percent', 'line_subtotal', 'iva_amount', 'irpf_amount', 'line_total')

    def __init__(self, *args, **kwargs):
        # "Pescamos" el objeto request que nos pasó el InvoiceAdmin
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Si estamos creando un item nuevo (no editando uno existente)
        # y tenemos el request, buscamos los impuestos por defecto.
        if not self.instance.pk and request:
            default_iva = Tax.objects.filter(user=request.user, tax_type=Tax.TaxType.IVA, is_default=True).first()
            default_irpf = Tax.objects.filter(user=request.user, tax_type=Tax.TaxType.IRPF, is_default=True).first()

            if default_iva:
                self.fields['iva_tax'].initial = default_iva
            if default_irpf:
                self.fields['irpf_tax'].initial = default_irpf

InvoiceItemFormSet = forms.inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,  # Número de formularios extra vacíos que se mostrarán.
    can_delete=True,  # Permite al usuario marcar líneas para ser borradas.
)
