from flask import Blueprint, request, jsonify
from models.SolicitationModel import SolicitationModel
from enums.SolicitationEnum import SolicitationEnum
from database.db import db
from datetime import datetime

solicitation_blueprint = Blueprint('solicitations', __name__)

@solicitation_blueprint.route('/', methods=['GET'])
def get_all_solicitations():
    solicitations = SolicitationModel.query.all()
    result = [{
        'id': s.id,
        'surplus': s.surplus,
        'loaded': s.loaded,
        'total': s.total,
        'delivered': s.delivered,
        'surplus2': s.surplus2,
        'notes': s.notes,
        'difference': s.difference,
        'client_id': s.client_id,
        'client_name': s.client_name,
        'status': s.status,
        'payment_method': s.payment_method,
        'description': s.description,
        'date_solicitation': s.date_solicitation.isoformat(),
        'date_collected': s.date_collected.isoformat() if s.date_collected else None,
        'driver_id': s.driver_id,
        'driver_name': s.driver_name
    } for s in solicitations]

    return jsonify(result), 200


@solicitation_blueprint.route('/', methods=['POST'])
def create_solicitation():
    data = request.get_json()
    required = ['date_collected', 'description', 'payment_method', 'client_id'] 


    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        new_solicitation = SolicitationModel(
            surplus=data['surplus'],
            loaded=data['loaded'],
            total=data['total'],
            delivered=data['delivered'],
            surplus2=data['surplus2'],
            notes=data.get('notes'),
            difference=data['difference'],
            client_id=data['client_id'],
            status=data.get('status', SolicitationEnum.PENDING.value),
            payment_method=data['payment_method'],
            description=data.get('description'),
            date_collected=datetime.fromisoformat(data['date_collected']) if data.get('date_collected') else None,
            driver_id=data.get('driver_id')
        )

        db.session.add(new_solicitation)
        db.session.commit()
        return jsonify({"message": "Solicitation created successfully", "id": new_solicitation.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@solicitation_blueprint.route('/<int:id>', methods=['GET'])
def get_solicitation(id):
    s = SolicitationModel.query.get(id)
    if not s:
        return jsonify({"error": "Solicitation not found"}), 404

    return jsonify({
        'id': s.id,
        'surplus': s.surplus,
        'loaded': s.loaded,
        'total': s.total,
        'delivered': s.delivered,
        'surplus2': s.surplus2,
        'notes': s.notes,
        'difference': s.difference,
        'client_id': s.client_id,
        'client_name': s.client_name,
        'status': s.status,
        'description': s.description,
        'date_solicitation': s.date_solicitation.isoformat(),
        'date_collected': s.date_collected.isoformat() if s.date_collected else None,
        'driver_id': s.driver_id,
        'driver_name': s.driver_name
    }), 200


@solicitation_blueprint.route('/<int:id>', methods=['PUT'])
def update_solicitation(id):
    solicitation = SolicitationModel.query.get(id)
    if not solicitation:
        return jsonify({"error": "Solicitation not found"}), 404

    data = request.get_json()
    try:
        for field in [
        'surplus', 'loaded', 'total', 'delivered', 'surplus2', 'notes', 
        'difference', 'status', 'driver_id', 'description', 'payment_method', 'client_id', 'client_name', 'driver_name'
    ]:

            if field in data:
                setattr(solicitation, field, data[field])

        if 'date_collected' in data:
            solicitation.date_collected = datetime.fromisoformat(data['date_collected']) if data['date_collected'] else None

        db.session.commit()
        return jsonify({"message": "Solicitation updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@solicitation_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_solicitation(id):
    solicitation = SolicitationModel.query.get(id)
    if not solicitation:
        return jsonify({"error": "Solicitation not found"}), 404

    try:
        db.session.delete(solicitation)
        db.session.commit()
        return jsonify({"message": "Solicitation deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
