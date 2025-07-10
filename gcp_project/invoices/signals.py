from django.db.models.signals import post_save, post_delete
from django.db.models import Sum, F
from django.dispatch import receiver
from .models import Invoice, InvoiceItem

@receiver([post_save, post_delete], sender=InvoiceItem)
def update_invoice_totals(sender, instance, **kwargs):
    """
    Cuando un InvoiceItem se guarda o se borra, recalcula los
    totales de la factura padre.
    """
    invoice = instance.invoice

    # Usamos la agregación de Django para sumar todos los items de la factura
    totals = invoice.items.aggregate(
        line_subtotal=Sum('line_subtotal'),
        total_iva=Sum('iva_amount'),
        total_irpf=Sum('irpf_amount')
    )

    invoice.subtotal = totals['line_subtotal'] or 0
    invoice.total_iva = totals['total_iva'] or 0
    invoice.total_irpf = totals['total_irpf'] or 0
    invoice.total = invoice.subtotal + invoice.total_iva - invoice.total_irpf
    
    # Usamos update en lugar de save para evitar bucles de señales
    Invoice.objects.filter(pk=invoice.pk).update(
        subtotal=invoice.subtotal,
        total_iva=invoice.total_iva,
        total_irpf=invoice.total_irpf,
        total=invoice.total
    )
