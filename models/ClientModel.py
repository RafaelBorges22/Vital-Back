from database.db import db 

class ClientModel(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    payment_method = db.Column(db.String(50), nullable=False)
    opening_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Client {self.name , self.email, self.cnpj, self.payment_method, self.opening_date, self.address}>'