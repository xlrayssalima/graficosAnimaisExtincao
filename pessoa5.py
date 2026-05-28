# ================================================================
# PROJETO: Espécies da Fauna Brasileira Ameaçadas de Extinção
# PESSOA 5 — Histograma + Gráfico de Barra + Estatísticas
# Grupos: Répteis e Tubarões e Raias
# Banco 1: MMA | Banco 2: SALVE/ICMBio
# ================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ═══════════════════════════════════════════════════════════════
# BANCO 1 — MMA
# ═══════════════════════════════════════════════════════════════
df_mma = pd.read_csv("br_mma_extincao_fauna_ameacada.csv")

df_mma_rep = df_mma[df_mma["grupo"] == "repteis"].copy()

ordem_cat_mma = ["VU", "EN", "CR", "CR (PEX)", "EX", "RE", "EW"]
df_mma_rep["categoria_num"] = df_mma_rep["categoria"].map(
    {c: i + 1 for i, c in enumerate(ordem_cat_mma)}
)

cores_mma = {
    "VU":      "#f9c74f",
    "EN":      "#f77f00",
    "CR":      "#d62828",
    "CR (PEX)":"#7b2d8b",
    "EX":      "#000000",
    "RE":      "#888888",
    "EW":      "#aaaaaa",
}

# ── ESTATÍSTICAS BANCO 1 ─────────────────────────────────────────
print("=" * 55)
print("ESTATÍSTICAS — Banco MMA | Grupo: Répteis")
print("(1=VU, 2=EN, 3=CR, 4=CR(PEX), 5=EX, 6=RE, 7=EW)")
print("=" * 55)
print(f"Média:          {df_mma_rep['categoria_num'].mean():.2f}")
print(f"Mediana:        {df_mma_rep['categoria_num'].median():.2f}")
print(f"Desvio Padrão:  {df_mma_rep['categoria_num'].std():.2f}")
print()
print("Contagem por categoria:")
print(df_mma_rep["categoria"].value_counts().reindex(ordem_cat_mma).dropna().astype(int))
print("=" * 55)
print()

# ── HISTOGRAMA — BANCO MMA ───────────────────────────────────────
contagem_mma = (
    df_mma_rep["categoria"]
    .value_counts()
    .reindex(ordem_cat_mma)
    .dropna()
    .astype(int)
    .reset_index()
)
contagem_mma.columns = ["categoria", "quantidade"]
contagem_mma["cor"] = contagem_mma["categoria"].map(cores_mma)

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(
    contagem_mma["categoria"],
    contagem_mma["quantidade"],
    color=contagem_mma["cor"],
    edgecolor="white",
    width=0.6,
)

for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=11, fontweight="bold"
    )

ax.set_title(
    "Histograma — Répteis Ameaçados por Categoria de Risco\n(Base MMA — Portaria 148/2022)",
    fontsize=13, fontweight="bold", pad=15
)
ax.set_xlabel("Categoria de Ameaça", fontsize=12)
ax.set_ylabel("Número de Espécies", fontsize=12)
ax.set_ylim(0, contagem_mma["quantidade"].max() + 8)
ax.grid(axis="y", linestyle="--", alpha=0.5)
sns.despine()

plt.tight_layout()
plt.show()


# ═══════════════════════════════════════════════════════════════
# BANCO 2 — SALVE/ICMBio
# ═══════════════════════════════════════════════════════════════
df_salve = pd.read_csv(
    "salve-publico-exportacao-fichas-planilha12-05-2026-15-56-40.csv",
    sep=None, engine="python"
)

grupos_salve = ["Répteis", "Tubarões e Raias"]
df_salve_g = df_salve[df_salve["grupo"].isin(grupos_salve)].copy()

categorias_ameacadas = [
    "Vulnerável", "Em Perigo", "Criticamente em Perigo",
    "Extinta", "Regionalmente Extinta", "Extinta na Natureza"
]
df_salve_am = df_salve_g[df_salve_g["categoria"].isin(categorias_ameacadas)].copy()

ordem_cat_salve = [
    "Vulnerável", "Em Perigo", "Criticamente em Perigo",
    "Regionalmente Extinta", "Extinta na Natureza", "Extinta"
]
df_salve_am["categoria_num"] = df_salve_am["categoria"].map(
    {c: i + 1 for i, c in enumerate(ordem_cat_salve)}
)

# ── ESTATÍSTICAS BANCO 2 ─────────────────────────────────────────
print("=" * 55)
print("ESTATÍSTICAS — Banco SALVE | Répteis + Tubarões e Raias")
print("(1=Vulnerável, 2=Em Perigo, 3=Crit. em Perigo ...)")
print("=" * 55)
print(f"Média:          {df_salve_am['categoria_num'].mean():.2f}")
print(f"Mediana:        {df_salve_am['categoria_num'].median():.2f}")
print(f"Desvio Padrão:  {df_salve_am['categoria_num'].std():.2f}")
print()
print("Contagem por grupo e categoria:")
print(df_salve_am.groupby(["grupo", "categoria"]).size().to_string())
print("=" * 55)

# ── GRÁFICO DE BARRA — BANCO SALVE ───────────────────────────────
contagem_salve = (
    df_salve_am.groupby(["grupo", "categoria"])
    .size()
    .reset_index(name="quantidade")
)

cores_grupo = {
    "Répteis":         "#52b788",
    "Tubarões e Raias": "#1e6091",
}

fig, ax = plt.subplots(figsize=(11, 6))

grupos = contagem_salve["grupo"].unique()
categorias_plot = [c for c in ordem_cat_salve
                   if c in contagem_salve["categoria"].values]
x = range(len(categorias_plot))
largura = 0.35

for i, grupo in enumerate(grupos):
    dados_grupo = []
    for cat in categorias_plot:
        val = contagem_salve[
            (contagem_salve["grupo"] == grupo) &
            (contagem_salve["categoria"] == cat)
        ]["quantidade"].sum()
        dados_grupo.append(val)

    offset = (i - 0.5) * largura
    bars = ax.bar(
        [xi + offset for xi in x],
        dados_grupo,
        width=largura,
        label=grupo,
        color=cores_grupo[grupo],
        edgecolor="white",
    )
    for bar in bars:
        if bar.get_height() > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                str(int(bar.get_height())),
                ha="center", va="bottom", fontsize=9, fontweight="bold"
            )

ax.set_title(
    "Répteis e Tubarões/Raias Ameaçados por Categoria\n(Base SALVE/ICMBio)",
    fontsize=13, fontweight="bold", pad=15
)
ax.set_xlabel("Categoria de Ameaça", fontsize=12)
ax.set_ylabel("Número de Espécies", fontsize=12)
ax.set_xticks(list(x))
ax.set_xticklabels(categorias_plot, rotation=15, ha="right", fontsize=10)
ax.legend(fontsize=11)
ax.grid(axis="y", linestyle="--", alpha=0.5)
sns.despine()

plt.tight_layout()
plt.show()