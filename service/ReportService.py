from database.db import db
from models.ReportModel import ReportModel
from models.DriverModel import DriverModel 
from models.ProductModel import ProductModel 
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

class ReportService:
    def create_reports_for_driver(self, driver_id: int) -> list[ReportModel]:
        try:
            driver = DriverModel.query.filter_by(id=driver_id).one()
        except NoResultFound:
             raise NoResultFound(f"Motorista com ID {driver_id} não encontrado.")

        products = ProductModel.query.all()
        if not products:
             return [] 
        created_reports = []
        today = datetime.today()

        for product in products:
            if ReportModel.query.filter_by(
                driver_id=driver_id, 
                products_id=product.id,
                report_date=today
            ).first():
                continue

            saldo_inicial_produto = product.saldo
            
            new_report_data = {
                'report_date': today,
                
                'driver_id': driver.id,
                'driver_name': driver.name, 
                'vehicle_plate': driver.vehicle_plate, 
                
                'products_id': product.id,
                'products_name': product.name,
                'product_saldo': saldo_inicial_produto, 
                
                'delivered': 0, 
                'notes': 0,
                
                'surplus': saldo_inicial_produto - 0, 
                'difference': False 
            }

            new_report = ReportModel(**new_report_data)
            db.session.add(new_report)
            created_reports.append(new_report)

        try:
            db.session.commit()
            return created_reports
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar relatórios iniciais: {e}")

    def get_report_by_id(self, report_id: int) -> ReportModel | None:
        return ReportModel.query.get(report_id)
    def get_all_reports(self) -> list[ReportModel]:
        return ReportModel.query.order_by(ReportModel.id.asc()).all()
    def update_report(self, report_id: int, data: dict) -> ReportModel | None:
        report = ReportModel.query.get(report_id)
        if not report:
            return None

        for key, value in data.items():
            if hasattr(report, key):
                setattr(report, key, value)

        try:
            db.session.commit()
            return report
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar o relatório: {e}")
        
    def get_reports_by_driver(self, driver_id: int) -> list[ReportModel]:
        return ReportModel.query.filter_by(driver_id=driver_id).order_by(ReportModel.id.asc()).all()
        
    def delete_report(self, report_id: int) -> bool:
        report = ReportModel.query.get(report_id)
        if not report:
            return False

        try:
            db.session.delete(report)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao deletar o relatório: {e}")