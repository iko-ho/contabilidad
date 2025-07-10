from django.db import models
from django.conf import settings


# ---- SHARE CLASSES (DRY) ----
class IDType(models.TextChoices):
    """
    Tipos de documentos de identificación compartidos por Clientes y Proveedores.
    Definido una sola vez aquí para no repetir código.
    """
    NIF = 'NIF', 'NIF'
    CIF = 'CIF', 'CIF'
    NIE = 'NIE', 'NIE'
    PASSPORT = 'PASSPORT', 'Pasaporte'
    DRIVERS_LICENSE = 'DRIVERS_LICENSE', 'Licencia de conducir'
    SOCIAL_SECURITY_CARD = 'SOCIAL_SECURITY_CARD', 'Tarjeta de Seguridad Social'


class Group(models.Model):
    name = models.CharField(max_length=100, help_text='Nombre del grupo')
    description = models.TextField(blank=True, help_text='Descripción del grupo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']


# ---- ABSTRACT MODEL BASE ----
class BaseContact(models.Model):
    """
    Modelo base para Clientes y Proveedores.
    """
    class PersonType(models.TextChoices):
        NATURAL = 'NATURAL', 'Persona Natural'
        JURIDICA = 'JURIDICA', 'Persona Jurídica'

    person_type = models.CharField(max_length=10, choices=PersonType.choices, default=PersonType.NATURAL, help_text='Indica si el contacto es una persona física o una empresa')
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    razon_social = models.CharField(max_length=255, help_text='Para empresas: Razón Social completa. Para personas físicas: Nombre y Apellidos completos.')
    nombre_comercial = models.CharField(max_length=255, blank=True, help_text='Nombre comercial o alias con el que se conoce al contacto (opcional).')    

    id_type = models.CharField(max_length=20, choices=IDType.choices, default=IDType.NIF, help_text='Tipo de documento')
    id_number = models.CharField(max_length=20, help_text='Número de documento')
    
    address = models.CharField(max_length=100, blank=True, help_text='Dirección del cliente')
    city = models.CharField(max_length=50, blank=True, help_text='Ciudad del cliente')
    province = models.CharField(max_length=50, blank=True, help_text='Provincia del cliente')
    zip_code = models.CharField(max_length=5, blank=True, help_text='Código postal del cliente')
    country = models.CharField(max_length=50, blank=True, help_text='País del cliente')
    
    phone = models.CharField(max_length=15, blank=True, help_text='Teléfono del cliente')
    email = models.EmailField(blank=True, help_text='Email del cliente')
    notes = models.TextField(blank=True, help_text='Notas del cliente')
    
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, blank=True, null=True, help_text='Grupo al que pertenece el cliente')
    
    def __str__(self):
        if self.nombre_comercial:
            return f"{self.razon_social} ({self.nombre_comercial})"
        else:
            return self.razon_social
    
    class Meta:
        abstract = True
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['razon_social']

# ---- FINAL MODELS ----
class Client(BaseContact):
    """
    Modelo para los Clientes. Hereda todos los campos de BaseContact.
    Aquí podríamos añadir campos que sean EXCLUSIVOS para clientes.
    """
    # Ejemplo de campo solo para clientes:
    # dias_de_pago_preferidos = models.IntegerField(default=30)
    default_iva_tax = models.ForeignKey('accounting.Tax', on_delete=models.SET_NULL, blank=True, null=True, help_text='IVA por defecto', related_name='default_iva_tax_client')
    default_irpf_tax = models.ForeignKey('accounting.Tax', on_delete=models.SET_NULL, blank=True, null=True, help_text='IRPF por defecto', related_name='default_irpf_tax_client')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

        # Evita que un mismo usuario cree dos clientes con el mismo id_number
        constraints = [
            models.UniqueConstraint(fields=['user', 'id_number'], name='unique_client_id_per_user')
        ]


class Provider(BaseContact):
    """
    Modelo para los Proveedores. Hereda todos los campos de BaseContact.
    Aquí podríamos añadir campos que sean EXCLUSIVOS para proveedores.
    """
    # Ejemplo de campo solo para proveedores:
    # dias_de_pago_preferidos = models.IntegerField(default=30)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

        # Evita que un mismo usuario cree dos proveedores con el mismo id_number
        constraints = [
            models.UniqueConstraint(fields=['user', 'id_number'], name='unique_provider_id_per_user')
        ]
