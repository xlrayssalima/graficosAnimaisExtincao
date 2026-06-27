import pandas as pd
import numpy as np
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# Configuração dos nomes dos arquivos
ARQ_MMA = 'br_mma_extincao_fauna_ameacada.csv'
ARQ_SALVE = 'salve-publico-exportacao-fichas-planilha12-05-2026-15-56-40 (1).csv'

def tratar_e_mesclar_dados():
    print("Iniciando o tratamento dos dados...")
    
    # 1. Carregar as bases
    if not os.path.exists(ARQ_MMA):
        raise FileNotFoundError(f"Arquivo do MMA não encontrado: {ARQ_MMA}")
    if not os.path.exists(ARQ_SALVE):
        raise FileNotFoundError(f"Arquivo do SALVE não encontrado: {ARQ_SALVE}")
        
    df_mma = pd.read_csv(ARQ_MMA, encoding='utf-8')
    df_salve = pd.read_csv(ARQ_SALVE, encoding='utf-8')

    
    # 2. Normalizar nomes científicos das espécies
    df_mma['especie_limpa'] = df_mma['especie_ou_subespecie'].astype(str).str.strip().str.lower()
    df_salve['especie_limpa'] = df_salve['especie'].astype(str).str.strip().str.lower()
    
    # 3. Remover duplicatas preservando a informação mais relevante
    # Para o MMA, se houver duplicatas de espécies, vamos manter a primeira ocorrência
    df_mma = df_mma.drop_duplicates(subset=['especie_limpa'])
    # Para o SALVE, removemos duplicatas
    df_salve = df_salve.drop_duplicates(subset=['especie_limpa'])
    
    # 4. Mesclar as duas bases com um Left Join no SALVE
    # Isso garante que mantemos todas as espécies analisadas recentemente (2026) com seus detalhes
    df_merged = pd.merge(df_salve, df_mma[['especie_limpa', 'categoria', 'lista_2014']], 
                          on='especie_limpa', how='left', suffixes=('_salve', '_mma'))
    
    # 5. Renomear e Padronizar Colunas de Categoria
    df_merged.rename(columns={
        'categoria_salve': 'categoria_2026',
        'categoria_mma': 'categoria_2014'
    }, inplace=True)
    
    # Mapeamento para códigos unificados da IUCN
    map_categorias_salve = {
        'Criticamente em Perigo': 'CR',
        'Em Perigo': 'EN',
        'Vulnerável': 'VU',
        'Quase Ameaçada': 'NT',
        'Menos Preocupante': 'LC',
        'Dados Insuficientes': 'DD',
        'Extinta': 'EX',
        'Regionalmente Extinta': 'RE',
        'Extinta na Natureza': 'EW',
        'Não Aplicável': 'NA'
    }
    
    map_categorias_mma = {
        'CR': 'CR',
        'CR (PEX)': 'CR',
        'EN': 'EN',
        'VU': 'VU',
        'EX': 'EX',
        'RE': 'RE',
        'EW': 'EW'
    }
    
    df_merged['status_2026'] = df_merged['categoria_2026'].map(map_categorias_salve).fillna('NE')
    df_merged['status_2014'] = df_merged['categoria_2014'].map(map_categorias_mma).fillna('NE')
    
    # 6. Tratar Valores Ausentes e Padronizar Características
    # Preencher vazios em colunas importantes
    df_merged['nome_comum'] = df_merged['nome_comum'].fillna('Não Informado').astype(str).str.strip()
    df_merged['bioma'] = df_merged['bioma'].fillna('Desconhecido').astype(str).str.strip()
    df_merged['regiao'] = df_merged['regiao'].fillna('Desconhecido').astype(str).str.strip()
    df_merged['estado'] = df_merged['estado'].fillna('Desconhecido').astype(str).str.strip()
    
    df_merged['endemica_brasil'] = df_merged['endemica_brasil'].fillna('Desconhecido').astype(str).str.strip()
    df_merged['migratoria'] = df_merged['migratoria'].fillna('Desconhecido').astype(str).str.strip()
    df_merged['tendencia_populacional'] = df_merged['tendencia_populacional'].fillna('Desconhecido').astype(str).str.strip()
    
    # 7. Criar base de dados geral tratada (para uso do modelo preditivo)
    # Primeiro salvamos a base completa de Aves e todas as outras classes tratada
    os.makedirs('data', exist_ok=True)
    df_merged.to_csv('data/fauna_geral_tratada.csv', index=False, encoding='utf-8')
    print(f"Salva base de dados geral tratada com {len(df_merged)} registros.")
    
    # 8. Filtrar apenas espécies Criticamente em Perigo (CR) em 2026 para os gráficos e uso da equipe
    df_cr = df_merged[df_merged['status_2026'] == 'CR'].copy()
    
    # Salvar base filtrada de CR para toda a equipe utilizar
    df_cr.to_csv('data/fauna_cr_consolidada.csv', index=False, encoding='utf-8')
    print(f"Salva base consolidada de espécies CR com {len(df_cr)} registros em data/fauna_cr_consolidada.csv.")
    
    # Exibir um resumo dos grupos na base CR
    print("\nResumo das espécies CR por grupo taxonômico:")
    print(df_cr['grupo'].value_counts())

if __name__ == '__main__':
    tratar_e_mesclar_dados()
