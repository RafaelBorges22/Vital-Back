from datetime import datetime
from database.db import db
from enums.SolicitationEnum import SolicitationEnum
from enums.PaymentEnum import PaymentEnum

class SolicitationModel(db.Model):
    __tablename__ = 'solicitations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surplus = db.Column(db.Integer, nullable=True)
    loaded = db.Column(db.Integer, nullable=True)
    total = db.Column(db.Integer, nullable=True)
    delivered = db.Column(db.Integer, nullable=True)
    surplus2 = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Integer, nullable=True)
    difference = db.Column(db.Boolean, nullable=True)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client_name = db.Column(db.String(100), nullable=True)
    status = db.Column(
        db.String(20),
        nullable=False,
        default=SolicitationEnum.PENDING.value
    )
    payment_method = db.Column(db.String(50), nullable=True, default=PaymentEnum.DINHEIRO.value)
    description = db.Column(db.Text, nullable=True)
    date_solicitation = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp()
    )
    date_collected = db.Column(db.DateTime, nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    driver_name = db.Column(db.String(100), nullable=True)

    client = db.relationship('ClientModel', back_populates='solicitations')
    driver = db.relationship('DriverModel', back_populates='solicitations')

    def __repr__(self):
        return (
            f'<Solicitation('
            f'surplus={self.surplus}, '
            f'loaded={self.loaded}, '
            f'total={self.total}, '
            f'delivered={self.delivered}, '
            f'surplus2={self.surplus2}, '
            f'notes={self.notes}, '
            f'difference={self.difference}, '
            f'client_id={self.client_id}, '
            f'status={self.status}, '
            f'payment_method={self.payment_method}, '
            f'description={self.description}, '
            f'date_solicitation={self.date_solicitation}, '
            f'date_collected={self.date_collected}, '
            f'driver_id={self.driver_id})>'
        )