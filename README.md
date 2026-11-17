# Simulador de Probabilidade de Lucro Empresarial (Simulação de Monte Carlo)

Projeto acadêmico — Atividade Prática A3 de Matemática Computacional Aplicada
Tema: Probabilidade e Simulação

## Sumário

- [Visão geral](#visão-geral)
- [Arquivos do projeto](#arquivos-do-projeto)
- [Ordem de execução](#ordem-de-execução)
- [Módulo dados.py](#módulo-dadospy--carregamento-e-validação-dos-dados)
- [Módulo estatistica.py](#módulo-estatisticapy--parâmetros-estatísticos-do-modelo)
- [Módulo simulacao.py](#módulo-simulacaopy--motor-da-simulação-de-monte-carlo)
- [Módulo analise.py](#módulo-analisepy--probabilidades-de-negócio)
- [Módulo cenarios.py](#módulo-cenariospy--cenários-otimista--realista--pessimista)
- [Módulo graficos.py](#módulo-graficospy--visualização-3-gráficos-png)
- [Módulo main.py](#módulo-mainpy--orquestração-do-programa)
- [Módulo textos.py](#módulo-textospy--microcopy-ui-writing)
- [Resumo das fórmulas matemáticas](#resumo-das-fórmulas-matemáticas)
- [Como rodar](#como-rodar)

## Visão geral

O programa simula milhares de futuros possíveis para o lucro de uma empresa a partir do histórico financeiro mensal (receita, custos e volume de vendas). Em vez de dar um único número de previsão, ele responde com percentuais de chance:

- O lucro vai aumentar, cair ou ficar estável?
- Qual a chance de bater uma meta de lucro?
- Qual a chance de dar prejuízo?
- Qual a chance de queda maior que 10%? E de aumento maior que 20%?
- Qual variável (receita, custo, volume de vendas) mais afeta o resultado?

**Técnica usada:** Simulação de Monte Carlo com distribuição Normal multivariada para sortear variações percentuais correlacionadas de receita e custo.

## Arquivos do projeto

| Arquivo | Descrição |
|---|---|
| `main.py` | Programa principal. Orquestra todo o fluxo. |
| `dados.py` | Carrega e valida os dados financeiros (exemplo ou CSV). |
| `estatistica.py` | Calcula média, variância, desvio, covariância, correlação, percentis e intervalo de confiança. |
| `simulacao.py` | Motor da Simulação de Monte Carlo (sorteia futuros possíveis). |
| `analise.py` | Calcula probabilidades de negócio a partir da simulação. |
| `cenarios.py` | Define os cenários otimista / realista / pessimista. |
| `graficos.py` | Gera os 3 gráficos PNG (distribuição, evolução, sensibilidade). |
| `textos.py` | Centraliza todo o microcopy (texto que o usuário lê). |
| `dados_exemplo.csv` | Conjunto de dados fictícios de demonstração (12 meses). |
| `requirements.txt` | Dependências (numpy, matplotlib, pandas). |

## Ordem de execução

Ao rodar `python main.py`, o programa executa, nesta ordem:

1. **Escolha e validação da fonte de dados** (`dados.py`)
2. **Estatística das variações percentuais** (`estatistica.py`)
3. **Configuração da simulação** (4 perguntas ao usuário)
4. **Simulação de Monte Carlo para 3 cenários** (`simulacao.py` + `cenarios.py`)
5. **Análise estatística adicional** (cenário realista) (`analise.py`)
6. **Geração dos 3 gráficos** (`graficos.py`)

Cada passo é detalhado a seguir, com as fórmulas usadas.

## Módulo dados.py — Carregamento e validação dos dados

### O que faz

Responsável por carregar o histórico financeiro mensal da empresa (receita, custos operacionais, volume de vendas) e validar se os dados estão consistentes antes de iniciar a simulação.

Pode usar:
- dados fictícios de demonstração (`dados_exemplo.csv` / `carregar_dados_exemplo`)
- um arquivo CSV real informado pelo usuário (`carregar_dados_csv`)

### Classe `DadosFinanceiros`

Estrutura de dados (dataclass) que armazena:

- `meses` — array com o número de cada mês (1, 2, 3, ...)
- `receita` — array com a receita de cada mês (R$)
- `custos` — array com os custos de cada mês (R$)
- `volume_vendas` — array com a quantidade vendida de cada mês (unidades)
- `origem` — texto dizendo de onde vieram os dados

Propriedades calculadas (somente leitura):

- `lucro` = receita − custos (R$)
- `margem_lucro` = (lucro / receita) × 100 (%)
- `n_meses` = quantidade de meses no histórico

### Funções

**`carregar_dados_exemplo()`**
Retorna um objeto `DadosFinanceiros` com 12 meses de dados fictícios (números redondos, só para demonstração). Não representa empresa real.

**`carregar_dados_csv(caminho_arquivo)`**
Lê um `.csv` com pandas, confere se existem as colunas obrigatórias (`mes`, `receita`, `custos`, `volume_vendas`), converte para numérico e retorna o objeto `DadosFinanceiros`. Levanta `ValueError` se faltar coluna ou se o pandas não estiver instalado.

**`validar_dados(dados)`**
Verifica, nesta ordem:
1. número mínimo de meses (`MESES_MINIMOS_EXIGIDOS = 4`)
2. receita estritamente positiva em todos os meses (evita divisão por zero)
3. custo não-negativo

Se algo falhar, levanta `ValueError` com mensagem clara.

### Fórmulas envolvidas

```
Lucro de um mês:              L_t = R_t - C_t
Margem de lucro de um mês:    M_t = (L_t / R_t) * 100 = ((R_t - C_t) / R_t) * 100
```
onde `R_t` = receita do mês t, `C_t` = custo do mês t, `L_t` = lucro do mês t.

## Módulo estatistica.py — Parâmetros estatísticos do modelo

### O que faz

Transforma o histórico bruto em parâmetros estatísticos que a simulação vai usar: média, variância, desvio padrão, covariância, correlação, percentis e intervalo de confiança.

### `calcular_variacoes_percentuais(serie)`

Recebe um vetor de valores mensais (ex.: receita de cada mês) e retorna as variações percentuais mês a mês.

```
x_t = (serie_t - serie_{t-1}) / serie_{t-1}
```

Exemplo: se a receita foi 10.000 no mês 1 e 10.400 no mês 2:
`x_2 = (10.400 - 10.000) / 10.000 = 0,04 = +4%`

### `media_variancia_desvio(amostra)`

Recebe um vetor de variações percentuais e retorna a tupla `(media, variancia, desvio_padrao)`, usando `ddof=1` (correção de Bessel).

```
média:      x̄ = (1/n) * Σ x_i
variância:  s² = (1/(n-1)) * Σ (x_i - x̄)²      ← divisor n-1 (amostral)
desvio:     s = sqrt(s²)
```

A correção de Bessel (n−1 em vez de n) é usada porque estamos estimando a variância de uma população a partir de uma amostra finita.

### `matriz_covariancia_correlacao(variacao_receita, variacao_custo)`

Recebe os dois vetores de variação (receita e custo) e retorna um dicionário com `vetor_medias`, `matriz_covariancia` e `correlacao`.

```
vetor de médias:  μ = [μ_R, μ_C]
covariância:      Cov(R, C) = (1/(n-1)) * Σ (xR_i - x̄R) * (xC_i - x̄C)
correlação:       ρ = Cov(R, C) / (s_R * s_C)
```

ρ varia de −1 a +1:
- Próximo de +1: receita e custo sobem/descem juntos (positiva)
- Próximo de 0: variam de forma quase independente
- Próximo de −1: quando um sobe, o outro tende a cair (negativa)

### `calcular_percentis(amostra, percentis=(10,25,50,75,90))`

Calcula os percentis pedidos de um vetor de resultados usando `numpy.percentile`. Retorna um dicionário `{p10: v10, p25: v25, ..., p90: v90}`.

### `intervalo_confianca_proporcao(p_estimado, n_amostras, confianca=0.95)`

Recebe uma probabilidade estimada (ex.: 0,87) e o número de simulações, e retorna o intervalo de confiança em torno dessa estimativa (método de Wilson).

```
z = 1,959964   (valor crítico para 95% de confiança)

denominador = 1 + z² / n
centro      = p + z² / (2n)
margem      = z * sqrt( (p*(1-p)/n) + z² / (4n²) )

limite_inferior = (centro - margem) / denominador
limite_superior = (centro + margem) / denominador
```

Isso comunica a incerteza da própria estimativa de probabilidade: quanto mais simulações, mais estreito o intervalo.

## Módulo simulacao.py — Motor da Simulação de Monte Carlo

### O que faz

É o núcleo matemático do projeto. Gera milhares de trajetórias possíveis de receita, custo e lucro ao longo de N meses futuros, sorteando variações percentuais correlacionadas de uma distribuição Normal multivariada.

### `gerar_variacoes_correlacionadas(...)`

Sorteia, de uma só vez (vetorizado, sem laços Python lentos), todas as variações percentuais conjuntas de receita e custo necessárias.

Usa:
```python
gerador.multivariate_normal(mean=vetor_medias, cov=matriz_covariancia,
                             size=n_simulacoes * n_meses)
```

O resultado é reorganizado em um array de formato `(n_simulacoes, n_meses, 2)`, onde a terceira dimensão contém `[variação_receita, variação_custo]` para cada mês de cada simulação.

### `simular_monte_carlo(...)`

A função central. Recebe receita_atual, custo_atual, parâmetros estatísticos, inflação mensal, número de meses, número de simulações e semente.

Passo a passo do algoritmo:

1. Cria um gerador de números aleatórios reproduzível: `gerador = np.random.default_rng(semente)` (semente = 42)
2. Sorteia as variações correlacionadas (receita e custo) para todos os meses e simulações.
3. Soma a inflação mensal à variação de custo.
4. Para cada mês (de 1 até n_meses), atualiza mês a mês:
   ```
   receita_corrente = receita_corrente * (1 + variação_receita)
   custo_corrente   = custo_corrente   * (1 + variação_custo + inflação)
   ```
   Trunca em zero (não permite receita/custo negativo): `valor = max(valor, 0)`
5. Ao final, calcula o lucro de cada simulação: `lucro_final = receita_final - custo_final`

Retorna um dicionário com três matrizes `(n_simulacoes, n_meses)`: `{"receitas": ..., "custos": ..., "lucros": ...}`

Fórmulas da simulação (mês a mês):
```
R_{novo} = R_{atual} * (1 + δ_R)        (truncado em 0)
C_{novo} = C_{atual} * (1 + δ_C + inf)  (truncado em 0)
L        = R_final - C_final
```
onde δ_R e δ_C são variações percentuais sorteadas da Normal multivariada e `inf` é a inflação mensal.

### `classificar_resultado(lucro_final, lucro_atual, tolerancia=0.02)`

Recebe o lucro final de cada simulação e classifica cada uma como aumento, queda ou estável, usando uma faixa de tolerância (±2% por padrão) ao redor do lucro atual.

```
limite_superior = lucro_atual * (1 + tolerancia)
limite_inferior = lucro_atual * (1 - tolerancia)

estável  se lucro_final >= limite_inferior E lucro_final <= limite_superior
aumento  se lucro_final >  limite_superior
queda    se lucro_final <  limite_inferior
```

## Módulo analise.py — Probabilidades de negócio

### O que faz

Calcula as probabilidades de negócio a partir dos resultados da simulação: chance de aumento/queda/estável, chance de bater meta, chance de prejuízo, chance de queda/aumento maior que um percentual, e um resumo estatístico.

### Funções e fórmulas

**`calcular_probabilidades_resultado(lucro_final, lucro_atual, ...)`**
Usa `classificar_resultado` e, para cada categoria, calcula a proporção de simulações naquela categoria (probabilidade por frequência relativa) e o intervalo de confiança dessa proporção.

```
P(evento) ≈ (número de simulações onde o evento ocorreu) / (total de simulações)
```

**`probabilidade_meta(lucro_final, meta)`**
`P(lucro >= meta)` = fração de simulações que atingiram ou superaram a meta

**`probabilidade_prejuizo(lucro_final)`**
`P(lucro < 0)` = fração de simulações com lucro negativo

**`probabilidade_queda_maior_que(lucro_final, lucro_atual, percentual)`**
```
limite = lucro_atual * (1 - percentual)
P(lucro_final <= limite)
```

**`probabilidade_aumento_maior_que(lucro_final, lucro_atual, percentual)`**
```
limite = lucro_atual * (1 + percentual)
P(lucro_final >= limite)
```

**`resumo_estatistico(lucro_final)`**
Agrega:
- `valor_esperado` = média dos lucros finais
- `minimo` = menor lucro simulado
- `maximo` = maior lucro simulado
- `mediana` = valor do meio (50% abaixo, 50% acima)
- `desvio_padrao` = desvio padrão amostral (ddof=1)
- `percentis` = p10, p25, p50, p75, p90

```
valor esperado:  E[L] ≈ (1/N) * Σ L_i
desvio padrão:   s = sqrt( (1/(N-1)) * Σ (L_i - x̄)² )
```

## Módulo cenarios.py — Cenários otimista / realista / pessimista

### O que faz

Define ajustes manuais aplicados aos parâmetros estatísticos para gerar três "humores" de futuro:

- **Otimista:** receita favorecida, custos controlados, menos volatilidade
- **Realista:** comportamento histórico direto (sem ajuste)
- **Pessimista:** receita reduzida, custos aumentados, mais volatilidade

### Dicionário `AJUSTES_CENARIOS`

Cada cenário tem:
- `ajuste_media_receita` — pontos percentuais somados à média de receita
- `ajuste_media_custo` — pontos percentuais somados à média de custo
- `fator_reducao_desvio` — fator que reescala o desvio padrão (variância × fator²)
- `ajuste_inflacao` — ajuste na inflação mensal
- `descricao` — texto amigável do cenário

| Cenário | Receita | Custo | Desvio | Inflação |
|---|---|---|---|---|
| Otimista | +2% | −1% | 0,85× | −0,1% |
| Realista | +0% | +0% | 1,00× | +0,0% |
| Pessimista | −2,5% | +1,5% | 1,25× | +0,3% |

### `montar_parametros_cenario(nome_cenario, ...)`

Aplica os ajustes sobre os parâmetros reais estimados do histórico:

```
vetor_medias_ajustado       = vetor_medias + [ajuste_receita, ajuste_custo]
matriz_covariancia_ajustada = matriz_covariancia * (fator²)
inflacao_ajustada           = inflacao_base + ajuste_inflacao
```

Retorna `vetor_medias`, `matriz_covariancia`, `inflacao_mensal` e `descricao`, prontos para alimentar `simular_monte_carlo()`.

## Módulo graficos.py — Visualização (3 gráficos PNG)

### O que faz

Gera três imagens PNG que resumem os resultados visualmente, usando Matplotlib. Todos usam formatação em Reais (R$) nos eixos e possuem título, legenda e rótulos compreensíveis para não-técnicos.

### Gráfico 1 — Distribuição do lucro (`grafico_1_distribuicao_lucro.png`)

Tipo: histograma com todos os lucros finais simulados.

- Barras vermelhas: futuros em que o lucro **caiu** (abaixo do lucro atual)
- Barras verdes: futuros em que o lucro **aumentou** (acima do lucro atual)
- Linha tracejada preta: lucro de hoje
- Linha roxa contínua: lucro esperado (média de todos os futuros)

Eixo X: lucro que a loja teria nesse futuro simulado (R$). Eixo Y: quantos futuros simulados deram nesse resultado.

### Gráfico 2 — Evolução do lucro mês a mês (`grafico_2_evolucao_lucro.png`)

Tipo: faixas de percentil ao longo dos meses.

- Faixa escura (p25 a p75): 50% dos cenários mais prováveis
- Faixa clara (p10 a p90): 80% dos cenários (inclui extremos plausíveis)
- Linha central: mediana (p50)
- Linha tracejada: lucro de hoje

Eixo X: meses no futuro. Eixo Y: lucro projetado (R$).

Quanto mais a faixa se abre com o tempo, maior a incerteza acumulada.

### Gráfico 3 — Análise de sensibilidade (`grafico_3_sensibilidade.png`)

Tipo: gráfico "tornado". Para cada indicador (receita, custos, volume de vendas), mostra o impacto exato em R$ no lucro caso esse indicador varie +10% (verde) ou −10% (vermelho), mantendo os outros dois constantes.

Cálculo para cada variável:
```
impacto_alta  = lucro_com_variacao_+10% - lucro_base
impacto_baixa = lucro_com_variacao_-10% - lucro_base
```
onde `lucro_base = receita_atual - custo_atual`. Para volume de vendas, usa `preço_medio = receita_atual / volume_atual`.

Quanto mais larga a barra, maior a influência desse indicador sobre o lucro final — ajuda a identificar onde a gestão deve focar.

### `formatar_reais(valor)`

Formata um número do eixo como "R$ 12.000" em vez de "12000.0".

## Módulo main.py — Orquestração do programa

### O que faz

Programa principal. Conecta todos os módulos e conduz o usuário pelo fluxo completo da simulação, imprimindo tudo no terminal de forma amigável.

### Passo a passo de `main()`

**Passo A — Cabeçalho e explicação simples**
Imprime o título e um texto simples (análogo à previsão do tempo) definindo RECEITA, CUSTO, LUCRO e CHANCE DE AUMENTAR/CAIR.

**Passo B — Escolha da fonte de dados**
Pergunta se o usuário quer dados fictícios ou um CSV real. Chama `dados.carregar_dados_exemplo()` ou `dados.carregar_dados_csv()`.

**Passo C — Validação**
Chama `dados.validar_dados()`. Se falhar, encerra com mensagem de erro.

**Passo D — Cabeçalho dos dados de partida**
Mostra origem, quantidade de meses, receita/custo/volume/lucro do último mês e margem de lucro.

**Passo E — Estatísticas de variação**
Calcula variações percentuais (`estatistica.calcular_variacoes_percentuais`), média/variância/desvio (`media_variancia_desvio`) e covariância/correlação (`matriz_covariancia_correlacao`). Imprime esses valores com interpretação (forte/fraca, positiva/negativa).

**Passo F — Configuração (4 perguntas)**
1. Faturamento mensal médio atual
2. Custo mensal médio atual
3. Quantos meses projetar (padrão: 12)
4. Ritmo/risco do mercado (1=estável→otimista, 2=normal→realista, 3=alta volatilidade→pessimista)

Cada pergunta tem validação via `ler_numero()` com valor padrão.

**Passo G — Simulação dos 3 cenários**
Para cada cenário (otimista, realista, pessimista):
- `monta_parametros_cenario()` ajusta os parâmetros
- `simular_monte_carlo()` sorteia N=10.000 futuros
- `calcular_probabilidades_resultado()` calcula chance de aumento/queda/estável com IC de 95%
- `resumo_estatistico()` calcula esperado, mediana, mín, máx, desvio

Imprime o resultado de cada cenário.

**Passo H — Perguntas específicas (cenário realista)**
- Chance de bater meta (lucro_atual × 1,5)
- Chance de prejuízo (lucro < 0)
- Chance de queda > 10%
- Chance de aumento > 20%
- Percentis p10/p25/p50/p75/p90 e desvio padrão

**Passo I — Gráficos**
Gera os 3 PNGs e informa os nomes dos arquivos.

### `ler_numero(mensagem, padrao, tipo, minimo)`

Lê um número do usuário com valor padrão e validação. Se digitar algo inválido ou abaixo do mínimo, avisa e usa o padrão (não trava o programa).

## Módulo textos.py — Microcopy (UI Writing)

Centraliza TODO o texto que o usuário lê (títulos, legendas, mensagens de erro, rótulos dos gráficos), separado da lógica dos módulos. Os módulos importam `import textos as T` e usam as constantes com `.format()` para as partes variáveis. Facilita revisar a linguagem sem quebrar o cálculo.

## Resumo das fórmulas matemáticas

```
Lucro mensal:                    L_t = R_t - C_t
Margem de lucro (%):             M_t = (L_t / R_t) * 100
Variação percentual:             x_t = (v_t - v_{t-1}) / v_{t-1}
Média amostral:                  x̄ = (1/n) * Σ x_i
Variância amostral (Bessel):     s² = (1/(n-1)) * Σ (x_i - x̄)²
Desvio padrão:                   s = sqrt(s²)
Covariância:                     Cov(R,C) = (1/(n-1)) * Σ (xR_i - x̄R)(xC_i - x̄C)
Correlação de Pearson:           ρ = Cov(R,C) / (s_R * s_C)
Simulação (mês a mês):           R_{novo} = R * (1 + δ_R)
                                  C_{novo} = C * (1 + δ_C + inflação)
                                  L = R_final - C_final
Estabilidade (±t):                aumenta se L > L_atual*(1+t)
                                  cai    se L < L_atual*(1-t)
                                  estável caso contrário
Probabilidade (freq. relativa):  P ≈ (ocorrências) / (total de simulações)
Meta:                             P(L >= meta)
Prejuízo:                         P(L < 0)
Queda > p%:                       P(L <= L_atual*(1-p))
Aumento > p%:                     P(L >= L_atual*(1+p))
Intervalo de confiança (Wilson): ver seção "estatistica.py"
```

## Como rodar

1. Instale o Python 3 (3.10+ recomendado) e marque "Add Python to PATH".
2. Na pasta do projeto, crie e ative um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\Activate.ps1      # Windows PowerShell
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Execute:
   ```
   python main.py
   ```
5. Responda as 4 perguntas (ou aperte Enter para usar os padrões).
6. Ao final, abra os três arquivos `.png` gerados na mesma pasta.
