import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Caminho da base
arquivo = "data/fauna_geral_tratada.csv"

# Leitura da base
df = pd.read_csv(arquivo)

print("Base carregada com sucesso!")
print(df.shape)


# =====================================================
# FILTRA APENAS MAMÍFEROS CR
# =====================================================

df_mamiferos = df[
    (df["classe"] == "Mammalia") &
    (df["categoria_2026"] == "Criticamente em Perigo")
].copy()

print(f"Total de mamíferos CR: {len(df_mamiferos)}")

# Cria pasta para salvar os gráficos
os.makedirs("graficos/mamiferos_cr", exist_ok=True)

plt.style.use("default")

# =====================================================
# GRÁFICO 1 - DISTRIBUIÇÃO POR BIOMA
# =====================================================

biomas = (
    df_mamiferos["bioma"]
    .fillna("Não informado")
    .str.split(";")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)

cores = plt.cm.viridis(np.linspace(0.15, 0.85, len(biomas)))

plt.figure(figsize=(10,6))

plt.barh(
    biomas.index[::-1],
    biomas.values[::-1],
    color=cores[::-1]
)

plt.title(
    "Distribuição de Mamíferos Criticamente em Perigo (CR) por Bioma (2026)",
    fontweight="bold"
)

plt.xlabel("Número de Espécies")
plt.ylabel("Bioma")

plt.grid(axis="x", alpha=0.30)

plt.tight_layout()

