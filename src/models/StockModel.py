from database.db import db
from datetime import date

class StockModel(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    quantity_products = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    end_date = db.Column(db.Date)

    products = db.relationship('ProductModel', back_populates='stock', lazy=True)

    def __repr__(self):
        return (
            f'<Stock(name={self.name}, quantity_products={self.quantity_products}, '
            f'entry_date={self.entry_date}, end_date={self.end_date})>'
        )

