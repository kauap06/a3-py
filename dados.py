"""
dados.py
========

Responsável por CARREGAR e VALIDAR os dados financeiros históricos da
empresa (receita, custos operacionais e volume de vendas mensais).
"""

from dataclasses import dataclass
import numpy as np

try:
    import pandas as pd
except ImportError:
    pd = None

MESES_MINIMOS_EXIGIDOS = 4


@dataclass
class DadosFinanceiros:
    meses: np.ndarray
    receita: np.ndarray
    custos: np.ndarray
    volume_vendas: np.ndarray
    origem: str

    @property
    def lucro(self) -> np.ndarray:
        return self.receita - self.custos

    @property
    def margem_lucro(self) -> np.ndarray:
        return (self.lucro / self.receita) * 100

    @property
    def n_meses(self) -> int:
        return len(self.receita)


def carregar_dados_exemplo() -> DadosFinanceiros:
    meses = np.arange(1, 13)
    receita = np.array([
        10000, 10400, 10600, 10300, 10800, 10900,
        10500, 11100, 10900, 11200, 11800, 11400,
    ], dtype=float)
    custos = np.array([
        6000, 6200, 6400, 6300, 6600, 6700,
        6600, 6900, 6900, 7100, 7400, 7300,
    ], dtype=float)
    volume_vendas = np.array([
        500, 520, 530, 520, 540, 540,
        520, 560, 540, 560, 590, 570,
    ], dtype=float)
    return DadosFinanceiros(
        meses=meses,
        receita=receita,
        custos=custos,
        volume_vendas=volume_vendas,
        origem="fictícios (dados de demonstração)",
    )


def carregar_dados_csv(caminho_arquivo: str) -> DadosFinanceiros:
    if pd is None:
        raise ValueError("A biblioteca pandas não está instalada.")
    tabela = pd.read_csv(caminho_arquivo)
    colunas_obrigatorias = {"mes", "receita", "custos", "volume_vendas"}
    colunas_faltando = colunas_obrigatorias - set(tabela.columns)
    if colunas_faltando:
        raise ValueError(f"Colunas faltando: {colunas_faltando}")
    dados = DadosFinanceiros(
        meses=tabela["mes"].to_numpy(),
        receita=tabela["receita"].to_numpy(dtype=float),
        custos=tabela["custos"].to_numpy(dtype=float),
        volume_vendas=tabela["volume_vendas"].to_numpy(dtype=float),
        origem=f"arquivo '{caminho_arquivo}'",
    )
    validar_dados(dados)
    return dados


def validar_dados(dados: DadosFinanceiros) -> None:
    n = dados.n_meses
    if n < MESES_MINIMOS_EXIGIDOS:
        raise ValueError(f"Histórico insuficiente: {n} meses (mínimo {MESES_MINIMOS_EXIGIDOS}).")
    if np.any(dados.receita <= 0):
        raise ValueError("Receita menor ou igual a zero encontrada.")
    if np.any(dados.custos < 0):
        raise ValueError("Custo negativo encontrado.")
