from database.db import db
from enums.ProductEnum import ProductEnum 

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
        return ProductEnum.from_quantity(self.saldo)

    def __repr__(self):
        return (
            f'<Product('
            f'name={self.name}, '
            f'min_stock={self.min_stock}, '
            f'med_stock={self.med_stock}, '
            f'saldo={self.saldo}, '
            f'price={self.price}, '
            f'value_total={self.value_total}, '
            f'situation={self.situation}' 
            f')>'
        )
