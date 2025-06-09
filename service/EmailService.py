# services/EmailService.py
import smtplib
from email.message import EmailMessage
import os

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.username = os.getenv("EMAIL_USERNAME")  
        self.password = os.getenv("EMAIL_PASSWORD") 

    def send_email(self, to_email: str, subject: str, content: str):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_email
        msg.set_content(content)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                print("Email enviado com sucesso.")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
