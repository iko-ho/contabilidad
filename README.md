Gestión Contable Pro (GCP)

GCP (Gestión Contable Pro) es una aplicación web de contabilidad y facturación diseñada a medida para profesionales y autónomos en España. El objetivo principal es simplificar la gestión de ingresos, gastos y la preparación de impuestos trimestrales y anuales, con una interfaz limpia e intuitiva.

Este proyecto nace como una solución robusta y escalable, construida con Django, pensando en la seguridad, la integridad de los datos y futuras integraciones.
✨ Características Principales (Roadmap v1.0)

    Gestión de Ingresos:
        Creación y gestión de Clientes.
        Generación de Presupuestos y Facturas Proforma.
        Conversión de Presupuestos a Facturas con un solo clic.
        Creación de Facturas con cálculo automático de IVA e IRPF.
        Numeración de facturas automática y correlativa.
        Cambio de estado de facturas (Borrador, Emitida, Pagada, Vencida).
        Generación de facturas en formato PDF.
        Envío de facturas por correo electrónico directamente desde la aplicación.
    Gestión de Gastos:
        Creación y gestión de Proveedores.
        Registro manual de gastos.
        Categorización de gastos para un mejor análisis.
    Informes y Fiscalidad:
        Panel de control (Dashboard) con un resumen visual del estado financiero.
        Informe de resultados (P&amp;G) filtrable por periodos.
        Informes trimestrales y anuales para la declaración de IVA e IRPF.
        Listado de facturas pendientes de cobro.

🛠️ Stack Tecnológico

    Backend: Python 3.x, Django 5.x
    Base de Datos: PostgreSQL (recomendado para producción), SQLite (para desarrollo local)
    Frontend: Plantillas de Django con HTML, CSS y una pizca de JavaScript. (Potencialmente se usará Bootstrap o TailwindCSS para el estilo).
    Generación de PDF: WeasyPrint / ReportLab
    Entorno: Python Virtual Environment (venv)

🚀 Cómo Empezar (Configuración Local)

Sigue estos pasos para poner en marcha el entorno de desarrollo en tu máquina local.

    Clona el repositorio:
    Bash

git clone [URL-DE-TU-REPOSITORIO-EN-GITHUB]
cd [NOMBRE-DEL-PROYECTO]

Crea y activa un entorno virtual:
Bash

# En Windows
python -m venv .venv
.\.venv\Scripts\activate

# En macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

Instala las dependencias:
Todas las librerías necesarias se encuentran en requirements.txt.
Bash

pip install -r requirements.txt

(Nota: Crearemos este archivo con pip freeze > requirements.txt después de instalar Django).

Configura las variables de entorno:
Crea un archivo .env en la raíz del proyecto a partir del archivo .env.example (que crearemos). Contendrá la configuración de la base de datos, la SECRET_KEY de Django, etc.

Aplica las migraciones de la base de datos:
Este comando creará las tablas en tu base de datos según los modelos definidos.
Bash

python manage.py migrate

Crea un superusuario:
Para poder acceder al panel de administrador de Django.
Bash

python manage.py createsuperuser

Inicia el servidor de desarrollo:
Bash

    python manage.py runserver

    La aplicación estará disponible en http://127.0.0.1:8000. El panel de administrador estará en http://127.0.0.1:8000/admin.

📂 Estructura del Proyecto

El proyecto seguirá una estructura modular basada en aplicaciones de Django para mantener el código organizado y desacoplado.

gcp_project/
├── core/         # App para la configuración principal, modelos base, etc.
├── invoices/     # App para toda la lógica de ingresos (clientes, presupuestos, facturas).
├── expenses/     # App para la lógica de gastos (proveedores, registro de gastos).
├── reports/      # App para la generación de informes y vistas fiscales.
├── templates/    # Directorio para las plantillas HTML base.
├── static/       # Directorio para archivos estáticos (CSS, JS, imágenes).
└── gcp_project/  # Directorio principal del proyecto (settings.py, urls.py).

🗺️ Roadmap de Desarrollo

