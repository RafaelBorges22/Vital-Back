from flask import Blueprint, request, jsonify
from models.SolicitationModel import SolicitationModel
from enums.SolicitationEnum import SolicitationEnum
from enums.PaymentEnum import PaymentEnum
from models.ClientModel import ClientModel
from models.DriverModel import DriverModel
from service.EmailService import EmailService
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
    required = ['client_id'] 

    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    client_id = data['client_id']
    driver_id = data.get('driver_id')
    
    client = ClientModel.query.get(client_id)
    if not client:
        return jsonify({"error": f"Client with ID {client_id} not found"}), 404
    client_name = client.name
    
    driver_name = None
    if driver_id:
        driver = DriverModel.query.get(driver_id)
        if not driver:
            return jsonify({"error": f"Driver with ID {driver_id} not found"}), 404
        driver_name = driver.name


    payment_method_input = data.get('payment_method', PaymentEnum.DINHEIRO.value)
    try:
        validated_payment_method = PaymentEnum.from_payment_method(payment_method_input)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        new_solicitation = SolicitationModel(
            surplus=data.get('surplus'),
            loaded=data.get('loaded'),
            total=data.get('total'),
            delivered=data.get('delivered'),
            surplus2=data.get('surplus2'),
            notes=data.get('notes'),
            difference=data.get('difference'),
            
            client_id=client_id,
            client_name=client_name, 
            
            status=data.get('status', SolicitationEnum.PENDING.value),
            payment_method=validated_payment_method,
            description=data.get('description'),
            
            date_collected=datetime.fromisoformat(data['date_collected']) if data.get('date_collected') else None, 
            
            driver_id=driver_id,
            driver_name=driver_name
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
        'payment_method': s.payment_method,
        'description': s.description,
        'date_solicitation': s.date_solicitation.isoformat(),
        'date_collected': s.date_collected.isoformat() if s.date_collected else None,
        'driver_id': s.driver_id,
        'driver_name': s.driver_name
    }), 200


@solicitation_blueprint.route('/<int:id>', methods=['PUT'])
def update_solicitation(id):
    from service.EmailService import EmailService 

    solicitation = SolicitationModel.query.get(id)
    if not solicitation:
        return jsonify({"error": "Solicitation not found"}), 404

    data = request.get_json()

    try:
        for field in [
            'surplus', 'loaded', 'total', 'delivered', 'surplus2', 'notes',
            'difference', 'status', 'driver_id', 'description', 'payment_method',
            'client_id', 'client_name', 'driver_name'
        ]:
            if field in data:
                setattr(solicitation, field, data[field])

        if 'date_collected' in data:
            solicitation.date_collected = (
                datetime.fromisoformat(data['date_collected'])
                if data['date_collected']
                else None
            )

        db.session.commit()
        if data.get("status", "").upper() == "APROVADO":
            try:
                client = ClientModel.query.get(solicitation.client_id)
                if client and client.email:
                    email_service = EmailService()
                    subject = f"Solicitação #{solicitation.id} Aprovada ✅"
                    content = (
                        f"Olá {client.name},\n\n"
                        f"Sua solicitação de coleta foi aprovada com sucesso!\n"
                        f"Descrição: {solicitation.description or 'Sem descrição'}\n"
                        f"Data da coleta: {solicitation.date_collected.strftime('%d/%m/%Y')}\n\n"
                        f"Caso não possa nos receber no dia agendado entrar com contato com vitalreciclagem@gmail.com.\n\n"
                        f"Atenciosamente,\nEquipe Vital Reciclagem"
                    )
                    email_service.send_email(client.email, subject, content)
                    print(f"Email de aprovação enviado para {client.email}")
                else:
                    print("Cliente sem e-mail cadastrado. Nenhum e-mail enviado.")
            except Exception as e:
                print(f"Erro ao enviar e-mail de aprovação: {e}")

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

@solicitation_blueprint.route('/clients/<int:client_id>', methods=['GET'])
def get_solicitations_by_client(client_id):
    solicitations = SolicitationModel.query.filter_by(client_id=client_id).all()
    result = [{
        'id': s.id,
        'notes': s.notes,
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