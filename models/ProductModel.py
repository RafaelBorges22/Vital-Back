from database.db import db

class ProductModel(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=True)
    stock = db.relationship('StockModel', back_populates='products')
    
    def __repr__(self):
        return (
            f'<Product(name={self.name}, description={self.description}, '
            f'price={self.price}, quantity={self.quantity}, '
            f'stock_id={self.stock_id})>'
        )

