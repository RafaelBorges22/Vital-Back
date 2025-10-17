from datetime import date
from database.db import db
from sqlalchemy import event


class ReportModel(db.Model):
    __tablename__ = "reports"

##Header
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_date = db.Column(db.Date, nullable=False, default=date.today)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    driver_name = db.Column(db.String(100), nullable=False)
    vehicle_plate = db.Column(db.String(10), nullable=False)

##Table Bodys
    #Products 
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    products_name = db.Column(db.String(100), nullable=False)
    product_saldo = db.Column(db.Integer, nullable=False)

    #Insert manually
    delivered = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Integer, nullable=False)

    #event
    difference = db.Column(db.Boolean, nullable=False)
    surplus = db.Column(db.Integer, nullable=False)


    driver = db.relationship('DriverModel', back_populates='reports')
    product = db.relationship('ProductModel', back_populates='reports')


    def __repr__(self):
        return (
            f'<Report('
            f'report_date={self.report_date}, '
            f'driver_id={self.driver_id}, '
            f'driver_name={self.driver_name}, '
            f'vehicle_plate={self.vehicle_plate}, '
            f'products_id={self.products_id}, '
            f'products_name={self.products_name}, '
            f'product_saldo={self.product_saldo}, '
            f'delivered={self.delivered}, '
            f'surplus={self.surplus}, '
            f'notes={self.notes}, '
            f'difference={self.difference}, '
            f')>'
        )
    
@event.listens_for(ReportModel, 'before_update', propagate=True)
@event.listens_for(ReportModel, 'before_insert', propagate=True)
def calculate_difference_flag(mapper, connection, target):
    target.surplus = target.product_saldo - target.delivered
    
    if target.surplus != target.notes:
        target.difference = True 
    else:
        target.difference = False 




