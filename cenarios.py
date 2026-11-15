"""
cenarios.py
===========
"""

import numpy as np

AJUSTES_CENARIOS = {
    "otimista": {
        "descricao": "Crescimento de receita favorável e controle de custos.",
        "ajuste_media_receita": 0.02,
        "ajuste_media_custo": -0.01,
        "fator_reducao_desvio": 0.85,
        "ajuste_inflacao": -0.001,
    },
    "realista": {
        "descricao": "Baseado diretamente no comportamento histórico observado.",
        "ajuste_media_receita": 0.0,
        "ajuste_media_custo": 0.0,
        "fator_reducao_desvio": 1.0,
        "ajuste_inflacao": 0.0,
    },
    "pessimista": {
        "descricao": "Redução de receita e aumento de custos.",
        "ajuste_media_receita": -0.025,
        "ajuste_media_custo": 0.015,
        "fator_reducao_desvio": 1.25,
        "ajuste_inflacao": 0.003,
    },
}


def montar_parametros_cenario(nome_cenario: str, vetor_medias: np.ndarray,
                                 matriz_covariancia: np.ndarray,
                                 inflacao_mensal_base: float) -> dict:
    if nome_cenario not in AJUSTES_CENARIOS:
        raise ValueError(f"Cenário desconhecido: '{nome_cenario}'.")
    ajuste = AJUSTES_CENARIOS[nome_cenario]
    vetor_medias_ajustado = vetor_medias + np.array([
        ajuste["ajuste_media_receita"],
        ajuste["ajuste_media_custo"],
    ])
    fator = ajuste["fator_reducao_desvio"]
    matriz_covariancia_ajustada = matriz_covariancia * (fator ** 2)
    inflacao_ajustada = inflacao_mensal_base + ajuste["ajuste_inflacao"]
    return {
        "vetor_medias": vetor_medias_ajustado,
        "matriz_covariancia": matriz_covariancia_ajustada,
        "inflacao_mensal": inflacao_ajustada,
        "descricao": ajuste["descricao"],
    }
