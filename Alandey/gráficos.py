import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# LEITURA DOS BANCO
# =========================

df1 = pd.read_csv("https://raw.githubusercontent.com/xlrayssalima/graficosAnimaisExtincao/main/br_mma_extincao_fauna_ameacada.csv")
df2 = pd.read_csv("https://raw.githubusercontent.com/xlrayssalima/graficosAnimaisExtincao/main/salve-publico-exportacao-fichas-planilha12-05-2026-15-56-40%20(1).csv")

# =========================
# FILTRAR INVERTEBRADOS
# DE ÁGUA DOCE E MARINHOS
# =========================

filtro = df2["grupo"].isin([
    "Invertebrados de Água Doce",
    "Invertebrados Marinhos"
])

dados = df2[filtro]

# =========================
# GRÁFICO 1 - BARRAS
# Quantidade por categoria
# =========================

plt.figure(figsize=(10, 6))

sns.countplot(
    data=dados,
    x="categoria",
    hue="grupo"
)

plt.title("Espécimes ameaçados por categoria")
plt.xlabel("Categoria de ameaça")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)

plt.show()

# =========================
# GRÁFICO 2 - DISPERSÃO
# =========================

dados["ano"] = dados["mesano_avaliacao"].astype(str).str.extract(r'(\d{4})')

dados["ano"] = pd.to_numeric(
    dados["ano"],
    errors="coerce"
)

plt.figure(figsize=(12, 6))

sns.scatterplot(
    data=dados,
    x="ano",
    y="categoria",
    hue="grupo",
    s=100
)

plt.title("Avaliações de espécies ameaçadas")
plt.xlabel("Ano da avaliação")
plt.ylabel("Categoria")

plt.xticks(rotation=45)

plt.show()

# =========================
# GRÁFICO 3 - PIZZA
# Distribuição dos grupos
# =========================

quantidade_grupos = dados["grupo"].value_counts()

plt.figure(figsize=(8, 8))

plt.pie(
    quantidade_grupos,
    labels=quantidade_grupos.index,
    autopct="%1.1f%%"
)

plt.title("Distribuição de Invertebrados")

plt.show()