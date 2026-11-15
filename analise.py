"""
analise.py
==========
"""

import numpy as np
from estatistica import calcular_percentis, intervalo_confianca_proporcao
from simulacao import classificar_resultado


def calcular_probabilidades_resultado(lucro_final: np.ndarray, lucro_atual: float,
                                        tolerancia: float = 0.02,
                                        confianca: float = 0.95) -> dict:
    n = len(lucro_final)
    classificacao = classificar_resultado(lucro_final, lucro_atual, tolerancia)
    resultado = {}
    for nome, mascara in classificacao.items():
        p = float(np.mean(mascara))
        ic_inferior, ic_superior = intervalo_confianca_proporcao(p, n, confianca)
        resultado[nome] = {
            "probabilidade": p,
            "intervalo_confianca": (ic_inferior, ic_superior),
        }
    return resultado


def probabilidade_meta(lucro_final: np.ndarray, meta: float) -> float:
    return float(np.mean(lucro_final >= meta))


def probabilidade_prejuizo(lucro_final: np.ndarray) -> float:
    return float(np.mean(lucro_final < 0))


def probabilidade_queda_maior_que(lucro_final: np.ndarray, lucro_atual: float,
                                    percentual: float = 0.10) -> float:
    limite = lucro_atual * (1 - percentual)
    return float(np.mean(lucro_final <= limite))


def probabilidade_aumento_maior_que(lucro_final: np.ndarray, lucro_atual: float,
                                      percentual: float = 0.20) -> float:
    limite = lucro_atual * (1 + percentual)
    return float(np.mean(lucro_final >= limite))


def resumo_estatistico(lucro_final: np.ndarray) -> dict:
    percentis = calcular_percentis(lucro_final, (10, 25, 50, 75, 90))
    return {
        "valor_esperado": float(np.mean(lucro_final)),
        "minimo": float(np.min(lucro_final)),
        "maximo": float(np.max(lucro_final)),
        "mediana": float(np.median(lucro_final)),
        "desvio_padrao": float(np.std(lucro_final, ddof=1)),
        "percentis": percentis,
    }
