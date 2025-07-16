# **Gestión Contable Pro (GCP)**

GCP (Gestión Contable Pro) es una aplicación web de contabilidad y facturación diseñada a medida para profesionales y autónomos en España. El objetivo principal es simplificar la gestión de ingresos, gastos y la preparación de impuestos trimestrales y anuales, con una interfaz limpia e intuitiva.

Este proyecto nace como una solución robusta y escalable, construida con Django, pensando en la seguridad, la integridad de los datos y futuras integraciones.

## **✨ Características Principales**

* **Gestión de Ingresos:**
    * Creación y gestión de Clientes.
    * Generación de Presupuestos y Facturas Proforma.
    * Conversión de Presupuestos a Facturas con un solo clic.
    * Creación de Facturas con cálculo automático de IVA e IRPF.
    * Numeración de facturas automática y correlativa.
    * Cambio de estado de facturas (Borrador, Emitida, Pagada, Vencida).
    * Generación de facturas en formato PDF.
    * Envío de facturas por correo electrónico directamente desde la aplicación.
* **Gestión de Gastos:**
    * Creación y gestión de Proveedores.
    * Registro manual de gastos.
    * Categorización de gastos para un mejor análisis.
* **Informes y Fiscalidad:**
    * Panel de control (Dashboard) con un resumen visual del estado financiero.
    * Informe de resultados (P&G) filtrable por periodos.
    * Informes trimestrales y anuales para la declaración de IVA e IRPF.
    * Listado de facturas pendientes de cobro.

## **🛠️ Stack Tecnológico**

* **Backend:** Python 3.x, Django 5.x
* **Base de Datos:** PostgreSQL (recomendado para producción), SQLite (para desarrollo local)
* **Frontend:** Plantillas de Django con HTML, CSS y una pizca de JavaScript. (Potencialmente se usará Bootstrap o TailwindCSS para el estilo).
* **Generación de PDF:** WeasyPrint / ReportLab
* **API:** Django Rest Framework (DRF)
* **Entorno:** Python Virtual Environment (venv)

## **🚀 Cómo Empezar (Configuración Local)**

Sigue estos pasos para poner en marcha el entorno de desarrollo en tu máquina local.

