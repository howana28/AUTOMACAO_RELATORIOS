from dataclasses import dataclass
import pandas as pd


@dataclass
class KPIs:
    faturamento_total: float
    total_pedidos: int
    ticket_medio: float
    itens_vendidos: int
    produto_mais_vendido: str
    produto_maior_faturamento: str
    lucro_total: float | None = None
    margem_percentual: float | None = None


def calcular_kpis(df: pd.DataFrame) -> KPIs:
    faturamento = float(df['Faturamento'].sum())
    pedidos = int(df['Pedido'].nunique())
    ticket = faturamento / pedidos if pedidos else 0.0
    itens = int(df['Quantidade'].sum())

    qtd_produto = df.groupby('Produto')['Quantidade'].sum().sort_values(ascending=False)
    fat_produto = df.groupby('Produto')['Faturamento'].sum().sort_values(ascending=False)

    lucro = None
    margem = None
    if 'Lucro' in df.columns:
        lucro = float(df['Lucro'].sum())
        margem = (lucro / faturamento * 100) if faturamento else 0.0

    return KPIs(
        faturamento_total=faturamento,
        total_pedidos=pedidos,
        ticket_medio=ticket,
        itens_vendidos=itens,
        produto_mais_vendido=qtd_produto.index[0] if not qtd_produto.empty else '-',
        produto_maior_faturamento=fat_produto.index[0] if not fat_produto.empty else '-',
        lucro_total=lucro,
        margem_percentual=margem,
    )


def vendas_por_dia(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(Dia=df['Data'].dt.date)
        .groupby('Dia', as_index=False)['Faturamento']
        .sum()
        .sort_values('Dia')
    )


def ranking_produtos(df: pd.DataFrame, limite: int = 10) -> pd.DataFrame:
    return (
        df.groupby('Produto', as_index=False)
        .agg(Quantidade=('Quantidade', 'sum'), Faturamento=('Faturamento', 'sum'))
        .sort_values('Faturamento', ascending=False)
        .head(limite)
    )


def vendas_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby('Categoria', as_index=False)['Faturamento']
        .sum()
        .sort_values('Faturamento', ascending=False)
    )
