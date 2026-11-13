import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("contactos.db")

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT,
            categoria TEXT NOT NULL
        )
    """)
    # Agrega las columnas nuevas sin borrar los contactos que ya existían.
    columnas = {fila[1] for fila in db.execute("PRAGMA table_info(contactos)")}
    if "favorito" not in columnas:
        db.execute("ALTER TABLE contactos ADD COLUMN favorito INTEGER NOT NULL DEFAULT 0")
    if "cumpleanos" not in columnas:
        db.execute("ALTER TABLE contactos ADD COLUMN cumpleanos TEXT")
    if "notas" not in columnas:
        db.execute("ALTER TABLE contactos ADD COLUMN notas TEXT")
    db.commit()
    db.close()

init_db()
