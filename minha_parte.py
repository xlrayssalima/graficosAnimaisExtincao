import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

# --- 1. CONFIGURAÇÃO DE DIRETÓRIO ---
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

arq_2014 = 'br_mma_extincao_fauna_ameacada.csv'
arq_atual = 'salve-publico-exportacao-fichas-planilha12-05-2026-15-56-40.csv'

def preparar_dados_completos():
    df1 = pd.read_csv(arq_2014)
    if 'especie_ou_subespecie' in df1.columns:
        df1 = df1.rename(columns={'especie_ou_subespecie': 'especie'}) 
    df1['nome_comum'] = 'Desconhecido' 
    df1['ano_avaliacao'] = '2014'
    
    df2 = pd.read_csv(arq_atual)
    df2['ano_avaliacao'] = df2['mesano_avaliacao'].astype(str).str.split('/').str[-1]
    
    df_total = pd.concat([df1[['grupo', 'categoria', 'especie', 'nome_comum', 'ano_avaliacao']], 
                          df2[['grupo', 'categoria', 'especie', 'nome_comum', 'ano_avaliacao']]], 
                         ignore_index=True)
    
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
        'DD': 'Dados Insuficientes'
    }
    df_ana['status'] = df_ana['categoria'].replace(mapa_cat).str.strip()
    
    ordem_risco = ['Menos Preocupante', 'Quase Ameaçada', 'Dados Insuficientes', 
                   'Vulnerável', 'Em Perigo', 'Criticamente em Perigo', 'Extinta']
    df_ana['status'] = pd.Categorical(df_ana['status'], categories=ordem_risco, ordered=True)
    
    return df_ana[df_ana['ano_avaliacao'].str.isnumeric() == True].sort_values('ano_avaliacao')

try:
    df_final = preparar_dados_completos()
except Exception as e:
    print(f"\nERRO: {e}")
    sys.exit()

sns.set_theme(style="whitegrid", rc={
    "axes.facecolor": "#FAF9F6",   
    "figure.facecolor": "#F5F5F0", 
    "grid.color": "#EAEAEA",       
    "text.color": "#4A4A4A",       
    "axes.labelcolor": "#4A4A4A",  
    "xtick.color": "#4A4A4A",      
    "ytick.color": "#4A4A4A"       
})

# --- GRÁFICO 1: RITOGRAMA MAMÍFEROS ---
plt.figure(figsize=(10, 5))
sns.countplot(data=df_final[df_final['grupo'] == 'Mamíferos'], x='ano_avaliacao', color='#FFD1BA', edgecolor='#D4A38D')
plt.title('HISTOGRAMA: Mamíferos por Ano', fontsize=14, fontweight='bold')
plt.xlabel('Ano da Avaliação', fontweight='bold')
plt.ylabel('Quantidade de Espécies', fontweight='bold')
plt.tight_layout()
plt.show()

# --- GRÁFICO 2: RITOGRAMA INVERTEBRADOS ---
plt.figure(figsize=(10, 5))
sns.countplot(data=df_final[df_final['grupo'] == 'Invertebrados Terrestres'], x='ano_avaliacao', color='#C1E1C1', edgecolor='#9EB89E')
plt.title('HISTOGRAMA: Invertebrados Terrestres por Ano', fontsize=14, fontweight='bold')
plt.xlabel('Ano da Avaliação', fontweight='bold')
plt.ylabel('Quantidade de Espécies', fontweight='bold')
plt.tight_layout()
plt.show()

# --- GRÁFICO 3: DISPERSÃO UNIFICADA ---
plt.figure(figsize=(12, 7))
sns.stripplot(
    data=df_final, 
    x='grupo', 
    y='status', 
    order=['Mamíferos', 'Invertebrados Terrestres'], 
    hue='status', 
    jitter=0.4, 
    size=10, 
    alpha=0.7, 
    palette='Set2', 
    legend=False,
    edgecolor='#8C8C8C',
    linewidth=0.5
)

plt.title('DISPERSÃO: Categorias de Risco por Grupo', fontsize=15, fontweight='bold')
plt.xlabel('Grupos Analisados', fontsize=12, fontweight='bold')
plt.ylabel('Status de Extinção', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()

# --- MÉTRICAS NO TERMINAL ---
print("\n" + "=" * 55)
print("       RELATÓRIO DE STATUS DE RISCO       ")
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