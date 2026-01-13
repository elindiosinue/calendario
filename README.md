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
   pip install -r requirements.txt
   ```

3. Configurar PostgreSQL:
   - Asegúrate de tener PostgreSQL instalado y en ejecución
   - El script de inicialización creará la base de datos y tablas automáticamente

4. Inicializar la base de datos:
   ```bash
   python init_db.py
   ```

5. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

6. Acceder a la aplicación en http://localhost:5000

## Configuración de la base de datos

Por defecto, la aplicación se conecta a PostgreSQL con la siguiente configuración:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'calendar_db',
    'user': 'postgres',
    'password': 'postgres'
}
```

Si necesitas cambiar estos valores, modifica las constantes en `app.py` e `init_db.py`.

## Funcionalidades

1. **Visualización del calendario**: Muestra el calendario del mes actual por defecto, con colores que indican el tipo de día.
2. **Navegación**: Permite navegar entre meses y años usando los botones de control.
3. **Contador de días laborables**: Calcula cuántos días laborables hay entre la fecha actual y una fecha objetivo seleccionada.
4. **Gestión de días festivos**: Permite añadir nuevos días festivos a través del formulario correspondiente.

## Estructura de la base de datos

La aplicación utiliza una tabla `holidays` en PostgreSQL con la siguiente estructura:

- `id`: Identificador único (SERIAL PRIMARY KEY)
- `holiday_date`: Fecha del día festivo (DATE NOT NULL UNIQUE)
- `description`: Descripción del día festivo (VARCHAR(255))
- `created_at`: Fecha de creación del registro (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

## Personalización

Puedes personalizar la aplicación modificando:

- Colores en el archivo `templates/index.html`
- Lógica de cálculo de días laborables en `app.py`
- Mensajes y etiquetas en el archivo HTML
