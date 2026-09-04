import pandas as pd
from src.analises import calcular_kpis, ranking_produtos
from src.validador import validar_e_preparar


def _df_exemplo():
    return pd.DataFrame({
        'Data': ['2026-04-01', '2026-04-01', '2026-04-02'],
        'Pedido': ['A1', 'A1', 'A2'],
        'Produto': ['Produto A', 'Produto B', 'Produto A'],
        'Categoria': ['Categoria 1', 'Categoria 2', 'Categoria 1'],
        'Quantidade': [2, 1, 3],
        'Preco_Unitario': [10.0, 20.0, 10.0],
        'Custo_Unitario': [5.0, 12.0, 5.0],
    })


def test_calcular_kpis():
    df = validar_e_preparar(_df_exemplo())
    kpis = calcular_kpis(df)
    assert kpis.faturamento_total == 70.0
    assert kpis.total_pedidos == 2
    assert kpis.ticket_medio == 35.0
    assert kpis.itens_vendidos == 6
    assert kpis.produto_mais_vendido == 'Produto A'
    assert kpis.lucro_total == 33.0


def test_ranking_produtos():
    df = validar_e_preparar(_df_exemplo())
    ranking = ranking_produtos(df)
    assert ranking.iloc[0]['Produto'] == 'Produto A'
    assert ranking.iloc[0]['Faturamento'] == 50.0