Seguiremos un plan de desarrollo por fases para construir la aplicación de manera incremental.

    🔲 Fase 0: Cimentación del Proyecto.
        * Setup inicial, configuración de Django, diseño de la BD y repositiorio Git.
    🔲 Fase 1: Módulo de Ingresos.
            * Modelos de datos para Clientes, Facturas y Líneas de Factura.
            * Lógica de negocio para cálculos y numeración.
            * Generación de PDF y envío por email.
    🔲 Fase 2: Módulo de Gastos.
            * Modelos y gestión para Proveedores, Categorías y Gastos.
            * Interfaz de usuario para registrar y listar gastos.
    🔲 Fase 3: Módulo de Informes y Fiscalidad.
        * Creación de los informes de P&amp;G, IVA e IRPF. Dashboard principal.
    🔲 Fase 4: Planificación para el Futuro.
        * Refactorizar el código para facilitar la creación de una API REST con DRF en el futuro.

🏛️ Arquitectura para el Futuro

El trabajo realizado en la Fase 4, especialmente la creación de la API REST, sienta las bases para futuras ampliaciones:

* **Interfaz de Escritorio (PySide):** Una futura aplicación de escritorio se comunicará con el servidor a través de esta API, leyendo y escribiendo datos de forma segura y estandarizada.
* **Integración con Terceros:** Si otra aplicación (como un software de gestión de despachos) necesita crear una factura, podrá hacerlo llamando al endpoint `/api/v1/invoices/` de nuestra API.
* **OCR de Tickets:** Una futura app móvil podrá tomar una foto de un ticket, procesarla y usar la API para registrar el gasto en el sistema (`POST /api/v1/expenses/`).


🤝 Contribuciones

Este es un proyecto en desarrollo. Para contribuir:

    Crea una nueva rama para tu feature o bugfix: git checkout -b feature/nombre-feature
    Haz tus cambios y realiza commits atómicos.
    Abre un Pull Request contra la rama develop.


# Checklist de Tareas: Fase 1 - Módulo de Ingresos

**Objetivo:** Implementar toda la funcionalidad de backend necesaria para crear y gestionar clientes y facturas, incluyendo la lógica de negocio clave, antes de construir la interfaz de usuario.

### Sub-fase 1.1: Estructura de Datos (Modelos)

-   [ ] **Crear la app `invoices`** y añadirla a `INSTALLED_APPS`.
-   [ ] **Definir el modelo `Client`** en `invoices/models.py` con los campos necesarios (nombre\_fiscal, nif, etc.).
-   [ ] **Definir el modelo `Invoice`** con su relación a `Client`, los estados (`Status` con `TextChoices`), y los campos monetarios como `DecimalField`.
-   [ ] **Definir el modelo `InvoiceItem`** con su relación a `Invoice` y los campos para el cálculo de cada línea.
-   [ ] **Implementar el método `__str__`** en todos los modelos para una mejor representación en el admin.
-   [ ] **Implementar el auto-cálculo del `total_linea`** en el método `save()` del modelo `InvoiceItem`.

### Sub-fase 1.2: Integración con el Panel de Administrador

-   [ ] **Registrar el modelo `Client`** en `invoices/admin.py`.
-   [ ] **Registrar el modelo `Invoice`** usando `@admin.register` para una configuración avanzada.
-   [ ] **Crear una clase `InvoiceItemInline`** (`admin.TabularInline`) para gestionar las líneas de factura directamente desde la vista de la factura.
-   [ ] **Añadir la `inline` a la clase `InvoiceAdmin`**.
-   [ ] **Mejorar la vista de lista de `InvoiceAdmin`** con `list_display` para ver información relevante de un vistazo.

### Sub-fase 1.3: Migraciones y Pruebas Iniciales

-   [ ] **Generar el archivo de migración** para la app `invoices` (`makemigrations`).
-   [ ] **Aplicar la migración a la base de datos** (`migrate`).
-   [ ] **Probar manualmente en el admin:**
    -   [ ] Crear un Cliente.
    -   [ ] Crear una Factura para ese cliente.
    -   [ ] Añadir varias líneas a esa factura desde la misma página.
    -   [ ] Verificar que el `total_linea` de cada ítem se calcula correctamente al guardar.

