from flask import Blueprint, request, jsonify
from models.StockModel import StockModel
from models.ProductModel import ProductModel
from database.db import db
from datetime import datetime

stock_blueprint = Blueprint('stock', __name__)

@stock_blueprint.route('/', methods=['GET'])
def read_stocks():
    try:
        stocks = StockModel.query.all()
        stock_list = [{
            'id': stock.id,
            'name': stock.name,
            'quantity_products': stock.quantity_products,
            'entry_date': stock.entry_date.isoformat() if stock.entry_date else None,
            'end_date': stock.end_date.isoformat() if stock.end_date else None,
            'products': [{
                'id': product.id,
                'name': product.name,
                'quantity': product.quantity
            } for product in stock.products]
        } for stock in stocks]
        
        return jsonify({
            "success": True,
            "data": stock_list,
            "count": len(stock_list)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@stock_blueprint.route('/', methods=['POST', 'OPTIONS'])
def create_stock():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json()
    try:
        if not data.get('name'):
            return jsonify({"error": "Name is required"}), 400

        new_stock = StockModel(
            name=data['name'],
            quantity_products=data.get('quantity_products', 0),
            entry_date=datetime.utcnow(),
            end_date=datetime.fromisoformat(data['end_date']) if 'end_date' in data else None
        )


        db.session.add(new_stock)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Stock created successfully",
            "id": new_stock.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@stock_blueprint.route('/<int:id>', methods=['GET'])
def get_stock(id):
    try:
        stock = StockModel.query.get_or_404(id)
        
        stock_data = {
            'id': stock.id,
            'name': stock.name,
            'quantity_products': stock.quantity_products,
            'entry_date': stock.entry_date.isoformat() if stock.entry_date else None,
            'end_date': stock.end_date.isoformat() if stock.end_date else None,
            'products': [{
                'id': product.id,
                'name': product.name,
                'quantity': product.quantity
            } for product in stock.products]
        }
        
        return jsonify({
            "success": True,
            "data": stock_data
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404 if "404" in str(e) else 500

@stock_blueprint.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_stock(id):
    try:
        stock = StockModel.query.get_or_404(id)
        data = request.get_json()

        if 'name' in data:
            stock.name = data['name']
        if 'quantity_products' in data:
            stock.quantity_products = data['quantity_products']
        if 'entry_date' in data:
            stock.entry_date = datetime.fromisoformat(data['entry_date']) if data['entry_date'] else None
        if 'end_date' in data:
            stock.end_date = datetime.fromisoformat(data['end_date']) if data['end_date'] else None

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Stock updated successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@stock_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_stock(id):
    try:
        stock = StockModel.query.get_or_404(id)

        for product in stock.products:
            product.stock_id = None

        db.session.delete(stock)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Stock deleted successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500