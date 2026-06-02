import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

# ======================================================
# CONFIGURAÇÃO INICIAL
# ======================================================
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

ARQ_2014 = '../br_mma_extincao_fauna_ameacada.csv'
ARQ_2026 = '../salve-publico-exportacao-fichas-planilha12-05-2026-15-56-40 (1).csv'

# ======================================================
# ESTILO GLOBAL DOS GRÁFICOS
# ======================================================
def configurar_estilo():
    sns.set_theme(
        style="whitegrid",
        palette="pastel",
        rc={
            "axes.facecolor": "#FAF9F6",
            "figure.facecolor": "#F5F5F0",
            "grid.color": "#EAEAEA",
            "text.color": "#4A4A4A",
            "axes.labelcolor": "#4A4A4A",
            "xtick.color": "#4A4A4A",
            "ytick.color": "#4A4A4A",
            "axes.titleweight": "bold",
            "axes.titlesize": 14,
            "font.size": 11
        }
    )

# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================
def carregar_bancos():
    df2022 = pd.read_csv(ARQ_2014)
    df2026 = pd.read_csv(ARQ_2026)
    return df2022, df2026

def salvar_e_exibir(nome_arquivo=None):
    plt.tight_layout()
    if nome_arquivo:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

def ajustar_rotulos_eixo_x():
    ax = plt.gca()
    labels = ax.get_xticklabels()
    quantidade = len(labels)
    if quantidade <= 5:
        angulo = 0
    elif quantidade <= 8:
        angulo = 30
    elif quantidade <= 12:
        angulo = 45
    else:
        angulo = 60
    plt.setp(
        labels,
        rotation=angulo,
        ha='right'
    )
    plt.tight_layout()

# ======================================================
# FUNÇÕES DE GRÁFICOS
# ======================================================
def grafico_dispersao(df, x, y, titulo, arquivo=None, hue=None):
    plt.figure(figsize=(10, 6))
    x_num = range(len(df))
    sns.regplot(
        x=list(x_num),
        y=df[y],
        scatter=True,
        ci=None,
        scatter_kws={
            "s": 120,
            "edgecolor": "#5D6D7E",
            "alpha": 0.8
        },
        line_kws={
            "color": "#E74C3C",
            "linewidth": 3
        }
    )
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel(x.replace('_', ' ').title(), fontweight='bold')
    plt.ylabel(y.replace('_', ' ').title(), fontweight='bold')
    plt.xticks(
        ticks=list(x_num),
        labels=df[x]
    )
    ajustar_rotulos_eixo_x()
    salvar_e_exibir(arquivo)

def grafico_barras(df, x, y, titulo, arquivo=None, cor="#FFD1BA"):
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df,
        x=x,
        y=y,
        color=cor,
        edgecolor="#D4A38D"
    )
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel(x.replace('_', ' ').title(), fontweight='bold')
    plt.ylabel(y.replace('_', ' ').title(), fontweight='bold')
    ajustar_rotulos_eixo_x()
    salvar_e_exibir(arquivo)

def grafico_pizza(serie, titulo, arquivo=None):
    total = serie.sum()
    if total == 0:
        print(f"Aviso: Sem dados para gerar o gráfico de pizza '{titulo}'.")
        return
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, _ = ax.pie(
        serie,
        startangle=90
    )
    legendas = [
        f"{categoria} ({valor} - {valor/total*100:.1f}%)"
        for categoria, valor in serie.items()
    ]
    quantidade = len(serie)
    if quantidade <= 4:
        colunas = 1
    elif quantidade <= 8:
        colunas = 2
    else:
        colunas = 3
    ax.legend(
        wedges,
        legendas,
        title="Categorias",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=colunas
    )
    ax.set_title(
        titulo,
        fontsize=14,
        fontweight='bold'
    )
    salvar_e_exibir(arquivo)

def grafico_histograma(df, coluna, titulo, arquivo=None, cor="#C1E1C1"):
    plt.figure(figsize=(10, 5))
    sns.histplot(
        data=df,
        x=coluna,
        bins=10,
        color=cor,
        edgecolor="#9EB89E"
    )
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel(coluna.replace('_', ' ').title(), fontweight='bold')
    plt.ylabel('Frequência', fontweight='bold')
    salvar_e_exibir(arquivo)

