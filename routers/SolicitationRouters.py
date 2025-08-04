from flask import Blueprint, request, jsonify
from models.SolicitationModel import SolicitationModel
from enums.SolicitationEnum import SolicitationEnum
from database.db import db
from datetime import datetime

solicitation_blueprint = Blueprint('solicitation', __name__)

@solicitation_blueprint.route('/', methods=['GET'])
def read_solicitations():
    try:
        solicitations = SolicitationModel.query.all()
        solicitation_list = [{
            'id': s.id,
            'client_name': s.client.name if s.client else None,
            'client_cnpj': s.client.cnpj if s.client else None, 
            'client_adress': s.client.address if s.client else None,
            'status': s.status,
            'description': s.description,
            'date_solicitation': s.date_solicitation.isoformat(),
            'date_collected': s.date_collected.isoformat() if s.date_collected else None
        } for s in solicitations]

        return jsonify({
            "success": True,
            "data": solicitation_list,
            "count": len(solicitation_list)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@solicitation_blueprint.route('/', methods=['POST', 'OPTIONS'])
@solicitation_blueprint.route('', methods=['POST', 'OPTIONS'])
def create_solicitation():
    data = request.get_json()
    try:
        required_fields = ['client_id', 'status', 'description', 'date_collected']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        try:
            status_value = SolicitationEnum.from_status(data['status'])
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        try:
            date_collected = datetime.fromisoformat(data['date_collected'])
        except ValueError:
            return jsonify({"error": "Formato inválido para date_collected. Use ISO 8601."}), 400

        if date_collected <= datetime.utcnow():
            return jsonify({"error": "date_collected deve ser uma data futura."}), 400
        
        new_solicitation = SolicitationModel(
            client_id=data['client_id'],
            status=status_value,
            description=data['description'],
            date_collected=date_collected
        )

        db.session.add(new_solicitation)
        db.session.commit()

        return jsonify({"message": "Solicitation created successfully", "id": new_solicitation.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@solicitation_blueprint.route('/<int:solicitation_id>', methods=['GET'])
def read_solicitation(solicitation_id):
    solicitation = SolicitationModel.query.get(solicitation_id)
    if not solicitation:
        return jsonify({"error": "Solicitation not found"}), 404

    return jsonify({
        'id': solicitation.id,
        'client_id': solicitation.client_id,
        'client_name': solicitation.client.name if solicitation.client else None,
        'adress': solicitation.adress,
        'status': solicitation.status,
        'description': solicitation.description,
        'date_solicitation': solicitation.date_solicitation.isoformat(),
        'date_collected': solicitation.date_collected.isoformat() if solicitation.date_collected else None
    }), 200


@solicitation_blueprint.route('/<int:solicitation_id>', methods=['PUT'])
def update_solicitation(solicitation_id):
    solicitation = SolicitationModel.query.get(solicitation_id)
    if not solicitation:
        return jsonify({"error": "Solicitation not found"}), 404

    data = request.get_json()
    try:
        if 'adress' in data:
            solicitation.adress = data['adress']
        if 'status' in data:
            try:
                solicitation.status = SolicitationEnum.from_status(data['status'])  
            except ValueError as ve:
                return jsonify({"error": str(ve)}), 400
        if 'description' in data:
            solicitation.description = data['description']
        if 'date_collected' in data:
            solicitation.date_collected = datetime.fromisoformat(data['date_collected'])

        db.session.commit()

        return jsonify({"message": "Solicitation updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@solicitation_blueprint.route('/<int:solicitation_id>', methods=['DELETE'])
def delete_solicitation(solicitation_id):
    solicitation = SolicitationModel.query.get(solicitation_id)
    if not solicitation:
        return jsonify({"error": "Solicitation not found"}), 404

    try:
        db.session.delete(solicitation)
        db.session.commit()
        return jsonify({"message": "Solicitation deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500













