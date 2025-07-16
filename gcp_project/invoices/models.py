from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import date

from accounting.models import Tax


# Create your models here.
class Invoice(models.Model):
    class InvoiceType(models.TextChoices):
        NORMAL = 'NORMAL', 'Normal'
        RECTIFICATIVE = 'RECTIFICATIVE', 'Rectificativa'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Borrador'
        PROFORMA = 'PROFORMA', 'Proforma'
        ISSUED = 'ISSUED', 'Emitida'
        PAID = 'PAID', 'Pagada'
        OVERDUE = 'OVERDUE', 'Vencida'
        RECTIFIED = 'RECTIFIED', 'Rectificada'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    client = models.ForeignKey('contact.Client', on_delete=models.PROTECT)

    concept = models.CharField(max_length=255, help_text="Concepto de la factura")
    
    invoice_type = models.CharField(max_length=20, choices=InvoiceType.choices, default=InvoiceType.NORMAL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    rectifies = models.ForeignKey('self', on_delete=models.SET_NULL, # Si se borra la original, no se borra la rectificativa
                                blank=True, null=True, related_name='rectified_by',
                                help_text="Factura rectificada")
    
    issue_date = models.DateField(default=date.today, help_text="Fecha de emisión")
    due_date = models.DateField(blank=True, null=True, help_text="Fecha de vencimiento")
    
    # La lógica de numeración se moverá al método save()
    invoice_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    # Los totales se calculan con señales, se guardan aquí.
    # Usamos default=0 para evitar problemas con valores Nulos.
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_irpf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # PDF
    pdf_file = models.FileField(upload_to='invoices/pdf', blank=True, null=True, help_text="Archivo PDF de la factura")

    def __str__(self):
        return f"Factura {self.invoice_number or '[BORRADOR]'} - {self.client}"

    # --- MÉTODO PARA GENERAR Y GUARDAR EL PDF ---
    def generate_pdf_and_save(self):
        html_string = render_to_string('invoices/invoice_pdf.html', {
            'invoice': self,
            'invoice_items': self.items.all()
        })
        pdf = HTML(string=html_string).write_pdf()

        # Guardamos el archivo en el campo FileField
        # Esto guarda el archivo en la ruta de MEDIA_ROOT por año y actualiza el campo en la BD.
        self.pdf_file.save(f'{self.issue_date.year}/factura_{self.invoice_number} {self.client.razon_social}.pdf', ContentFile(pdf), save=False) # save=False para evitar recursión
        
        # No es necesario un super().save() extra aquí, lo haremos en el save principal.

    def save(self, *args, **kwargs):
        # Guardamos el estado original para compararlo después
        original_status = None
        if self.pk:
            original_status = Invoice.objects.get(pk=self.pk).status

        # Lógica de numeración: se asigna solo al pasar de Borrador o Proforma a Emitida o de Emitida a Rectificada
        if (self.status == self.Status.ISSUED and original_status in [self.Status.DRAFT, self.Status.PROFORMA]) or \
            (self.status == self.Status.RECTIFIED and original_status == self.Status.ISSUED):
            last_invoice = Invoice.objects.filter(
                user=self.user, 
                issue_date__year=self.issue_date.year
            ).order_by('invoice_number').last()
            
            if last_invoice and last_invoice.invoice_number:
                # Extrae el número secuencial y lo incrementa
                last_seq = int(last_invoice.invoice_number.split('-')[-1])
                new_seq = last_seq + 1
            else:
                new_seq = 1
            
            # Generar un número de factura único
            # AÑO.NNNN -> Ejemplo: 2025-0001
            self.invoice_number = f"{self.issue_date.year}-{str(new_seq).zfill(4)}"
            
            # Generar y guardar el PDF
            self.generate_pdf_and_save()

        # El cálculo de totales lo hacen las señales, no es necesario aquí.
        # self.total = self.subtotal + self.total_iva - self.total_irpf

        # Guardamos el objeto
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-issue_date']


class InvoiceItem(models.Model):
    invoice = models.ForeignKey('invoices.Invoice', on_delete=models.CASCADE, related_name='items')

    description = models.CharField(max_length=255, help_text="Descripción del concepto")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1, help_text="Cantidad del producto")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio unitario")

    # --- Lógica de Impuestos ---
    # 1. Enlazamos a la regla de impuesto que se aplicó
    iva_tax = models.ForeignKey('accounting.Tax',
                                on_delete=models.PROTECT,
                                limit_choices_to={'tax_type': Tax.TaxType.IVA},
                                help_text='El tipo de IVA aplicado a esta línea',
                                related_name='iva_tax_items',
                                verbose_name='IVA')
    irpf_tax = models.ForeignKey('accounting.Tax',
                                on_delete=models.PROTECT,
                                limit_choices_to={'tax_type': Tax.TaxType.IRPF},
                                help_text='El tipo de IRPF aplicado a esta línea',
                                related_name='irpf_tax_items',
                                verbose_name='IRPF')
    
    # Campos para "congelar" el valor del impuesto
    iva_percent = models.DecimalField(max_digits=5, decimal_places=2)
    irpf_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Campos calculados para esta línea
    line_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva_amount = models.DecimalField(max_digits=10, decimal_places=2)
    irpf_amount = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "Concepto"


    def save(self, *args, **kwargs):
        # Congelamos los porcentajes de impuestos
        self.iva_percent = self.iva_tax.percent
        if self.irpf_tax:
            self.irpf_percent = self.irpf_tax.percent
        else:
            self.irpf_percent = 0

        self.line_subtotal = self.quantity * self.unit_price
        self.iva_amount = self.line_subtotal * (self.iva_percent / 100)
        self.irpf_amount = self.line_subtotal * (self.irpf_percent / 100)
        self.line_total = self.line_subtotal + self.iva_amount - self.irpf_amount
        
        # Guardamos el objeto
        super().save(*args, **kwargs)
