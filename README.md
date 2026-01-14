# Calendario de Días Laborables

Aplicación web en Python con Flask que muestra un calendario donde se pueden identificar los días laborables, contando los días laborables entre dos fechas. La aplicación considera como días no laborables los fines de semana (sábados y domingos) y los días festivos almacenados en una base de datos PostgreSQL.

## Características

- Visualización de calendario mensual con colores para distinguir tipos de días
- Contador de días laborables entre la fecha actual y una fecha objetivo
- Gestión de días festivos (agregar nuevos días festivos)
- Navegación entre meses y años
- Diferenciación visual de días:
  - Verdes: Días laborables
  - Rojos: Fines de semana (sábados y domingos)
  - Naranjas: Días festivos

## Requisitos

- Python 3.7+
- PostgreSQL

## Instalación

1. Clonar este repositorio
2. Instalar las dependencias:
   ```bash
   # Calendario de Días Laborables

   Aplicación web en Python con Flask que muestra un calendario donde se pueden identificar los días laborables, contando los días laborables entre dos fechas. La aplicación considera como días no laborables los fines de semana (sábados y domingos) y los días festivos almacenados en una base de datos SQLite por defecto (configurable con `DB_PATH`).

   ## Características

   - Visualización de calendario mensual con colores para distinguir tipos de días
   - Contador de días laborables entre la fecha actual y una fecha objetivo
   - Gestión de días festivos (agregar nuevos días festivos)
   - Navegación entre meses y años
   - Diferenciación visual de días:
     - Verdes: Días laborables
     - Rojos: Fines de semana (sábados y domingos)
     - Naranjas: Días festivos

   ## Requisitos

   - Python 3.8+

   > Por defecto la app usa SQLite (archivo local). Si prefieres usar PostgreSQL, adapta la capa de datos (se recomienda `SQLAlchemy` + `Flask-Migrate` para producción).

   ## Instalación

   1. Clonar este repositorio
   2. Instalar las dependencias:
      ```bash
      pip install -r requirements.txt
      ```

   3. Configuración por entorno

      - Copia `.env.example` a `.env` y ajusta variables (`DB_PATH`, `FLASK_DEBUG`, `PORT`, `SECRET_KEY`, `LOG_LEVEL`).

   4. Inicializar la base de datos (SQLite por defecto):
      ```bash
      python init_db.py
      ```

   5. Ejecutar la aplicación en desarrollo:
      ```bash
      python app.py
      ```

   6. Ejecutar en producción (ejemplo con gunicorn):
      ```bash
      gunicorn -w 4 app:app
      ```

   Accede a la aplicación en http://localhost:5000

   ## Configuración

   La aplicación lee `DB_PATH` desde las variables de entorno (o `.env`). Por defecto el archivo se crea en el directorio del proyecto (`./calendar.db`).

   ## Tests

   Hay pruebas unitarias básicas que pueden ejecutarse con `pytest`:

   ```bash
   pytest -q
   ```

   ## Recomendaciones

   - Usar `python-dotenv` para variables de entorno en desarrollo.
   - Añadir `Flask-WTF` para CSRF y validación de formularios si amplías la UI.
   - Para producción, usar `gunicorn` y un motor de base de datos gestionado (Postgres) con `SQLAlchemy` y migraciones.

   ## Personalización

   Puedes personalizar colores en `templates/index.html` y la lógica de cálculo en `app.py`.
