from flask import Flask
from database.db import db
from routers.ClientRouters import client_blueprint
from routers.ProductRouters import product_blueprint
from routers.StockRouters import stock_blueprint 
from routers.AdminRouters import admin_blueprint 
from dotenv import load_dotenv


load_dotenv()
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Registrar blueprints
app.register_blueprint(client_blueprint)
app.register_blueprint(product_blueprint, url_prefix = "/products")
app.register_blueprint(stock_blueprint, url_prefix = "/stock")
app.register_blueprint(admin_blueprint, url_prefix = "/admin")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)