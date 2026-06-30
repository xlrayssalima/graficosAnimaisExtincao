Relatório Técnico de Análise Preditiva e Prescritiva – Tubarões e Raias (CR)
Etapa 2 – Projeto Integrado de Ciência de Dados  
Autor: Pessoa responsável pelo Grupo de Tubarões e Raias

1. Introdução e Contexto
Este documento apresenta os resultados obtidos por meio de um modelo preditivo baseado em inteligência artificial para avaliar o risco de extinção das espécies de tubarões e raias brasileiras. Utilizando dados integrados do Ministério do Meio Ambiente (MMA, 2014) e do sistema SALVE (ICMBio, 2026), o modelo estima a probabilidade de uma espécie tornar-se Criticamente em Perigo (CR) — a última categoria antes da extinção na natureza — considerando fatores ambientais, biogeográficos e pressões antrópicas.

2. Resultados do Modelo Preditivo
O modelo foi desenvolvido utilizando o algoritmo Random Forest Classifier treinado sobre o conjunto de espécies de tubarões e raias listadas no banco de dados.

Acurácia Global: 93.2%

ROC-AUC Score: 0.9275 (indica excelente poder de separação entre espécies em risco crítico e de menor risco)

Fatores Determinantes de Extinção (Feature Importance)
Os recursos com maior peso preditivo para classificar tubarões e raias como Criticamente em Perigo foram:

Risco histórico em 2014 (MMA)

Presença no Bioma Costeiro-Marinho

Tendência Populacional em Declínio

Ameaça de Atividade Pesqueira (industrial e artesanal)

Ameaça de Poluição Marinha (resíduos e contaminantes)

Ameaça de Transporte/Infraestrutura costeira

Espécie Endêmica da costa brasileira

Modificações de Sistemas Naturais (ex: destruição de manguezais)

3. Análise Preditiva: Espécies Sob Risco Iminente
A análise preditiva permite identificar espécies que ainda não estão em CR, mas apresentam alta probabilidade de transição para essa categoria.

Exemplos de espécies com maior risco iminente:

Espécie (Nome Científico)	Nome Popular	Status Atual (2026)	Histórico (2014)	Probabilidade de Colapso (Predição)
Pristis perotteti	peixe-serra	EN	VU	86.7%
Squatina guggenheim	cação-anjo	EN	VU	82.4%
Sphyrna lewini	tubarão-martelo	VU	VU	79.5%
Mobula thurstoni	raia-manta	VU	VU	77.2%
Rhinobatos percellens	cação-viola	VU	VU	74.8%


Padrões Identificados:
Pressão Pesqueira Intensa: Espécies alvo de pesca comercial ou incidental apresentam risco elevado.

Degradação de Habitats Costeiros: Manguezais e recifes degradados reduzem áreas de reprodução e alimentação.

Poluição Marinha: Resíduos sólidos e contaminantes químicos aumentam mortalidade e reduzem resiliência populacional.

4. Ação Prescritiva
Para mitigar os riscos identificados, propõe-se uma Ação Prescritiva Estruturada em Três Pilares:

Ação 1: Criação de Áreas Marinhas Protegidas (AMPs)
Problema: A maioria das espécies em risco crítico está concentrada no bioma costeiro-marinho.

Prescrição: Expandir e fiscalizar AMPs em regiões estratégicas, garantindo refúgio para reprodução e alimentação.

Ação 2: Controle da Pesca e Monitoramento Populacional
Problema: A atividade pesqueira é o principal vetor de ameaça.

Prescrição: Implementar cotas de captura, proibição de pesca de espécies críticas e monitoramento contínuo das populações.

Ação 3: Redução da Poluição Marinha
Problema: Resíduos sólidos e químicos impactam diretamente tubarões e raias.

Prescrição: Programas de redução de plásticos, saneamento costeiro e fiscalização de efluentes industriais.