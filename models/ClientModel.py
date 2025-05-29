from database.db import db
from enums.PaymentEnum import PaymentEnum
from datetime import date

class ClientModel(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    cnpj = db.Column(db.String(20))
    payment_method = db.Column("payment_method", db.String(50))  
    opening_date = db.Column(db.Date, nullable=False, default=date.today)

    address = db.Column(db.String(255))

    ##@property
    ##def payment_method(self):
        ##return PaymentEnum.from_payment_method(self._payment_method)

    ##@payment_method.setter
    ##def payment_method(self, value):
        ##self._payment_method = value
