"""
main.py
========

SIMULADOR DE PROBABILIDADE DE LUCRO EMPRESARIAL
-------------------------------------------------

Programa principal: conecta todos os módulos do projeto (dados,
estatistica, simulacao, analise, cenarios, graficos) e conduz o usuário
pelo fluxo completo da simulação.

Projeto acadêmico — Atividade Prática A3 de Matemática Computacional
Aplicada. Tema: Probabilidade e Simulação (Simulação de Monte Carlo).

Para rodar: `python main.py`
"""

import os
import sys

import numpy as np

from dados import carregar_dados_exemplo, carregar_dados_csv, validar_dados, MESES_MINIMOS_EXIGIDOS
from estatistica import (
    calcular_variacoes_percentuais,
    media_variancia_desvio,
    matriz_covariancia_correlacao,
)
from simulacao import simular_monte_carlo
from analise import (
    calcular_probabilidades_resultado,
    probabilidade_meta,
    probabilidade_prejuizo,
    probabilidade_queda_maior_que,
    probabilidade_aumento_maior_que,
    resumo_estatistico,
)
from cenarios import montar_parametros_cenario, AJUSTES_CENARIOS
from graficos import (
    grafico_distribuicao_lucro,
    grafico_evolucao_lucro,
    grafico_analise_sensibilidade,
    formatar_reais,
)


# =======================================================================
# FUNÇÕES AUXILIARES DE ENTRADA (COM VALIDAÇÃO)
# =======================================================================

def ler_numero(mensagem: str, padrao, tipo=int, minimo=None):
    """
    Lê um número digitado pelo usuário, com valor padrão (caso o usuário
    apenas aperte Enter) e validação de tipo e de valor mínimo.

    Em caso de entrada inválida (texto não numérico, ou abaixo do
    mínimo permitido), o programa avisa e usa o valor padrão, em vez de
    travar com uma exceção não tratada — importante para um programa
    que será usado por um usuário não técnico.
    """
    texto = input(mensagem).strip()
    if texto == "":
        return padrao
    try:
        valor = tipo(texto)
    except ValueError:
        print(f"  -> Entrada inválida ('{texto}'). Usando valor padrão: {padrao}.")
        return padrao

    if minimo is not None and valor < minimo:
        print(f"  -> Valor abaixo do mínimo permitido ({minimo}). Usando valor padrão: {padrao}.")
        return padrao

    return valor


def escolher_fonte_de_dados():
    """
    Pergunta ao usuário se ele quer usar o conjunto de dados fictício de
    demonstração ou carregar um arquivo .csv com dados reais da empresa.
    """
    print("\nFonte dos dados financeiros:")
    print("  [1] Usar dados fictícios de demonstração (padrão)")
    print("  [2] Carregar um arquivo .csv com dados reais da empresa")
    escolha = input("Escolha uma opção (1 ou 2) [1]: ").strip()

    if escolha == "2":
        caminho = input("Caminho do arquivo .csv: ").strip()
        try:
            dados = carregar_dados_csv(caminho)
            print(f"  -> Dados carregados com sucesso de '{caminho}'.")
            return dados
        except ValueError as erro:
            print(f"  -> ERRO ao carregar o arquivo: {erro}")
            print("  -> Usando dados fictícios de demonstração em vez disso.")
            return carregar_dados_exemplo()

    return carregar_dados_exemplo()


# =======================================================================
# APRESENTAÇÃO DOS RESULTADOS NO TERMINAL
# =======================================================================

def imprimir_explicacao_simples():
    """
    Explica o programa em linguagem simples, do zero, ANTES de qualquer
    número aparecer na tela — pensando em quem nunca trabalhou com
    finanças ou com uma empresa.
    """
    print(
        "\nO que este programa faz, em poucas palavras:\n"
        "\n"
        "  É parecido com uma previsão do tempo. Quando a previsão diz\n"
        "  '70% de chance de chuva amanhã', ninguém tem certeza absoluta —\n"
        "  é uma estimativa, baseada em como o tempo se comportou em\n"
        "  situações parecidas no passado.\n"
        "\n"
        "  Este programa faz o mesmo, mas com o LUCRO de uma loja/empresa:\n"
        "  ele olha para os meses anteriores (quanto a loja ganhou e quanto\n"
        "  ela gastou) e usa essa história para 'sortear' milhares de\n"
        "  futuros possíveis no computador. No final, ele conta: em quantos\n"
        "  desses futuros o lucro subiu? Em quantos caiu? Essa contagem vira\n"
        "  uma porcentagem — a chance estimada de cada coisa acontecer.\n"
        "\n"
        "  Você vai ver estes termos ao longo da execução:\n"
        "  - RECEITA  = tudo que a loja recebeu vendendo no mês.\n"
        "  - CUSTO    = tudo que a loja gastou para funcionar no mês.\n"
        "  - LUCRO    = o que sobra: Receita menos Custo.\n"
        "  - CHANCE DE AUMENTAR/CAIR = em quantos dos futuros simulados o\n"
        "    lucro ficou maior ou menor do que está hoje.\n"
    )


