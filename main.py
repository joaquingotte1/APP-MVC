from flask import Flask, request
from controllers.robos_secuestrados_controller import (
    fetch_all_robos_secuestrados,
    fetch_robos_secuestrados_by_field,
    fetch_robos_secuestrados_by_date_range
)
from views.responses import json_response, error_response

app = Flask(__name__)

@app.route('/robos_secuestrados', methods=['GET'])
def get_all_robos_secuestrados():
    data = fetch_all_robos_secuestrados()
    return json_response(data)

@app.route('/robos_secuestrados/filtro/<string:field>/<string:value>', methods=['GET'])
def get_robos_secuestrados_by_field(field, value):
    try:
        data = fetch_robos_secuestrados_by_field(field, value)
        return json_response(data)
    except Exception as e:
        return error_response(str(e))

@app.route('/robos_secuestrados/filtro/rango_fecha/<string:start_date>/<string:end_date>', methods=['GET'])
def get_robos_secuestrados_by_date_range(start_date, end_date):
    try:
        data = fetch_robos_secuestrados_by_date_range(start_date, end_date)
        return json_response(data)
    except Exception as e:
        return error_response(str(e))

if __name__ == '__main__':
    app.run(debug=True)