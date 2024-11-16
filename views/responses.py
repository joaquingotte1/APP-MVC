from flask import jsonify

def json_response(data, status=200):
    return jsonify(data), status

def error_response(message, status=400):
    return jsonify({'error': message}), status