### Sub-fase 1.4: Lógica de Negocio (El "Cerebro")

-   [ ] **Numeración automática de facturas:**
    -   Investigar cómo obtener el último número de factura y generar el siguiente (Ej: `2025-001`, `2025-002`).
    -   Implementar esta lógica en el método `save()` del modelo `Invoice`, asegurándose de que solo se asigne un número la primera vez que la factura deja de ser un borrador.
-   [ ] **Cálculo automático de totales en la factura:**
    -   Crear un método en el modelo `Invoice` (ej: `update_totals()`) que calcule la `base_imponible`, el `iva` y el `total` sumando los totales de todas sus `InvoiceItem` asociadas.
    -   **Investigar e implementar Señales de Django (Signals):** Usar las señales `post_save` y `post_delete` en el modelo `InvoiceItem` para que, cada vez que una línea de factura se guarde o se borre, se llame automáticamente al método `update_totals()` de la factura padre. Esto mantiene los datos siempre sincronizados.

### Sub-fase 1.5: Generación de Documentos

-   [ ] **Instalar una librería de generación de PDF** (ej: `pip install weasyprint`).
-   [ ] **Crear una vista en Django** que reciba el ID de una factura.
-   [ ] **Crear una plantilla HTML** con la estructura de una factura real (con tus datos, los del cliente, las líneas de la factura, totales, etc.).
-   [ ] **Configurar la vista** para que renderice esa plantilla HTML y la convierta a un PDF usando la librería instalada.
-   [ ] **Añadir una URL en `urls.py`** que apunte a esta vista (ej: `/invoice/<int:pk>/pdf/`).
-   [ ] **Probar** que al acceder a esa URL se descarga un PDF correcto de la factura.

---

Este desglose te da una hoja de ruta muy clara para esta fase. Te recomiendo que te centres ahora en la **Sub-fase 1.4**, que es la más desafiante y donde reside la verdadera lógica del negocio. Las Señales de Django son un concepto intermedio, pero son la solución perfecta y más elegante para este problema.

¡Por supuesto! Aquí tienes el checklist detallado para la Fase 2. Utilízalo como tu guía de trabajo para no dejarte nada en el tintero. Ve marcando las casillas a medida que completes cada tarea.


# Fase 2: Módulo de Gastos
✅ Checklist de Tareas: Fase 2 - Módulo de Gastos

Objetivo: Implementar la funcionalidad completa para registrar, categorizar y visualizar los gastos profesionales, incluyendo una interfaz de usuario básica.

Sub-fase 2.1: Estructura de Datos (Modelos)

    [ ] Crear la app expenses con el comando python manage.py startapp expenses.

    [ ] Añadir la app 'expenses' a la lista INSTALLED_APPS en gcp_project/settings.py.

    [ ] Definir el modelo Provider en expenses/models.py con sus campos correspondientes (nombre, nif, etc.).

    [ ] Definir el modelo ExpenseCategory en expenses/models.py.

    [ ] Definir el modelo Expense en expenses/models.py, asegurando:

        [ ] ForeignKey al usuario (settings.AUTH_USER_MODEL).

        [ ] ForeignKey a Provider.

        [ ] ForeignKey a ExpenseCategory.

        [ ] Uso de DecimalField para todos los campos monetarios (base_imponible, iva, total).

        [ ] Inclusión de un campo adjunto de tipo FileField para futuras implementaciones.

    [ ] Implementar el método __str__ en los tres modelos (Provider, ExpenseCategory, Expense) para una representación clara.

    [ ] Implementar el método save() en el modelo Expense para calcular el total automáticamente a partir de la base imponible y el IVA.

