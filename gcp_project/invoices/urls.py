from django.urls import path
from .views import InvoicesListView, InvoiceDetailView, invoice_pdf_view, InvoiceCreateView, InvoiceUpdateView, InvoiceDeleteView, InvoiceRectifyView

app_name = 'invoices'

urlpatterns = [
    path('', InvoicesListView.as_view(), name='invoices'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('<int:pk>/pdf/', invoice_pdf_view, name='invoice_pdf'),
    path('create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('<int:pk>/rectify/', InvoiceRectifyView.as_view(), name='invoice_rectify'),
]
