import smtplib
from email.message import EmailMessage
import os
import mimetypes 
import dotenv

dotenv.load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")

        if not self.username or not self.password:
            raise ValueError("Variáveis de ambiente EMAIL_USERNAME ou EMAIL_PASSWORD não configuradas.")

    def send_email(self, to_email: str, subject: str, content: str, attachment_path: str = None):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_email
        msg.set_content(content)

        if attachment_path and os.path.exists(attachment_path):
            try:
                ctype, encoding = mimetypes.guess_type(attachment_path)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                
                maintype, subtype = ctype.split('/', 1)

                with open(attachment_path, 'rb') as fp:
                    msg.add_attachment(fp.read(),
                                       maintype=maintype,
                                       subtype=subtype,
                                       filename=os.path.basename(attachment_path))
            except Exception as e:
                print(f"Erro ao adicionar anexo {attachment_path}: {e}")
                pass

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls() 
                server.login(self.username, self.password)
                server.send_message(msg)
                print("Email enviado com sucesso.")
        except smtplib.SMTPAuthenticationError:
            print("Erro de autenticação SMTP. Verifique seu usuário e senha.")
            raise 
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            raise 