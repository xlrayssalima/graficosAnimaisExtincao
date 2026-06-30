import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Configurar encoding do console para evitar erros de caracteres no Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Garantir que as pastas de saída existam
os.makedirs('graficos/tubaroes_raias', exist_ok=True)
os.makedirs('data', exist_ok=True)

def carregar_dados():
    # Ajuste para o nome correto do arquivo
    caminho = 'data/fauna_cr_consolidada.csv'
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Base de dados '{caminho}' não encontrada.")
    return pd.read_csv(caminho)

def gerar_graficos_tubaroes_raias(df_tr):
    print("[Tub/Raias] Gerando gráficos otimizados...")

    df_cr = df_tr[df_tr['status_2026'] == 'CR'].copy()
    if df_cr.empty:
        print("[Tub/Raias] Nenhuma espécie CR encontrada.")
        return

    # --- CONFIGURAÇÃO DE ESTILO ---
    sns.set_theme(style="white")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.facecolor'] = '#FAF9F6'
    plt.rcParams['axes.facecolor'] = '#FAF9F6'

    # --- 1. Distribuição por Biomas ---
    if 'bioma' in df_cr.columns:
        df_biomas = df_cr['bioma'].value_counts().reset_index()
        df_biomas.columns = ['Bioma', 'Quantidade']
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df_biomas, x='Quantidade', y='Bioma', hue='Bioma', palette='crest', legend=False, ax=ax)
        ax.bar_label(ax.containers[0], padding=5, fontsize=10, fontweight='bold', color='#333333')
        plt.title('Tubarões e Raias CR por Bioma', fontsize=14, fontweight='bold')
        plt.xlabel('Número de Espécies')
        plt.ylabel('')
        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        plt.savefig('graficos/tubaroes_raias/biomas_cr.png', dpi=300)
        plt.close()

    # --- 2. Principais Ameaças (separado Tubarões vs Raias) ---
    if 'ameaca' in df_cr.columns and 'nome_comum' in df_cr.columns:
        df_tubaroes = df_cr[df_cr['nome_comum'].str.contains("tubarão|cação", case=False, na=False)]
        df_raias = df_cr[df_cr['nome_comum'].str.contains("raia", case=False, na=False)]

        for grupo, df_g in [('Tubarões', df_tubaroes), ('Raias', df_raias)]:
            if not df_g.empty:
                df_ameacas = df_g['ameaca'].value_counts().reset_index()
                df_ameacas.columns = ['Ameaça', 'Quantidade']
                fig, ax = plt.subplots(figsize=(11, 5))
                sns.barplot(data=df_ameacas, x='Quantidade', y='Ameaça', hue='Ameaça', palette='flare', legend=False, ax=ax)
                ax.bar_label(ax.containers[0], padding=5, fontsize=10, fontweight='bold', color='#333333')
                plt.title(f'Principais Ameaças - {grupo} (CR)', fontsize=14, fontweight='bold')
                plt.xlabel('Número de Espécies Afetadas')
                plt.ylabel('')
                sns.despine(left=True, bottom=True)
                plt.tight_layout()
                plt.savefig(f'graficos/tubaroes_raias/ameacas_{grupo.lower()}.png', dpi=300)
                plt.close()

    # --- 3. Tendência Populacional ---
    if 'tendencia_populacional' in df_cr.columns:
        df_tendencia = df_cr['tendencia_populacional'].value_counts().reset_index()
        df_tendencia.columns = ['Tendência', 'Quantidade']
        fig, ax = plt.subplots(figsize=(7, 5))
        cores = ['#e15759', '#f28e2b', '#4e79a7']
        wedges, texts, autotexts = ax.pie(
            df_tendencia['Quantidade'], labels=df_tendencia['Tendência'], autopct='%1.1f%%',
            startangle=140, colors=cores[:len(df_tendencia)], pctdistance=0.75,
            textprops=dict(fontsize=11, fontweight='bold')
        )
        centre_circle = plt.Circle((0,0),0.55,fc='#FAF9F6')
        fig.gca().add_artist(centre_circle)
        plt.setp(autotexts, size=10, weight="bold", color="white")
        plt.title('Tendência Populacional - Tubarões e Raias CR', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('graficos/tubaroes_raias/tendencia_populacional.png', dpi=300)
        plt.close()

    # --- 4. Transição de Status ---
    if 'transicao_status' in df_cr.columns:
        df_transicao = df_cr['transicao_status'].value_counts().reset_index()
        df_transicao.columns = ['Transição', 'Quantidade']
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df_transicao, x='Transição', y='Quantidade', palette='mako', ax=ax)
        plt.title('Transição de Status - Tubarões e Raias (CR)', fontsize=14, fontweight='bold')
        plt.xlabel('')
        plt.ylabel('Número de Espécies')
        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        plt.savefig('graficos/tubaroes_raias/transicao_status.png', dpi=300)
        plt.close()

def treinar_modelo_tubaroes_raias(df_tr):
    print("\n[Tub/Raias] Treinando modelo preditivo...")
    features = ['familia', 'ordem', 'regiao', 'bioma', 'ameaca']
    X = pd.get_dummies(df_tr[features])
    y = (df_tr['status_2026'] == 'CR').astype(int)

    if len(df_tr) > 5 and y.nunique() > 1:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
        clf = RandomForestClassifier(n_estimators=150, max_depth=6, class_weight='balanced', random_state=42)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_proba = clf.predict_proba(X_test)[:, 1]

        print("\n--- MÉTRICAS DE VALIDAÇÃO ---")
        print(classification_report(y_test, y_pred, target_names=['Não CR', 'CR']))
        try:
            auc = roc_auc_score(y_test, y_proba)
            print(f"ROC-AUC Score: {auc:.4f}")
        except Exception:
            auc = 0.0

        return clf, auc
    else:
        print("Dados insuficientes ou apenas uma categoria em 'status_2026'.")
        return None, 0.0

if __name__ == '__main__':
    try:
        df = carregar_dados()
        grupos_tr = ['Tubarões e Raias']
        df_tr = df[df['grupo'].isin(grupos_tr)].copy()

        print(f"[Tub/Raias] Registros localizados: {len(df_tr)}")

        gerar_graficos_tubaroes_raias(df_tr)
        clf, auc = treinar_modelo_tubaroes_raias(df_tr)

        print("\n[SUCESSO] Gráficos e modelo de Tubarões e Raias atualizados em 'graficos/tubaroes_raias/'!")
    except Exception as e:
        print(f"\n[ERRO] Falha na execução: {e}")
