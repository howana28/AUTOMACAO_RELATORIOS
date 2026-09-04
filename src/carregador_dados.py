from pathlib import Path
from typing import BinaryIO, Union
import pandas as pd

OrigemDados = Union[str, Path, BinaryIO]


def carregar_planilha(origem: OrigemDados) -> pd.DataFrame:
    try:
        return pd.read_excel(origem)
    except FileNotFoundError as exc:
        raise FileNotFoundError('A planilha informada não foi encontrada.') from exc
    except Exception as exc:
        raise ValueError(f'Não foi possível ler a planilha: {exc}') from exc