Sub-fase 2.2: Integración con el Panel de Administrador

    [ ] Crear el archivo expenses/admin.py.

    [ ] Registrar los modelos Provider y ExpenseCategory para que sean gestionables.

    [ ] Crear una clase ExpenseAdmin con el decorador @admin.register(Expense).

    [ ] Configurar list_display en ExpenseAdmin para mostrar columnas útiles (ej: fecha, concepto, categoria, total).

    [ ] Configurar list_filter en ExpenseAdmin para poder filtrar por categoria y fecha.

    [ ] Configurar search_fields en ExpenseAdmin para habilitar la búsqueda por concepto.

Sub-fase 2.3: Migraciones y Pruebas en el Admin

    [ ] Generar el archivo de migración para la app expenses con python manage.py makemigrations expenses.

    [ ] Aplicar la migración a la base de datos con python manage.py migrate.

    [ ] Realizar pruebas manuales en el panel de administrador:

        [ ] Acceder al panel (/admin).

        [ ] Crear al menos 3 ExpenseCategory (ej: Suministros, Dietas, Software).

        [ ] Crear un Provider de prueba.

        [ ] Crear un Expense completo, asociando la categoría y el proveedor creados.

        [ ] Verificar que el gasto aparece correctamente en la lista y que los filtros funcionan.

Sub-fase 2.4: Interfaz de Usuario (Views, Forms, Templates)

    [ ] Crear el archivo expenses/forms.py y definir la clase ExpenseForm usando ModelForm.

    [ ] Añadir el widget DateInput al campo fecha en ExpenseForm para una mejor experiencia de usuario.

    [ ] Crear las vistas basadas en clases en expenses/views.py:

        [ ] ExpenseListView (heredando de ListView) para mostrar la lista de gastos.

            [ ] Sobrescribir get_queryset para filtrar por el usuario logueado.

        [ ] ExpenseCreateView (heredando de CreateView) para el formulario de añadir gasto.

            [ ] Sobrescribir form_valid para asignar el usuario logueado al nuevo gasto.

    [ ] Crear el archivo expenses/urls.py con app_name y las rutas para las vistas de lista y creación.

    [ ] Incluir las URLs de la app expenses en el archivo principal gcp_project/urls.py.

    [ ] Crear el directorio expenses/templates/expenses/.

    [ ] Crear la plantilla expense_list.html para mostrar la tabla de gastos y un botón para "Añadir Gasto".

    [ ] Crear la plantilla expense_form.html para renderizar el formulario de creación.

    [ ] Probar el flujo completo como usuario final: navegar a /gastos/, ver la lista (inicialmente vacía) y añadir un nuevo gasto a través del formulario.

✅ Checklist de Tareas: Fase 3 - Módulo de Informes y Fiscalidad

Objetivo: Desarrollar un dashboard que presente informes financieros clave (P&G, IVA, Facturas Pendientes) de forma clara y útil, con filtros por fechas.

Sub-fase 3.1: Preparación y Entorno de la App

    [ ] Crear la app reports con python manage.py startapp reports.

    [ ] Añadir 'reports' a la lista INSTALLED_APPS en gcp_project/settings.py.

    [ ] Crear el archivo reports/urls.py y definir una ruta para el dashboard principal (ej: path('', DashboardView.as_view(), name='dashboard')).

    [ ] Incluir las URLs de reports en gcp_project/urls.py bajo el prefijo /reports/.

    [ ] Crear una vista inicial DashboardView en reports/views.py (puede heredar de TemplateView).

    [ ] Crear la plantilla base reports/templates/reports/dashboard.html.

