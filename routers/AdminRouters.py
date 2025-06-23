from flask import Blueprint, request, jsonify
from models.AdminModel import AdminModel
from enums.AdminEnum import AdminEnum
from database.db import db
from werkzeug.security import generate_password_hash
import traceback

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/', methods=['GET'])
def read_admins():
    try:
        admins = AdminModel.query.all()
        admin_list = [{
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
            'level': admin.level_name
        } for admin in admins]
        
        return jsonify({
            "success": True,
            "data": admin_list,
            "count": len(admin_list)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@admin_blueprint.route('/', methods=['POST'])
def create_admin():
    data = request.get_json()
    try:
        required_fields = ['name', 'email', 'password', 'level']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        try:
            level_enum = AdminEnum[data['level']] 
            level_value = AdminEnum.to_level(level_enum.value) 
        except (KeyError, ValueError) as e:
            return jsonify({
                "error": f"Level inválido. Valores válidos: {[e.name for e in AdminEnum]}",
                "valid_levels": [e.name for e in AdminEnum]
            }), 400

        if AdminModel.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email já cadastrado"}), 400

        new_admin = AdminModel(
            name=data['name'],
            email=data['email'],
            password=generate_password_hash(data['password']),  
            level=level_value  
        )

        db.session.add(new_admin)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Admin criado com sucesso",
            "id": new_admin.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e),
            "stacktrace": traceback.format_exc()  
        }), 500
    
@admin_blueprint.route('/<int:id>', methods=['GET'])
def get_admin(id):
    try:
        admin = AdminModel.query.get(id)
        if not admin:
            return jsonify({"error": "Admin not found"}), 404

        admin_data = {
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
            'level': admin.level_name
        }

        return jsonify({
            "success": True,
            "data": admin_data
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@admin_blueprint.route('/<int:id>', methods=['PUT'])
def update_admin(id):
    data = request.get_json()
    try:
        admin = AdminModel.query.get(id)
        if not admin:
            return jsonify({"error": "Admin not found"}), 404

        if 'name' in data:
            admin.name = data['name']
        if 'email' in data:
            admin.email = data['email']
        if 'password' in data:
            admin.password = data['password']
        if 'level' in data:
            try:
                level_enum = AdminEnum[data['level']]
                admin.level=AdminEnum.to_level(level_enum.value)
            except KeyError:
                return jsonify({"error": "Invalid level"}), 400

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Admin updated successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@admin_blueprint.route('/<int:id>', methods=['DELETE']) 
def delete_admin(id):
    try:
        admin = AdminModel.query.get(id)
        if not admin:
            return jsonify({"error": "Admin not found"}), 404

        db.session.delete(admin)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Admin deleted successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@admin_blueprint.route('/login-admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    try:
        admin = AdminModel.query.filter_by(email=data['email']).first()
        
        if not admin or not admin.check_password(data['password']):
            return jsonify({"error": "Credenciais inválidas"}), 401

        response = jsonify({
            "message": "Login bem-sucedido",
            "admin": {
                "id": admin.id,
                "name": admin.name,
                "email": admin.email,
                "level": admin.level_name
            }
        })
        
        return response, 200

    except Exception as e:
        return jsonify({
            "error": "Erro interno no servidor",
            "details": str(e)
        }), 500
              

