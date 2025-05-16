from flask import Blueprint, request, jsonify
from models.AdminModel import AdminModel
from enums.AdminEnum import AdminEnum
from database.db import db

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
        if not data.get('name'):
            return jsonify({"error": "name is required"}), 400
        if not data.get('email'):
            return jsonify({"error": "Email is required"}), 400
        if not data.get('password'):
            return jsonify({"error": "Password is required"}), 400
        if not data.get('level'):
            return jsonify({"error": "Level is required"}), 400

        new_admin = AdminModel(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            level=data['level']
        )

        db.session.add(new_admin)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Admin created successfully",
            "id": new_admin.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
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
            admin.level = data['level']

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

