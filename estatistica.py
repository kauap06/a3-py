"""
estatistica.py
==============
"""

import numpy as np


def calcular_variacoes_percentuais(serie: np.ndarray) -> np.ndarray:
    serie = np.asarray(serie, dtype=float)
    return (serie[1:] - serie[:-1]) / serie[:-1]


def media_variancia_desvio(amostra: np.ndarray) -> tuple:
    media = float(np.mean(amostra))
    variancia = float(np.var(amostra, ddof=1))
    desvio = float(np.std(amostra, ddof=1))
    return media, variancia, desvio


def matriz_covariancia_correlacao(variacao_receita: np.ndarray,
                                    variacao_custo: np.ndarray) -> dict:
    vetor_medias = np.array([np.mean(variacao_receita), np.mean(variacao_custo)])
    matriz_cov = np.cov(variacao_receita, variacao_custo, ddof=1)
    correlacao = float(np.corrcoef(variacao_receita, variacao_custo)[0, 1])
    return {
        "vetor_medias": vetor_medias,
        "matriz_covariancia": matriz_cov,
        "correlacao": correlacao,
    }


def calcular_percentis(amostra: np.ndarray, percentis=(10, 25, 50, 75, 90)) -> dict:
    valores = np.percentile(amostra, percentis)
    return {f"p{p}": float(v) for p, v in zip(percentis, valores)}


def intervalo_confianca_proporcao(p_estimado: float, n_amostras: int,
                                    confianca: float = 0.95) -> tuple:
    if n_amostras <= 0:
        return (0.0, 1.0)
    z = 1.959964
    n = n_amostras
    p = p_estimado
    denominador = 1 + (z ** 2) / n
    centro = p + (z ** 2) / (2 * n)
    margem = z * np.sqrt((p * (1 - p) / n) + (z ** 2) / (4 * n ** 2))
    limite_inferior = (centro - margem) / denominador
    limite_superior = (centro + margem) / denominador
    return (max(0.0, float(limite_inferior)), min(1.0, float(limite_superior)))