def grafico_countplot(df, coluna, titulo, arquivo=None, cor="#FFD1BA"):
    plt.figure(figsize=(10, 5))
    sns.countplot(
        data=df,
        x=coluna,
        color=cor,
        edgecolor="#D4A38D"
    )
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel(coluna.replace('_', ' ').title(), fontweight='bold')
    plt.ylabel('Quantidade', fontweight='bold')
    ajustar_rotulos_eixo_x()
    salvar_e_exibir(arquivo)

def grafico_histograma_repteis_mma(df_mma_rep, ordem_cat_mma, arquivo=None):
    cores_mma = {
        "VU":      "#f9c74f",
        "EN":      "#f77f00",
        "CR":      "#d62828",
        "CR (PEX)":"#7b2d8b",
        "EX":      "#000000",
        "RE":      "#888888",
        "EW":      "#aaaaaa",
    }
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
    ax.set_xlabel("Categoria de Ameaça", fontsize=12, fontweight="bold")
    ax.set_ylabel("Número de Espécies", fontsize=12, fontweight="bold")
    if not contagem_mma["quantidade"].empty:
        ax.set_ylim(0, contagem_mma["quantidade"].max() + 8)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    sns.despine()
    salvar_e_exibir(arquivo)

def grafico_barras_salve_individual(df_salve_am, grupo, ordem_cat_salve, cor, arquivo=None):
    dados_grupo = df_salve_am[df_salve_am["grupo"] == grupo]
    contagem = (
        dados_grupo["categoria"]
        .value_counts()
        .reindex(ordem_cat_salve)
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    contagem.columns = ["categoria", "quantidade"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(
        contagem["categoria"],
        contagem["quantidade"],
        color=cor,
        edgecolor="white",
        width=0.5
    )
    for bar in bars:
        if bar.get_height() > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                str(int(bar.get_height())),
                ha="center", va="bottom", fontsize=10, fontweight="bold"
            )
    ax.set_title(
        f"Espécies Ameaçadas por Categoria: {grupo}\n(Base SALVE/ICMBio)",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.set_xlabel("Categoria de Ameaça", fontsize=12, fontweight="bold")
    ax.set_ylabel("Número de Espécies", fontsize=12, fontweight="bold")
    if not contagem["quantidade"].empty:
        ax.set_ylim(0, contagem["quantidade"].max() + 5)
    ax.set_xticklabels(ordem_cat_salve, rotation=15, ha="right", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    sns.despine()
    salvar_e_exibir(arquivo)

# --- NOVAS FUNÇÕES DE GRÁFICOS ADICIONADAS / CORRIGIDAS ---
def grafico_countplot_historico_grupo(df, grupo, titulo, arquivo=None, cor="#FFD1BA", cor_borda="#D4A38D"):
    plt.figure(figsize=(10, 5))
    dados_filtrados = df[df['grupo'] == grupo]
    sns.countplot(
        data=dados_filtrados, 
        x='ano_avaliacao', 
        color=cor, 
        edgecolor=cor_borda
    )
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel('Ano da Avaliação', fontweight='bold')
    plt.ylabel('Quantidade de Espécies', fontweight='bold')
    ajustar_rotulos_eixo_x()
    salvar_e_exibir(arquivo)

def grafico_stripplot_individual(df, grupo, titulo, cor_paleta, arquivo=None):
    plt.figure(figsize=(10, 6))
    dados_filtrados = df[df['grupo'] == grupo]
    sns.stripplot(
        data=dados_filtrados, 
        x='status', 
        y='ano_avaliacao',
        hue='status', 
        jitter=0.4, 
        size=10, 
        alpha=0.7, 
        palette=cor_paleta, 
        legend=False,
        edgecolor='#8C8C8C',
        linewidth=0.5
    )
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel('Status de Extinção', fontsize=12, fontweight='bold')
    plt.ylabel('Ano de Avaliação', fontsize=12, fontweight='bold')
    ajustar_rotulos_eixo_x()
    salvar_e_exibir(arquivo)

# ======================================================
# PREPARAÇÃO DOS DADOS
# ======================================================
def preparar_dados(df2022, df2026):
    dados = pd.concat([df2022, df2026], ignore_index=True)
    anfibios = dados[dados['grupo'] == 'Anfíbios']
    aves = dados[dados['grupo'] == 'Aves']
    contagem_anfibios = (
        anfibios['categoria']
        .value_counts()
        .reset_index()
    )
    contagem_anfibios.columns = ['categoria', 'quantidade']
    contagem_aves = (
        aves['categoria']
        .value_counts()
        .reset_index()
    )
    contagem_aves.columns = ['categoria', 'quantidade']
    return {
        'dados': dados,
        'anfibios': anfibios,
        'aves': aves,
        'contagem_anfibios': contagem_anfibios,
        'contagem_aves': contagem_aves
    }

def preparar_dados_peixes(df2022, df2026):
    peixes_continentais_2022 = df2022[
        df2022["grupo"] == "Peixes Continentais"
    ].copy()
    peixes_marinhos_2022 = df2022[
        df2022["grupo"] == "Peixes Marinhos (Ósseos)"
    ].copy()
    peixes_osseos_2026 = df2026[
        df2026["classe"] == "Actinopterygii"
    ]
    biomas_continentais = [
        "Amazônia", "Pantanal", "Mata Atlântica", "Caatinga", "Cerrado", "Pampa"
    ]
    peixes_continentais_2026 = peixes_osseos_2026[
        peixes_osseos_2026["bioma"]
        .str.contains("|".join(biomas_continentais), na=False)
    ]
    peixes_marinhos_2026 = peixes_osseos_2026[
        peixes_osseos_2026["bioma"]
        .str.contains("Sistema Costeiro-Marinho", na=False)
    ]
    peixes_continentais_2022["lista_2014"] = pd.to_numeric(
        peixes_continentais_2022["lista_2014"],
        errors="coerce"
    )
    peixes_marinhos_2022["lista_2014"] = pd.to_numeric(
        peixes_marinhos_2022["lista_2014"],
        errors="coerce"
    )
    peixes_continentais_2026["consta_em_lista_nacional_oficial"] = (
        peixes_continentais_2026["consta_em_lista_nacional_oficial"]
        .map({
            "Sim": 1, "Não": 0, "True": 1, "False": 0, 1: 1, 0: 0
        })
    )
    peixes_marinhos_2026["consta_em_lista_nacional_oficial"] = (
        peixes_marinhos_2026["consta_em_lista_nacional_oficial"]
        .map({
            "Sim": 1, "Não": 0, "True": 1, "False": 0, 1: 1, 0: 0
        })
    )
    return {
        'continentais_2022': peixes_continentais_2022,
        'continentais_2026': peixes_continentais_2026,
        'marinhos_2022': peixes_marinhos_2022,
        'marinhos_2026': peixes_marinhos_2026
    }

def preparar_dados_invertebrados(df2026):
    filtro = df2026["grupo"].isin([
        "Invertebrados de Água Doce",
        "Invertebrados Marinhos"
    ])
    dados_invertebrados = df2026[filtro].copy()
    dados_invertebrados["ano"] = (
        dados_invertebrados["mesano_avaliacao"]
        .astype(str)
        .str.extract(r'(\d{4})')
    )
    dados_invertebrados["ano"] = pd.to_numeric(
        dados_invertebrados["ano"],
        errors="coerce"
    )
    return dados_invertebrados

def preparar_dados_repteis_tubaroes(df2022, df2026):
    df_mma_rep = df2022[df2022["grupo"].astype(str).str.lower().str.strip() == "repteis"].copy()
    ordem_cat_mma = ["VU", "EN", "CR", "CR (PEX)", "EX", "RE", "EW"]
    df_mma_rep["categoria_num"] = df_mma_rep["categoria"].map(
        {c: i + 1 for i, c in enumerate(ordem_cat_mma)}
    )
    
    grupos_salve = ["Répteis", "Tubarões e Raias"]
    df_salve_g = df2026[df2026["grupo"].isin(grupos_salve)].copy()
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
    return {
        'mma_rep': df_mma_rep,
        'salve_am': df_salve_am,
        'ordem_cat_mma': ordem_cat_mma,
        'ordem_cat_salve': ordem_cat_salve
    }

def preparar_dados_mamiferos_invertebrados(df2022, df2026):
    df1 = df2022.copy()
    if 'especie_ou_subespecie' in df1.columns:
        df1 = df1.rename(columns={'especie_ou_subespecie': 'especie'}) 
    
    df1['nome_comum'] = 'Desconhecido' 
    df1['ano_avaliacao'] = '2014'
    
    df2 = df2026.copy()
    if 'mesano_avaliacao' in df2.columns:
        df2['ano_avaliacao'] = df2['mesano_avaliacao'].astype(str).str.split('/').str[-1]
    else:
        df2['ano_avaliacao'] = '2026'
        
    if 'nome_comum' not in df2.columns:
        df2['nome_comum'] = 'Desconhecido'
    
    colunas_finais = ['grupo', 'categoria', 'especie', 'nome_comum', 'ano_avaliacao']
    for col in colunas_finais:
        if col not in df1.columns: df1[col] = 'Desconhecido'
        if col not in df2.columns: df2[col] = 'Desconhecido'
    df_total = pd.concat([df1[colunas_finais], df2[colunas_finais]], ignore_index=True)
    
    df_total['grupo'] = df_total['grupo'].astype(str).str.lower().str.strip()
    mapa_grupos = {
        'mamiferos': 'Mamíferos', 'mamíferos': 'Mamíferos',
        'invertebrados_terrestres': 'Invertebrados Terrestres',
        'invertebrados terrestres': 'Invertebrados Terrestres'
    }
    df_ana = df_total[df_total['grupo'].isin(mapa_grupos.keys())].copy()
    df_ana['grupo'] = df_ana['grupo'].map(mapa_grupos)
    
    mapa_cat = {
        'VU': 'Vulnerável', 'EN': 'Em Perigo', 'CR': 'Criticamente em Perigo', 
        'CR (PEX)': 'Criticamente em Perigo', 'EX': 'Extinta', 'RE': 'Regionalmente Extinta', 
        'EW': 'Extinta na Natureza', 'LC': 'Menos Preocupante', 'NT': 'Quase Ameaçada', 
        'DD': 'Dados Insuficientes', 'Vulnerável': 'Vulnerável', 'Em Perigo': 'Em Perigo',
        'Criticamente em Perigo': 'Criticamente em Perigo', 'Extinta': 'Extinta'
    }
    df_ana['status'] = df_ana['categoria'].replace(mapa_cat).str.strip()
    
    ordem_risco = ['Menos Preocupante', 'Quase Ameaçada', 'Dados Insuficientes', 
                   'Vulnerável', 'Em Perigo', 'Criticamente em Perigo', 'Extinta']
    df_ana['status'] = pd.Categorical(df_ana['status'], categories=ordem_risco, ordered=True)
    
    return df_ana[df_ana['ano_avaliacao'].str.isnumeric() == True].sort_values('ano_avaliacao')

# ======================================================
# ESTATÍSTICAS
# ======================================================
def mostrar_estatisticas(nome, coluna):
    print("\n" + "=" * 55)
    print(f"ESTATÍSTICAS — {nome}")
    print("=" * 55)
    if not coluna.empty:
        print(f"Média: {coluna.mean():.2f}")
        print(f"Mediana: {coluna.median():.2f}")
        print(f"Desvio padrão: {coluna.std():.2f}")
    else:
        print("Sem dados estatísticos disponíveis.")

def mostrar_estatisticas_repteis_tubaroes(dados_rep_tub):
    df_mma_rep = dados_rep_tub['mma_rep']
    ordem_cat_mma = dados_rep_tub['ordem_cat_mma']
    df_salve_am = dados_rep_tub['salve_am']
    print("\n" + "=" * 55)
    print("ESTATÍSTICAS — Banco MMA | Grupo: Répteis")
    print("(1=VU, 2=EN, 3=CR, 4=CR(PEX), 5=EX, 6=RE, 7=EW)")
    print("=" * 55)
    if not df_mma_rep.empty:
        print(f"Média:          {df_mma_rep['categoria_num'].mean():.2f}")
        print(f"Mediana:        {df_mma_rep['categoria_num'].median():.2f}")
        print(f"Desvio Padrão:  {df_mma_rep['categoria_num'].std():.2f}")
        print("\nContagem por categoria:")
        print(df_mma_rep["categoria"].value_counts().reindex(ordem_cat_mma).dropna().astype(int))
    print("=" * 55)
    print("\n" + "=" * 55)
    print("ESTATÍSTICAS — Banco SALVE | Répteis + Tubarões e Raias")
    print("(1=Vulnerável, 2=Em Perigo, 3=Crit. em Perigo ...)")
    print("=" * 55)
    if not df_salve_am.empty:
        print(f"Média:          {df_salve_am['categoria_num'].mean():.2f}")
        print(f"Mediana:        {df_salve_am['categoria_num'].median():.2f}")
        print(f"Desvio Padrão:  {df_salve_am['categoria_num'].std():.2f}")
        print("\nContagem por grupo e categoria:")
        print(df_salve_am.groupby(["grupo", "categoria"]).size().to_string())
    print("=" * 55)

def mostrar_estatisticas_mamiferos_invertebrados(df_final):
    print("\n" + "=" * 55)
    print("        RELATÓRIO DE STATUS DE RISCO       ")
    print("=" * 55)
    print(df_final.groupby(['grupo', 'status'], observed=False).size().unstack().fillna(0))
    print("-" * 55)
    ameacadas_icmbio = ['Em Perigo', 'Criticamente em Perigo']
    print("Algumas espécies de Mamíferos em perigo:")
    lista_nomes_comuns = df_final[(df_final['grupo'] == 'Mamíferos') & 
                                   (df_final['status'].isin(ameacadas_icmbio)) & 
                                   (df_final['nome_comum'] != 'Desconhecido')]['nome_comum'].dropna().unique()
    for nome in lista_nomes_comuns[:5]: 
        print(f"- {nome}")
    print("=" * 55 + "\n")

# ======================================================
# EXECUÇÃO PRINCIPAL
# ======================================================
def main():
    configurar_estilo()
    try:
        df2022, df2026 = carregar_bancos()
    except Exception as erro:
        print(f"Erro ao carregar os arquivos: {erro}")
        sys.exit()

    # ==================================================
    # DADOS GERAIS (ANFÍBIOS E AVES)
    # ==================================================
    dados = preparar_dados(df2022, df2026)
    contagem_anfibios = dados['contagem_anfibios']
    contagem_aves = dados['contagem_aves']

    # GRÁFICOS — ANFÍBIOS
    grafico_dispersao(contagem_anfibios, 'categoria', 'quantidade', 'Dispersão - Anfíbios', 'dispersao_anfibios.png')
    grafico_barras(contagem_anfibios, 'categoria', 'quantidade', 'Barra - Anfíbios', 'barra_anfibios.png')
    grafico_pizza(contagem_anfibios.set_index('categoria')['quantidade'], 'Pizza - Anfíbios', 'pizza_anfibios.png')

    # GRÁFICOS — AVES
    grafico_dispersao(contagem_aves, 'categoria', 'quantidade', 'Dispersão - Aves', 'dispersao_aves.png')
    grafico_barras(contagem_aves, 'categoria', 'quantidade', 'Barra - Aves', 'barra_aves.png')
    grafico_pizza(contagem_aves.set_index('categoria')['quantidade'], 'Pizza - Aves', 'pizza_aves.png')

    # ==================================================
    # PEIXES
    # ==================================================
    peixes = preparar_dados_peixes(df2022, df2026)
    grafico_histograma(peixes['continentais_2022'], 'lista_2014', 'Histograma - Peixes Continentais (2022)')
    grafico_histograma(peixes['marinhos_2022'], 'lista_2014', 'Histograma - Peixes Marinhos (2022)', cor="#A7D8F0")
    grafico_histograma(peixes['continentais_2026'], 'consta_em_lista_nacional_oficial', 'Histograma - Peixes Continentais (2026)', 'histograma_peixes_continentais_2026.png', cor="#C1E1C1")
    grafico_histograma(peixes['marinhos_2026'], 'consta_em_lista_nacional_oficial', 'Histograma - Peixes Marinhos (2026)', 'histograma_peixes_marinhos_2026.png', cor="#A7D8F0")
    
    grafico_pizza(peixes['continentais_2022']['categoria'].value_counts(), 'Pizza - Peixes Continentais (2022)', 'pizza_peixes_continentais_2022.png')
    grafico_pizza(peixes['continentais_2026']['categoria'].value_counts(), 'Pizza - Peixes Continentais (2026)', 'pizza_peixes_continentais_2026.png')
    grafico_pizza(peixes['marinhos_2022']['categoria'].value_counts(), 'Pizza - Peixes Marinhos (2022)', 'pizza_peixes_marinhos_2022.png')
    grafico_pizza(peixes['marinhos_2026']['categoria'].value_counts(), 'Pizza - Peixes Marinhos (2026)', 'pizza_peixes_marinhos_2026.png')

    # ==================================================
    # INVERTEBRADOS AQUÁTICOS/MARINHOS
    # ==================================================
    dados_invertebrados = preparar_dados_invertebrados(df2026)
    plt.figure(figsize=(10, 6))
    sns.countplot(data=dados_invertebrados, x="categoria", hue="grupo", edgecolor="#D9D9D9")
    plt.title("Espécimes ameaçados por categoria", fontsize=14, fontweight='bold')
    plt.xlabel("Categoria de ameaça", fontweight='bold')
    plt.ylabel("Quantidade", fontweight='bold')
    ajustar_rotulos_eixo_x()
    salvar_e_exibir('countplot_invertebrados.png')

    # DISPERSÃO — INVERTEBRADOS
    mapa_categoria = {"Vulnerável": 1, "Em Perigo": 2, "Criticamente em Perigo": 3, "Regionalmente Extinta": 4, "Extinta na Natureza": 5, "Extinta": 6}
    dados_invertebrados["categoria_num"] = dados_invertebrados["categoria"].map(mapa_categoria)
    plt.figure(figsize=(12, 6))
    sns.regplot(data=dados_invertebrados, x="ano", y="categoria_num", scatter=True, ci=None, scatter_kws={"s": 100, "alpha": 0.8, "edgecolor": "#5D6D7E"}, line_kws={"color": "#E74C3C", "linewidth": 3})
    plt.title("Avaliações de Espécies Ameaçadas", fontsize=14, fontweight='bold')
    plt.xlabel("Ano da Avaliação", fontweight='bold')
    plt.ylabel("Categoria", fontweight='bold')
    plt.yticks([1, 2, 3, 4, 5, 6], ["Vulnerável", "Em Perigo", "Criticamente em Perigo", "Regionalmente Extinta", "Extinta na Natureza", "Extinta"])
    ajustar_rotulos_eixo_x()
    salvar_e_exibir('dispersao_invertebrados.png')

    # PIZZA — INVERTEBRADOS AQUÁTICOS
    quantidade_grupos = dados_invertebrados["grupo"].value_counts()
    grafico_pizza(quantidade_grupos, "Distribuição de Invertebrados", "pizza_invertebrados.png")

    # ==================================================
    # RÉPTEIS E TUBARÕES / RAIAS (CORRIGIDO)
    # ==================================================
    dados_rep_tub = preparar_dados_repteis_tubaroes(df2022, df2026)
    
    # Histograma base MMA para Répteis
    grafico_histograma_repteis_mma(dados_rep_tub['mma_rep'], dados_rep_tub['ordem_cat_mma'], 'histograma_repteis_mma.png')
    
    # SEPARAÇÃO: Gráficos de barras individuais para base SALVE
    grafico_barras_salve_individual(dados_rep_tub['salve_am'], "Répteis", dados_rep_tub['ordem_cat_salve'], "#52b788", 'barras_repteis_salve.png')
    grafico_barras_salve_individual(dados_rep_tub['salve_am'], "Tubarões e Raias", dados_rep_tub['ordem_cat_salve'], "#1e6091", 'barras_tubaroes_salve.png')

    # CRIAÇÃO: Gráficos de Pizza individuais (Base SALVE)
    df_salve_repteis = dados_rep_tub['salve_am'][dados_rep_tub['salve_am']['grupo'] == 'Répteis']
    df_salve_tubaroes = dados_rep_tub['salve_am'][dados_rep_tub['salve_am']['grupo'] == 'Tubarões e Raias']
    
    grafico_pizza(df_salve_repteis['categoria'].value_counts(), "Distribuição por Categoria - Répteis (SALVE)", "pizza_repteis_salve.png")
    grafico_pizza(df_salve_tubaroes['categoria'].value_counts(), "Distribuição por Categoria - Tubarões/Raias (SALVE)", "pizza_tubaroes_salve.png")

    # CRIAÇÃO: Gráficos de Dispersão para Répteis e Tubarões/Raias
    contagem_disp_rep = df_salve_repteis['categoria'].value_counts().reindex(dados_rep_tub['ordem_cat_salve']).fillna(0).reset_index()
    contagem_disp_rep.columns = ['categoria', 'quantidade']
    grafico_dispersao(contagem_disp_rep, 'categoria', 'quantidade', 'Dispersão - Répteis (SALVE)', 'dispersao_repteis_salve.png')

    contagem_disp_tub = df_salve_tubaroes['categoria'].value_counts().reindex(dados_rep_tub['ordem_cat_salve']).fillna(0).reset_index()
    contagem_disp_tub.columns = ['categoria', 'quantidade']
    grafico_dispersao(contagem_disp_tub, 'categoria', 'quantidade', 'Dispersão - Tubarões e Raias (SALVE)', 'dispersao_tubaroes_salve.png')

    # ==================================================
    # INTEGRADO: MAMÍFEROS E INVERTEBRADOS TERRESTRES (CORRIGIDO)
    # ==================================================
    df_final_mam_inv = preparar_dados_mamiferos_invertebrados(df2022, df2026)
    
    # Gráficos de Histórico Temporal
    grafico_countplot_historico_grupo(df_final_mam_inv, 'Mamíferos', 'HISTOGRAMA: Mamíferos por Ano', 'ritograma_mamiferos.png', cor='#FFD1BA', cor_borda='#D4A38D')
    grafico_countplot_historico_grupo(df_final_mam_inv, 'Invertebrados Terrestres', 'HISTOGRAMA: Invertebrados Terrestres por Ano', 'ritograma_invertebrados.png', cor='#C1E1C1', cor_borda='#9EB89E')
    
    # SEPARAÇÃO: Gráficos de Dispersão individuais (Substituindo o Unificado)
    grafico_stripplot_individual(df_final_mam_inv, 'Mamíferos', 'DISPERSÃO: Categorias de Risco — Mamíferos', 'Oranges', 'dispersao_mamiferos.png')
    grafico_stripplot_individual(df_final_mam_inv, 'Invertebrados Terrestres', 'DISPERSÃO: Categorias de Risco — Invertebrados Terrestres', 'Greens', 'dispersao_invertebrados_terrestres.png')

    # CRIAÇÃO: Gráficos de Pizza individuais para Mamíferos e Invertebrados Terrestres
    df_mamiferos_pizza = df_final_mam_inv[df_final_mam_inv['grupo'] == 'Mamíferos']
    df_inv_terr_pizza = df_final_mam_inv[df_final_mam_inv['grupo'] == 'Invertebrados Terrestres']

    grafico_pizza(df_mamiferos_pizza['status'].value_counts(), "Distribuição de Status — Mamíferos", "pizza_mamiferos.png")
    grafico_pizza(df_inv_terr_pizza['status'].value_counts(), "Distribuição de Status — Invertebrados Terrestres", "pizza_invertebrados_terrestres.png")

    # ==================================================
    # IMPRESSÃO DE ESTATÍSTICAS E RELATÓRIOS
    # ==================================================
    mostrar_estatisticas("Peixes Continentais (2022)", peixes['continentais_2022']['lista_2014'])
    mostrar_estatisticas("Peixes Marinhos (2022)", peixes['marinhos_2022']['lista_2014'])
    mostrar_estatisticas_repteis_tubaroes(dados_rep_tub)
    
    # Relatório terminal de Mamíferos e Invertebrados Terrestres
    mostrar_estatisticas_mamiferos_invertebrados(df_final_mam_inv)

# ======================================================
# EXECUTAR SISTEMA
# ======================================================
if __name__ == '__main__':
    main()