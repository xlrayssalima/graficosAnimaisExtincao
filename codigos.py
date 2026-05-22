import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# CARREGAR OS BANCOS
# =========================

df = pd.read_csv('br_mma_extincao_fauna_ameacada.csv')
dt = pd.read_csv('salve-publico-exportacao-fichas-planilha12-05-2026-15-56-40 (1).csv')

# visualizar colunas
print(df.columns)
print(dt.columns)

# =========================
# JUNTAR OS BANCOS
# =========================

dados = pd.concat([df, dt], ignore_index=True)

# =========================
# FILTRAR DADOS
# =========================

anfibios = dados[dados['grupo'] == 'Anfíbios']
aves = dados[dados['grupo'] == 'Aves']

# =========================
# CONTAGEM DOS DADOS
# =========================

contagem_anfibios = anfibios['categoria'].value_counts().reset_index()
contagem_anfibios.columns = ['categoria', 'quantidade']

contagem_aves = aves['categoria'].value_counts().reset_index()
contagem_aves.columns = ['categoria', 'quantidade']

# =========================
# DISPERSÃO - ANFÍBIOS
# =========================

sns.scatterplot(
    data=contagem_anfibios,
    x='categoria',
    y='quantidade'
)

plt.title('Dispersão - Anfíbios')
plt.grid(True)
plt.savefig('dispersao_anfibios.png')
plt.show()

# =========================
# DISPERSÃO - AVES
# =========================

sns.scatterplot(
    data=contagem_aves,
    x='categoria',
    y='quantidade'
)

plt.title('Dispersão - Aves')
plt.grid(True)
plt.savefig('dispersao_aves.png')
plt.show()

# =========================
# BARRA - ANFÍBIOS
# =========================

contagem_anfibios.plot(
    kind='bar',
    x='categoria',
    y='quantidade'
)

plt.title('Barra - Anfíbios')
plt.savefig('barra_anfibios.png')
plt.show()

# =========================
# BARRA - AVES
# =========================

contagem_aves.plot(
    kind='bar',
    x='categoria',
    y='quantidade'
)

plt.title('Barra - Aves')
plt.savefig('barra_aves.png')
plt.show()

# =========================
# PIZZA - ANFÍBIOS
# =========================

contagem_anfibios.set_index('categoria')['quantidade'].plot(
    kind='pie',
    autopct='%1.1f%%'
)

plt.ylabel('')
plt.title('Pizza - Anfíbios')
plt.savefig('pizza_anfibios.png')
plt.show()

# =========================
# PIZZA - AVES
# =========================

contagem_aves.set_index('categoria')['quantidade'].plot(
    kind='pie',
    autopct='%1.1f%%'
)

plt.ylabel('')
plt.title('Pizza - Aves')
plt.savefig('pizza_aves.png')
plt.show()