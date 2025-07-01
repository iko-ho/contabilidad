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

    ✅ Fase 0: Cimentación del Proyecto.
        Setup inicial, configuración de Django, diseño de la BD y repositiorio Git.
    🔲 Fase 1: Módulo de Ingresos.
        CRUD de Clientes, lógica de Presupuestos y Facturas (incluyendo PDF y email).
    🔲 Fase 2: Módulo de Gastos.
        CRUD de Proveedores y registro de gastos.
    🔲 Fase 3: Módulo de Informes y Fiscalidad.
        Creación de los informes de P&amp;G, IVA e IRPF. Dashboard principal.
    🔲 Fase 4: Planificación para el Futuro.
        Refactorizar el código para facilitar la creación de una API REST con DRF en el futuro.

🤝 Contribuciones

Este es un proyecto en desarrollo. Para contribuir:

    Crea una nueva rama para tu feature o bugfix: git checkout -b feature/nombre-feature
    Haz tus cambios y realiza commits atómicos.
    Abre un Pull Request contra la rama develop.