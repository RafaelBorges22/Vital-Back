from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.DriverModel import DriverModel
from database.db import db

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





