import pandas as pd
import plotly.express as px

def gerar_relatorio(caminho_dados, caminho_pdf):
    # Lê a planilha
    df = pd.read_excel(caminho_dados)

    # Agrupa vendas
    resumo = df.groupby('Produto')['Quantidade'].sum().reset_index()

    # Gera gráfico de barras interativo com Plotly
    fig = px.bar(
        resumo,
        x='Produto',
        y='Quantidade',
        title='Quantidade Vendida por Produto',
        labels={'Quantidade': 'Qtd Vendida'},
        color='Produto'
    )

    # Exporta diretamente para PDF (com gráfico vetorial)
    fig.write_image(caminho_pdf, format='pdf')
    print(f"✅ Relatório gerado com sucesso em: {caminho_pdf}")
