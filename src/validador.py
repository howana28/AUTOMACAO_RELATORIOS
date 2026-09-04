import pandas as pd

COLUNAS_OBRIGATORIAS = {
    'Data', 'Pedido', 'Produto', 'Categoria', 'Quantidade', 'Preco_Unitario'
}
COLUNAS_OPCIONAIS = {'Custo_Unitario'}


def validar_e_preparar(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError('A planilha está vazia.')

    faltantes = sorted(COLUNAS_OBRIGATORIAS - set(df.columns))
    if faltantes:
        raise ValueError(
            'A planilha não possui todas as colunas obrigatórias. Faltando: '
            + ', '.join(faltantes)
        )

    dados = df.copy()
    dados['Data'] = pd.to_datetime(dados['Data'], errors='coerce')
    dados['Quantidade'] = pd.to_numeric(dados['Quantidade'], errors='coerce')
    dados['Preco_Unitario'] = pd.to_numeric(dados['Preco_Unitario'], errors='coerce')

    if 'Custo_Unitario' in dados.columns:
        dados['Custo_Unitario'] = pd.to_numeric(dados['Custo_Unitario'], errors='coerce')

    colunas_criticas = ['Data', 'Pedido', 'Produto', 'Quantidade', 'Preco_Unitario']
    invalidas = dados[colunas_criticas].isna().any(axis=1)
    if invalidas.any():
        qtd = int(invalidas.sum())
        raise ValueError(f'Existem {qtd} linha(s) com dados obrigatórios inválidos ou vazios.')

    if (dados['Quantidade'] <= 0).any():
        raise ValueError('A coluna Quantidade deve conter apenas valores maiores que zero.')

    if (dados['Preco_Unitario'] < 0).any():
        raise ValueError('A coluna Preco_Unitario não pode conter valores negativos.')

    dados['Categoria'] = dados['Categoria'].fillna('Sem categoria').astype(str).str.strip()
    dados['Produto'] = dados['Produto'].astype(str).str.strip()
    dados['Pedido'] = dados['Pedido'].astype(str).str.strip()

    dados['Faturamento'] = dados['Quantidade'] * dados['Preco_Unitario']

    if 'Custo_Unitario' in dados.columns:
        dados['Custo_Total'] = dados['Quantidade'] * dados['Custo_Unitario'].fillna(0)
        dados['Lucro'] = dados['Faturamento'] - dados['Custo_Total']

    return dados.sort_values('Data').reset_index(drop=True)
