import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Dados da sua conta no Mailtrap
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525 
SMTP_USER = "67a8baf93d62bb"
SMTP_PASSWORD = "da5418ccaa6407"

def enviar_alerta_vagas(email_destinatario: str, vagas: list):
    if not vagas:
        return

    msg = MIMEMultipart()
    msg['From'] = "alerta@vagas-ti.com.br"
    msg['To'] = email_destinatario
    msg['Subject'] = f"Novas Vagas de TI Encontradas!"

    corpo = "<h2>Vagas encontradas:</h2><ul>"
    for vaga in vagas:
        corpo += f'<li>{vaga.titulo} - <a href="{vaga.link}">Link</a></li>'
    corpo += "</ul>"

    msg.attach(MIMEText(corpo, 'html'))

    try:
        # Usamos context manager para garantir que a conexao feche so no final
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls() # Protege a conexao
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Sucesso: E-mail enviado para {email_destinatario}")
    except Exception as e:
        print(f"Erro detalhado: {e}")