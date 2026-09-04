from io import BytesIO
from pathlib import Path
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

from .analises import calcular_kpis, vendas_por_dia, ranking_produtos, vendas_por_categoria


def _moeda(valor: float) -> str:
    txt = f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {txt}'


def _grafico_linha(df):
    dados = vendas_por_dia(df)
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(dados['Dia'].astype(str), dados['Faturamento'], marker='o')
    ax.set_title('Evolução do faturamento')
    ax.set_xlabel('Data')
    ax.set_ylabel('Faturamento (R$)')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer


def _grafico_produtos(df):
    dados = ranking_produtos(df, 8).sort_values('Faturamento')
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.barh(dados['Produto'], dados['Faturamento'])
    ax.set_title('Produtos com maior faturamento')
    ax.set_xlabel('Faturamento (R$)')
    fig.tight_layout()
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer


def gerar_relatorio_pdf(df, caminho_saida: Path, titulo: str = 'Relatório Comercial') -> Path:
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    kpis = calcular_kpis(df)
    categorias = vendas_por_categoria(df)
    ranking = ranking_produtos(df, 10)

    doc = SimpleDocTemplate(
        str(caminho_saida),
        pagesize=A4,
        rightMargin=1.4 * cm,
        leftMargin=1.4 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TituloRelatorio', parent=styles['Title'], fontSize=20, leading=24, spaceAfter=8))
    styles.add(ParagraphStyle(name='Subtitulo', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#555555')))

    inicio = df['Data'].min().strftime('%d/%m/%Y')
    fim = df['Data'].max().strftime('%d/%m/%Y')

    story = [
        Paragraph(titulo, styles['TituloRelatorio']),
        Paragraph(f'Período analisado: {inicio} a {fim}', styles['Subtitulo']),
        Spacer(1, 0.45 * cm),
    ]

    linha1 = [
        ['Faturamento', _moeda(kpis.faturamento_total)],
        ['Pedidos', f'{kpis.total_pedidos:,}'.replace(',', '.')],
        ['Ticket médio', _moeda(kpis.ticket_medio)],
        ['Itens vendidos', f'{kpis.itens_vendidos:,}'.replace(',', '.')],
    ]
    tabela_kpi = Table(linha1, colWidths=[3.2*cm, 2.2*cm] * 2)
    tabela_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F4F6F8')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D0D7DE')),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#D0D7DE')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.extend([tabela_kpi, Spacer(1, 0.35 * cm)])

    destaques = [
        ['Produto mais vendido', kpis.produto_mais_vendido],
        ['Maior faturamento por produto', kpis.produto_maior_faturamento],
    ]
    if kpis.lucro_total is not None:
        destaques += [
            ['Lucro estimado', _moeda(kpis.lucro_total)],
            ['Margem estimada', f'{kpis.margem_percentual:.1f}%'.replace('.', ',')],
        ]

    tabela_destaques = Table(destaques, colWidths=[5.5*cm, 11.0*cm])
    tabela_destaques.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D0D7DE')),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#E5E7EB')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8FAFC')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.extend([tabela_destaques, Spacer(1, 0.35 * cm)])

    grafico1 = _grafico_linha(df)
    grafico2 = _grafico_produtos(df)
    story.extend([
        Image(grafico1, width=17.3*cm, height=6.2*cm),
        Spacer(1, 0.25*cm),
        Image(grafico2, width=17.3*cm, height=7.2*cm),
        PageBreak(),
        Paragraph('Ranking de produtos', styles['Heading2']),
        Spacer(1, 0.2*cm),
    ])

    tabela_produtos = [['Produto', 'Quantidade', 'Faturamento']]
    for _, row in ranking.iterrows():
        tabela_produtos.append([
            str(row['Produto']),
            f"{int(row['Quantidade']):,}".replace(',', '.'),
            _moeda(float(row['Faturamento'])),
        ])
    tp = Table(tabela_produtos, repeatRows=1, colWidths=[9.3*cm, 3.1*cm, 4.1*cm])
    tp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#111827')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.35, colors.HexColor('#D1D5DB')),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ]))
    story.extend([tp, Spacer(1, 0.4*cm), Paragraph('Faturamento por categoria', styles['Heading2'])])

    tabela_cat = [['Categoria', 'Faturamento']]
    for _, row in categorias.iterrows():
        tabela_cat.append([str(row['Categoria']), _moeda(float(row['Faturamento']))])
    tc = Table(tabela_cat, repeatRows=1, colWidths=[10.5*cm, 6.0*cm])
    tc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#111827')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.35, colors.HexColor('#D1D5DB')),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
    ]))
    story.append(tc)
    doc.build(story)
    return caminho_saida
