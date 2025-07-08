import smtplib
import os
from email.message import EmailMessage

def enviar_email(destinatario, assunto, corpo, caminho_anexo):
    # Configurações do remetente
    remetente = 'howanacarolina@gmail.com'
    senha = "ktxz ljfd aqyd hfes"  # Use uma senha de app (veja abaixo)

    # Criação da mensagem
    msg = EmailMessage()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.set_content(corpo)

    # Anexar o PDF
    with open(caminho_anexo, 'rb') as f:
        conteudo_pdf = f.read()
        nome_arquivo = os.path.basename(caminho_anexo)
        msg.add_attachment(conteudo_pdf, maintype='application', subtype='pdf', filename=nome_arquivo)

    # Enviar o e-mail via Gmail (SMTP TLS - porta 587)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(remetente, senha)
        smtp.send_message(msg)
        print(f'✅ E-mail enviado para {destinatario}')
