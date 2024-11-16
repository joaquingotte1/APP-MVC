from .database import get_db_connection

def get_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM robos_secuestrados")
    resultados = cursor.fetchall()
    conn.close()
    return [dict(fila) for fila in resultados]

def get_by_field(field, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM robos_secuestrados WHERE {field} = ?"
    cursor.execute(query, (value,))
    resultados = cursor.fetchall()
    conn.close()
    return [dict(fila) for fila in resultados]

def get_by_date_range(start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM robos_secuestrados
        WHERE tramite_fecha BETWEEN ? AND ?
    """, (start_date, end_date))
    resultados = cursor.fetchall()
    conn.close()
    return [dict(fila) for fila in resultados]