plt.savefig(
    "graficos/mamiferos_cr/distribuicao_biomas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# =====================================================
# GRÁFICO 2 - PRINCIPAIS AMEAÇAS
# =====================================================
import re

# Separa todas as ameaças
ameacas = (
    df_mamiferos["ameaca"]
    .dropna()
    .str.split(";")
    .explode()
    .str.strip()
)

# Extrai apenas a categoria principal (1,2,3...11)
def categoria_principal(texto):
    m = re.match(r"(\d+)", texto)
    if m:
        return m.group(1)
    return "Outros"

ameacas = ameacas.apply(categoria_principal)

# Tradução das categorias IUCN
nomes = {
    "1": "Desenvolvimento Residencial e Comercial",
    "2": "Agricultura e Aquicultura",
    "3": "Energia e Mineração",
    "4": "Corredores de Transporte",
    "5": "Uso de Recursos Biológicos",
    "6": "Intrusão e Perturbação Humana",
    "7": "Modificações dos Sistemas Naturais",
    "8": "Espécies Exóticas Invasoras",
    "9": "Poluição",
    "10": "Eventos Geológicos",
    "11": "Mudanças Climáticas"
}

contagem = ameacas.value_counts().sort_index()

labels = [nomes.get(c, c) for c in contagem.index]

cores = plt.cm.magma(np.linspace(0.20, 0.85, len(contagem)))

plt.figure(figsize=(11,6))

plt.barh(labels, contagem.values, color=cores)

plt.title(
    "Principais Ameaças aos Mamíferos Criticamente em Perigo (CR)",
    fontweight="bold"
)

plt.xlabel("Número de Ocorrências (Espécies Afetadas)")
plt.ylabel("Categoria de Ameaça (IUCN)")

plt.grid(axis="x", alpha=0.30)

plt.tight_layout()

plt.savefig(
    "graficos/mamiferos_cr/principais_ameacas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# GRÁFICO 3 - TENDÊNCIA POPULACIONAL
# =====================================================

tendencia = (
    df_mamiferos["tendencia_populacional"]
    .fillna("Desconhecida")
    .value_counts()
)

cores = [
    "#d94b46",
    "#f4b04a",
    "#73b76d",
    "#6aaed6"
][:len(tendencia)]

plt.figure(figsize=(8,8))

plt.pie(
    tendencia.values,
    labels=tendencia.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=cores
)

plt.title(
    "Tendência Populacional dos Mamíferos Criticamente em Perigo (CR)",
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "graficos/mamiferos_cr/tendencia_populacional.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# GRÁFICO 4 - STATUS EM 2014
# =====================================================

status = (
    df_mamiferos["status_2014"]
    .fillna("Não Avaliada/Não Listada em 2014")
    .replace("NE", "Não Avaliada/Não Listada em 2014")
    .replace("CR", "Criticamente em Perigo")
    .value_counts()
)

cores = plt.cm.viridis(np.linspace(0.35, 0.70, len(status)))

plt.figure(figsize=(10,6))

plt.barh(
    status.index[::-1],
    status.values[::-1],
    color=cores[::-1]
)

plt.title(
    "Status em 2014 dos Mamíferos Atualmente em Risco Crítico (CR)",
    fontweight="bold"
)

plt.xlabel("Número de Espécies")
plt.ylabel("Status Histórico (Lista Vermelha de 2014)")

plt.grid(axis="x", alpha=0.30)

plt.tight_layout()

plt.savefig(
    "graficos/mamiferos_cr/transicao_status.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# FILTRA APENAS RÉPTEIS CR
# =====================================================

df_repteis = df[
    (df["classe"] == "Reptilia") &
    (df["categoria_2026"] == "Criticamente em Perigo")
].copy()

print(f"Total de répteis CR: {len(df_repteis)}")

# Cria pasta para salvar os gráficos
os.makedirs("graficos/repteis_cr", exist_ok=True)

# =====================================================
# GRÁFICO 1 - DISTRIBUIÇÃO POR BIOMA
# =====================================================

biomas = (
    df_repteis["bioma"]
    .fillna("Não informado")
    .str.split(";")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)

cores = plt.cm.viridis(np.linspace(0.15, 0.85, len(biomas)))

plt.figure(figsize=(10,6))

plt.barh(
    biomas.index[::-1],
    biomas.values[::-1],
    color=cores[::-1]
)

plt.title(
    "Distribuição de Répteis Criticamente em Perigo (CR) por Bioma (2026)",
    fontweight="bold"
)

plt.xlabel("Número de Espécies")
plt.ylabel("Bioma")

plt.grid(axis="x", alpha=0.30)

plt.tight_layout()

plt.savefig(
    "graficos/repteis_cr/distribuicao_biomas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# GRÁFICO 2 - PRINCIPAIS AMEAÇAS (RÉPTEIS)
# =====================================================
import re

# Separa todas as ameaças
ameacas = (
    df_repteis["ameaca"]
    .dropna()
    .str.split(";")
    .explode()
    .str.strip()
)

# Extrai apenas a categoria principal (1,2,3...11)
def categoria_principal(texto):
    m = re.match(r"(\d+)", texto)
    if m:
        return m.group(1)
    return "Outros"

ameacas = ameacas.apply(categoria_principal)

# Tradução das categorias IUCN
nomes = {
    "1": "Desenvolvimento Residencial e Comercial",
    "2": "Agricultura e Aquicultura",
    "3": "Energia e Mineração",
    "4": "Corredores de Transporte",
    "5": "Uso de Recursos Biológicos",
    "6": "Intrusão e Perturbação Humana",
    "7": "Modificações dos Sistemas Naturais",
    "8": "Espécies Exóticas Invasoras",
    "9": "Poluição",
    "10": "Eventos Geológicos",
    "11": "Mudanças Climáticas"
}

contagem = ameacas.value_counts().sort_index()

labels = [nomes.get(c, c) for c in contagem.index]

cores = plt.cm.magma(np.linspace(0.20, 0.85, len(contagem)))

plt.figure(figsize=(11,6))

plt.barh(labels, contagem.values, color=cores)

plt.title(
    "Principais Ameaças aos Mamíferos Criticamente em Perigo (CR)",
    fontweight="bold"
)

plt.xlabel("Número de Ocorrências (Espécies Afetadas)")
plt.ylabel("Categoria de Ameaça (IUCN)")

plt.grid(axis="x", alpha=0.30)

plt.tight_layout()

plt.savefig(
    "graficos/mamiferos_cr/principais_ameacas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# GRÁFICO 3 - TENDÊNCIA POPULACIONAL
# =====================================================

tendencia = (
    df_repteis["tendencia_populacional"]
    .fillna("Desconhecida")
    .value_counts()
)

cores = [
    "#d94b46",
    "#f4b04a",
    "#73b76d",
    "#6aaed6"
][:len(tendencia)]

plt.figure(figsize=(8,8))

plt.pie(
    tendencia.values,
    labels=tendencia.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=cores
)

plt.title(
    "Tendência Populacional dos Répteis Criticamente em Perigo (CR)",
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "graficos/repteis_cr/tendencia_populacional.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# GRÁFICO 4 - STATUS EM 2014
# =====================================================

status = (
    df_repteis["status_2014"]
    .fillna("Não Avaliada/Não Listada em 2014")
    .replace("NE", "Não Avaliada/Não Listada em 2014")
    .replace("CR", "Criticamente em Perigo")
    .value_counts()
)

cores = plt.cm.viridis(np.linspace(0.35, 0.70, len(status)))

plt.figure(figsize=(10,6))

plt.barh(
    status.index[::-1],
    status.values[::-1],
    color=cores[::-1]
)

plt.title(
    "Status em 2014 dos Répteis Atualmente em Risco Crítico (CR)",
    fontweight="bold"
)

plt.xlabel("Número de Espécies")
plt.ylabel("Status Histórico (Lista Vermelha de 2014)")

plt.grid(axis="x", alpha=0.30)

plt.tight_layout()

plt.savefig(
    "graficos/repteis_cr/transicao_status.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()