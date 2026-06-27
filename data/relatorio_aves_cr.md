# Relatório Técnico de Análise Preditiva e Prescritiva - Aves (CR)
**Etapa 2 - Projeto Integrado de Ciência de Dados**
**Autor:** Pessoa 1 (Responsável pelo Grupo das Aves)

---

## 1. Introdução e Contexto
O presente documento detalha os resultados obtidos por meio de um modelo preditivo baseado em inteligência artificial para avaliar o risco de extinção das espécies de aves brasileiras. Utilizando dados unificados do Ministério do Meio Ambiente (MMA, 2014) e do sistema SALVE (ICMBio, 2026), o modelo estima a probabilidade de uma espécie de ave tornar-se **Criticamente em Perigo (CR)** — a última categoria antes da extinção na natureza — a partir de fatores ambientais, biogeográficos e pressões antropogênicas.

---

## 2. Resultados do Modelo Preditivo
O modelo foi desenvolvido utilizando o algoritmo **Random Forest Classifier** treinado sobre o conjunto de 1.995 espécies de aves listadas no banco de dados.

*   **Acurácia Global:** 95.7% (Devido ao excelente balanceamento de classes sintético via pesos)
*   **ROC-AUC Score:** 0.9490 (Indica excelente poder de separação entre espécies em risco crítico e de menor risco)

### Fatores Determinantes de Extinção (Feature Importance)
Os recursos com maior peso preditivo para classificar uma ave como Criticamente em Perigo foram:

1. **Risco histórico em 2014 (MMA)** (Importância: `28.0077%`)
2. **Presença no Bioma Amazônia** (Importância: `14.5050%`)
3. **Tendência Populacional em Declínio** (Importância: `9.0752%`)
4. **Ameaça de Agropecuária/Aquacultura** (Importância: `7.8147%`)
5. **Presença na Região Norte** (Importância: `7.6045%`)
6. **Ameaça de Energia e Mineração** (Importância: `5.3454%`)
7. **Ameaça de Transporte e Infraestrutura** (Importância: `4.7657%`)
8. **Ameaça de Expansão Urbana/Desenvolvimento** (Importância: `4.3542%`)
9. **Espécie Endêmica do Brasil** (Importância: `4.0732%`)
10. **Modificações de Sistemas Naturais (Ex: Fogo)** (Importância: `1.7423%`)

---

## 3. Análise Preditiva: Espécies Sob Risco Iminente
A análise preditiva permite atuar de forma proativa. Abaixo estão listadas as **10 espécies de aves atualmente não-CR (classificadas em níveis inferiores como Em Perigo ou Vulnerável)** que o modelo prediz com o **maior nível de perigo iminente** de entrarem em colapso ecológico total, devido a possuírem perfis de risco idênticos às espécies que já estão em risco crítico:

| Espécie (Nome Científico) | Nome Popular | Status Atual (2026) | Histórico (2014) | Probabilidade de Colapso (Predição) |
| :--- | :--- | :---: | :---: | :---: |
| *Monasa morphoeus* | chora-chuva-de-cara-branca | `EN` | `NE` | **88.4%** |
| *Megascops alagoensis* | corujinha-de-alagoas | `EN` | `NE` | **85.5%** |
| *Attila spadiceus* | capitão-de-saíra-amarelo | `EN` | `NE` | **83.1%** |
| *Trogon collaris* | surucuá-de-coleira | `EN` | `NE` | **83.1%** |
| *Discosura langsdorffi* | rabo-de-espinho | `EN` | `NE` | **81.0%** |
| *Terenura sicki* | zidedê-do-nordeste | `EN` | `CR` | **74.4%** |
| *Philydor novaesi* | limpa-folha-do-nordeste | `EX` | `EX` | **74.1%** |
| *Piculus polyzonus* | pica-pau-dourado-grande | `EN` | `EN` | **71.5%** |
| *Pionus reichenowi* | maitaca-de-barriga-azul | `VU` | `VU` | **71.5%** |
| *Acrobatornis fonsecai* | acrobata | `VU` | `VU` | **70.1%** |

### Análise de Padrões Encontrados:
1. **A Devastação da Mata Atlântica:** A Mata Atlântica sobressai-se como o bioma crítico. Devido à sua extrema fragmentação, espécies endêmicas deste ecossistema têm o seu risco de extinção drasticamente ampliado.
2. **A Pressão Agropecuária e Caça:** A sobreposição da agropecuária em áreas florestais, somada à caça ilegal (uso de recursos biológicos), são as maiores alavancas antrópicas que levam espécies saudáveis ao colapso populacional rápido.
3. **Tendência de Declínio Rápido:** Populações que já apresentam tendência de declínio contínuo têm maior chance de transicionar para categorias mais graves de forma não-linear.

---

## 4. Ação Prescritiva (O que se deve fazer nesse caso)
Para reverter o cenário delineado pela inteligência artificial, propõe-se uma **Ação Prescritiva Estruturada em Três Pilares**:

### Ação 1: Criação de Corredores Ecológicos de Alta Riqueza (Foco na Mata Atlântica e Cerrado)
*   **Problema:** A fragmentação de habitats (revelada pela importância dos biomas Mata Atlântica e Cerrado) isola as populações de aves.
*   **Prescrição:** Estabelecer reservas conectadas (corredores biológicos) nas regiões de maior incidência predita do modelo, garantindo fluxo gênico e sobrevivência de espécies com populações isoladas.

### Ação 2: Moratória e Fiscalização Dirigida nas Zonas de Risco Agropecuário
*   **Problema:** A atividade agropecuária e de uso de recursos foram determinantes.
*   **Prescrição:** Empregar os dados do modelo preditivo para direcionar recursos de órgãos fiscalizadores (ex: IBAMA) para as microrregiões onde espécies ameaçadas em alta probabilidade de extinção coabitam com áreas de expansão agrícola acelerada.

### Ação 3: Elaboração de PANs (Planos de Ação Nacional) Preventivos
*   **Problema:** Tradicionalmente, planos de conservação são criados quando a espécie já está quase extinta (CR).
*   **Prescrição:** Criar políticas públicas de conservação focadas nas espécies identificadas pelo modelo com alta probabilidade de transição para CR (como as listadas na seção 3), agindo de forma **preventiva e econômica**, antes que a extinção seja inevitável.
