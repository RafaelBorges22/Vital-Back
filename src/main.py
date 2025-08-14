from flask import Flask
from database.db import db
from routers.ClientRouters import client_blueprint
from routers.ProductRouters import product_blueprint
from routers.AdminRouters import admin_blueprint 
from routers.EmailRouters import email_blueprint
from routers.DriverRouters import driver_blueprint
from routers.SolicitationRouters import solicitation_blueprint
from routers.StockRouters import stock_blueprint 
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
import os
print(os.urandom(24).hex())

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'minha_chave_secreta') 


db.init_app(app)
migrate = Migrate(app, db)

from models import *

# Registrar blueprints
app.register_blueprint(client_blueprint, url_prefix = "/clients")
app.register_blueprint(product_blueprint, url_prefix = "/products")
app.register_blueprint(stock_blueprint, url_prefix = "/stocks")
app.register_blueprint(admin_blueprint, url_prefix = "/admins")
app.register_blueprint(email_blueprint, url_prefix = "/email")
app.register_blueprint(driver_blueprint, url_prefix = "/drivers")
app.register_blueprint(solicitation_blueprint, url_prefix = "/solicitations")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)