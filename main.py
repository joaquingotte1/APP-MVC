from flask import Flask, request, render_template
from controllers.robos_secuestrados_controller import*
from views.responses import json_response, error_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all_robos_secuestrados():
    try:
        # Obtener el número de página desde los parámetros de la URL (default: 1)
        page = request.args.get('page', 1, type=int)
        records_per_page = 10  # Número de registros por página

        # Obtener los registros de la página actual y el total de registros
        data, total_records = get_all_paginated(page, records_per_page)

        # Calcular el número total de páginas
        total_pages = (total_records // records_per_page) + (1 if total_records % records_per_page > 0 else 0)

        # Limitar el número de páginas visibles a un máximo de 3
        visible_pages = min(total_pages, 3)

        # Renderizar la vista con los datos de la página actual, total de páginas y registros
        return render_template('robos_secuestrados.html', 
                               registros=data, 
                               page=page, 
                               total_pages=total_pages,
                               visible_pages=visible_pages)
    except Exception as e:
        return render_template('error.html', mensaje=str(e))

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
