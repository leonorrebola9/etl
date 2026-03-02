import pandas as pd

clientes = pd.read_csv("clientes.csv")

produtos = pd.read_csv("produtos.csv")

vendas = pd.read_csv("vendas.csv")

# Converter data
vendas["Data"] = pd.to_datetime(vendas["Data"])
clientes["DataRegisto"] = pd.to_datetime(clientes["DataRegisto"], errors="coerce")

# Remover duplicados
clientes = clientes.drop_duplicates()
produtos = produtos.drop_duplicates()
vendas = vendas.drop_duplicates()

#valores nulos
clientes = clientes.fillna("Desconhecido")
produtos = produtos.fillna("Desconhecido")
vendas = vendas.dropna() 


# Criar dimensão tempo
dim_tempo = vendas[["Data"]].drop_duplicates()
dim_tempo["Ano"] = dim_tempo["Data"].dt.year
dim_tempo["Mes"] = dim_tempo["Data"].dt.month
dim_tempo["Trimestre"] = dim_tempo["Data"].dt.quarter

dim_tempo = dim_tempo.reset_index(drop=True)
dim_tempo["IDTempoDW"] = dim_tempo.index + 1

clientes = clientes.reset_index(drop=True)
clientes["IDClienteDW"] = clientes.index + 1

produtos = produtos.reset_index(drop=True)
produtos["IDProdutoDW"] = produtos.index + 1

print(dim_tempo.columns)

fact_vendas = vendas.merge(
    produtos[["IDProduto", "IDProdutoDW"]],
    on="IDProduto",
    how="left"
)

fact_vendas = fact_vendas.merge(
    clientes[["IDCliente", "IDClienteDW"]],
    on="IDCliente",
    how="left"
)

fact_vendas = fact_vendas.merge(
    dim_tempo[["Data", "IDTempoDW"]],
    on="Data",
    how="left"
)

fact_vendas = fact_vendas[[
    "IDTempoDW",
    "IDProdutoDW",
    "IDClienteDW",
    "Quantidade",
    "Valor"
]]

print(fact_vendas.isnull().sum())