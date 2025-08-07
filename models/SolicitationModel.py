from database.db import db
from enums.SolicitationEnum import SolicitationEnum
from datetime import datetime 

class SolicitationModel(db.Model):
    __tablename__ = 'solicitations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=SolicitationEnum.PENDING.value)
    description = db.Column(db.Text, nullable=True)
    date_solicitation = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date_collected = db.Column(db.DateTime, nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    
    client = db.relationship('ClientModel', back_populates='solicitations')
    driver = db.relationship('DriverModel', back_populates='solicitations') 

    def __repr__(self):
        return f'<Solicitation(client_id={self.client_id}, status={self.status}, driver_id={self.driver_id})>'