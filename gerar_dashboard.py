import pandas as pd
import json
import os

ARQ1 = 'br_mma_extincao_fauna_ameacada.csv'
ARQ2 = 'salve-publico-exportacao-fichas-planilha12-05-2026-15-56-40 (1).csv'

df1 = pd.read_csv(ARQ1)
df2 = pd.read_csv(ARQ2)

especies_risco = {}

# Lista oficial de categorias de risco aceitáveis
CATEGORIAS_VALIDAS = [
    "Criticamente em Perigo", "Em Perigo", "Vulnerável", 
    "Quase Ameaçada", "Menos Preocupante", "Dados Insuficientes",
    "Extinta", "Extinta na Natureza", "Regionalmente Extinta", "Não Aplicável"
]

def extrair_risco_valido(row):
    """Varre todas as células da linha procurando uma categoria de risco válida"""
    for val in row.dropna().astype(str):
        val_cleaned = val.strip()
        # Busca por correspondência exata na lista oficial
        for cat in CATEGORIAS_VALIDAS:
            if cat.lower() == val_cleaned.lower():
                return cat
    return None

# 1. Processar o arquivo do SALVE (ICMBio)
col_esp_df2 = [c for c in df2.columns if c.lower() == 'especie']
if col_esp_df2:
    esp_col = col_esp_df2[0]
    for _, row in df2.dropna(subset=[esp_col]).iterrows():
        nome_sp = str(row[esp_col]).strip()
        if nome_sp and len(nome_sp) > 3:
            risco = extrair_risco_valido(row)
            if risco:
                especies_risco[nome_sp] = risco

# 2. Processar o arquivo do MMA (Complementar)
col_esp_df1 = df1.columns[0]
for _, row in df1.dropna(subset=[col_esp_df1]).iterrows():
    nome_sp = str(row[col_esp_df1]).strip()
    if nome_sp and len(nome_sp) > 3:
        # Verifica se já não foi mapeada de forma case-insensitive
        match_existe = any(ex.lower() == nome_sp.lower() for ex in especies_risco.keys())
        if not match_existe:
            risco = extrair_risco_valido(row)
            especies_risco[nome_sp] = risco if risco else "Ameaçada"

# Limpeza final de chaves que possam ser ruídos de cabeçalho
chaves_invalidas = ['especie', 'anfibios', 'repteis', 'aves', 'mamiferos', 'peixes', 'invertebrados']
for ci in chaves_invalidas:
    especies_risco.pop(ci, None)

lista_especies = sorted(list(especies_risco.keys()))
lista_categorias = sorted(list(set(especies_risco.values())))

dados = {
    'total_especies': len(lista_especies),
    'total_grupos': int(df2['grupo'].nunique()) if 'grupo' in df2.columns else 7,
    'total_categorias': len(lista_categorias),
    'categorias': lista_categorias,
    'especies_risco': especies_risco,
    'especies': lista_especies
}

os.makedirs('data', exist_ok=True)
with open('data/dashboard.json', 'w', encoding='utf8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print(f"Sucesso! {len(lista_especies)} espécies mapeadas com tratamento rigoroso de categorias.")