def imprimir_cabecalho_dados(dados):
    print("\n" + "=" * 72)
    print("1. OS DADOS DE PARTIDA (o histórico da loja)")
    print("=" * 72)
    print(f"Origem dos dados: {dados.origem}")
    print(f"Quantos meses de histórico temos: {dados.n_meses}")
    print(f"Quanto a loja recebeu no último mês (receita): {formatar_reais(dados.receita[-1])}")
    print(f"Quanto a loja gastou no último mês (custo): {formatar_reais(dados.custos[-1])}")
    print(f"Quantos produtos foram vendidos no último mês: {dados.volume_vendas[-1]:.0f}")
    print(f"Quanto sobrou de lucro no último mês: {formatar_reais(dados.lucro[-1])}")
    print(f"De cada R$ 100 recebidos, quanto virou lucro no último mês: "
          f"R$ {dados.margem_lucro[-1]:.0f}")
    print(f"Em média, nos últimos {dados.n_meses} meses, de cada R$ 100 recebidos "
          f"viraram lucro: R$ {np.mean(dados.margem_lucro):.0f}")


def imprimir_estatisticas(estat_receita, estat_custo, correlacao):
    media_r, var_r, desvio_r = estat_receita
    media_c, var_c, desvio_c = estat_custo

    print("\n" + "=" * 72)
    print("2. COMO A RECEITA E O CUSTO COSTUMAM VARIAR DE UM MÊS PARA O OUTRO")
    print("=" * 72)
    print("(Isso é o que o programa usa como base para 'sortear' os futuros possíveis)")
    print(f"Receita -> em média, sobe/desce {media_r*100:+.0f}% por mês, "
          f"oscilando (para mais ou para menos) cerca de {desvio_r*100:.0f}% ao redor disso")
    print(f"Custo   -> em média, sobe/desce {media_c*100:+.0f}% por mês, "
          f"oscilando (para mais ou para menos) cerca de {desvio_c*100:.0f}% ao redor disso")
    print(f"\nRelação entre receita e custo (de -100% a +100%): {correlacao*100:+.0f}%")
    if correlacao > 0.3:
        print("  -> Isso é uma relação forte e positiva: quando a receita sobe, o custo "
              "tende a subir junto (faz sentido: vendendo mais, a loja compra mais "
              "mercadoria). O programa leva essa relação em conta ao sortear os futuros, "
              "em vez de sortear receita e custo cada um 'por conta própria'.")
    elif correlacao < -0.3:
        print("  -> Relação forte e negativa entre receita e custo (incomum).")
    else:
        print("  -> Relação fraca: receita e custo parecem variar de forma quase independente.")


def imprimir_resultado_cenario(nome_cenario: str, resultado_analise: dict,
                                  resumo: dict, descricao: str):
    nomes_amigaveis = {
        "otimista": "CENÁRIO OTIMISTA (se as coisas melhorarem)",
        "realista": "CENÁRIO REALISTA (se tudo continuar como no histórico)",
        "pessimista": "CENÁRIO PESSIMISTA (se as coisas piorarem)",
    }
    print(f"\n--- {nomes_amigaveis.get(nome_cenario, nome_cenario.upper())} ---")
    print(f"  {descricao}")
    p_aumento = resultado_analise["aumento"]["probabilidade"]
    ic_aumento = resultado_analise["aumento"]["intervalo_confianca"]
    p_queda = resultado_analise["queda"]["probabilidade"]
    ic_queda = resultado_analise["queda"]["intervalo_confianca"]
    p_estavel = resultado_analise["estavel"]["probabilidade"]

    print(f"  Chance de o lucro AUMENTAR : {p_aumento*100:3.0f}%  "
          f"(entre {ic_aumento[0]*100:.0f}% e {ic_aumento[1]*100:.0f}%, com 95% de confiança)")
    print(f"  Chance de o lucro CAIR     : {p_queda*100:3.0f}%  "
          f"(entre {ic_queda[0]*100:.0f}% e {ic_queda[1]*100:.0f}%, com 95% de confiança)")
    print(f"  Chance de o lucro ficar ESTÁVEL : {p_estavel*100:3.0f}%")
    print(f"  Lucro esperado (a média de todos os futuros simulados): {formatar_reais(resumo['valor_esperado'])}")
    print(f"  Resultado mais típico (mediana): {formatar_reais(resumo['mediana'])}  |  "
          f"Pior caso simulado: {formatar_reais(resumo['minimo'])}  |  "
          f"Melhor caso simulado: {formatar_reais(resumo['maximo'])}")


