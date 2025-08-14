from service.EmailService import EmailService
from flask import Blueprint, request, jsonify
import os

email_blueprint = Blueprint('email', __name__)
email_service = EmailService()

UPLOAD_FOLDER = 'temp_attachments'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@email_blueprint.post("/notify")
def notify_client():
    to_email = request.form.get("to")
    subject = request.form.get("subject")
    message = request.form.get("message")
    attachment = request.files.get("attachment")

    if not to_email:
        return jsonify({"error": "E-mail de destino não informado"}), 400
    if not subject:
        return jsonify({"error": "Assunto não informado"}), 400
    if not message:
        return jsonify({"error": "Mensagem não informada"}), 400

    attachment_path = None
    if attachment:
        filename = attachment.filename
        attachment_path = os.path.join(UPLOAD_FOLDER, filename)
        attachment.save(attachment_path)
        print(f"Arquivo '{filename}' salvo em {attachment_path}")

    try:
        email_service.send_email(
            to_email=to_email,
            subject=subject,
            content=message,
            attachment_path=attachment_path 
        )
        return jsonify({"message": f"E-mail enviado para {to_email}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if attachment_path and os.path.exists(attachment_path):
            os.remove(attachment_path)
            print(f"Arquivo temporário '{attachment_path}' removido.")