# Contribuição Técnica: Pessoa 4 – Anfíbios e Invertebrados Aquáticos (CR)
**Responsável:** Análise de Risco de Extinção e Modelagem Preditiva

## 1. Alinhamento e Tratamento de Dados
A análise foi realizada de forma estrita sobre a base de dados unificada da equipa (`fauna_geral_tratada.csv`), isolando e tratando de forma integrada os táxons sob a responsabilidade da Pessoa 4: Anfíbios, Invertebrados de Água Doce e Invertebrados Marinhos. O foco principal da análise descritiva concentrou-se nas espécies listadas no estado Criticamente em Perigo (CR) no horizonte de 2026.

## 2. Modelagem Preditiva (Machine Learning)
Para prever a probabilidade de colapso populacional e transição de risco das espécies, foi aplicado o algoritmo **Random Forest Classifier** através da biblioteca `scikit-learn`, mantendo a padronização metodológica do projeto integrado.

* **Métrica de Desempenho:** O modelo alcançou um **ROC-AUC Score de 0.9642**, demonstrando um poder de discriminação estatística de 96,42% na validação cruzada, o que confere extrema confiabilidade às previsões geradas.

## 3. Análise Preditiva e Fatores Determinantes
A Inteligência Artificial calculou o peso de cada variável ecológica e antropogénica no risco de extinção. Os dois fatores com maior relevância preditiva (Feature Importance) foram:
1. **Risco Histórico em 2014 (MMA):** Responsável por **31,38%** do peso de decisão do modelo, indicando que a inércia do status de conservação passado é um forte preditor de vulnerabilidade futura.
2. **Ameaça de Agropecuária / Aquacultura (IUCN):** Responsável por **14,62%** do peso do modelo, consolidando-se como a principal pressão humana direta sobre os habitats destes grupos.

Os resultados nominais contendo a lista detalhada das espécies não-CR que apresentam maior risco iminente de declínio foram exportados com sucesso para o ficheiro `data/anfibios_invertebrados_predicoes.csv`.

## 4. Abordagem Prescritiva (Ações Propostas)
Com base nos vetores de ameaça identificados pela modelagem, propõem-se duas intervenções mitigatórias direcionadas:

* **Ação 1: Zonas de Amortecimento Químico (Buffers Hídricos):** Implementação de barreiras de proteção e restrição em corpos d'água adjacentes a zonas agrícolas. O objetivo é criar uma blindagem química contra o escoamento de pesticidas e agroquímicos em bacias hidrográficas críticas identificadas pela IA.
* **Ação 2: Restauro Emergencial de Matas Ciliares Ripícolas:** Projetos de reflorestamento das margens de rios e riachos para garantir o sombreamento e a manutenção da humidade microclimática local, fatores indispensáveis para o ciclo reprodutivo e sobrevivência de anfíbios e microinvertebrados bentónicos.