# =======================================================================
# PROGRAMA PRINCIPAL
# =======================================================================

def main():
    print("=" * 72)
    print(" SIMULADOR DE PROBABILIDADE DE LUCRO EMPRESARIAL ".center(72, "="))
    print(" Projeto Acadêmico - Matemática Computacional Aplicada (A3) ".center(72))
    print(" Tema: Probabilidade e Simulação / Simulação de Monte Carlo ".center(72))
    print("=" * 72)

    imprimir_explicacao_simples()

    # --- 1. Carregamento e validação dos dados ---------------------------------
    dados = escolher_fonte_de_dados()
    try:
        validar_dados(dados)
    except ValueError as erro:
        print(f"\nERRO nos dados fornecidos: {erro}")
        print("Encerrando o programa.")
        sys.exit(1)

    imprimir_cabecalho_dados(dados)

    # --- 2. Estatística das variáveis aleatórias (variações percentuais) -------
    variacao_receita = calcular_variacoes_percentuais(dados.receita)
    variacao_custo = calcular_variacoes_percentuais(dados.custos)

    estat_receita = media_variancia_desvio(variacao_receita)
    estat_custo = media_variancia_desvio(variacao_custo)
    info_conjunta = matriz_covariancia_correlacao(variacao_receita, variacao_custo)

    imprimir_estatisticas(estat_receita, estat_custo, info_conjunta["correlacao"])

    # --- 3. Parâmetros da simulação: 4 perguntas básicas para o usuário ---
    print("\n" + "=" * 72)
    print("3. VAMOS CONFIGURAR A SUA PREVISÃO (Responda 4 perguntas simples)")
    print("=" * 72)

    receita_base = float(dados.receita[-1])
    custo_base = float(dados.custos[-1])

    print(f"\n[1/4] Qual é o faturamento mensal médio atual da sua empresa?")
    receita_atual = ler_numero(
        f"      (Pressione Enter para usar o valor atual de R$ {receita_base:,.2f}): ",
        padrao=receita_base, tipo=float, minimo=0.01
    )

    print(f"\n[2/4] Qual é o custo mensal médio atual para manter o negócio funcionando?")
    custo_atual = ler_numero(
        f"      (Pressione Enter para usar o valor atual de R$ {custo_base:,.2f}): ",
        padrao=custo_base, tipo=float, minimo=0.0
    )

    print(f"\n[3/4] Quantos meses no futuro você deseja projetar?")
    n_meses = ler_numero(
        "      (Quantos meses à frente? [Padrão: 12]): ",
        padrao=12, tipo=int, minimo=1
    )

    print(f"\n[4/4] Como você avalia o ritmo ou o risco do seu mercado atualmente?")
    print("      [1] Negócio estável (pouca variação de vendas e custos)")
    print("      [2] Ritmo normal de mercado (variação moderada — recomendado)")
    print("      [3] Alta volatilidade (mercado muito instável e imprevisível)")
    escolha_risco = input("      Escolha 1, 2 ou 3 [2]: ").strip()

    if escolha_risco == "1":
        fator_ajuste_cenario = "otimista"
    elif escolha_risco == "3":
        fator_ajuste_cenario = "pessimista"
    else:
        fator_ajuste_cenario = "realista"

    n_simulacoes = 10000
    semente = 42
    tolerancia = 0.02
    inflacao_mensal = 0.004

    volume_atual = float(dados.volume_vendas[-1])
    lucro_atual = receita_atual - custo_atual
    meta_lucro = lucro_atual * 1.5

    # --- 4. Execução da simulação para os três cenários de negócio -------------
    print("\n" + "=" * 72)
    print("4. RESULTADOS: 3 CENÁRIOS DIFERENTES (otimista, realista e pessimista)")
    print("=" * 72)
    print(f"(o programa sorteou {n_simulacoes} futuros possíveis, olhando {n_meses} "
          f"mês(es) à frente)")

    resultados_por_cenario = {}

    for nome_cenario in ("otimista", "realista", "pessimista"):
        parametros = montar_parametros_cenario(
            nome_cenario, info_conjunta["vetor_medias"], info_conjunta["matriz_covariancia"],
            inflacao_mensal,
        )

        simulacao = simular_monte_carlo(
            receita_atual=receita_atual,
            custo_atual=custo_atual,
            vetor_medias=parametros["vetor_medias"],
            matriz_covariancia=parametros["matriz_covariancia"],
            inflacao_mensal=parametros["inflacao_mensal"],
            n_meses=n_meses,
            n_simulacoes=n_simulacoes,
            semente=semente,
        )

        lucro_final = simulacao["lucros"][:, -1]
        analise_resultado = calcular_probabilidades_resultado(lucro_final, lucro_atual, tolerancia)
        resumo = resumo_estatistico(lucro_final)

        imprimir_resultado_cenario(nome_cenario, analise_resultado, resumo, parametros["descricao"])

        resultados_por_cenario[nome_cenario] = {
            "simulacao": simulacao,
            "lucro_final": lucro_final,
            "analise_resultado": analise_resultado,
            "resumo": resumo,
        }

    # --- 5. Análise estatística adicional (sobre o cenário REALISTA) -----------
    realista = resultados_por_cenario["realista"]
    lucro_final_realista = realista["lucro_final"]

    print("\n" + "=" * 72)
    print("5. PERGUNTAS ESPECÍFICAS (usando o cenário realista)")
    print("=" * 72)

    p_meta = probabilidade_meta(lucro_final_realista, meta_lucro)
    p_prejuizo = probabilidade_prejuizo(lucro_final_realista)
    p_queda_10 = probabilidade_queda_maior_que(lucro_final_realista, lucro_atual, 0.10)
    p_aumento_20 = probabilidade_aumento_maior_que(lucro_final_realista, lucro_atual, 0.20)

    print(f"Chance de bater a meta de {formatar_reais(meta_lucro)} de lucro: {p_meta*100:.0f}%")
    print(f"Chance de a loja dar PREJUÍZO (lucro abaixo de R$ 0): {p_prejuizo*100:.0f}%")
    print(f"Chance de o lucro cair MAIS DE 10% em relação a hoje: {p_queda_10*100:.0f}%")
    print(f"Chance de o lucro subir MAIS DE 20% em relação a hoje: {p_aumento_20*100:.0f}%")

    percentis = realista["resumo"]["percentis"]
    print("\nFaixa de resultados simulados, do pior para o melhor (cenário realista):")
    print(f"  Entre os 10% piores casos, o lucro ficou abaixo de: {formatar_reais(percentis['p10'])}")
    print(f"  Entre os 25% piores casos, o lucro ficou abaixo de: {formatar_reais(percentis['p25'])}")
    print(f"  Bem no meio de todos os casos (mediana): {formatar_reais(percentis['p50'])}")
    print(f"  Entre os 25% melhores casos, o lucro ficou acima de: {formatar_reais(percentis['p75'])}")
    print(f"  Entre os 10% melhores casos, o lucro ficou acima de: {formatar_reais(percentis['p90'])}")
    print(f"\nO quanto os resultados costumam variar para mais ou para menos: "
          f"{formatar_reais(realista['resumo']['desvio_padrao'])}")

    # --- 6. Geração dos gráficos -------------------------------------------------
    print("\n" + "=" * 72)
    print("6. GERANDO OS GRÁFICOS (imagens que resumem tudo visualmente)")
    print("=" * 72)

    grafico_distribuicao_lucro(
        lucro_final_realista, lucro_atual, realista["resumo"]["valor_esperado"],
        realista["analise_resultado"]["aumento"]["probabilidade"],
        realista["analise_resultado"]["queda"]["probabilidade"],
    )
    grafico_evolucao_lucro(realista["simulacao"]["lucros"], lucro_atual)
    grafico_analise_sensibilidade(receita_atual, custo_atual, volume_atual)

    print("Gráfico 1 (todos os futuros possíveis, lado a lado): grafico_1_distribuicao_lucro.png")
    print("Gráfico 2 (como o lucro evolui mês a mês): grafico_2_evolucao_lucro.png")
    print("Gráfico 3 (o que mais pesa no resultado): grafico_3_sensibilidade.png")

    print("\n" + "=" * 72)
    print("PRONTO! Abra os três arquivos .png para ver os resultados em forma de gráfico.")
    print("=" * 72)


if __name__ == "__main__":
    main()
