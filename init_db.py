#!/usr/bin/env python3
"""Script para inicializar la base de datos SQLite"""

import sqlite3
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Configuración de la base de datos SQLite (desde variable de entorno o por defecto)
DEFAULT_DB = Path(__file__).parent / 'calendar.db'
DB_PATH = Path(os.getenv('DB_PATH', DEFAULT_DB)).resolve()

def init_tables():
    """Inicializa las tablas en la base de datos"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.cursor()

        # Crear tabla de días festivos
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
                ('2024-07-20', 'Día de la Independencia'),
                ('2024-01-06', 'Día de los Reyes Magos'),
                ('2024-03-25', 'Día de San José'),
                ('2024-05-13', 'Día de la Ascensión'),
                ('2024-06-03', 'Corpus Christi'),
                ('2024-06-10', 'Sagrado Corazón'),
                ('2024-07-01', 'San Pedro y San Pablo'),
                ('2024-08-07', 'Batalla de Boyacá'),
                ('2024-08-19', 'Asunción de la Virgen'),
                ('2024-10-14', 'Día de la Raza'),
                ('2024-11-04', 'Todos los Santos'),
                ('2024-11-11', 'Independencia de Cartagena'),
                ('2024-12-08', 'Inmaculada Concepción')
            ]
            for holiday_date, description in example_holidays:
                cursor.execute(
                    "INSERT OR IGNORE INTO holidays (holiday_date, description) VALUES (?, ?)",
                    (holiday_date, description)
                )
            print("Días festivos de ejemplo insertados.")
        else:
            print("Ya existen días festivos en la base de datos.")

        conn.commit()
        print("Tablas inicializadas exitosamente en %s." % DB_PATH)

if __name__ == "__main__":
    print("Inicializando base de datos SQLite en %s..." % DB_PATH)
    init_tables()
    print("¡Base de datos SQLite inicializada correctamente!")