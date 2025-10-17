from flask import Blueprint, request, jsonify
from models.ProductModel import ProductModel
from database.db import db

product_blueprint = Blueprint('products', __name__)

@product_blueprint.route('/', methods=['GET'])
def read_products():
    products = ProductModel.query.order_by(ProductModel.id.asc()).all()
    product_list = [{
        'id': p.id,
        'name': p.name,
        'min_stock': p.min_stock,
        'med_stock': p.med_stock,
        'saldo': p.saldo,
        'price': p.price,
        'value_total': p.value_total,
        'situation': p.situation
    } for p in products]

    return jsonify(product_list), 200


@product_blueprint.route('/', methods=['POST', "OPTIONS"])
def create_product():
    data = request.get_json()
    required_fields = ['name', 'min_stock', 'med_stock', 'saldo', 'price']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        product = ProductModel(
            name=data['name'],
            min_stock=data['min_stock'],
            med_stock=data['med_stock'],
            saldo=data['saldo'],
            price=data['price'],
        )
        product.value_total = product.saldo * product.price
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product created successfully", "id": product.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@product_blueprint.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = ProductModel.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        'id': product.id,
        'name': product.name,
        'min_stock': product.min_stock,
        'med_stock': product.med_stock,
        'saldo': product.saldo,
        'price': product.price,
        'value_total': product.value_total,
        'situation': product.situation
    }), 200


@product_blueprint.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = ProductModel.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    try:
        for field in ['name', 'min_stock', 'med_stock', 'saldo', 'price']:
            if field in data:
                setattr(product, field, data[field])

        product.value_total = product.saldo * product.price 
        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@product_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = ProductModel.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
