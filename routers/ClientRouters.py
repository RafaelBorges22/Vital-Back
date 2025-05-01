from flask import Blueprint, request, jsonify
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
        name = data['name']
        email = data['email']
        password = data['password']
        cnpj = data['cnpj']
        payment_method = data['payment_method']
        opening_date = datetime.strptime(data['opening_date'], '%Y-%m-%d').date()
        address = data['address']

        new_client = ClientModel(
            name=name,
            email=email,
            password=password,
            cnpj=cnpj,
            payment_method=payment_method,
            opening_date=opening_date,
            address=address
        )

        db.session.add(new_client)
        db.session.commit()

        return jsonify({"message": "Client created successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

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
