import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path


def enviar_email(
    destinatario: str,
    assunto: str,
    corpo: str,
    caminho_anexo: Path,
    remetente: str,
    senha: str,
    smtp_host: str = 'smtp.gmail.com',
    smtp_port: int = 587,
) -> None:
    if not remetente or not senha:
        raise ValueError('Credenciais de e-mail não configuradas. Verifique o arquivo .env.')

    if not caminho_anexo.exists():
        raise FileNotFoundError(f'Anexo não encontrado: {caminho_anexo}')

    mensagem = EmailMessage()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto
    mensagem.set_content(corpo)

    mime, _ = mimetypes.guess_type(caminho_anexo.name)
    tipo, subtipo = (mime or 'application/octet-stream').split('/', 1)
    with caminho_anexo.open('rb') as arquivo:
        mensagem.add_attachment(
            arquivo.read(),
            maintype=tipo,
            subtype=subtipo,
            filename=caminho_anexo.name,
        )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(mensagem)
