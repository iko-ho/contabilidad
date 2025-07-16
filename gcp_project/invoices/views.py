from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Invoice
from .forms import InvoiceForm, InvoiceItemFormSet


class InvoicesListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoices/invoices_list.html'
    context_object_name = 'invoices'

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
    context_object_name = 'invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice_items'] = self.object.items.all()
        return context
    
    def get_queryset(self):
        """
        ¡CRÍTICO! Filtramos para que el usuario solo vea sus propias facturas.
        """
        return Invoice.objects.filter(user=self.request.user)

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva Factura junto con sus líneas.
    """
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoices:invoices') # Redirige a la lista de facturas

    def get_form_kwargs(self):
        """
        Pasa el usuario logueado como argumento al constructor del formulario.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Añade el formset de las líneas de factura al contexto.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InvoiceItemFormSet(self.request.POST, prefix='items')
        else:
            context['formset'] = InvoiceItemFormSet(prefix='items')
        return context

    def form_valid(self, form):
        """
        Se ejecuta cuando el formulario principal (InvoiceForm) es válido.
        Aquí gestionamos el guardado del formulario principal y del formset.
        """
        context = self.get_context_data()
        formset = context['formset']
        
        # Usamos una transacción atómica para asegurar que si algo falla,
        # no se guarde nada en la base de datos.
        with transaction.atomic():
            # Asignamos el usuario a la factura antes de guardarla.
            form.instance.user = self.request.user
            self.object = form.save() # Guardamos la factura

            if formset.is_valid():
                # Vinculamos el formset a la instancia de la factura recién creada
                # y guardamos las líneas.
                formset.instance = self.object
                formset.save()
                # --- Recargamos los totales desde la BD ---
                self.object.refresh_from_db(fields=['subtotal', 'total_iva', 'total_irpf', 'total'])
            else:
                # Si el formset no es válido, devolvemos el formulario con los errores.
                return self.form_invalid(form)

        # Redirigimos directamente para evitar que super().form_valid() guarde de nuevo
        # el formulario principal con los totales antiguos, sobrescribiendo los que
        # ha calculado la señal.
        return HttpResponseRedirect(self.get_success_url())


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar una Factura existente y sus líneas.
    """
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'

    def get_queryset(self):
        """
        Aseguramos que el usuario solo pueda editar sus propias facturas.
        """
        return Invoice.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        """
        Pasa el usuario logueado al formulario.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Añade el formset, pero esta vez vinculado a la factura existente.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InvoiceItemFormSet(self.request.POST, instance=self.object, prefix='items')
        else:
            context['formset'] = InvoiceItemFormSet(instance=self.object, prefix='items')
        return context

    def form_valid(self, form):
        """
        Misma lógica de guardado atómico que en la creación.
        """
        context = self.get_context_data()
        formset = context['formset']
        
        with transaction.atomic():
            self.object = form.save() # Guardamos los cambios de la factura

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                # --- Recargamos los totales desde la BD ---
                self.object.refresh_from_db(fields=['subtotal', 'total_iva', 'total_irpf', 'total'])
            else:
                return self.form_invalid(form)

        # Redirigimos directamente para evitar que super().form_valid() guarde de nuevo
        # el formulario principal con los totales antiguos.
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self) -> str:
        # Redirige a la factura actualizada después de guardar.
        return reverse_lazy('invoices:invoice_detail', kwargs={'pk': self.object.pk})


class InvoiceRectifyView(LoginRequiredMixin, UpdateView):
    """
    Vista para emitir una Factura Rectificativa.
    """
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'

    def get_queryset(self):
        """
        Aseguramos que el usuario solo pueda emitir rectificaciones de sus propias facturas emitidas.
        """
        return Invoice.objects.filter(user=self.request.user, status=Invoice.Status.ISSUED)

    def get_form_kwargs(self):
        """
        Pasa el usuario logueado al formulario, el estado de la factura rectificativa y la factura a la que se rectifica.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['status'] = Invoice.Status.RECTIFIED
        kwargs['type'] = Invoice.InvoiceType.RECTIFICATIVE
        kwargs['original_invoice'] = self.get_object() # Factura a la que se rectifica
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Añade el formset, pero esta vez vinculado a la factura existente.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InvoiceItemFormSet(self.request.POST, instance=self.object, prefix='items')
        else:
            context['formset'] = InvoiceItemFormSet(instance=self.object, prefix='items')
        return context

    def get_success_url(self) -> str:
        # Redirige a la factura rectificativa después de guardar.
        return reverse_lazy('invoices:invoice_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """
        Misma lógica de guardado atómico que en la creación.
        """
        context = self.get_context_data()
        formset = context['formset']
        
        with transaction.atomic():
            self.object = form.save() # Guardamos los cambios de la factura

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                # --- Recargamos los totales desde la BD ---
                self.object.refresh_from_db(fields=['subtotal', 'total_iva', 'total_irpf', 'total'])
            else:
                return self.form_invalid(form)

        # Redirigimos directamente para evitar que super().form_valid() guarde de nuevo
        # el formulario principal con los totales antiguos.
        return HttpResponseRedirect(self.get_success_url())


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una Factura existente.
    """
    model = Invoice
    template_name = 'invoices/invoice_confirm_delete.html'
    success_url = reverse_lazy('invoices:invoices')

    def get_queryset(self):
        """
        Aseguramos que el usuario solo pueda eliminar sus propias facturas.
        """
        return Invoice.objects.filter(user=self.request.user)


def invoice_pdf_view(request, pk):
    """
    Genera o sirve el PDF de una factura, dependiendo de su estado.
    """
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)

    # --- Lógica de Decisión ---

    # CASO 1: La factura está emitida y tiene su PDF guardado.
    if invoice.status == Invoice.Status.ISSUED and invoice.pdf_file:
        return FileResponse(invoice.pdf_file.open(), as_attachment=True, filename=invoice.pdf_file.name)
    
    # CASO 2: La factura es un borrador o una proforma.
    elif invoice.status in [Invoice.Status.DRAFT, Invoice.Status.PROFORMA]:
        # Generamos el PDF al vuelo y lo servimos
        # No lo guardamos en el modelo, solo lo generamos en el momento de la solicitud.
        html_string = render_to_string('invoices/invoice_pdf.html', {
            'invoice': invoice,
            'invoice_items': invoice.items.all()
        })
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        # El nombre del archivo reflejará si es una proforma o un borrador
        file_name = f"{invoice.issue_date.year}{invoice.issue_date.month}{invoice.issue_date.day} {invoice.client.razon_social} {invoice.status}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    
    # CASO 3: La factura no está emitida.
    else:
        # Si la factura no está emitida, no tiene PDF. Devolvemos un error 404.
        # Podríamos también mostrar un mensaje o generar una vista previa.
        raise Http404(f"El PDF para la factura {invoice.invoice_number} no está disponible en su estado actual.")