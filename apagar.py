import pandas as pd
import re
"""

df = pd.read_csv("wikipedia_dataset.csv", encoding="utf-8")

# conjunto para guardar caracteres encontrados
caracteres_especiais = set()

# percorrer colunas de texto
for coluna in df.select_dtypes(include="object"):
    for valor in df[coluna].dropna():
        encontrados = re.findall(r"[^\w\s]", str(valor))
        caracteres_especiais.update(encontrados)

print("Caracteres especiais encontrados:")
print(sorted(caracteres_especiais))

"""
df = pd.read_csv(
    "wikipedia_dataset.csv",
    sep=";",
    encoding="latin-1",
    on_bad_lines="skip"
)

df = df.drop_duplicates()

print(df.columns)

colunas_limpar = ["title", "text"]

# Remover caracteres especiais apenas nessas colunas
for col in colunas_limpar:
    df[col] = df[col].astype(str).str.replace(r"[^\w\s]", "", regex=True)

# Guardar o CSV limpo
df.to_csv("wikipedia_dataset_limpo.csv", index=False, encoding="utf-8")
