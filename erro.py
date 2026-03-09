import pandas as pd
import re

# Ler o CSV
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