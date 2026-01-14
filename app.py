from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
import logging
from pathlib import Path

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# App and config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

# Configuración de la base de datos SQLite (ruta configurable por entorno)
DEFAULT_DB = Path(__file__).parent / 'calendar.db'
DB_PATH = Path(os.getenv('DB_PATH', DEFAULT_DB)).resolve()

# Logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row  # Para poder acceder a las columnas por nombre
        return conn
    except Exception as e:
        logger.exception("Error connecting to database")
        return None

def init_database():
    """Inicializa la base de datos y crea la tabla de días festivos si no existe"""
    conn = get_db_connection()
    if not conn:
        logger.error("No DB connection available for initialization")
        return

    with conn:
        cursor = conn.cursor()
        # Crear tabla de días festivos si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS holidays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                holiday_date TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insertar algunos días festivos de ejemplo si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM holidays")
        count = cursor.fetchone()[0]
        if count == 0:
            example_holidays = [
                ('2024-01-01', 'Año Nuevo'),
                ('2024-05-01', 'Día del Trabajo'),
                ('2024-12-25', 'Navidad'),
                ('2024-07-20', 'Día de la Independencia')
            ]
            for holiday_date, description in example_holidays:
                cursor.execute(
                    "INSERT OR IGNORE INTO holidays (holiday_date, description) VALUES (?, ?)",
                    (holiday_date, description)
                )
    logger.info('Database initialized at %s', DB_PATH)

def get_holidays(year):
    """Obtiene los días festivos para un año específico"""
    conn = get_db_connection()
    if not conn:
        return []

    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT holiday_date, description FROM holidays WHERE strftime('%Y', holiday_date) = ? ORDER BY holiday_date",
            (str(year),)
        )
        holidays = cursor.fetchall()
    return [(datetime.strptime(date, '%Y-%m-%d').date(), desc) for date, desc in holidays]

def is_weekend(date):
    """Verifica si una fecha es sábado (5) o domingo (6)"""
    return date.weekday() >= 5

def is_holiday(date, holidays):
    """Verifica si una fecha es un día festivo"""
    return date in [h[0] for h in holidays]

def is_working_day(date, holidays):
    """Verifica si una fecha es un día laboral"""
    return not is_weekend(date) and not is_holiday(date, holidays)

def count_working_days(start_date, end_date, holidays):
    """Cuenta los días laborables entre dos fechas"""
    current_date = start_date
    working_days = 0
    
    while current_date <= end_date:
        if is_working_day(current_date, holidays):
            working_days += 1
        current_date += timedelta(days=1)
    
    return working_days

@app.route('/')
def index():
    today = datetime.now().date()
    year = request.args.get('year', type=int, default=today.year)
    month = request.args.get('month', type=int, default=today.month)
    
    # Obtener días festivos para el año
    holidays = get_holidays(year)
    
    # Preparar datos para mostrar en el calendario
    month_name = calendar.month_name[month]
    
    # Obtener todas las fechas del mes y precomputar clases/atributos para el template
    first_day = datetime(year, month, 1).date()
    if month == 12:
        next_month = datetime(year + 1, 1, 1).date()
    else:
        next_month = datetime(year, month + 1, 1).date()
    last_day = next_month - timedelta(days=1)

    all_dates = []
    current_date = first_day
    while current_date <= last_day:
        is_hol = is_holiday(current_date, holidays)
        is_wend = is_weekend(current_date)
        css_class = 'working-day'
        if is_wend:
            css_class = 'weekend'
        if is_hol:
            css_class = 'holiday'

        if current_date == today:
            css_class = (css_class + ' today').strip()

        all_dates.append({
            'date': current_date,
            'day': current_date.day,
            'css_class': css_class,
            'holiday_description': next((desc for d, desc in holidays if d == current_date), '')
        })
        current_date += timedelta(days=1)
    
    return render_template('index.html', 
                          year=year, 
                          month=month, 
                          month_name=month_name,
                          dates=all_dates,
                          today=today)

@app.route('/calculate')
def calculate():
    target_date_str = request.args.get('target_date')
    if not target_date_str:
        return jsonify({'error': 'Fecha objetivo requerida'}), 400
    
    try:
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        
        # Asegurar que el año esté en el rango adecuado para obtener festivos
        holidays = get_holidays(target_date.year)
        if target_date.year != today.year:
            holidays += get_holidays(today.year)

        working_days_count = count_working_days(today, target_date, holidays)
        
        return jsonify({
            'working_days_count': working_days_count,
            'start_date': today.isoformat(),
            'target_date': target_date.isoformat(),
            'success': True
        })
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    date_str = request.form.get('date')
    description = request.form.get('description', '')
    
    if not date_str:
        return jsonify({'error': 'Fecha requerida'}), 400
    
    try:
        holiday_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        with get_db_connection() as conn:
            if conn is None:
                return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO holidays (holiday_date, description) VALUES (?, ?)",
                    (holiday_date, description)
                )
            except sqlite3.IntegrityError:
                cursor.execute(
                    "UPDATE holidays SET description = ? WHERE holiday_date = ?",
                    (description, holiday_date)
                )
            return jsonify({'success': True, 'message': 'Día festivo agregado correctamente'})
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

if __name__ == '__main__':
    init_database()
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))