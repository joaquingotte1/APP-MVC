import sqlite3

DATABASE = 'base_datos_robos_secuestrados.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn