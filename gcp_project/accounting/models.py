from django.db import models
from django.conf import settings

# Create your models here.

class Tax(models.Model):
    class TaxType(models.TextChoices):
        IVA = 'IVA', 'IVA'
        IRPF = 'IRPF', 'IRPF'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Nombre descriptivo (ej: IVA General 21%)')
    tax_type = models.CharField(max_length=10, choices=TaxType.choices, default=TaxType.IVA, help_text='Tipo de impuesto')
    percent = models.DecimalField(max_digits=5, decimal_places=2, help_text='Porcentaje del impuesto (ej: 21.00)')
    is_default = models.BooleanField(default=False, help_text='Marcar si este es el impuesto por defecto para nuevos clientes')
    is_active = models.BooleanField(default=True, help_text='Desmarcar para desactivar un impuesto antiguo sin borrarlo')

    def __str__(self):
        return f"{self.percent} %"

    class Meta:
        verbose_name = 'Impuesto'
        verbose_name_plural = 'Impuestos'