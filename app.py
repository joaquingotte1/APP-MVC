from flask import Flask, request, render_template
from controllers.robos_secuestrados_controller import*
from views.responses import json_response, error_response
from datetime import datetime

app = Flask(__name__)
app.config['RECORDS_PER_PAGE'] = 10

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@app.route('/', methods=['GET'])
def get_all_robos_secuestrados():
    try:
        page = request.args.get('page', 1, type=int)
        search_term = request.args.get('search', '', type=str)
        records_per_page = app.config['RECORDS_PER_PAGE']

        if search_term:
            data, total_records = search_records(search_term, page, records_per_page)
        else:
            data, total_records = get_all_paginated(page, records_per_page)

        total_pages = (total_records // records_per_page) + (1 if total_records % records_per_page > 0 else 0)

        # if page < 1 or page > total_pages:
        #     return render_template('error.html', mensaje="Número de página inválido.")

        # Definir visible_pages (por ejemplo, mostrar hasta 3 páginas)
        visible_pages = min(3, total_pages)

        return render_template('robos_secuestrados.html', 
                               registros=data, 
                               page=page, 
                               total_pages=total_pages, 
                               visible_pages=visible_pages,
                               search_term=search_term)
    except Exception as e:
        return render_template('error.html', mensaje=str(e))


@app.route('/robos_secuestrados/filtro', methods=['GET'])
def filter_robos_secuestrados():
    field = request.args.get('field')
    value = request.args.get('value')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        if field and value:
            data = get_by_field(field, value)
        elif start_date and end_date:
            if not is_valid_date(start_date) or not is_valid_date(end_date):
                return render_template('error.html', mensaje="Formato de fecha inválido. Use YYYY-MM-DD.")
            data = get_by_date_range(start_date, end_date)
        else:
            return render_template('error.html', mensaje="Parámetros insuficientes para filtrar.")
        return render_template('robos_secuestrados.html', registros=data)
    except Exception as e:
        return render_template('error.html', mensaje=str(e))
#Filtro por fecha desde y hasta 
@app.route('/robos_secuestrados/filtro', methods=['GET'])
def filter_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        # Validar que las fechas sean correctas
        if start_date and end_date:
            if not is_valid_date(start_date) or not is_valid_date(end_date):
                return render_template('error.html', mensaje="Formato de fecha inválido. Use YYYY-MM-DD.")

            # Obtener los datos filtrados por el rango de fechas
            data = get_by_date_range(start_date, end_date)
            return render_template('robos_secuestrados.html', registros=data, start_date=start_date, end_date=end_date)
        else:
            return render_template('error.html', mensaje="Debe seleccionar un rango de fechas.")
    except Exception as e:
        return render_template('error.html', mensaje=str(e))

def get_by_date_range(start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta para filtrar por el rango de fechas
    cursor.execute("""
        SELECT * FROM robos_secuestrados
        WHERE tramite_fecha BETWEEN ? AND ?
    """, (start_date, end_date))
    
    resultados = cursor.fetchall()
    conn.close()

    return [dict(fila) for fila in resultados]

@app.route('/robos_secuestrados/filtro/<string:field>/<string:value>', methods=['GET'])
def get_robos_secuestrados_by_field(field, value):
    try:
        data = get_by_field(field, value)
        return render_template('robos_secuestrados.html', registros=data)
    except Exception as e:
        return render_template('error.html', mensaje=str(e))

@app.route('/robos_secuestrados/filtro/rango_fecha/<string:start_date>/<string:end_date>', methods=['GET'])
def get_robos_secuestrados_by_date_range(start_date, end_date):
    try:
        data = get_by_date_range(start_date, end_date)
        return render_template('robos_secuestrados.html', registros=data)
    except Exception as e:
        return render_template('error.html', mensaje=str(e))

if __name__ == '__main__':
    app.run(debug=True)
