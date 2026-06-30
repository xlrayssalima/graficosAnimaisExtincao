import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# Garantir que as pastas de saída existam no padrão da equipe
os.makedirs('graficos/p4_cr', exist_ok=True)
os.makedirs('data', exist_ok=True)

def carregar_dados():
    caminho = 'data/fauna_geral_tratada.csv'
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Base de dados '{caminho}' não encontrada. Verifique os arquivos na pasta data.")
    return pd.read_csv(caminho)

def gerar_graficos_p4_cr(df_p4):
    print("[P4] Gerando gráficos otimizados para a apresentação...")
    df_cr = df_p4[df_p4['status_2026'] == 'CR'].copy()
    
    if df_cr.empty:
        print("[P4] Aviso: Nenhuma espécie CR encontrada para estes grupos.")
        return
    
    # --- CONFIGURAÇÃO DE ESTILO PREMIUM ---
    sns.set_theme(style="white")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.facecolor'] = '#FAF9F6'
    plt.rcParams['axes.facecolor'] = '#FAF9F6'
    
    df_anfibios_cr = df_cr[df_cr['grupo'] == 'Anfíbios'].copy()
    df_invertebrados_cr = df_cr[df_cr['grupo'].str.contains('Invertebrados', na=False)].copy()

    # --- 1. Anfíbios por Bioma (Otimizado) ---
    if not df_anfibios_cr.empty:
        biomas_anf = []
        for b_set in df_anfibios_cr['bioma'].dropna():
            for b in b_set.split(','):
                biomas_f = b.strip()
                if biomas_f: biomas_anf.append(biomas_f)
        if biomas_anf:
            df_biomas_anf = pd.Series(biomas_anf).value_counts().reset_index()
            df_biomas_anf.columns = ['Bioma', 'Quantidade']
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=df_biomas_anf, x='Quantidade', y='Bioma', hue='Bioma', palette='crest', legend=False, ax=ax)
            ax.bar_label(ax.containers[0], padding=5, fontname='sans-serif', fontsize=10, fontweight='bold', color='#333333')
            plt.title('Anfíbios em Risco Crítico (CR) por Bioma', fontsize=14, fontweight='bold', pad=15, color='#111111')
            plt.xlabel('Número de Espécies', fontsize=11, labelpad=10)
            plt.ylabel('')
            sns.despine(left=True, bottom=True)
            plt.tight_layout()
            plt.savefig('graficos/p4_cr/biomas_anfibios_cr.png', dpi=300)
            plt.close()

    # --- 2. Invertebrados por Bioma (Otimizado) ---
    if not df_invertebrados_cr.empty:
        biomas_inv = []
        for b_set in df_invertebrados_cr['bioma'].dropna():
            for b in b_set.split(','):
                biomas_f = b.strip()
                if biomas_f: biomas_inv.append(biomas_f)
        if biomas_inv:
            df_biomas_inv = pd.Series(biomas_inv).value_counts().reset_index()
            df_biomas_inv.columns = ['Bioma', 'Quantidade']
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=df_biomas_inv, x='Quantidade', y='Bioma', hue='Bioma', palette='mako', legend=False, ax=ax)
            ax.bar_label(ax.containers[0], padding=5, fontname='sans-serif', fontsize=10, fontweight='bold', color='#333333')
            plt.title('Invertebrados Aquáticos em Risco Crítico (CR) por Bioma', fontsize=14, fontweight='bold', pad=15, color='#111111')
            plt.xlabel('Número de Espécies', fontsize=11, labelpad=10)
            plt.ylabel('')
            sns.despine(left=True, bottom=True)
            plt.tight_layout()
            plt.savefig('graficos/p4_cr/biomas_invertebrados_cr.png', dpi=300)
            plt.close()

    # --- 3. Vetores de Ameaça (Otimizado) ---
    threat_map = {
        '1': 'Expansão Urbana', '2': 'Agropecuária', '3': 'Energia/Mineração',
        '4': 'Transporte/Infraestrutura', '5': 'Uso Recursos Biológicos',
        '6': 'Perturbação Humana', '7': 'Modificação Sistemas',
        '8': 'Espécies Invasoras/Doenças', '9': 'Poluição', '11': 'Mudanças Climáticas'
    }
    ameacas_list = []
    for ameacas in df_cr['ameaca'].dropna():
        for line in ameacas.split('\n'):
            for code, desc in threat_map.items():
                if line.startswith(f"{code} - ") or line.startswith(f"{code}."):
                    ameacas_list.append(desc)
                    break
    if ameacas_list:
        df_ameacas = pd.Series(ameacas_list).value_counts().reset_index()
        df_ameacas.columns = ['Ameaça', 'Quantidade']
        
        fig, ax = plt.subplots(figsize=(11, 5.5))
        sns.barplot(data=df_ameacas.head(8), x='Quantidade', y='Ameaça', hue='Ameaça', palette='flare', legend=False, ax=ax)
        ax.bar_label(ax.containers[0], padding=5, fontname='sans-serif', fontsize=10, fontweight='bold', color='#333333')
        plt.title('Principais Vetores de Ameaça sobre as Espécies (CR) - P4', fontsize=14, fontweight='bold', pad=15, color='#111111')
        plt.xlabel('Número de Espécies Afetadas', fontsize=11, labelpad=10)
        plt.ylabel('')
        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        plt.savefig('graficos/p4_cr/principais_ameacas.png', dpi=300)
        plt.close()

    # --- 4. Tendência Populacional (Donut Otimizado) ---
    df_tendencia = df_cr['tendencia_populacional'].value_counts().reset_index()
    df_tendencia.columns = ['Tendência', 'Quantidade']
    traducao_tendencia = {'Declinando': 'Em Declínio', 'Estável': 'Estável', 'Desconhecido': 'Não Informada'}
    df_tendencia['Tendência'] = df_tendencia['Tendência'].map(traducao_tendencia).fillna(df_tendencia['Tendência'])
    
    fig, ax = plt.subplots(figsize=(7, 5))
    cores = ['#e15759', '#f28e2b', '#4e79a7']
    wedges, texts, autotexts = ax.pie(
        df_tendencia['Quantidade'], labels=df_tendencia['Tendência'], autopct='%1.1f%%', 
        startangle=140, colors=cores[:len(df_tendencia)], pctdistance=0.75,
        textprops=dict(fontname='sans-serif', fontsize=11, fontweight='bold')
    )
    # Transforma em gráfico de Donut (mais moderno)
    centre_circle = plt.Circle((0,0),0.55,fc='#FAF9F6')
    fig.gca().add_artist(centre_circle)
    
    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.title('Tendência Populacional das Espécies CR', fontsize=14, fontweight='bold', pad=15, color='#111111')
    plt.tight_layout()
    plt.savefig('graficos/p4_cr/tendencia_populacional.png', dpi=300)
    plt.close()

