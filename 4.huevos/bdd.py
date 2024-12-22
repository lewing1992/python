import os
import sqlite3
import shutil


def conectar_bd():
    # Configuración de la base de datos
    db_source = os.path.join(os.path.dirname(__file__), "huevos_app.db")
    db_destination = os.path.join(os.path.expanduser("~"), "huevos_app.db")

    if not os.path.exists(db_destination):
        shutil.copy(db_source, db_destination)

    db = sqlite3.connect(db_destination)
    cursor = db.cursor()

    # Crear tablas si no existen
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        cantidad INTEGER,
        pago REAL,
        deuda REAL,
        fecha TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cajas_totales INTEGER,
        huevos_restantes INTEGER
    )
    """)
    db.commit()

    # Inicializar inventario si está vacío
    cursor.execute("SELECT * FROM inventario")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO inventario (cajas_totales, huevos_restantes) VALUES (0, 0)")
        db.commit()

    return db
