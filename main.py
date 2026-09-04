import argparse
from pathlib import Path
from datetime import datetime

from src.analises import calcular_kpis
from src.carregador_dados import carregar_planilha
from src.config import CONFIG
from src.email_service import enviar_email
from src.logger_config import configurar_logger
from src.relatorio_pdf import gerar_relatorio_pdf
from src.validador import validar_e_preparar

logger = configurar_logger(CONFIG.diretorio_logs / 'automacao.log')


def executar(caminho_planilha: Path, destinatario: str | None = None) -> Path:
    logger.info('Iniciando processamento de %s', caminho_planilha)
    df = validar_e_preparar(carregar_planilha(caminho_planilha))
    kpis = calcular_kpis(df)

    nome = f"relatorio_comercial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    caminho_pdf = CONFIG.diretorio_saida / nome
    gerar_relatorio_pdf(df, caminho_pdf)
    logger.info('Relatório gerado: %s | Faturamento: %.2f', caminho_pdf, kpis.faturamento_total)

    if destinatario:
        enviar_email(
            destinatario=destinatario,
            assunto='Relatório Comercial Automatizado',
            corpo='Olá! Segue em anexo o relatório comercial gerado automaticamente.',
            caminho_anexo=caminho_pdf,
            remetente=CONFIG.email_remetente,
            senha=CONFIG.email_senha,
            smtp_host=CONFIG.smtp_host,
            smtp_port=CONFIG.smtp_port,
        )
        logger.info('E-mail enviado para %s', destinatario)

    return caminho_pdf


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automação de Relatórios Comerciais')
    parser.add_argument('--arquivo', type=Path, default=CONFIG.dados_exemplo, help='Caminho para a planilha .xlsx')
    parser.add_argument('--email', type=str, default=None, help='Destinatário opcional do relatório')
    args = parser.parse_args()

    try:
        resultado = executar(args.arquivo, args.email)
        print(f'Relatório gerado com sucesso: {resultado}')
    except Exception as exc:
        logger.exception('Falha na execução')
        raise SystemExit(f'Erro: {exc}') from exc
