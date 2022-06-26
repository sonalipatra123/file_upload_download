from flask_jwt_extended import JWTManager
from flask import jsonify
jwt = JWTManager()

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401