def treinar_modelo_preditivo(df_p4):
    print("\n[P4] Treinando o modelo preditivo RandomForest...")
    
    biomas = ['Amazônia', 'Mata Atlântica', 'Cerrado', 'Caatinga', 'Pampa', 'Pantanal', 'Sistema Costeiro-Marinho']
    for b in biomas:
        col_name = f'bioma_{b.lower().replace(" ", "_").replace("-", "_").replace("ô", "o").replace("â", "a").replace("á", "a").replace("í", "i")}'
        df_p4[col_name] = df_p4['bioma'].str.contains(b, na=False).astype(int)
        
    regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
    for r in regioes:
        col_name = f'regiao_{r.lower().replace("-", "_")}'
        df_p4[col_name] = df_p4['regiao'].str.contains(r, na=False).astype(int)
        
    df_p4['is_endemica'] = (df_p4['endemica_brasil'] == 'Sim').astype(int)
    df_p4['is_migratoria'] = (df_p4['migratoria'] == 'Sim').astype(int)
    df_p4['tendencia_declinando'] = (df_p4['tendencia_populacional'] == 'Declinando').astype(int)
    
    threat_keywords = {
        'ameaca_expansao_urbana': '1 - ', 'ameaca_agropecuaria': '2 - ', 'ameaca_energia_mineracao': '3 - ',
        'ameaca_transporte': '4 - ', 'ameaca_uso_recursos': '5 - ', 'ameaca_perturbacao_humana': '6 - ',
        'ameaca_modificacoes_sistema': '7 - ', 'ameaca_invasoras': '8 - ', 'ameaca_poluicao': '9 - ',
        'ameaca_mudancas_climaticas': '11 - '
    }
    for col, pat in threat_keywords.items():
        df_p4[col] = df_p4['ameaca'].str.contains(pat, na=False, regex=False).astype(int)
        
    df_p4['risco_inicial_2014'] = df_p4['status_2014'].map({
        'NE': 0.0, 'LC': 0.0, 'NT': 0.5, 'VU': 1.0, 'EN': 2.0, 'CR': 3.0
    }).fillna(0.0)
    
    features = [
        'bioma_amazonia', 'bioma_mata_atlantica', 'bioma_cerrado', 'bioma_caatinga', 
        'bioma_pampa', 'bioma_pantanal', 'bioma_sistema_costeiro_marinho',
        'regiao_norte', 'regiao_nordeste', 'regiao_sudeste', 'regiao_sul', 'regiao_centro_oeste',
        'is_endemica', 'is_migratoria', 'tendencia_declinando',
        'ameaca_expansao_urbana', 'ameaca_agropecuaria', 'ameaca_energia_mineracao', 
        'ameaca_transporte', 'ameaca_uso_recursos', 'ameaca_perturbacao_humana', 
        'ameaca_modificacoes_sistema', 'ameaca_invasoras', 'ameaca_poluicao', 
        'ameaca_mudancas_climaticas', 'risco_inicial_2014'
    ]
    
    df_p4['is_cr'] = (df_p4['status_2026'] == 'CR').astype(int)
    X = df_p4[features]
    y = df_p4['is_cr']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    clf = RandomForestClassifier(n_estimators=150, max_depth=6, class_weight='balanced', random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]
    
    print("\n--- MÉTRICAS DE VALIDAÇÃO (P4) ---")
    print(classification_report(y_test, y_pred, target_names=['Não CR', 'CR']))
    try:
        auc = roc_auc_score(y_test, y_proba)
        print(f"ROC-AUC Score: {auc:.4f}")
    except:
        auc = 0.0
        
    df_p4['proba_extincao'] = clf.predict_proba(X)[:, 1]
    
    # --- 5. GRÁFICO PREDIÇÃO: Lista de Animais Sob Maior Risco (Otimizado) ---
    print("[P4] Criando gráfico de alta definição para as espécies sob maior risco predito...")
    df_risco_animais = df_p4[df_p4['status_2026'] != 'CR'].sort_values(by='proba_extincao', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    df_risco_animais['nome_exibicao'] = df_risco_animais['especie'] + " \n(" + df_risco_animais['nome_comum'].fillna('Sem nome popular') + ")"
    
    sns.barplot(data=df_risco_animais, x='proba_extincao', y='nome_exibicao', hue='nome_exibicao', palette='rocket_r', legend=False, ax=ax)
    
    # Adicionar porcentagem exata no final de cada barra de predição
    for p in ax.patches:
        width = p.get_width()
        ax.text(width + 0.01, p.get_y() + p.get_height()/2, f'{width:.1%}', 
                va='center', fontname='sans-serif', fontsize=10, fontweight='bold', color='#444444')
                
    plt.title('Top 10 Espécies de Anfíbios/Invertebrados com Maior Risco Preditivo de Extinção', fontsize=14, fontweight='bold', pad=15, color='#111111')
    plt.xlabel('Probabilidade de Extinção Futura Calculada pela IA', fontsize=11, labelpad=10)
    plt.ylabel('')
    plt.xlim(0, 1.1)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig('graficos/p4_cr/top_especies_risco.png', dpi=300)
    plt.close()

    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    importancias_relatorio = [(features[indices[f]], importances[indices[f]]) for f in range(10)]
    
    df_p4_salvar = df_p4[['especie', 'nome_comum', 'status_2014', 'status_2026', 'is_cr', 'proba_extincao'] + features].copy()
    df_p4_salvar.sort_values(by='proba_extincao', ascending=False, inplace=True)
    df_p4_salvar.to_csv('data/anfibios_invertebrados_predicoes.csv', index=False, encoding='utf-8')
    
    return df_p4_salvar, importancias_relatorio, auc

def gerar_relatorio_final_p4(df_pred, importancias, auc):
    df_risco_iminente = df_pred[df_pred['status_2026'] != 'CR'].head(10)
    feature_tr = {
        'risco_inicial_2014': 'Risco histórico em 2014 (MMA)', 'tendencia_declinando': 'Tendência Populacional em Declínio',
        'ameaca_agropecuaria': 'Ameaça de Agropecuária/Aquacultura', 'ameaca_uso_recursos': 'Ameaça de Uso de Recursos Hídricos',
        'bioma_mata_atlantica': 'Presença na Mata Atlântica', 'ameaca_modificacoes_sistema': 'Modificações de Sistemas Naturais'
    }
    report_content = f"""# Relatório Técnico Preditivo - Anfíbios e Invertebrados Aquáticos (CR)
**Autor:** Pessoa 4 (Anfíbios e Invertebrados)

## Resultados do Modelo Preditivo (Random Forest)
* **ROC-AUC Score:** {auc:.4f}

## Fatores Determinantes de Extinção
1. {feature_tr.get(importancias[0][0], importancias[0][0])} ({importancias[0][1]:.2%})
2. {feature_tr.get(importancias[1][0], importancias[1][0])} ({importancias[1][1]:.2%})

## Ações Prescritivas Propostas
* **Zonas de Amortecimento Químico (Buffers Hídricos):** Blindagem química de corpos d'água onde vivem os anfíbios e invertebrados mapeados com risco crítico pela IA.
* **Restauro de Matas Ciliares:** Garantia de umidade e sombreamento essenciais para a sobrevivência dos táxons vulneráveis.
"""
    with open('data/relatorio_p4_cr.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    print("[P4] Relatório analítico final exportado em 'data/relatorio_p4_cr.md'.")

if __name__ == '__main__':
    try:
        df = carregar_dados()
        grupos_p4 = ['Anfíbios', 'Invertebrados de Água Doce', 'Invertebrados Marinhos']
        df_p4 = df[df['grupo'].isin(grupos_p4)].copy()
        
        print(f"[P4] Registros localizados: {len(df_p4)}")
        
        gerar_graficos_p4_cr(df_p4)
        df_pred, importancias, auc = treinar_modelo_preditivo(df_p4)
        gerar_relatorio_final_p4(df_pred, importancias, auc)
        
        print("\n[SUCESSO] Todos os gráficos foram atualizados e salvos com acabamento premium em 'graficos/p4_cr/'!")
    except Exception as e:
        print(f"\n[ERRO] Falha na execução: {e}")