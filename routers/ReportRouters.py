from flask import Blueprint, request, jsonify
from service.ReportService import ReportService 
from sqlalchemy.exc import NoResultFound

report_blueprint = Blueprint('reports', __name__)
report_service = ReportService()

@report_blueprint.route('/driver/<int:driver_id>', methods=['POST'])
def create_reports_route(driver_id):
    try:
        new_reports = report_service.create_reports_for_driver(driver_id)
        return jsonify({
            "message": f"{len(new_reports)} relatórios iniciais criados para o motorista {driver_id}.",
            "reports_count": len(new_reports)
        }), 201 
    except NoResultFound as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@report_blueprint.route('/<int:report_id>', methods=['GET'])
def get_report_route(report_id):
    report = report_service.get_report_by_id(report_id)
    if report:
        return jsonify({
            "report_date": report.report_date.isoformat(),
            "driver_name": report.driver_name,
            "vehicle_plate": report.vehicle_plate,
            "products_name": report.products_name,
            "product_saldo": report.product_saldo,
            "delivered": report.delivered,
            "surplus": report.surplus,
            "notes": report.notes,
            "difference": report.difference,
        }), 200
    return jsonify({"message": "Relatório não encontrado"}), 404

@report_blueprint.route('/', methods=['GET'])
def get_all_reports_route():
    reports = report_service.get_all_reports()
    reports_list = [{
        "report_id": report.id,
        "report_date": report.report_date.isoformat(),
        "driver_name": report.driver_name,
        "vehicle_plate": report.vehicle_plate,
        "products_name": report.products_name,
        "product_saldo": report.product_saldo,
        "delivered": report.delivered,
        "surplus": report.surplus,
        "notes": report.notes,
        "difference": report.difference,
    } for report in reports]
    
    return jsonify(reports_list), 200

@report_blueprint.route('/driver/<int:driver_id>', methods=['GET'])
def get_reports_by_driver_route(driver_id):
    reports = report_service.get_reports_by_driver(driver_id)
    reports_list = [{
        "report_id": report.id,
        "report_date": report.report_date.isoformat(),
        "driver_name": report.driver_name,
        "vehicle_plate": report.vehicle_plate,
        "products_name": report.products_name,
        "product_saldo": report.product_saldo,
        "delivered": report.delivered,
        "surplus": report.surplus,
        "notes": report.notes,
        "difference": report.difference,
    } for report in reports]
    
    return jsonify(reports_list), 200

@report_blueprint.route('/<int:report_id>', methods=['PUT'])
def update_report_route(report_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Nenhum dado enviado"}), 400

    try:
        updated_report = report_service.update_report(report_id, data)
        return jsonify({
            "message": "Relatório atualizado com sucesso",
            "report_id": updated_report.id,
            "surplus": updated_report.surplus,
            "difference_flag": updated_report.difference
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@report_blueprint.route('/<int:report_id>', methods=['DELETE'])
def delete_report_route(report_id):
    try:
        report_service.delete_report(report_id)
        return jsonify({"message": "Relatório deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500