Sub-fase 3.2: Lógica de Negocio y Consultas (Backend)

    [ ] Crear un archivo reports/utils.py para alojar la lógica de las consultas, manteniendo las vistas limpias.

    [ ] Implementar la función get_profit_loss_data(start_date, end_date) en utils.py:

        [ ] Realizar la agregación (Sum) sobre la base_imponible de las Invoice con estado 'Pagada' en el rango de fechas.

        [ ] Realizar la agregación (Sum) sobre el campo iva de las Invoice emitidas (estados 'Emitida', 'Pagada', 'Vencida') en el rango. -> IVA Repercutido.

        [ ] Realizar la agregación (Sum) sobre el campo iva de todos los Expense en el rango. -> IVA Soportado.

        [ ] Devolver un diccionario con {'total_ingresos': ..., 'total_gastos': ..., 'beneficio': ...}.

    [ ] Implementar la función get_vat_data(start_date, end_date) en utils.py:

        [ ] Realizar la agregación (Sum) sobre el campo iva de las Invoice emitidas (estados 'Emitida', 'Pagada', 'Vencida') en el rango. -> IVA Repercutido.

        [ ] Realizar la agregación (Sum) sobre el campo iva de todos los Expense en el rango. -> IVA Soportado.

        [ ] Devolver un diccionario con {'iva_repercutido': ..., 'iva_soportado': ..., 'resultado_iva': ...}.

    [ ] Implementar la función get_unpaid_invoices() en utils.py:

        [ ] Realizar una consulta (filter) sobre las Invoice con estado 'Emitida' o 'Vencida'.

        [ ] Ordenar el resultado (order_by) por fecha_vencimiento.

        [ ] Devolver el queryset resultante.

Sub-fase 3.3: Construcción del Dashboard (Frontend)

    [ ] Mejorar la vista DashboardView en reports/views.py:

        [ ] Añadir lógica para leer los parámetros start_date y end_date de la petición GET.

        [ ] Establecer un rango de fechas por defecto si no se proporcionan parámetros. (Pro-Tip: para hoy, 2 de Julio de 2025, un buen defecto sería el tercer trimestre: del 2025-07-01 al 2025-09-30).

        [ ] Importar y llamar a las funciones de reports/utils.py con el rango de fechas.

        [ ] Pasar todos los diccionarios de datos y el queryset de facturas impagadas al contexto de la plantilla.

    [ ] Desarrollar la plantilla dashboard.html:

        [ ] Crear un formulario HTML (<form method="GET">) con dos campos de tipo date para el filtro de fechas y un botón de "Aplicar".

        [ ] Crear una sección de "KPIs" (Key Performance Indicators):

            [ ] Mostrar los datos de P&G (ingresos, gastos, beneficio) en tarjetas o elementos visuales destacados.

            [ ] Mostrar los datos de IVA (repercutido, soportado, resultado) de la misma manera.

            [ ] (Opcional) Usar clases de CSS para colorear los resultados (ej: text-success para beneficio, text-danger para pérdida).

        [ ] Crear una sección "Facturas Pendientes de Cobro":

            [ ] Comprobar si el queryset de facturas impagadas no está vacío.

            [ ] Si hay facturas, crear una tabla HTML para mostrarlas.

            [ ] La tabla debe incluir columnas como: Nº Factura, Cliente, Fecha Vencimiento, Total.

            [ ] Añadir un enlace en cada fila que lleve al detalle o al PDF de esa factura.

Sub-fase 3.4: Mejoras Visuales con Gráficos (Opcional pero Recomendado)

    [ ] Instalar una librería de gráficos JavaScript en tus archivos estáticos (ej: Chart.js).

    [ ] Crear una nueva vista (MonthlyStatsJsonView) que devuelva datos agregados por mes (ej: total ingresos y gastos de cada mes del año) en formato JsonResponse.

    [ ] Añadir una URL en reports/urls.py que apunte a esta nueva vista JSON.

    [ ] En la plantilla dashboard.html, añadir un <canvas> para el gráfico.

    [ ] Escribir el código JavaScript que haga una petición fetch a tu endpoint JSON y use los datos para inicializar y renderizar el gráfico de barras o líneas.

Al completar esta fase, la aplicación pasará de ser un simple libro de contabilidad a una verdadera herramienta de inteligencia de negocio. ¡Es un gran paso!

¡Desde luego! Aquí tienes el checklist final para la Fase 4. Esta es la lista de tareas que transformará tu aplicación en un producto de software profesional y preparado para el futuro.

✅ Checklist de Tareas: Fase 4 - Profesionalización y Futuro

Objetivo: Refactorizar el código, construir una API REST, documentarla y preparar el proyecto para su despliegue en un entorno de producción.

