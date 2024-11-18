from models.database import get_db_connection

def get_all_paginated(page, records_per_page):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Calcula el offset (desplazamiento) basado en la página
    offset = (page - 1) * records_per_page

    # Ejecuta la consulta para obtener los registros paginados
    cursor.execute("""
        SELECT * FROM robos_secuestrados
        LIMIT ? OFFSET ?
    """, (records_per_page, offset))

    resultados = cursor.fetchall()

    # Ejecuta otra consulta para obtener el total de registros (para calcular el total de páginas)
    cursor.execute("SELECT COUNT(*) FROM robos_secuestrados")
    total_records = cursor.fetchone()[0]

    conn.close()

    return [dict(fila) for fila in resultados], total_records


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

def search_records(search_term, page, records_per_page):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Calcula el offset (desplazamiento) basado en la página
    offset = (page - 1) * records_per_page

    # Consulta para buscar por término en campos relevantes
    cursor.execute("""
        SELECT * FROM robos_secuestrados
        WHERE tramite_tipo LIKE ? OR automotor_modelo_descripcion LIKE ? OR titular_domicilio_localidad LIKE ?
                   OR titular_genero LIKE ? OR titular_pais_nacimiento LIKE ? OR automotor_tipo_descripcion LIKE ?
        LIMIT ? OFFSET ?
    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", records_per_page, offset))
    
    resultados = cursor.fetchall()

    # Ejecuta otra consulta para obtener el total de registros coincidentes
    cursor.execute("""
        SELECT COUNT(*) FROM robos_secuestrados
        WHERE tramite_tipo LIKE ? OR automotor_modelo_descripcion LIKE ? OR titular_domicilio_localidad LIKE ?
                   OR titular_genero LIKE ? OR titular_pais_nacimiento LIKE ? OR automotor_tipo_descripcion LIKE ?
    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    total_records = cursor.fetchone()[0]

    conn.close()

    return [dict(fila) for fila in resultados], total_records
