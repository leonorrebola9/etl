import pandas as pd

df = pd.read_csv(
    "wikipedia_dataset.csv",
    sep=";",
    encoding="latin-1",
    on_bad_lines="skip"
)

print(df.columns)


colunas_limpar = ["title", "text"]

# Remover caracteres especiais apenas nessas colunas
for col in colunas_limpar:
    df[col] = df[col].astype(str).str.replace(r"[^\w\s]", "", regex=True)

# Guardar o CSV limpo
df.to_csv("wikipedia_dataset_limpo.csv", index=False, encoding="utf-8")