Sub-fase 4.1: Refactorización y Preparación

    [ ] Crear un archivo services.py en la app invoices.

    [ ] Crear un archivo services.py en la app expenses.

    [ ] Mover la lógica de negocio de las vistas a los servicios:

        [ ] Crear una función create_invoice_from_data en invoices/services.py que contenga la lógica de creación de facturas.

        [ ] Refactorizar InvoiceCreateView para que llame a esta nueva función de servicio.

        [ ] Repetir el proceso para otras lógicas complejas (ej: update_invoice_totals, create_expense, etc.).

    [ ] Revisar el código para asegurar que las vistas son "delgadas" (poca lógica) y los servicios son "gruesos" (contienen la lógica de negocio).

Sub-fase 4.2: Construcción de la API (con Django Rest Framework)

    [ ] Instalar Django Rest Framework: pip install djangorestframework.

    [ ] Añadir 'rest_framework' a INSTALLED_APPS en settings.py.

    [ ] Crear serializers.py en las apps invoices y expenses.

    [ ] Definir ModelSerializer para cada modelo que necesite una API: ClientSerializer, InvoiceSerializer, ExpenseSerializer, ProviderSerializer, ExpenseCategorySerializer.

    [ ] Crear api_views.py en las apps invoices y expenses.

    [ ] Implementar ModelViewSet en api_views.py para cada serializer (ej: InvoiceViewSet).

    [ ] Crear un urls.py para la API (ej: api/urls.py) y usar un DefaultRouter de DRF para registrar todos los ViewSet.

    [ ] Incluir las URLs de la API en gcp_project/urls.py bajo un prefijo como /api/v1/.

Sub-fase 4.3: Documentación y Pruebas de la API

    [ ] Instalar una librería de documentación de API: pip install drf-spectacular.

    [ ] Configurar drf-spectacular en settings.py (añadiéndola a INSTALLED_APPS y configurando el DEFAULT_SCHEMA_CLASS).

    [ ] Añadir las URLs de la documentación (Swagger UI y ReDoc) en el urls.py de la API.

    [ ] Realizar pruebas manuales de la API usando una herramienta como Postman, Insomnia o la propia interfaz de Swagger:

        [ ] GET (List): Comprobar que /api/v1/invoices/ devuelve una lista de facturas.

        [ ] POST (Create): Comprobar que se puede crear una nueva factura enviando datos JSON a /api/v1/invoices/.

        [ ] GET (Retrieve): Comprobar que /api/v1/invoices/1/ devuelve el detalle de una factura.

        [ ] PUT (Update): Comprobar que se puede actualizar una factura.

        [ ] DELETE: Comprobar que se puede eliminar una factura.

        [ ] Repetir las pruebas para los endpoints de gastos y otros modelos.

Sub-fase 4.4: Preparación para Producción (Deployment)

    [ ] Generar el archivo requirements.txt final: pip freeze > requirements.txt.

    [ ] Instalar django-environ: pip install django-environ.

    [ ] Crear un archivo .env en la raíz del proyecto (y añadirlo a .gitignore).

    [ ] Crear un archivo .env.example como plantilla.

    [ ] Refactorizar settings.py para leer SECRET_KEY, DEBUG, y DATABASES desde el archivo .env.

    [ ] Asegurar que DEBUG = env.bool('DEBUG', default=False), para que sea False en producción por defecto.

    [ ] Configurar ALLOWED_HOSTS para que lea el dominio de producción desde las variables de entorno.

    [ ] Instalar y configurar WhiteNoise para el servicio de archivos estáticos en producción.

    [ ] Definir una estrategia de backup para la base de datos (ej: documentar el comando pg_dump en el README o crear un script).

Una vez completes este último checklist, tu proyecto estará en un estado profesional, listo para ser desplegado y para servir como base sólida para todas las ideas futuras. ¡Es el broche de oro a todo tu esfuerzo!

¡Desde luego! Aquí tienes el checklist final para la Fase 4. Esta es la lista de tareas que transformará tu aplicación en un producto de software profesional y preparado para el futuro.

