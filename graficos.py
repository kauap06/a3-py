"""
graficos.py
============

Geração de todos os gráficos do projeto, usando Matplotlib.

Gráfico 1 — Distribuição do lucro simulado (histograma, verde/vermelho)
Gráfico 2 — Evolução do lucro futuro mês a mês (faixas de percentis)
Gráfico 3 — Análise de sensibilidade (quais variáveis mais afetam o lucro)

Todos os gráficos usam formatação em Reais (R$) nos eixos e possuem
título, legenda e rótulos de eixo, para que sejam compreensíveis mesmo
para quem não é técnico (ex.: um gestor da empresa).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def formatar_reais(valor, pos=None):
    """Formata um número do eixo como 'R$ 12.000' em vez de '12000.0'."""
    sinal = "-" if valor < 0 else ""
    return f"{sinal}R$ {abs(valor):,.0f}".replace(",", ".")


def _estilizar_eixos(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25)


# ---------------------------------------------------------------------
# GRÁFICO 1 — Distribuição do lucro final simulado
# ---------------------------------------------------------------------

def grafico_distribuicao_lucro(lucro_final: np.ndarray, lucro_atual: float,
                                 valor_esperado: float, prob_aumento: float,
                                 prob_queda: float,
                                 nome_arquivo: str = "grafico_1_distribuicao_lucro.png") -> None:
    bins = np.linspace(lucro_final.min(), lucro_final.max(), 60)
    cenarios_queda = lucro_final[lucro_final <= lucro_atual]
    cenarios_aumento = lucro_final[lucro_final > lucro_atual]

    plt.figure(figsize=(11, 6.5))
    plt.hist(cenarios_queda, bins=bins, color="#e74c3c", edgecolor="white",
              alpha=0.85, label=f"Futuros em que o lucro CAIU ({prob_queda * 100:.0f}% dos casos)")
    plt.hist(cenarios_aumento, bins=bins, color="#2ecc71", edgecolor="white",
              alpha=0.85, label=f"Futuros em que o lucro AUMENTOU ({prob_aumento * 100:.0f}% dos casos)")

    plt.axvline(lucro_atual, color="#2c3e50", linestyle="--", linewidth=2.2,
                label=f"Lucro de hoje: {formatar_reais(lucro_atual)}")
    plt.axvline(valor_esperado, color="#8e44ad", linestyle="-", linewidth=2.5,
                label=f"Lucro esperado (média de todos os futuros): {formatar_reais(valor_esperado)}")

    ax = plt.gca()
    ax.xaxis.set_major_formatter(FuncFormatter(formatar_reais))
    _estilizar_eixos(ax)

    plt.title("Gráfico 1 — Todos os futuros possíveis para o lucro, lado a lado\n(cada barra é um grupo de 'sorteios' do computador)",
               fontsize=15, fontweight="bold", pad=16)
    plt.xlabel("Lucro que a loja teria, nesse futuro simulado", fontsize=12, labelpad=10)
    plt.ylabel("Quantos futuros simulados deram nesse resultado", fontsize=12, labelpad=10)
    plt.xticks(fontsize=10, rotation=15)
    plt.yticks(fontsize=10)
    plt.legend(fontsize=10.5, loc="upper left", frameon=True, framealpha=0.95)
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=180)
    plt.close()


# ---------------------------------------------------------------------
# GRÁFICO 2 — Evolução do lucro futuro mês a mês
# ---------------------------------------------------------------------

def grafico_evolucao_lucro(lucros_simulados: np.ndarray, lucro_atual: float,
                             nome_arquivo: str = "grafico_2_evolucao_lucro.png") -> None:
    n_meses = lucros_simulados.shape[1]
    meses = np.arange(1, n_meses + 1)

    p10 = np.percentile(lucros_simulados, 10, axis=0)
    p25 = np.percentile(lucros_simulados, 25, axis=0)
    p50 = np.percentile(lucros_simulados, 50, axis=0)
    p75 = np.percentile(lucros_simulados, 75, axis=0)
    p90 = np.percentile(lucros_simulados, 90, axis=0)

    plt.figure(figsize=(11, 6.5))
    plt.fill_between(meses, p10, p90, color="#3498db", alpha=0.18,
                       label="Praticamente todos os futuros simulados caem nesta faixa")
    plt.fill_between(meses, p25, p75, color="#3498db", alpha=0.38,
                       label="A metade dos futuros mais comuns cai nesta faixa (mais provável)")
    plt.plot(meses, p50, color="#1a5276", linewidth=2.8,
              label="O resultado 'do meio' (metade ficou acima, metade abaixo)")
    plt.axhline(lucro_atual, color="#2c3e50", linestyle="--", linewidth=1.8,
                label=f"Lucro de hoje: {formatar_reais(lucro_atual)}")

    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(formatar_reais))
    _estilizar_eixos(ax)

    passo_xticks = max(1, n_meses // 12)
    plt.title("Gráfico 2 — Como o lucro tende a se mover, mês a mês\n(quanto mais larga a faixa, maior a incerteza)",
               fontsize=15, fontweight="bold", pad=16)
    plt.xlabel("Meses no futuro", fontsize=12, labelpad=10)
    plt.ylabel("Lucro projetado", fontsize=12, labelpad=10)
    plt.xticks(meses[::passo_xticks], fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(fontsize=10.5, loc="upper left", frameon=True, framealpha=0.95)
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=180)
    plt.close()


# ---------------------------------------------------------------------
# GRÁFICO 3 — Análise de sensibilidade (gráfico "tornado" aprimorado)
# ---------------------------------------------------------------------

def grafico_analise_sensibilidade(receita_atual: float, custo_atual: float,
                                     volume_atual: float,
                                     variacao_analise: float = 0.10,
                                     nome_arquivo: str = "grafico_3_sensibilidade.png") -> None:
    """
    Gráfico de sensibilidade (estilo "tornado") aprimorado para máxima clareza:
    exibe o impacto exato em R$ nas pontas das barras, facilitando a leitura visual.
    """
    lucro_base = receita_atual - custo_atual
    preco_medio = receita_atual / volume_atual if volume_atual > 0 else 0

    variaveis = []

    # Receita
    receita_baixa = receita_atual * (1 - variacao_analise)
    receita_alta = receita_atual * (1 + variacao_analise)
    variaveis.append((
        "Faturamento (Receita)",
        (receita_baixa - custo_atual) - lucro_base,
        (receita_alta - custo_atual) - lucro_base,
    ))

    # Custos
    custo_baixo = custo_atual * (1 - variacao_analise)
    custo_alto = custo_atual * (1 + variacao_analise)
    variaveis.append((
        "Custos Operacionais",
        (receita_atual - custo_alto) - lucro_base,
        (receita_atual - custo_baixo) - lucro_base,
    ))

    # Volume de Vendas
    vol_baixo_rec = preco_medio * volume_atual * (1 - variacao_analise)
    vol_alto_rec = preco_medio * volume_atual * (1 + variacao_analise)
    variaveis.append((
        "Volume de Vendas",
        (vol_baixo_rec - custo_atual) - lucro_base,
        (vol_alto_rec - custo_atual) - lucro_base,
    ))

    # Ordena pelo impacto total (do maior para o menor)
    variaveis.sort(key=lambda item: abs(item[2] - item[1]), reverse=True)

    nomes = [v[0] for v in variaveis]
    impacto_baixa = [v[1] for v in variaveis]
    impacto_alta = [v[2] for v in variaveis]
    posicoes = np.arange(len(nomes))

    fig, ax = plt.subplots(figsize=(11, 5.5))

    ax.barh(posicoes, impacto_alta, color="#2ecc71", alpha=0.85, height=0.48,
              label=f"Se o indicador subir {variacao_analise * 100:.0f}%")
    ax.barh(posicoes, impacto_baixa, color="#e74c3c", alpha=0.85, height=0.48,
              label=f"Se o indicador cair {variacao_analise * 100:.0f}%")

    ax.axvline(0, color="#2c3e50", linewidth=1.5, linestyle="-")

    # Escreve o valor exato em R$ na ponta de cada barra para clareza absoluta
    for i, (imp_b, imp_a) in enumerate(zip(impacto_baixa, impacto_alta)):
        ha_b = "right" if imp_b < 0 else "left"
        ax.text(imp_b, i, formatar_reais(imp_b), va="center", ha=ha_b, fontsize=9.5, fontweight="bold", color="#c0392b")

        ha_a = "left" if imp_a >= 0 else "right"
        ax.text(imp_a, i, formatar_reais(imp_a), va="center", ha=ha_a, fontsize=9.5, fontweight="bold", color="#27ae60")

    ax.xaxis.set_major_formatter(FuncFormatter(formatar_reais))
    ax.set_yticks(posicoes)
    ax.set_yticklabels(nomes, fontsize=11, fontweight="bold")
    _estilizar_eixos(ax)

    plt.title(f"Gráfico 3 — O que mais impacta o seu lucro?\n(Mudança estimada no lucro caso o indicador varie {variacao_analise*100:.0f}%)",
               fontsize=14, fontweight="bold", pad=16)
    plt.xlabel("Impacto financeiro no lucro mensal (R$)", fontsize=11, labelpad=10)
    plt.xticks(fontsize=10)
    plt.legend(fontsize=10, loc="upper right", frameon=True, framealpha=0.95)
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=180)
    plt.close()
