from flask import Blueprint, request, jsonify
from models.SolicitationModel import SolicitationModel
from models.DriverModel import DriverModel  
from enums.SolicitationEnum import SolicitationEnum
from service.EmailService import EmailService
from database.db import db
from datetime import datetime

solicitation_blueprint = Blueprint('solicitation', __name__)
email_service = EmailService()

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
            'date_collected': s.date_collected.isoformat() if s.date_collected else None,
            'driver_id': s.driver_id,
            'driver_name': s.driver.name if s.driver else 'Motorista pendente' 
        } for s in solicitations]

        return jsonify({
            "success": True,
            "data": solicitation_list,
            "count": len(solicitation_list)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@solicitation_blueprint.route('/', methods=['POST', 'OPTIONS'])
def create_solicitation():
    data = request.get_json()
    try:
        required_fields = ['client_id', 'description', 'date_collected']
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
        
        driver_id = data.get('driver_id')
        if driver_id:
            driver = DriverModel.query.get(driver_id)
            if not driver:
                return jsonify({"error": "Driver not found"}), 404
        
        new_solicitation = SolicitationModel(
            client_id=data['client_id'],
            status=status_value,
            description=data['description'],
            date_collected=date_collected,
            driver_id=driver_id 
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
        'client_adress': solicitation.client.address if solicitation.client else None,
        'status': solicitation.status,
        'description': solicitation.description,
        'date_solicitation': solicitation.date_solicitation.isoformat(),
        'date_collected': solicitation.date_collected.isoformat() if solicitation.date_collected else None,
        'driver_id': solicitation.driver_id,
        'driver_name': solicitation.driver.name if solicitation.driver else 'Motorista pendente' 
    }), 200

@solicitation_blueprint.route('/<int:solicitation_id>', methods=['PUT'])
def update_solicitation(solicitation_id):
    solicitation = SolicitationModel.query.get_or_404(solicitation_id)
    data = request.get_json()
    
    try:
        old_status = solicitation.status
        
        if 'status' in data:
            new_status = SolicitationEnum.from_status(data['status'])
            solicitation.status = new_status
            
        if 'driver_id' in data:
            solicitation.driver_id = data['driver_id']
        
        if 'date_collected' in data:
            if data['date_collected']:
                solicitation.date_collected = datetime.fromisoformat(data['date_collected'])
            else:
                solicitation.date_collected = None

        db.session.commit()

        if old_status != SolicitationEnum.APPROVED.value and solicitation.status == SolicitationEnum.APPROVED.value:
            try:
                client_email = solicitation.client.email
                subject = "Sua solicitação foi aprovada!"
                content = f"Olá {solicitation.client.name},\n\n" \
                          f"Sua solicitação de coleta foi aprovada e está em andamento. " \
                          f"Agradeçemos pela confiança em nosso serviço.\n\n" \
                          f"Atenciosamente,\n" \
                          f"A equipe Vital."
                
                email_service.send_email(to_email=client_email, subject=subject, content=content)
                print(f"E-mail de aprovação enviado para {client_email}.")
            except Exception as email_e:
                print(f"Erro ao enviar e-mail de aprovação para o cliente {solicitation.client.id}: {str(email_e)}")

        return jsonify({"message": f"Solicitação {solicitation_id} atualizada com sucesso."}), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ocorreu um erro ao atualizar a solicitação."}), 500


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