✅ Checklist de Tareas: Fase 4 - Profesionalización y Futuro

Objetivo: Refactorizar el código, construir una API REST, documentarla y preparar el proyecto para su despliegue en un entorno de producción.

Sub-fase 4.1: Refactorización y Preparación

    [ ] Crear un archivo services.py en la app invoices.

    [ ] Crear un archivo services.py en la app expenses.

    [ ] Mover la lógica de negocio de las vistas a los servicios:

        [ ] Crear una función create_invoice_from_data en invoices/services.py que contenga la lógica de creación de facturas.

        [ ] Refactorizar InvoiceCreateView para que llame a esta nueva función de servicio.

        [ ] Repetir el proceso para otras lógicas complejas (ej: update_invoice_totals, create_expense, etc.).

    [ ] Revisar el código para asegurar que las vistas son "delgadas" (poca lógica) y los servicios son "gruesos" (contienen la lógica de negocio).

Sub-fase 4.2: Construcción de la API (con Django Rest Framework)

    [ ] Instalar Django Rest Framework: pip install djangorestframework.

    [ ] Añadir 'rest_framework' a INSTALLED_APPS en settings.py.

    [ ] Crear serializers.py en las apps invoices y expenses.

    [ ] Definir ModelSerializer para cada modelo que necesite una API: ClientSerializer, InvoiceSerializer, ExpenseSerializer, ProviderSerializer, ExpenseCategorySerializer.

    [ ] Crear api_views.py en las apps invoices y expenses.

    [ ] Implementar ModelViewSet en api_views.py para cada serializer (ej: InvoiceViewSet).

    [ ] Crear un urls.py para la API (ej: api/urls.py) y usar un DefaultRouter de DRF para registrar todos los ViewSet.

    [ ] Incluir las URLs de la API en gcp_project/urls.py bajo un prefijo como /api/v1/.

Sub-fase 4.3: Documentación y Pruebas de la API

    [ ] Instalar una librería de documentación de API: pip install drf-spectacular.

    [ ] Configurar drf-spectacular en settings.py (añadiéndola a INSTALLED_APPS y configurando el DEFAULT_SCHEMA_CLASS).

    [ ] Añadir las URLs de la documentación (Swagger UI y ReDoc) en el urls.py de la API.

    [ ] Realizar pruebas manuales de la API usando una herramienta como Postman, Insomnia o la propia interfaz de Swagger:

        [ ] GET (List): Comprobar que /api/v1/invoices/ devuelve una lista de facturas.

        [ ] POST (Create): Comprobar que se puede crear una nueva factura enviando datos JSON a /api/v1/invoices/.

        [ ] GET (Retrieve): Comprobar que /api/v1/invoices/1/ devuelve el detalle de una factura.

        [ ] PUT (Update): Comprobar que se puede actualizar una factura.

        [ ] DELETE: Comprobar que se puede eliminar una factura.

        [ ] Repetir las pruebas para los endpoints de gastos y otros modelos.

Sub-fase 4.4: Preparación para Producción (Deployment)

    [ ] Generar el archivo requirements.txt final: pip freeze > requirements.txt.

    [ ] Instalar django-environ: pip install django-environ.

    [ ] Crear un archivo .env en la raíz del proyecto (y añadirlo a .gitignore).

    [ ] Crear un archivo .env.example como plantilla.

    [ ] Refactorizar settings.py para leer SECRET_KEY, DEBUG, y DATABASES desde el archivo .env.

    [ ] Asegurar que DEBUG = env.bool('DEBUG', default=False), para que sea False en producción por defecto.

    [ ] Configurar ALLOWED_HOSTS para que lea el dominio de producción desde las variables de entorno.

    [ ] Instalar y configurar WhiteNoise para el servicio de archivos estáticos en producción.

    [ ] Definir una estrategia de backup para la base de datos (ej: documentar el comando pg_dump en el README o crear un script).

Una vez completes este último checklist, tu proyecto estará en un estado profesional, listo para ser desplegado y para servir como base sólida para todas las ideas futuras. ¡Es el broche de oro a todo tu esfuerzo!