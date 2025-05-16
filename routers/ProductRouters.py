from flask import Blueprint, request, jsonify
from models.ProductModel import ProductModel
from models.StockModel import StockModel
from database.db import db
from enums.ProductEnum import ProductEnum
product_blueprint = Blueprint('products', __name__)

@product_blueprint.route('/', methods=['GET'])
def read_products():
    products = ProductModel.query.all()
    product_list = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'image': product.image,
            'quantity': product.quantity,
            'stock_level': ProductEnum.from_quantity(product.quantity)
        }
        if product.stock:
            product_data['stock'] = {
                'id': product.stock.id,
                'name': product.stock.name, 
                'quantity_products': product.stock.quantity_products
            }
        product_list.append(product_data)
    
    return jsonify({"message": "Product list retrieved successfully", "products": product_list}), 200

@product_blueprint.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        name = data['name']
        description = data['description']
        price = data['price']
        image = data.get('image', '')
        quantity = data.get('quantity', 0)
        stock_id = data.get('stock_id')

        new_product = ProductModel(
            name=name,
            description=description,
            price=price,
            image=image,
            quantity=quantity,
            stock_id=stock_id
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product created successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

@product_blueprint.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = ProductModel.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image': product.image,
        'quantity': product.quantity,
        'stock_level': ProductEnum.from_quantity(product.quantity)
    }
    if product.stock:
        product_data['stock'] = {
            'id': product.stock.id,
            'name': product.stock.name, 
            'quantity_products': product.stock.quantity_products 
        }
    return jsonify({"product": product_data}), 200

@product_blueprint.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = ProductModel.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    try:
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.image = data.get('image', product.image)
        product.quantity = data.get('quantity', product.quantity)
        product.stock_id = data.get('stock_id', product.stock_id)

        db.session.commit()

        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@product_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = ProductModel.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200