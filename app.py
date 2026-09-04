from datetime import datetime
from pathlib import Path
import plotly.express as px
import streamlit as st

from src.analises import calcular_kpis, ranking_produtos, vendas_por_categoria, vendas_por_dia
from src.carregador_dados import carregar_planilha
from src.config import CONFIG
from src.email_service import enviar_email
from src.relatorio_pdf import gerar_relatorio_pdf
from src.validador import validar_e_preparar

st.set_page_config(page_title='Automação de Relatórios Comerciais', page_icon='📊', layout='wide')

st.title('Automação de Relatórios Comerciais')
st.caption('Pipeline automatizado de análise, visualização, geração e distribuição de relatórios de vendas.')

with st.sidebar:
    st.header('Entrada de dados')
    arquivo = st.file_uploader('Envie uma planilha Excel', type=['xlsx'])
    usar_exemplo = st.checkbox('Usar dados de demonstração', value=arquivo is None)

try:
    origem = arquivo if arquivo is not None else (CONFIG.dados_exemplo if usar_exemplo else None)
    if origem is None:
        st.info('Envie uma planilha ou selecione os dados de demonstração.')
        st.stop()

    df = validar_e_preparar(carregar_planilha(origem))

    with st.sidebar:
        st.header('Filtros')
        data_min = df['Data'].min().date()
        data_max = df['Data'].max().date()
        periodo = st.date_input('Período', value=(data_min, data_max), min_value=data_min, max_value=data_max)
        categorias = sorted(df['Categoria'].dropna().unique().tolist())
        categorias_sel = st.multiselect('Categorias', categorias, default=categorias)

    if isinstance(periodo, tuple) and len(periodo) == 2:
        inicio, fim = periodo
        df_filtrado = df[(df['Data'].dt.date >= inicio) & (df['Data'].dt.date <= fim)]
    else:
        df_filtrado = df
    if categorias_sel:
        df_filtrado = df_filtrado[df_filtrado['Categoria'].isin(categorias_sel)]

    if df_filtrado.empty:
        st.warning('Nenhum registro encontrado com os filtros selecionados.')
        st.stop()

    kpis = calcular_kpis(df_filtrado)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Faturamento', f"R$ {kpis.faturamento_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col2.metric('Pedidos', f'{kpis.total_pedidos:,}'.replace(',', '.'))
    col3.metric('Ticket médio', f"R$ {kpis.ticket_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col4.metric('Itens vendidos', f'{kpis.itens_vendidos:,}'.replace(',', '.'))

    if kpis.lucro_total is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric('Lucro estimado', f"R$ {kpis.lucro_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        c2.metric('Margem estimada', f'{kpis.margem_percentual:.1f}%'.replace('.', ','))
        c3.metric('Produto mais vendido', kpis.produto_mais_vendido)
    else:
        st.info(f'Produto mais vendido: {kpis.produto_mais_vendido} | Maior faturamento: {kpis.produto_maior_faturamento}')

    graf1, graf2 = st.columns(2)
    por_dia = vendas_por_dia(df_filtrado)
    with graf1:
        st.plotly_chart(
            px.line(por_dia, x='Dia', y='Faturamento', markers=True, title='Evolução do faturamento'),
            use_container_width=True,
        )
    ranking = ranking_produtos(df_filtrado, 10)
    with graf2:
        st.plotly_chart(
            px.bar(ranking.sort_values('Faturamento'), x='Faturamento', y='Produto', orientation='h', title='Top produtos por faturamento'),
            use_container_width=True,
        )

    cat1, cat2 = st.columns([1, 1.2])
    categorias_df = vendas_por_categoria(df_filtrado)
    with cat1:
        st.plotly_chart(px.pie(categorias_df, values='Faturamento', names='Categoria', hole=.45, title='Participação por categoria'), use_container_width=True)
    with cat2:
        st.subheader('Ranking de produtos')
        tabela = ranking.copy()
        tabela['Faturamento'] = tabela['Faturamento'].map(lambda v: f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.dataframe(tabela, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader('Gerar relatório')
    col_pdf, col_email = st.columns(2)

    if col_pdf.button('Gerar PDF', type='primary', use_container_width=True):
        nome = f"relatorio_comercial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        caminho = CONFIG.diretorio_saida / nome
        gerar_relatorio_pdf(df_filtrado, caminho)
        st.session_state['ultimo_pdf'] = str(caminho)
        st.success('Relatório gerado com sucesso.')

    if 'ultimo_pdf' in st.session_state:
        caminho_pdf = Path(st.session_state['ultimo_pdf'])
        with caminho_pdf.open('rb') as f:
            st.download_button('Baixar último PDF', data=f.read(), file_name=caminho_pdf.name, mime='application/pdf', use_container_width=True)

    with col_email:
        destinatario = st.text_input('E-mail do destinatário')
        if st.button('Enviar último PDF por e-mail', use_container_width=True):
            if 'ultimo_pdf' not in st.session_state:
                st.error('Gere um PDF antes de enviar.')
            elif not destinatario:
                st.error('Informe o e-mail do destinatário.')
            else:
                enviar_email(
                    destinatario=destinatario,
                    assunto='Relatório Comercial Automatizado',
                    corpo='Olá! Segue em anexo o relatório comercial gerado automaticamente.',
                    caminho_anexo=Path(st.session_state['ultimo_pdf']),
                    remetente=CONFIG.email_remetente,
                    senha=CONFIG.email_senha,
                    smtp_host=CONFIG.smtp_host,
                    smtp_port=CONFIG.smtp_port,
                )
                st.success('E-mail enviado com sucesso.')

except Exception as exc:
    st.error(f'Não foi possível processar os dados: {exc}')
