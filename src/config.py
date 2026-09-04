from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


@dataclass(frozen=True)
class Config:
    app_nome: str = 'Automação de Relatórios Comerciais'
    dados_exemplo: Path = BASE_DIR / 'dados' / 'vendas_exemplo.xlsx'
    diretorio_saida: Path = BASE_DIR / 'saida'
    diretorio_logs: Path = BASE_DIR / 'logs'
    smtp_host: str = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port: int = int(os.getenv('SMTP_PORT', '587'))
    email_remetente: str = os.getenv('EMAIL_REMETENTE', '')
    email_senha: str = os.getenv('EMAIL_SENHA', '')


CONFIG = Config()
CONFIG.diretorio_saida.mkdir(parents=True, exist_ok=True)
CONFIG.diretorio_logs.mkdir(parents=True, exist_ok=True)
