from gerar_relatorio import gerar_relatorio
from enviar_email import enviar_email

if __name__ == "__main__":
    # Caminhos dos arquivos
    caminho_dados = 'dados/vendas_abril.xlsx'
    caminho_pdf = 'relatorio_final/relatorio_abril.pdf'

    # Gerar relatório PDF a partir dos dados
    gerar_relatorio(caminho_dados, caminho_pdf)

    # Informações do e-mail
    destinatario = 'howanacarolina@email.com'
    assunto = 'Relatório de Vendas - Abril'
    corpo = 'Olá! Segue em anexo o relatório de vendas do mês de abril.'

    # Enviar e-mail com o PDF anexado
    enviar_email(destinatario, assunto, corpo, caminho_pdf)
