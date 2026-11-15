"""
simulacao.py
=============

Núcleo do SIMULADOR DE MONTE CARLO.
"""

import numpy as np


def gerar_variacoes_correlacionadas(vetor_medias: np.ndarray,
                                      matriz_covariancia: np.ndarray,
                                      n_simulacoes: int,
                                      n_meses: int,
                                      gerador: np.random.Generator) -> np.ndarray:
    total_sorteios = n_simulacoes * n_meses
    amostras = gerador.multivariate_normal(
        mean=vetor_medias,
        cov=matriz_covariancia,
        size=total_sorteios,
    )
    return amostras.reshape(n_simulacoes, n_meses, 2)


def simular_monte_carlo(receita_atual: float,
                          custo_atual: float,
                          vetor_medias: np.ndarray,
                          matriz_covariancia: np.ndarray,
                          inflacao_mensal: float,
                          n_meses: int,
                          n_simulacoes: int,
                          semente: int = 42) -> dict:
    if n_meses <= 0 or n_simulacoes <= 0:
        raise ValueError("Parâmetros inválidos.")

    gerador = np.random.default_rng(semente)
    variacoes = gerar_variacoes_correlacionadas(
        vetor_medias, matriz_covariancia, n_simulacoes, n_meses, gerador
    )
    variacao_receita = variacoes[:, :, 0]
    variacao_custo = variacoes[:, :, 1] + inflacao_mensal

    receitas = np.zeros((n_simulacoes, n_meses))
    custos = np.zeros((n_simulacoes, n_meses))

    receita_corrente = np.full(n_simulacoes, receita_atual, dtype=float)
    custo_corrente = np.full(n_simulacoes, custo_atual, dtype=float)

    for mes in range(n_meses):
        receita_corrente = receita_corrente * (1 + variacao_receita[:, mes])
        custo_corrente = custo_corrente * (1 + variacao_custo[:, mes])
        receita_corrente = np.maximum(receita_corrente, 0.0)
        custo_corrente = np.maximum(custo_corrente, 0.0)
        receitas[:, mes] = receita_corrente
        custos[:, mes] = custo_corrente

    lucros = receitas - custos
    return {"receitas": receitas, "custos": custos, "lucros": lucros}


def classificar_resultado(lucro_final: np.ndarray, lucro_atual: float,
                            tolerancia: float = 0.02) -> dict:
    limite_superior = lucro_atual * (1 + tolerancia)
    limite_inferior = lucro_atual * (1 - tolerancia)
    estavel = (lucro_final >= limite_inferior) & (lucro_final <= limite_superior)
    aumento = lucro_final > limite_superior
    queda = lucro_final < limite_inferior
    return {"aumento": aumento, "queda": queda, "estavel": estavel}