1.  **Clona el repositorio:**
    ```bash
    git clone [URL-DE-TU-REPOSITORIO-EN-GITHUB]
    cd [NOMBRE-DEL-PROYECTO]
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # En Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    > *Nota: Crearemos este archivo con `pip freeze > requirements.txt` después de instalar las librerías iniciales.*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto a partir del archivo `.env.example`. Contendrá la configuración de la base de datos, la `SECRET_KEY` de Django, etc.

5.  **Aplica las migraciones de la base de datos:**
    Este comando creará las tablas en tu base de datos según los modelos definidos.
    ```bash
    python manage.py migrate
    ```

6.  **Crea un superusuario:**
    Para poder acceder al panel de administrador de Django.
    ```bash
    python manage.py createsuperuser
    ```

7.  **Inicia el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en http://127.0.0.1:8000. El panel de administrador estará en http://127.0.0.1:8000/admin.

## **📂 Estructura del Proyecto**

El proyecto seguirá una estructura modular basada en aplicaciones de Django para mantener el código organizado y desacoplado.


gcp_project/
├── core/         # App para la configuración principal, modelos base, etc.
├── contacts/     # App para la gestión de contactos (clientes y proveedores).
├── invoices/     # App para toda la lógica de ingresos (presupuestos y facturas).
├── expenses/     # App para la lógica de gastos (registro de gastos).
├── reports/      # App para la generación de informes y vistas fiscales.
├── api/          # App para la API REST (serializers, viewsets).
├── templates/    # Directorio para las plantillas HTML base.
├── static/       # Directorio para archivos estáticos (CSS, JS, imágenes).
└── gcp_project/  # Directorio principal del proyecto (settings.py, urls.py).

## **🗺️ Roadmap de Desarrollo y Checklist de Tareas**

Seguiremos un plan de desarrollo por fases para construir la aplicación de manera incremental. Cada fase tiene una checklist de tareas detallada.

<details>
<summary><strong>✅ Fase 0: Cimentación del Proyecto</strong></summary>

* **Objetivo:** Preparar el terreno para un buen comienzo que nos ahorrará dolores de cabeza.
* [X] **Planificación:** Diseño de la Base de Datos, definición de la arquitectura y creación del repositorio Git.
* [X] **Inicializar el proyecto Django:** Crear la estructura del proyecto y la primera app (`core`).
* [X] **Configurar el entorno:**
    * [X] Crear y activar el entorno virtual (`venv`).
    * [x] Crear el repositorio Git desde el día uno.
    * [X] Instalar Django y generar el `requirements.txt` inicial.
* [ ] **Diseño de Modelos (v1.0):**
    * [X] `User`: Utilizar el modelo de usuario por defecto de Django.
    * [X] `Client`: Tabla para clientes (NIF, nombre, dirección, etc.).
    * [X] `Provider`: Tabla para proveedores.
    * [X] `Invoice` / `InvoiceItem`: Tablas para facturas y sus líneas, incluyendo campos clave como `numero_factura`, `estado`, y campos `DecimalField` para los importes.
    * [ ] `Expense`: Tabla para gastos, con relación a proveedores y categorías.
* [ ] **Configurar el Panel de Administrador de Django:** Habilitar el admin para poder gestionar los modelos básicos desde el principio.

</details>

<details>
<summary><strong>🔲 Fase 1: Módulo de Ingresos</strong></summary>

* **Objetivo:** Poder crear, gestionar y enviar todo el ciclo de ingresos.

* **Sub-fase 1.1: Estructura de Datos (Modelos)**
    * [X] **Crear la app `invoices`** y añadirla a `INSTALLED_APPS`.
    * [X] **Definir el modelo `Client`** en `invoices/models.py`.
    * [X] **Definir el modelo `Invoice`** con su relación a `Client`, los estados (`Status` con `TextChoices`) y los campos monetarios como `DecimalField`.
    * [X] **Definir el modelo `InvoiceItem`** con su relación a `Invoice`.
    * [X] **Implementar el método `__str__`** en todos los modelos para una mejor representación.
    * [X] **Implementar el auto-cálculo del `total_linea`** en el método `save()` del modelo `InvoiceItem`.

* **Sub-fase 1.2: Integración con el Admin**
    * [X] **Registrar el modelo `Client`** en `invoices/admin.py`.
    * [X] **Crear una clase `InvoiceItemInline`** (`admin.TabularInline`) para gestionar las líneas desde la factura.
    * [X] **Registrar el modelo `Invoice`** con una clase `InvoiceAdmin` que use la `inline` anterior.
    * [X] **Mejorar la vista de lista de `InvoiceAdmin`** con `list_display` (`numero_factura`, `cliente`, `fecha_emision`, `total`, `estado`).

* **Sub-fase 1.3: Migraciones y Pruebas**
    * [X] **Generar el archivo de migración** para la app `invoices` (`makemigrations`).
    * [X] **Aplicar la migración a la base de datos** (`migrate`).
    * [X] **Probar manualmente en el admin:** Crear Clientes y Facturas con sus líneas.

* **Sub-fase 1.4: Lógica de Negocio**
    * [X] **Numeración automática de facturas:** Implementar la lógica para generar un número correlativo (ej: '2025-001') en el método `save()` de `Invoice` cuando deja de ser borrador.
    * [X] **Cálculo automático de totales en la factura:** Usar Señales de Django (`post_save`, `post_delete` en `InvoiceItem`) para llamar a un método en `Invoice` que actualice la base imponible, el IVA y el total de la factura.
        > **Nota del Senior:** El uso de Señales es la solución ideal y más robusta para mantener los totales de la factura siempre sincronizados sin esfuerzo manual.

* **Sub-fase 1.5: Generación de Documentos**
    * [X] **Instalar una librería de generación de PDF** (ej: `weasyprint`).
    * [X] **Crear una vista en Django** que reciba el ID de una factura.
    * [X] **Crear una plantilla HTML** con la estructura de una factura real.
    * [X] **Configurar la vista** para renderizar el HTML y convertirlo a una respuesta HTTP con el PDF.
    * [X] **Añadir una URL** que apunte a esta vista (ej: `/invoices/<int:pk>/pdf/`).
    * [X] **Implementar el almacenamiento del PDF:** Al emitir la factura, guardar el PDF generado en el servidor y vincularlo a la factura en la BD con un campo `FileField`.

</details>

<details>
<summary><strong>🔲 Fase 2: Módulo de Gastos</strong></summary>

* **Objetivo:** Tener un registro claro y categorizado de todos los gastos profesionales.

* **Sub-fase 2.1: Estructura de Datos (Modelos)**
    * [ ] **Crear la app `expenses`** y añadirla a `INSTALLED_APPS`.
    * [ ] **Definir el modelo `Provider`**.
    * [ ] **Definir el modelo `ExpenseCategory`**.
    * [ ] **Definir el modelo `Expense`**, asegurando las relaciones con `User`, `Provider` y `ExpenseCategory`, y usando `DecimalField` para los importes.
    * [ ] **Implementar el método `save()`** en el modelo `Expense` para calcular el total a partir de la base y el IVA.

* **Sub-fase 2.2: Integración con el Admin**
    * [ ] **Registrar los modelos `Provider` y `ExpenseCategory`**.
    * [ ] **Crear una clase `ExpenseAdmin`** con `list_display`, `list_filter` y `search_fields` para una gestión cómoda.

* **Sub-fase 2.3: Migraciones y Pruebas**
    * [ ] **Generar y aplicar las migraciones** para la app `expenses`.
    * [ ] **Probar en el admin:** Crear categorías, proveedores y registrar gastos para verificar que todo funciona.

* **Sub-fase 2.4: Interfaz de Usuario (Views, Forms, Templates)**
    * [ ] **Crear `ExpenseForm`** usando `ModelForm`.
    * [ ] **Crear las vistas `ExpenseListView` y `ExpenseCreateView`**.
        * En `ExpenseListView`, sobrescribir `get_queryset` para filtrar por el usuario logueado.
        * En `ExpenseCreateView`, sobrescribir `form_valid` para asignar el usuario actual al gasto.
    * [ ] **Crear las URLs** en `expenses/urls.py` e incluirlas en el proyecto principal.
    * [ ] **Crear las plantillas HTML** `expense_list.html` y `expense_form.html`.

</details>

<details>
<summary><strong>🔲 Fase 3: Módulo de Informes y Fiscalidad</strong></summary>

* **Objetivo:** Darte la visión financiera que necesitas para tomar decisiones y cumplir con tus obligaciones fiscales.

* **Sub-fase 3.1: Preparación de la App**
    * [ ] **Crear la app `reports`** y añadirla a `INSTALLED_APPS`.
    * [ ] **Crear la estructura de URLs** para el dashboard en `/informes/`.
    * [ ] **Crear la vista `DashboardView`** y la plantilla `dashboard.html`.

* **Sub-fase 3.2: Lógica de Negocio (Consultas)**
    > **Nota del Senior:** Es una buena práctica crear un archivo `reports/utils.py` para alojar estas funciones de consulta, manteniendo las vistas limpias.
    * [ ] **Implementar la función `get_profit_loss_data(start_date, end_date)`** para calcular ingresos (de facturas pagadas), gastos y el beneficio.
    * [ ] **Implementar la función `get_vat_data(start_date, end_date)`** para calcular el IVA Repercutido (de facturas emitidas) y el IVA Soportado (de gastos).
    * [ ] **Implementar la función `get_unpaid_invoices()`** para obtener un listado de facturas emitidas o vencidas, ordenadas por fecha.

* **Sub-fase 3.3: Construcción del Dashboard (Frontend)**
    * [ ] **Modificar `DashboardView`** para que maneje un formulario de fechas (GET), llame a las funciones de `utils.py` y pase los datos al contexto.
    * [ ] **Desarrollar la plantilla `dashboard.html`:**
        * [ ] Añadir un formulario con filtros de fecha.
        * [ ] Mostrar los KPIs de P&G e IVA en tarjetas destacadas.
        * [ ] Mostrar una tabla con las facturas pendientes de cobro, con enlaces a cada una.
* **(Opcional) Sub-fase 3.4: Gráficos**
    * [ ] **Integrar una librería de gráficos JS** (ej: Chart.js).
    * [ ] **Crear un endpoint en Django** que devuelva datos mensuales en formato JSON.
    * [ ] **Usar `fetch` en el frontend** para llamar a ese endpoint y renderizar un gráfico.

</details>

<details>
<summary><strong>🔲 Fase 4: Profesionalización y Futuro</strong></summary>

* **Objetivo:** Refactorizar el código para hacerlo más robusto, construir una API REST para futuras integraciones y preparar el proyecto para producción.

* **Sub-fase 4.1: Refactorización**
    * [ ] **Crear archivos `services.py`** en las apps `invoices` y `expenses`.
    * [ ] **Mover la lógica de negocio** (ej: creación de facturas, cálculos complejos) de las vistas a funciones en estos archivos de servicio.
    * [ ] **Refactorizar las vistas** para que sean más "delgadas", llamando a las funciones de servicio.

* **Sub-fase 4.2: Construcción de la API con DRF**
    * [ ] **Instalar y configurar Django Rest Framework** (`pip install djangorestframework`).
    * [ ] **Crear archivos `serializers.py`** en las apps y definir los `ModelSerializer` para los modelos principales.
    * [ ] **Crear archivos `api_views.py`** e implementar los `ModelViewSet` para cada serializer.
    * [ ] **Configurar las URLs de la API** usando un `DefaultRouter` bajo el prefijo `/api/v1/`.

* **Sub-fase 4.3: Documentación y Prueba de la API**
    * [ ] **Instalar y configurar `drf-spectacular`** para generar documentación OpenAPI (Swagger UI) automáticamente.
    * [ ] **Probar todos los endpoints CRUD** (GET, POST, PUT, DELETE) para los recursos principales (invoices, expenses, etc.) usando Swagger UI o Postman.

* **Sub-fase 4.4: Preparación para Producción**
    * [ ] **Generar el archivo `requirements.txt` final**.
    * [ ] **Mover datos sensibles** (SECRET_KEY, DEBUG, DB config) a un archivo `.env` usando `django-environ`.
    * [ ] **Configurar `settings.py` para producción:** `DEBUG=False`, `ALLOWED_HOSTS` leídos desde `.env`.
    * [ ] **Configurar WhiteNoise** para el servicio de archivos estáticos.
    * [ ] **Definir y documentar una estrategia de backup** para la base de datos.

</details>

## **🏗️ Arquitectura para el Futuro**

El trabajo realizado en la Fase 4, especialmente la creación de la API REST, sienta las bases para futuras ampliaciones:

* **Interfaz de Escritorio (PySide):** Una futura aplicación de escritorio se comunicará con el servidor a través de esta API, leyendo y escribiendo datos de forma segura y estandarizada.
* **Integración con Terceros:** Si otra aplicación necesita interactuar con los datos (ej: crear una factura), podrá hacerlo llamando a los endpoints de nuestra API.
* **OCR de Tickets:** Una futura app móvil podrá tomar una foto de un ticket, procesarla y usar la API para registrar el gasto en el sistema (`POST /api/v1/expenses/`).

## **🤝 Contribuciones**

Este es un proyecto en desarrollo. Para contribuir:

1.  Crea una nueva rama para tu feature o bugfix: `git checkout -b feature/nombre-feature`
2.  Haz tus cambios y realiza commits atómicos.
3.  Abre un Pull Request contra la rama `develop`.