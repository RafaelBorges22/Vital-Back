# routers/EmailRouters.py (por exemplo)
from service.EmailService import EmailService
from flask import Blueprint, request, jsonify

email_blueprint = Blueprint('email', __name__)
email_service = EmailService()

@email_blueprint.post("/notify")
def notify_client():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "E-mail não informado"}), 400

    try:
        email_service.send_email(
            to_email=email,
            subject="Teste de Envio de E-mail",
            content="Certificado Enviado com sucesso!"
        )
        return jsonify({"message": f"E-mail enviado para {email}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
