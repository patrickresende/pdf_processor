import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Securely fetch email credentials from environment variables
EMAIL_ADDRESS = ('patrickresende021@gmail.com')  # Replace with your environment variable name
EMAIL_PASSWORD = ('ruje ntut tjym jzxy')  # Replace with your environment variable name

print(f"EMAIL_ADDRESS: {EMAIL_ADDRESS}")
print(f"EMAIL_PASSWORD: {EMAIL_PASSWORD}")

# Check if credentials are available
if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError("Email credentials not set in environment variables.")

# Email details
remetente = EMAIL_ADDRESS
destinatario = ['patrickresende@proton.me']
conteudo = 'Testando esta putaria'

# Create email message
msg = MIMEMultipart()
msg['From'] = remetente
msg['To'] = ', '.join(destinatario)
msg['Subject'] = 'Teste de Envio de Email'
msg.attach(MIMEText(conteudo, 'plain'))

# Connect to the server
try:
    servidor_email = smtplib.SMTP('smtp.gmail.com', 587)  # Use port 587
    servidor_email.starttls()  # Upgrade to secure connection
    servidor_email.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    servidor_email.sendmail(remetente, destinatario, msg.as_string())
    print("Email enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar email: {e}")
finally:
    if 'servidor_email' in locals():
        servidor_email.quit()