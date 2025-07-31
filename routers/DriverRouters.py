from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.DriverModel import DriverModel
from database.db import db
from datetime import datetime, timedelta
import jwt

driver_blueprint = Blueprint('driver', __name__)

@driver_blueprint.route('/', methods=['GET'])
def read_drivers():
    drivers = DriverModel.query.all()
    driver_list = []
    for driver in drivers:
        driver_list.append({
                'id': driver.id,
                'name': driver.name,
                'cnh': driver.cnh,
                'vehicle_plate': driver.vehicle_plate
            })
        return jsonify({"message": "Driver list retrieved successfully", "drivers": driver_list}), 200

@driver_blueprint.route('/', methods=['POST'])
def create_driver():
    data = request.get_json()
    
    try:
        required_fields = ['name', 'password', 'cnh', 'vehicle_plate']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        hashed_password = generate_password_hash(data['password'])

        new_driver = DriverModel(
            name=data['name'],
            password_hash=hashed_password,
            cnh=data['cnh'],
            vehicle_plate=data['vehicle_plate']
        )

        db.session.add(new_driver)
        db.session.commit()

        return jsonify({"message": "Driver created successfully"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@driver_blueprint.route('/<int:driver_id>', methods=['GET'])
def read_driver(driver_id):
    driver = DriverModel.query.get_or_404(driver_id)
    return jsonify({
        'id': driver.id,
        'name': driver.name,
        'cnh': driver.cnh,
        'vehicle_plate': driver.vehicle_plate
    }), 200

@driver_blueprint.route('/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    data = request.get_json()
    driver = DriverModel.query.get_or_404(driver_id)

    try:
        if 'name' in data:
            driver.name = data['name']
        if 'password' in data:
            driver.password_hash = generate_password_hash(data['password'])
        if 'cnh' in data:
            driver.cnh = data['cnh']
        if 'vehicle_plate' in data:
            driver.vehicle_plate = data['vehicle_plate']

        db.session.commit()
        return jsonify({"message": "Driver updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@driver_blueprint.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = DriverModel.query.get_or_404(driver_id)

    try:
        db.session.delete(driver)
        db.session.commit()
        return jsonify({"message": "Driver deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@driver_blueprint.route('/login-motorista', methods=['POST'])
def login_driver():
    data = request.get_json()
    senha = data.get('password')
    cnh = data.get("cnh")


    if not cnh or not senha:
        return jsonify({"error": "CNH e senha são obrigatórios"}), 400

    driver = DriverModel.query.filter_by(cnh=cnh).first()

    if not driver or not driver.check_password(senha):
        return jsonify({"error": "Credenciais inválidas"}), 401

    try:
        token_payload = {
            'id': driver.id,
            'cnh': driver.cnh,
            'role': 'driver',
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({
            "message": "Bem vindo " + driver.name,
            "access_token": token,
            "driver": {
                "id": driver.id,
                "name": driver.name,
                "cnh": driver.cnh,
                "vehicle_plate": driver.vehicle_plate}
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao gerar token: {str(e)}"}), 500






