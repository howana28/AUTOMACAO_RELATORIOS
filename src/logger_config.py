import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configurar_logger(caminho_log: Path) -> logging.Logger:
    logger = logging.getLogger('automacao_relatorios')
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    arquivo = RotatingFileHandler(caminho_log, maxBytes=1_000_000, backupCount=3, encoding='utf-8')
    arquivo.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(arquivo)
    logger.addHandler(console)
    return logger
