import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar os dois bancos
df2022 = pd.read_csv("dados.csv")   # lista de 2022
df2026 = pd.read_csv("dados2.csv")  # lista de 2026

# --- Separação 2022 (usa coluna 'grupo') ---
peixes_continentais_2022 = df2022[df2022["grupo"] == "Peixes Continentais"]
peixes_marinhos_2022 = df2022[df2022["grupo"] == "Peixes Marinhos (Ósseos)"]

# --- Separação 2026 (usa classe + bioma) ---
# Primeiro filtrar só peixes ósseos
peixes_osseos_2026 = df2026[df2026["classe"] == "Actinopterygii"]

# Definir biomas continentais e marinhos
biomas_continentais = ["Amazônia", "Pantanal", "Mata Atlântica", "Caatinga", "Cerrado", "Pampa"]

# Continentais: qualquer bioma que contenha um dos nomes acima
peixes_continentais_2026 = peixes_osseos_2026[
    peixes_osseos_2026["bioma"].str.contains("|".join(biomas_continentais), na=False)
]

# Marinhos: qualquer bioma que mencione Sistema Costeiro-Marinho
peixes_marinhos_2026 = peixes_osseos_2026[
    peixes_osseos_2026["bioma"].str.contains("Sistema Costeiro-Marinho", na=False)
]

# Converter colunas para numéricas
peixes_continentais_2022["lista_2014"] = pd.to_numeric(peixes_continentais_2022["lista_2014"], errors="coerce")
peixes_marinhos_2022["lista_2014"] = pd.to_numeric(peixes_marinhos_2022["lista_2014"], errors="coerce")

peixes_continentais_2026["consta_em_lista_nacional_oficial"] = peixes_continentais_2026["consta_em_lista_nacional_oficial"].map({"Sim":1,"Não":0,"True":1,"False":0,1:1,0:0})
peixes_marinhos_2026["consta_em_lista_nacional_oficial"] = peixes_marinhos_2026["consta_em_lista_nacional_oficial"].map({"Sim":1,"Não":0,"True":1,"False":0,1:1,0:0})

# --- HISTOGRAMAS ---
plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
sns.histplot(peixes_continentais_2022["lista_2014"], bins=2, kde=False)
plt.title("Histograma Peixes Continentais (2022)")

plt.subplot(2,2,2)
sns.histplot(peixes_continentais_2026["consta_em_lista_nacional_oficial"], bins=2, kde=False)
plt.title("Histograma Peixes Continentais (2026)")

plt.subplot(2,2,3)
sns.histplot(peixes_marinhos_2022["lista_2014"], bins=2, kde=False)
plt.title("Histograma Peixes Marinhos Ósseos (2022)")

plt.subplot(2,2,4)
sns.histplot(peixes_marinhos_2026["consta_em_lista_nacional_oficial"], bins=2, kde=False)
plt.title("Histograma Peixes Marinhos Ósseos (2026)")

plt.tight_layout()
plt.show()

# --- GRÁFICOS DE PIZZA ---
plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
peixes_continentais_2022["categoria"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90)
plt.title("Categorias Peixes Continentais (2022)")

plt.subplot(2,2,2)
peixes_continentais_2026["categoria"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90)
plt.title("Categorias Peixes Continentais (2026)")

plt.subplot(2,2,3)
peixes_marinhos_2022["categoria"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90)
plt.title("Categorias Peixes Marinhos Ósseos (2022)")

plt.subplot(2,2,4)
peixes_marinhos_2026["categoria"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90)
plt.title("Categorias Peixes Marinhos Ósseos (2026)")

plt.tight_layout()
plt.show()

# --- ESTATÍSTICAS ---
print("Estatísticas Peixes Continentais (2022):")
print("Média:", peixes_continentais_2022["lista_2014"].mean())
print("Mediana:", peixes_continentais_2022["lista_2014"].median())
print("Desvio padrão:", peixes_continentais_2022["lista_2014"].std())

print("\nEstatísticas Peixes Continentais (2026):")
print("Média:", peixes_continentais_2026["consta_em_lista_nacional_oficial"].mean())
print("Mediana:", peixes_continentais_2026["consta_em_lista_nacional_oficial"].median())
print("Desvio padrão:", peixes_continentais_2026["consta_em_lista_nacional_oficial"].std())

print("\nEstatísticas Peixes Marinhos Ósseos (2022):")
print("Média:", peixes_marinhos_2022["lista_2014"].mean())
print("Mediana:", peixes_marinhos_2022["lista_2014"].median())
print("Desvio padrão:", peixes_marinhos_2022["lista_2014"].std())

print("\nEstatísticas Peixes Marinhos Ósseos (2026):")
print("Média:", peixes_marinhos_2026["consta_em_lista_nacional_oficial"].mean())
print("Mediana:", peixes_marinhos_2026["consta_em_lista_nacional_oficial"].median())
print("Desvio padrão:", peixes_marinhos_2026["consta_em_lista_nacional_oficial"].std())

