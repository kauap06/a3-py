# Simulador de Probabilidade de Lucro Empresarial

Projeto acadêmico de **Matemática Computacional Aplicada** — Atividade
Prática A3. Tema: **Probabilidade e Simulação** (Simulação de Monte
Carlo).

---

## Sumário

0. [Explicação Simples (comece por aqui)](#0-explicação-simples-comece-por-aqui)
1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Tecnologias Utilizadas](#2-tecnologias-utilizadas)
3. [Conceitos Matemáticos](#3-conceitos-matemáticos)
4. [Indicadores Financeiros](#4-indicadores-financeiros)
5. [Estrutura do Projeto](#5-estrutura-do-projeto)
6. [Guia de Instalação](#6-guia-de-instalação)
7. [Explicação do Código (Code Walkthrough)](#7-explicação-do-código-code-walkthrough)
8. [A Simulação de Monte Carlo, Explicada em Detalhe](#8-a-simulação-de-monte-carlo-explicada-em-detalhe)
9. [Interpretação dos Gráficos](#9-interpretação-dos-gráficos)
10. [Exemplo de Execução (fictício)](#10-exemplo-de-execução-fictício)
11. [Limitações do Modelo](#11-limitações-do-modelo)
12. [Melhorias Futuras](#12-melhorias-futuras)

---

## 0. Explicação Simples (comece por aqui)

> Esta seção não usa nenhum termo técnico. Se você nunca trabalhou com
> finanças ou com uma empresa, comece por aqui antes de ir para o resto
> do documento.

**A ideia, em uma frase:** este programa é como uma previsão do tempo,
mas em vez de prever chuva, ele "prevê" (em forma de chance, de
porcentagem) se o lucro de uma loja vai subir ou cair.

**Por que usar "chance" em vez de dizer um número certo?** Porque
ninguém sabe o futuro com certeza — nem o programa. Em vez de fingir que
sabe exatamente quanto a loja vai lucrar daqui a um ano, o programa é
honesto: ele mostra um *leque* de futuros possíveis e diz o quão comum
(ou raro) é cada um deles.

**Como ele faz isso, com um exemplo bem simples:**

1. Imagine uma pequena loja. Nos últimos 12 meses, ela anotou quanto
   **recebeu** vendendo (chamamos isso de **receita**) e quanto
   **gastou** para funcionar (chamamos isso de **custo**). O que sobra
   depois de pagar os gastos é o **lucro**: `Lucro = Receita − Custo`.
2. Olhando para esses 12 meses, o programa percebe, por exemplo, que a
   receita da loja costuma subir cerca de 1% por mês, mas às vezes sobe
   mais, às vezes cai um pouco — e o mesmo vale para o custo.
3. Em vez de sortear só UM futuro, o programa pede para o computador
   "jogar os dados" 10.000 vezes: a cada jogada, ele sorteia uma
   variação plausível de receita e de custo para cada mês seguinte,
   igual ao que já aconteceu no histórico, e calcula onde o lucro
   terminaria **naquela jogada**.
4. No final das 10.000 jogadas, o programa simplesmente CONTA: em
   quantas delas o lucro ficou maior do que está hoje? Em quantas ficou
   menor? Essa contagem, transformada em porcentagem, é a resposta que
   você vê na tela: "66% de chance de cair", por exemplo.

**O que você vai ver ao rodar o programa:**

- Um resumo dos dados da loja (fictícios, de exemplo).
- Três "humores" diferentes para o futuro: um cenário **otimista**
  (coisas melhoram), um **realista** (tudo continua como no histórico)
  e um **pessimista** (coisas pioram) — cada um com sua própria chance
  de aumento/queda de lucro.
- Respostas a perguntas concretas, tipo "qual a chance de dar
  prejuízo?" ou "qual a chance de bater uma meta de lucro?".
- Três gráficos que mostram tudo isso visualmente (explicados na seção
  9 deste documento).

Depois dessa explicação simples, o restante do documento detalha a
matemática por trás (para quem for escrever a fundamentação teórica do
relatório) e o código, função por função.

---

## 1. Visão Geral do Projeto

**Nome do projeto:** Simulador de Probabilidade de Lucro Empresarial

**Objetivo principal:** construir um simulador capaz de **estimar a
probabilidade de uma empresa aumentar ou diminuir o seu lucro** em meses
futuros, a partir do histórico financeiro mensal (receita, custos
operacionais e volume de vendas), usando **Simulação de Monte Carlo**.

**Contexto acadêmico:** este projeto foi desenvolvido como Atividade
Prática A3 da Unidade Curricular de Matemática Computacional Aplicada,
dentro da área de aprendizagem "Probabilidade e Simulação" (espaço
amostral, probabilidade condicional, variáveis aleatórias, valor
esperado e variância), combinando fundamentação teórica com
implementação computacional em Python.

**Problema que a aplicação resolve:** projetar o lucro futuro de uma
empresa não é só "repetir a taxa de crescimento do ano passado". Receita
e custos oscilam, estão relacionados entre si (quando a receita sobe,
parte dos custos sobe junto) e sofrem o efeito de fatores externos como
a inflação. Em vez de entregar **um único número** de previsão (o que
passa uma falsa sensação de certeza), o programa gera **milhares de
cenários futuros possíveis** e responde, com base neles, perguntas
concretas de gestão:

- Qual a probabilidade de o lucro aumentar/diminuir/ficar estável?
- Qual a chance de bater uma meta específica de lucro?
- Qual a chance de a empresa dar prejuízo?
- Qual a chance de uma queda maior que 10%? E de um aumento maior que 20%?
- Quais variáveis (receita, custo, volume de vendas) mais afetam o
  resultado final, caso algo mude?

---

## 2. Tecnologias Utilizadas

| Tecnologia | Para que é usada neste projeto |
| --- | --- |
| **Python 3** | Linguagem principal do projeto. |
| **NumPy** | Cálculo numérico e estatístico: médias, variância, desvio padrão, matriz de covariância/correlação, geração de números aleatórios (`default_rng`) e amostragem de distribuições (Normal multivariada), cálculo vetorizado das simulações (muito mais rápido do que laços `for` puros em Python). |
| **Matplotlib** | Geração dos três gráficos do projeto (histograma de distribuição, faixas de evolução por percentil e análise de sensibilidade), com formatação em Reais (R$) nos eixos. |
| **Pandas** | Leitura e validação de arquivos `.csv` com dados financeiros reais da empresa, permitindo substituir o conjunto de dados fictício de demonstração por dados verdadeiros. |

---

## 3. Conceitos Matemáticos

### 3.1 Probabilidade

Probabilidade é uma medida numérica, entre 0 e 1 (ou 0% e 100%), de
quão provável é que um determinado evento ocorra. Neste projeto, a
probabilidade não é calculada por uma fórmula fechada, e sim **estimada
por frequência relativa** a partir da simulação:

$$
P(\text{evento}) \approx \frac{\text{número de simulações em que o evento ocorreu}}{\text{número total de simulações}}
$$

Quanto maior o número de simulações, mais essa estimativa se aproxima
da probabilidade teórica do modelo — isso é uma consequência da **Lei
dos Grandes Números**.

### 3.2 Espaço amostral

O **espaço amostral** é o conjunto de todos os resultados possíveis de
um experimento aleatório. Neste projeto, o experimento aleatório é "qual
vai ser o lucro da empresa daqui a N meses?", e o espaço amostral é
formado por **todas as trajetórias de lucro possíveis** que a simulação
de Monte Carlo pode gerar — na prática, aproximamos esse espaço amostral
(que seria infinito) simulando um número finito, mas grande, de cenários
(ex.: 10.000).

### 3.3 Variáveis aleatórias

Uma **variável aleatória** é uma função que associa um número a cada
resultado possível de um experimento aleatório. Neste projeto, as
principais variáveis aleatórias são:

$$
X_R = \frac{R_t - R_{t-1}}{R_{t-1}} \qquad \qquad X_C = \frac{C_t - C_{t-1}}{C_{t-1}}
$$

em que $R_t$ é a receita no mês $t$ e $C_t$ é o custo operacional no mês
$t$. Ou seja, $X_R$ e $X_C$ são, respectivamente, a **variação
percentual mensal da receita** e **dos custos** — são essas variáveis
que o programa estima a partir do histórico e depois sorteia
repetidamente na simulação.

### 3.4 Média aritmética e valor esperado

A **média aritmética** de uma amostra de $n$ observações é:

$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

Quando usamos a média de uma amostra histórica para **estimar** o
**valor esperado** $E[X]$ de uma variável aleatória (ou seja, o "valor
médio que ela deve assumir no longo prazo"), estamos usando a média
amostral como estimador do valor esperado populacional: $E[X] \approx
\bar{x}$.

No código, isso é a média das variações percentuais mensais de receita
e de custo, calculada em `estatistica.media_variancia_desvio()`.

### 3.5 Variância e desvio padrão

A **variância** mede o quanto os valores de uma variável aleatória
costumam se afastar da média (dispersão):

$$
s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})^2
$$

O **desvio padrão** é a raiz quadrada da variância, $s = \sqrt{s^2}$, e
tem a vantagem de estar na mesma unidade da variável original (por
exemplo, variação percentual), o que facilita a interpretação.

> Usamos o divisor $n-1$ (e não $n$) porque estamos estimando a
> variância de uma população a partir de uma amostra finita — essa é a
> correção de Bessel, padrão em estatística inferencial.

### 3.6 Covariância e correlação (relação entre receita e custo)

A **covariância** entre duas variáveis aleatórias $X$ e $Y$ mede como
elas variam juntas:

$$
\text{Cov}(X, Y) = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})
$$

A **correlação de Pearson** normaliza a covariância para um valor entre
-1 e 1:

$$
\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{s_X \cdot s_Y}
$$

Neste projeto, $\rho$ mede o quanto a variação de custo tende a
acompanhar a variação de receita (ex.: custos variáveis). Esse valor é
usado para montar a **matriz de covariância conjunta**, garantindo que a
simulação não trate receita e custo como se fossem independentes — ver
a seção 8 para o detalhe de como isso é usado na prática.

### 3.7 Distribuição Normal

A **distribuição Normal** (ou gaussiana) é uma distribuição de
probabilidade contínua, em formato de "sino", descrita por dois
parâmetros: a média $\mu$ e o desvio padrão $\sigma$. Sua função de
densidade é:

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}} \, e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}
$$

Este projeto assume, como **hipótese inicial de modelagem**
(documentada e simplificadora), que as variações percentuais mensais de
receita e custo seguem aproximadamente uma distribuição Normal
**multivariada** (a versão da Normal para duas ou mais variáveis
correlacionadas ao mesmo tempo), estimada a partir da média, do desvio
padrão e da correlação históricos.

### 3.8 Simulação de Monte Carlo

**Simulação de Monte Carlo** é uma técnica que usa amostragem aleatória
repetida para estimar resultados numéricos (incluindo probabilidades)
de processos que seriam difíceis, complexos ou impossíveis de resolver
analiticamente. A ideia central: em vez de calcular a probabilidade de
um evento por uma fórmula fechada, **simula-se o processo milhares de
vezes** e **conta-se a frequência** com que o evento de interesse
ocorreu. A seção 8 explica, passo a passo e com um exemplo numérico,
como isso é feito neste projeto.

---

## 4. Indicadores Financeiros

| Indicador | O que representa | Como influencia a lucratividade |
| --- | --- | --- |
| **Receita mensal** | Total das vendas (R$) da empresa no mês. | É a principal fonte de lucro: quanto maior a receita, mantendo os custos sob controle, maior o lucro. |
| **Custos operacionais** | Tudo que a empresa gasta para funcionar no mês (insumos, salários, aluguel, logística, impostos, etc.). | Reduz diretamente o lucro. Parte dos custos é variável (acompanha a receita), outra parte é fixa. |
| **Volume de vendas** | Quantidade de produtos/serviços vendidos no mês (unidades). | Junto com o preço médio, determina a receita (Receita ≈ Preço médio × Volume). Aumentar o volume sem reduzir o preço médio tende a aumentar a receita e, consequentemente, o lucro. |
| **Inflação** | Taxa de aumento geral de preços, aplicada aqui como pressão adicional sobre os custos operacionais. | Infla os custos ao longo do tempo mesmo que a operação da empresa não mude, reduzindo a margem se a receita não acompanhar o mesmo ritmo. |
| **Margem de lucro** | Percentual da receita que efetivamente "sobra" como lucro: $\text{Margem} = \frac{\text{Lucro}}{\text{Receita}} \times 100$. | Mostra a eficiência da operação: duas empresas com o mesmo lucro em R$ podem ter margens muito diferentes se tiverem receitas diferentes. |

A equação financeira fundamental usada em todo o projeto é:

$$
\text{Lucro} = \text{Receita} - \text{Custos}
$$

---

## 5. Estrutura do Projeto

```
simulador_lucro/
├── main.py               # Programa principal: conduz o fluxo completo da simulação
├── dados.py               # Carregamento e validação dos dados financeiros (exemplo ou .csv)
├── estatistica.py          # Estatística descritiva: média, variância, covariância, percentis, IC
├── simulacao.py            # Motor da Simulação de Monte Carlo (núcleo matemático do projeto)
├── analise.py              # Probabilidades de negócio calculadas a partir da simulação
├── cenarios.py              # Definição dos cenários otimista / realista / pessimista
├── graficos.py              # Geração dos 3 gráficos (Matplotlib)
├── dados_exemplo.csv        # Conjunto de dados FICTÍCIO de demonstração (12 meses, números redondos)
├── requirements.txt         # Dependências do projeto
└── README.md                # Esta documentação
```

Ao rodar `main.py`, os seguintes arquivos de imagem são gerados na
mesma pasta:

```
grafico_1_distribuicao_lucro.png
grafico_2_evolucao_lucro.png
grafico_3_sensibilidade.png
```

---

## 6. Guia de Instalação

### Passo 1 — Instalar o Python

Baixe e instale o Python 3 (versão 3.10 ou superior recomendada) em
<https://www.python.org/downloads/>. Durante a instalação no Windows,
marque a opção **"Add Python to PATH"**.

Para verificar se já está instalado, abra o terminal (Prompt de
Comando/PowerShell no Windows, Terminal no macOS/Linux) e digite:

```bash
python --version
```

### Passo 2 — Baixar/extrair os arquivos do projeto

Coloque todos os arquivos deste projeto (`main.py`, `dados.py`, etc.)
dentro de uma mesma pasta, por exemplo `simulador_lucro/`.

### Passo 3 — Abrir o terminal na pasta do projeto

```bash
cd caminho/para/simulador_lucro
```

### Passo 4 — Criar um ambiente virtual (recomendado)

Um ambiente virtual isola as dependências deste projeto do restante do
sistema.

```bash
python -m venv venv
```

Ativar o ambiente virtual:

- **Windows (PowerShell):**
  ```bash
  venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### Passo 5 — Instalar as dependências

```bash
pip install -r requirements.txt
```

### Passo 6 — Executar o programa

```bash
python main.py
```

O programa vai pedir, de forma interativa, algumas informações (fonte
dos dados, número de meses a simular, número de simulações etc.) — basta
apertar Enter em qualquer pergunta para usar o valor padrão sugerido
entre colchetes.

---

## 7. Explicação do Código (Code Walkthrough)

Esta seção segue a ordem real de execução do programa, explicando o que
cada função faz, quais parâmetros recebe, quais cálculos matemáticos
realiza, quais resultados retorna e como as funções se conectam.

### 7.1 `dados.py` — carregamento e validação

- **`carregar_dados_exemplo()`** → não recebe parâmetros. Retorna um
  objeto `DadosFinanceiros` com 12 meses de receita, custo e volume de
  vendas **fictícios**, criados apenas para demonstração (correlação
  realista entre receita e custo, mas sem corresponder a nenhuma empresa
  real).
- **`carregar_dados_csv(caminho_arquivo)`** → recebe o caminho de um
  arquivo `.csv`. Usa `pandas.read_csv` para ler o arquivo, confere se
  as colunas obrigatórias (`mes`, `receita`, `custos`, `volume_vendas`)
  existem e não têm valores vazios, e retorna um `DadosFinanceiros` com
  os dados reais. Levanta `ValueError` com mensagens claras em caso de
  arquivo não encontrado, colunas faltando ou valores ausentes.
- **`validar_dados(dados)`** → recebe um `DadosFinanceiros` e verifica,
  na ordem: (1) número mínimo de meses de histórico (`MESES_MINIMOS_EXIGIDOS
  = 4`); (2) mesmo número de observações em receita/custo/volume; (3)
  receita estritamente positiva em todos os meses (evita divisão por
  zero ao calcular variações percentuais e margem); (4) custo e volume
  não-negativos; (5) ausência de `NaN`/infinitos. Levanta `ValueError`
  descrevendo exatamente qual validação falhou.
- A classe `DadosFinanceiros` também expõe duas propriedades calculadas:
  `lucro` (receita − custo) e `margem_lucro` (lucro / receita × 100).

### 7.2 `estatistica.py` — dos dados brutos aos parâmetros do modelo

- **`calcular_variacoes_percentuais(serie)`** → recebe um vetor (ex.:
  receita mensal) e retorna o vetor de variações percentuais mês a mês:
  $\frac{serie_i - serie_{i-1}}{serie_{i-1}}$. É a transformação que
  converte o histórico bruto na variável aleatória do modelo.
- **`media_variancia_desvio(amostra)`** → recebe um vetor de variações
  percentuais e retorna a tupla `(média, variância, desvio_padrão)`,
  calculados com `ddof=1` (ver seção 3.5).
- **`matriz_covariancia_correlacao(variacao_receita, variacao_custo)`**
  → recebe os dois vetores de variação (receita e custo) e retorna um
  dicionário com o `vetor_medias` (média de cada variável), a
  `matriz_covariancia` (2×2) e a `correlacao` (coeficiente de Pearson).
  Essa matriz de covariância é o ingrediente que permite sortear receita
  e custo de forma **correlacionada** na simulação (seção 8.3).
- **`calcular_percentis(amostra, percentis)`** → calcula os percentis
  pedidos (padrão: 10, 25, 50, 75, 90) de um vetor de resultados, usando
  `numpy.percentile`.
- **`intervalo_confianca_proporcao(p_estimado, n_amostras, confianca)`**
  → recebe uma probabilidade estimada (ex.: 0.87) e o número de
  simulações usadas para estimá-la, e retorna o intervalo de confiança
  (usando o método de Wilson — ver comentário no código) em torno dessa
  estimativa. Isso comunica a **incerteza da própria estimativa de
  probabilidade** (quanto maior o número de simulações, mais estreito
  o intervalo).

### 7.3 `simulacao.py` — o motor de Monte Carlo

- **`gerar_variacoes_correlacionadas(vetor_medias, matriz_covariancia,
  n_simulacoes, n_meses, gerador)`** → usa
  `gerador.multivariate_normal(mean=vetor_medias, cov=matriz_covariancia,
  size=n_simulacoes*n_meses)` para sortear, de uma só vez (vetorizado,
  sem laços Python lentos), todas as variações percentuais conjuntas de
  receita e custo necessárias, e reorganiza o resultado em um array de
  formato `(n_simulacoes, n_meses, 2)`.
- **`simular_monte_carlo(receita_atual, custo_atual, vetor_medias,
  matriz_covariancia, inflacao_mensal, n_meses, n_simulacoes, semente)`**
  → a função central do projeto. Cria um gerador de números aleatórios
  reprodutível (`np.random.default_rng(semente)`), chama a função
  acima para obter as variações sorteadas, soma a inflação mensal à
  variação de custo, e então, mês a mês, multiplica a receita/custo
  acumulados por `(1 + variação)`, truncando em zero (não permite
  receita/custo negativos). Retorna um dicionário com três matrizes
  `(n_simulacoes, n_meses)`: `receitas`, `custos` e `lucros` (= receitas
  − custos).
- **`classificar_resultado(lucro_final, lucro_atual, tolerancia)`** →
  recebe o lucro final de cada simulação e classifica cada uma como
  `aumento`, `queda` ou `estavel`, usando uma faixa de tolerância (ex.:
  ±2%) ao redor do lucro atual para definir "estabilidade".

### 7.4 `analise.py` — probabilidades de negócio

- **`calcular_probabilidades_resultado(lucro_final, lucro_atual,
  tolerancia, confianca)`** → usa `classificar_resultado` e, para cada
  categoria (aumento/queda/estável), calcula a proporção de simulações
  naquela categoria (a probabilidade, por frequência relativa) e o
  intervalo de confiança dessa proporção.
- **`probabilidade_meta(lucro_final, meta)`** → $P(\text{lucro} \geq
  \text{meta})$, a fração de simulações que atingiram ou superaram uma
  meta de lucro informada pelo usuário.
- **`probabilidade_prejuizo(lucro_final)`** → $P(\text{lucro} < 0)$.
- **`probabilidade_queda_maior_que(lucro_final, lucro_atual,
  percentual)`** e **`probabilidade_aumento_maior_que(...)`** →
  probabilidade de uma queda ou aumento **maior que** um percentual
  específico (padrões do projeto: queda > 10%, aumento > 20%).
- **`resumo_estatistico(lucro_final)`** → agrega valor esperado
  (média), mínimo, máximo, mediana, desvio padrão e os percentis
  10/25/50/75/90 do lucro final simulado.

### 7.5 `cenarios.py` — otimista, realista e pessimista

- O dicionário **`AJUSTES_CENARIOS`** documenta, de forma explícita, os
  ajustes manuais aplicados em cada cenário (ex.: no cenário otimista,
  soma-se +2 pontos percentuais à média histórica da variação de
  receita e reduz-se o desvio padrão em 15%).
- **`montar_parametros_cenario(nome_cenario, vetor_medias,
  matriz_covariancia, inflacao_mensal_base)`** → aplica esses ajustes
  sobre os parâmetros estatísticos reais estimados do histórico,
  retornando um novo `vetor_medias`, uma nova `matriz_covariancia`
  (reescalada para ajustar o desvio padrão mantendo a correlação) e uma
  nova `inflacao_mensal`, prontos para alimentar
  `simulacao.simular_monte_carlo()`.

### 7.6 `graficos.py` — visualização

- **`grafico_distribuicao_lucro(...)`** → Gráfico 1 (histograma, seção 9.1).
- **`grafico_evolucao_lucro(...)`** → Gráfico 2 (faixas de percentil, seção 9.2).
- **`grafico_analise_sensibilidade(...)`** → Gráfico 3 (tornado, seção 9.3).

### 7.7 `main.py` — orquestração

`main()` executa, em ordem: (1) escolha e validação da fonte de dados;
(2) cálculo das estatísticas das variáveis aleatórias; (3) leitura dos
parâmetros de simulação informados pelo usuário (com validação via
`ler_numero`); (4) execução da Simulação de Monte Carlo para os três
cenários de negócio, imprimindo os resultados de cada um; (5) cálculo
das análises estatísticas adicionais sobre o cenário realista; (6)
geração dos três gráficos.

---

## 8. A Simulação de Monte Carlo, Explicada em Detalhe

### 8.1 Por que simular em vez de calcular diretamente?

Calcular analiticamente a distribuição exata do lucro depois de, por
exemplo, 12 meses de variações aleatórias **correlacionadas** entre
receita e custo é matematicamente complexo (envolveria o produto de
variáveis aleatórias correlacionadas ao longo de várias etapas). A
Simulação de Monte Carlo contorna esse problema: em vez de resolver a
matemática de forma fechada, **repetimos o processo aleatório milhares
de vezes no computador** e observamos empiricamente a distribuição de
resultados.

### 8.2 O algoritmo, passo a passo

1. **Estimar os parâmetros do modelo** a partir do histórico: média e
   desvio padrão da variação percentual mensal de receita e de custo, e
   a correlação entre elas (seção 3.4 a 3.6).
2. **Para cada uma das $N$ simulações** (ex.: $N = 10.000$):
   a. Começar do lucro atual (receita e custo do último mês observado).
   b. **Para cada um dos $M$ meses futuros** a simular:
      - Sortear, de uma distribuição Normal multivariada com a média e
        a matriz de covariância estimadas, um par de variações
        percentuais $(\delta_R, \delta_C)$ para aquele mês.
      - Somar a inflação mensal a $\delta_C$.
      - Atualizar: $R_{novo} = R_{atual} \times (1 + \delta_R)$ e
        $C_{novo} = C_{atual} \times (1 + \delta_C)$ (truncados em zero).
   c. Ao final dos $M$ meses, calcular o lucro final daquela simulação:
      $L = R_{final} - C_{final}$.
3. Ao final das $N$ simulações, temos $N$ valores possíveis de lucro
   final — essa coleção de valores **é** a distribuição de probabilidade
   estimada do lucro futuro.
4. **Estimar probabilidades por frequência relativa**: por exemplo,
   $P(\text{aumento}) = \dfrac{\text{quantidade de simulações com lucro final} > \text{lucro atual}}{N}$.

### 8.3 Por que a correlação entre receita e custo importa

Se sorteássemos $\delta_R$ e $\delta_C$ **de forma independente**
(cada um de sua própria distribuição Normal, sem relação entre eles),
estaríamos ignorando que, historicamente, quando a receita sobe, os
custos (em parte variáveis) tendem a subir junto. Isso faria a simulação
**superestimar o risco de lucro muito alto ou muito baixo** de forma
artificial (porque permitiria, por exemplo, receita subir muito e custo
cair muito ao mesmo tempo — um cenário estatisticamente raro no
histórico real). Por isso, o projeto sorteia $(\delta_R, \delta_C)$
**conjuntamente**, de uma Normal multivariada parametrizada pela matriz
de covariância histórica — isso preserva a relação real entre as duas
variáveis em cada cenário simulado.

### 8.4 Exemplo numérico simplificado (com 3 simulações e 1 mês)

Suponha, para simplificar a ilustração, que a receita atual seja **R$
10.000** e o custo atual **R$ 6.000** (lucro atual = R$ 4.000), e que o
modelo tenha estimado:

- Variação média de receita: $\mu_R = +2\%$, desvio padrão $\sigma_R = 3\%$
- Variação média de custo: $\mu_C = +1\%$, desvio padrão $\sigma_C = 4\%$
- Correlação entre as duas: $\rho = +0{,}7$ (positiva, como esperado)

Ao sortear da Normal multivariada para **3 simulações fictícias** de
**1 mês**, poderíamos obter, por exemplo:

| Simulação | $\delta_R$ sorteado | $\delta_C$ sorteado | Receita final | Custo final | Lucro final | Resultado |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | +4,0% | +3,0% | R$ 10.400 | R$ 6.180 | R$ 4.220 | Aumento |
| 2 | -1,5% | +0,5% | R$ 9.850 | R$ 6.030 | R$ 3.820 | Queda |
| 3 | +6,0% | +4,5% | R$ 10.600 | R$ 6.270 | R$ 4.330 | Aumento |

Com apenas 3 simulações, a estimativa seria $P(\text{aumento}) = 2/3
\approx 66{,}7\%$ — mas, com só 3 amostras, essa estimativa é muito
instável (o intervalo de confiança seria enorme). É por isso que, na
prática, o programa usa milhares de simulações (10.000 por padrão): a
estimativa de probabilidade se torna muito mais estável e confiável
(intervalos de confiança mais estreitos — ver seção 3.1 e a função
`intervalo_confianca_proporcao`).

---

## 9. Interpretação dos Gráficos

### 9.1 Gráfico 1 — Distribuição do lucro futuro (`grafico_1_distribuicao_lucro.png`)

Um histograma com **todos** os lucros finais simulados. Cada barra
representa "quantas simulações terminaram com um lucro próximo daquele
valor". As barras são coloridas de **vermelho** (cenários abaixo do
lucro atual — queda) e **verde** (cenários acima — aumento). A linha
tracejada preta marca o lucro atual; a linha roxa contínua marca o lucro
esperado (a média de todos os cenários). Quanto mais estreita e alta a
"corcova" do histograma, menor a incerteza do modelo; quanto mais larga
e espalhada, maior o risco (boa ou má sorte são mais prováveis).

### 9.2 Gráfico 2 — Evolução do lucro mês a mês (`grafico_2_evolucao_lucro.png`)

Mostra como o lucro tende a evoluir ao longo dos meses futuros, usando
**faixas de percentil** em vez de milhares de linhas sobrepostas. A
faixa mais escura cobre os percentis 25 a 75 (50% dos cenários simulados
— "o range mais provável"); a faixa mais clara cobre os percentis 10 a
90 (80% dos cenários — inclui situações mais extremas, mas ainda assim
plausíveis). A linha central é a mediana (percentil 50). Quanto mais a
faixa se abre conforme os meses avançam, maior a incerteza acumulada ao
longo do tempo — um comportamento esperado em qualquer simulação desse
tipo.

### 9.3 Gráfico 3 — Análise de sensibilidade (`grafico_3_sensibilidade.png`)

Um gráfico "tornado": para cada indicador (receita, custos, volume de
vendas), mostra o quanto o lucro mudaria se aquele indicador variasse
+10% (barra verde) ou -10% (barra vermelha), **mantendo os outros dois
indicadores constantes**. Quanto mais larga a barra de um indicador,
maior a sua influência sobre o lucro final — é uma forma rápida de
identificar onde a gestão deveria focar esforços (ex.: negociar custos
com fornecedores vs. aumentar o volume de vendas).

---

## 10. Exemplo de Execução (fictício)

> Os valores abaixo são **ilustrativos**, gerados com o conjunto de
> dados fictício de demonstração (`dados_exemplo.csv` / `carregar_dados_exemplo()`)
> incluído no projeto, apenas para mostrar o formato da saída do
> programa. Não representam nenhuma empresa real.

```
Fonte dos dados financeiros:
  [1] Usar dados fictícios de demonstração (padrão)
  [2] Carregar um arquivo .csv com dados reais da empresa
Escolha uma opção (1 ou 2) [1]: 1

========================================================================
1. OS DADOS DE PARTIDA (o histórico da loja)
========================================================================
Origem dos dados: fictícios (dados de demonstração, com números redondos só
para facilitar o entendimento — NÃO representam uma empresa real)
Quantos meses de histórico temos: 12
Quanto a loja recebeu no último mês (receita): R$ 11.400
Quanto a loja gastou no último mês (custo): R$ 7.300
Quantos produtos foram vendidos no último mês: 570
Quanto sobrou de lucro no último mês: R$ 4.100
De cada R$ 100 recebidos, quanto virou lucro no último mês: R$ 36
Em média, nos últimos 12 meses, de cada R$ 100 recebidos viraram lucro: R$ 38

========================================================================
2. COMO A RECEITA E O CUSTO COSTUMAM VARIAR DE UM MÊS PARA O OUTRO
========================================================================
Receita -> em média, sobe/desce +1% por mês, oscilando cerca de 4% ao redor disso
Custo   -> em média, sobe/desce +2% por mês, oscilando cerca de 3% ao redor disso

Relação entre receita e custo (de -100% a +100%): +98%
  -> Relação forte e positiva: quando a receita sobe, o custo tende a subir
     junto. O programa leva essa relação em conta ao sortear os futuros.

[... você escolhe quantos meses simular, quantas "jogadas" fazer etc. ...]

--- CENÁRIO REALISTA (se tudo continuar como no histórico) ---
  Chance de o lucro AUMENTAR : 28%  (entre 27% e 29%, com 95% de confiança)
  Chance de o lucro CAIR     : 66%  (entre 65% e 66%, com 95% de confiança)
  Chance de o lucro ficar ESTÁVEL :  6%
  Lucro esperado (a média de todos os futuros simulados): R$ 3.739
  Resultado mais típico (mediana): R$ 3.683  |  Pior caso: R$ 1.230  |  Melhor caso: R$ 7.685

[... cenários otimista e pessimista, perguntas específicas, faixa de resultados ...]

Gráfico 1 (todos os futuros possíveis, lado a lado): grafico_1_distribuicao_lucro.png
Gráfico 2 (como o lucro evolui mês a mês): grafico_2_evolucao_lucro.png
Gráfico 3 (o que mais pesa no resultado): grafico_3_sensibilidade.png

PRONTO! Abra os três arquivos .png para ver os resultados em forma de gráfico.
```

Repare que, neste exemplo, o cenário realista mostra mais chance de
QUEDA (66%) do que de aumento (28%) — porque, nesses dados fictícios, o
custo da loja tem subido, em média, um pouco mais rápido (+2% ao mês) do
que a receita (+1% ao mês). É exatamente esse tipo de alerta — "seus
custos estão crescendo mais rápido que suas vendas" — que esta
ferramenta ajuda a enxergar antes que o problema fique grande.

---

## 11. Limitações do Modelo

- Os resultados são **estimativas condicionadas** aos dados históricos
  fornecidos e às hipóteses matemáticas assumidas (distribuição Normal
  multivariada para as variações percentuais) — **não são previsões
  financeiras garantidas**.
- O modelo assume que o comportamento estatístico do passado (média,
  desvio padrão, correlação) permanece válido no período futuro
  simulado. Mudanças estruturais do negócio (novo concorrente, nova
  regulamentação, crise econômica severa) não são capturadas
  automaticamente, apenas de forma aproximada através dos cenários
  pessimista/otimista.
- A distribuição Normal tem "caudas leves": eventos extremos raros
  (crises muito severas, picos de demanda muito fora do padrão) tendem a
  ser **subestimados** em frequência, comparado a distribuições com
  caudas mais pesadas, que poderiam descrever melhor certos mercados.
- A sazonalidade explícita (ex.: picos de vendas em datas comemorativas
  específicas) não é modelada separadamente — ela só aparece de forma
  indireta, "diluída" dentro da variância histórica estimada.
- A truncagem de receita e custo em zero (para evitar valores
  economicamente impossíveis) introduz um pequeno viés estatístico nos
  casos mais extremos de queda simulada.
- Os cenários otimista e pessimista usam ajustes **definidos
  manualmente** (documentados em `cenarios.py`), não probabilidades
  objetivamente calculadas — eles servem para ilustrar sensibilidade do
  modelo a premissas de gestão, não como previsão estatística adicional.
- O gráfico de sensibilidade assume relação linear simples entre preço
  médio e volume de vendas (receita = preço médio × volume, com preço
  médio fixo), o que é uma simplificação.
- Quanto menor o número de meses de histórico, menos confiáveis são as
  estimativas de média, desvio padrão e correlação (o programa exige um
  mínimo de 4 meses, mas o ideal é ter, no mínimo, 12 a 24 meses de
  dados reais).

---

## 12. Melhorias Futuras

- Permitir a escolha de outras distribuições de probabilidade além da
  Normal (ex.: distribuição t de Student, para caudas mais pesadas; ou
  distribuições empíricas via bootstrap histórico).
- Modelar a sazonalidade explicitamente (ex.: decompondo a série
  histórica em tendência + sazonalidade + resíduo antes de simular).
- Incluir mais variáveis correlacionadas no modelo conjunto (ex.: volume
  de vendas como uma terceira variável correlacionada, além de receita e
  custo).
- Adicionar uma interface gráfica (ex.: com Streamlit ou Tkinter) para
  tornar o uso mais acessível a usuários não técnicos.
- Validar o modelo comparando previsões passadas simuladas com o que
  realmente aconteceu (backtesting), para medir a qualidade das
  estimativas de forma mais rigorosa.
- Exportar os resultados completos (todas as métricas e percentis) para
  um relatório em PDF ou planilha, além dos gráficos.
