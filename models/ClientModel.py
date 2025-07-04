from database.db import db
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

class ClientModel(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))  
    cnpj = db.Column(db.String(14), unique=True)  # CNPJ tem 14 caracteres
    payment_method = db.Column(db.String(50))
    opening_date = db.Column(db.Date)
    address = db.Column(db.String(200))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)