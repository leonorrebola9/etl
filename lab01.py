import pandas as pd
import pyodbc
from sqlalchemy import create_engine

# ==============================
# 1️⃣ CONEXÃO SQL SERVER
# ==============================

import pandas as pd
from sqlalchemy import create_engine

server = r'LAPTOP-VG0H1U7H\SQLEXPRESS'   # <-- substitui pelo teu
database = 'ShopX'

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string)

# Teste
with engine.connect() as conn:
    print("Conexão bem-sucedida!")

# ==============================
# 2️⃣ CRIAR TABELAS NO SQL
# ==============================

with engine.begin() as conn:

    conn.exec_driver_sql("""
    IF OBJECT_ID('DimCliente', 'U') IS NOT NULL DROP TABLE DimCliente;
    CREATE TABLE DimCliente (
        ClienteID INT PRIMARY KEY,
        Nome NVARCHAR(100),
        Cidade NVARCHAR(100)
    );
    """)

    conn.exec_driver_sql("""
    IF OBJECT_ID('DimProduto', 'U') IS NOT NULL DROP TABLE DimProduto;
    CREATE TABLE DimProduto (
        ProdutoID INT PRIMARY KEY,
        Produto NVARCHAR(100),
        Categoria NVARCHAR(100)
    );
    """)

    conn.exec_driver_sql("""
    IF OBJECT_ID('DimTempo', 'U') IS NOT NULL DROP TABLE DimTempo;
    CREATE TABLE DimTempo (
        IDTempoDW INT PRIMARY KEY,
        Data DATE,
        Ano INT,
        Mes INT,
        Trimestre INT
    );
    """)

    conn.exec_driver_sql("""
    IF OBJECT_ID('FatoVendas', 'U') IS NOT NULL DROP TABLE FatoVendas;
    CREATE TABLE FatoVendas (
        IDVendaDW INT IDENTITY(1,1) PRIMARY KEY,
        IDClienteDW INT,
        IDProdutoDW INT,
        IDTempoDW INT,
        Quantidade INT,
        Valor DECIMAL(10,2)
    );
    """)

print("Tabelas recriadas com sucesso!")

# ==============================
# 3️⃣ LER FICHEIROS CSV
# ==============================

clientes = pd.read_csv("clientes.csv", encoding="latin-1")
produtos = pd.read_csv("produtos.csv", encoding="latin-1")
vendas = pd.read_csv("vendas.csv", encoding="latin-1")

# ==============================
# 4️⃣ CRIAR DIMENSÃO TEMPO
# ==============================

vendas['Data'] = pd.to_datetime(vendas['Data'])

DimTempo = vendas[['Data']].drop_duplicates().copy()
DimTempo['Ano'] = DimTempo['Data'].dt.year
DimTempo['Mes'] = DimTempo['Data'].dt.month
DimTempo['Dia'] = DimTempo['Data'].dt.day
DimTempo['DataID'] = DimTempo['Data'].dt.strftime('%Y%m%d').astype(int)

DimTempo = DimTempo[['DataID', 'Data', 'Ano', 'Mes', 'Dia']]

# ==============================
# 5️⃣ PREPARAR DIMENSÕES
# ==============================

DimCliente = clientes[['ClienteID', 'Nome', 'Cidade']]
DimProduto = produtos[['ProdutoID', 'Produto', 'Categoria']]

# ==============================
# 6️⃣ PREPARAR FACT TABLE
# ==============================

vendas['DataID'] = vendas['Data'].dt.strftime('%Y%m%d').astype(int)

FatoVendas = vendas[['VendaID', 'ClienteID', 'ProdutoID', 'DataID', 'Quantidade', 'Valor']]

# ==============================
# 7️⃣ CARREGAR PARA SQL
# ==============================

DimCliente.to_sql("DimCliente", engine, if_exists="append", index=False)
DimProduto.to_sql("DimProduto", engine, if_exists="append", index=False)
DimTempo.to_sql("DimTempo", engine, if_exists="append", index=False)
FatoVendas.to_sql("FatoVendas", engine, if_exists="append", index=False)

print("Dados carregados com sucesso no Data Warehouse!")