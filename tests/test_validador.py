import pandas as pd
import pytest
from src.validador import validar_e_preparar


def test_erro_coluna_obrigatoria():
    df = pd.DataFrame({'Produto': ['A']})
    with pytest.raises(ValueError, match='colunas obrigatórias'):
        validar_e_preparar(df)


def test_cria_faturamento():
    df = pd.DataFrame({
        'Data': ['2026-04-01'],
        'Pedido': ['1'],
        'Produto': ['A'],
        'Categoria': ['Teste'],
        'Quantidade': [2],
        'Preco_Unitario': [15],
    })
    resultado = validar_e_preparar(df)
    assert resultado.loc[0, 'Faturamento'] == 30
