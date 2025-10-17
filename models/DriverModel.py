from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class DriverModel(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200))  
    cnh = db.Column(db.String(11), unique=True)  
    vehicle_plate = db.Column(db.String(10), nullable=False)  

    solicitations = db.relationship('SolicitationModel', back_populates='driver', lazy=True)
    reports = db.relationship('ReportModel', back_populates='driver')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)