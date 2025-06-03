from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.ClientModel import ClientModel
from database.db import db
from datetime import datetime

client_blueprint = Blueprint('client', __name__)

@client_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello Vital !!"}), 200

@client_blueprint.route('/clients', methods=['GET'])
def read_client():
    clients = ClientModel.query.all()
    client_list = []
    for client in clients:
        client_list.append({
            'id': client.id,
            'name': client.name,
            'email': client.email,
            'cnpj': client.cnpj,
            'payment_method': client.payment_method,
            'opening_date': client.opening_date.strftime('%d/%m/%y'),
            'address': client.address
        })
    return jsonify({"message": "Client list retrieved successfully", "clients": client_list}), 200

@client_blueprint.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    
    try:
        # Primeiro verifique todos os campos obrigatórios
        required_fields = ['name', 'email', 'password', 'cnpj', 
                         'payment_method', 'opening_date', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Processamento dos dados
        hashed_password = generate_password_hash(data['password'])
        opening_date = datetime.strptime(data['opening_date'], '%Y-%m-%d').date()

        # Criação do cliente
        new_client = ClientModel(
            name=data['name'],
            email=data['email'],
            password_hash=hashed_password,  # Use um campo password_hash no model
            cnpj=data['cnpj'],
            payment_method=data['payment_method'],
            opening_date=opening_date,
            address=data['address']
        )

        db.session.add(new_client)
        db.session.commit()

        return jsonify({"message": "Client created successfully"}), 201
        
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@client_blueprint.route('/clients/<int:id>', methods=['GET'])
def get_client(id):
    client = ClientModel.query.get(id)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    client_data = {
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'cnpj': client.cnpj,
        'payment_method': client.payment_method,
        'opening_date': client.opening_date.isoformat(),
        'address': client.address
    }
    return jsonify({"client": client_data}), 200

@client_blueprint.route('/clients/<int:id>', methods=['PUT'])
def update_client(id):
    client = ClientModel.query.get(id)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    data = request.get_json()
    try:
        client.name = data.get('name', client.name)
        client.email = data.get('email', client.email)
        client.password = data.get('password', client.password)
        client.cnpj = data.get('cnpj', client.cnpj)
        client.payment_method = data.get('payment_method', client.payment_method)
        
        if 'opening_date' in data:
            client.opening_date = datetime.strptime(data['opening_date'], '%Y-%m-%d').date()

        client.address = data.get('address', client.address)

        db.session.commit()

        return jsonify({"message": "Client updated successfully"}), 200
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

@client_blueprint.route('/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    client = ClientModel.query.get(id)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    db.session.delete(client)
    db.session.commit()

    return jsonify({"message": "Client deleted successfully"}), 200

@client_blueprint.route('/clients/login', methods=['POST'])
def login_client():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('password')

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    client = ClientModel.query.filter_by(email=email).first()

    if not client or not client.check_password(senha):
        return jsonify({"error": "Credenciais inválidas"}), 401

    return jsonify({
        "message": "Login bem-sucedido",
        "client": {
            "id": client.id,
            "name": client.name,
            "email": client.email
        }
    }), 200

