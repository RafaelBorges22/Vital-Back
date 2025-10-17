from database.db import db
from enums.ProductEnum import ProductEnum
from sqlalchemy import event

class ProductModel(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    min_stock = db.Column(db.Integer, nullable=False) 
    med_stock = db.Column(db.Integer, nullable=False)
    saldo = db.Column(db.Integer, nullable=False)  
    price = db.Column(db.Float, nullable=False)
    value_total = db.Column(db.Float, nullable=False)

    @property
    def situation(self) -> str:
        return ProductEnum.from_quantity(self.saldo, self.min_stock, self.med_stock)

    def __repr__(self):
        return (
            f'<Product('
            f'name={self.name}, '
            f'saldo={self.saldo}, '
            f'price={self.price}, '
            f'value_total={self.value_total}, '
            f'situation={self.situation}'
            f')>'
        )

@event.listens_for(ProductModel, 'before_insert')
def before_insert(mapper, connection, target):
    target.value_total = target.saldo * target.price

@event.listens_for(ProductModel, 'before_update')
def before_update(mapper, connection, target):
    target.value_total = target.saldo * target.price
