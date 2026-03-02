import pandas as pd
from sqlalchemy import create_engine

# =====================================================
# 1️⃣ CONEXÃO SQL SERVER
# =====================================================

server = r'PC0ADRIANA\SQLEXPRESS'
database = 'ShopX'

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string)

with engine.connect() as conn:
    print("Conexão bem-sucedida!")

# =====================================================
# 2️⃣ CRIAR TABELAS (DROP + CREATE)
# =====================================================

with engine.begin() as conn:

    # DIM CLIENTE
    conn.exec_driver_sql("""
    IF OBJECT_ID('DimCliente', 'U') IS NOT NULL DROP TABLE DimCliente;
    CREATE TABLE DimCliente (
        IDCliente INT PRIMARY KEY,
        Nome NVARCHAR(100),
        Cidade NVARCHAR(100)
    );
    """)

    # DIM PRODUTO
    conn.exec_driver_sql("""
    IF OBJECT_ID('DimProduto', 'U') IS NOT NULL DROP TABLE DimProduto;
    CREATE TABLE DimProduto (
        IDProduto INT PRIMARY KEY,
        NomeProduto NVARCHAR(100),
        Categoria NVARCHAR(100)
    );
    """)

    # DIM TEMPO
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

    # FACT VENDAS
    conn.exec_driver_sql("""
    IF OBJECT_ID('FactVendas', 'U') IS NOT NULL DROP TABLE FactVendas;
    CREATE TABLE FactVendas (
        IDVendaDW INT IDENTITY(1,1) PRIMARY KEY,
        IDClienteDW INT,
        IDProdutoDW INT,
        IDTempoDW INT,
        Quantidade INT,
        Valor DECIMAL(10,2)
    );
    """)

print("Tabelas recriadas com sucesso!")

# =====================================================
# 3️⃣ LER CSV
# =====================================================

clientes = pd.read_csv("clientes.csv", sep=";", encoding="latin-1")
produtos = pd.read_csv("produtos.csv", sep=";", encoding="latin-1")
vendas = pd.read_csv("vendas.csv", sep=";", encoding="latin-1")

# Remover espaços invisíveis nos nomes
clientes.columns = clientes.columns.str.strip()
produtos.columns = produtos.columns.str.strip()
vendas.columns = vendas.columns.str.strip()

# =====================================================
# 4️⃣ TRANSFORMAÇÕES
# =====================================================

# Converter data
vendas['Data'] = pd.to_datetime(vendas['Data'], dayfirst=True)

# -------------------------
# DIM TEMPO
# -------------------------

DimTempo = vendas[['Data']].drop_duplicates().copy()

DimTempo['Ano'] = DimTempo['Data'].dt.year
DimTempo['Mes'] = DimTempo['Data'].dt.month
DimTempo['Trimestre'] = DimTempo['Data'].dt.quarter
DimTempo['IDTempoDW'] = DimTempo['Data'].dt.strftime('%Y%m%d').astype(int)

DimTempo = DimTempo[['IDTempoDW', 'Data', 'Ano', 'Mes', 'Trimestre']]

# -------------------------
# DIM CLIENTE
# -------------------------

DimCliente = clientes[['IDCliente', 'Nome', 'Cidade']]

# -------------------------
# DIM PRODUTO
# -------------------------

DimProduto = produtos[['IDProduto', 'NomeProduto', 'Categoria']]

# -------------------------
# FACT VENDAS
# -------------------------

vendas['IDTempoDW'] = vendas['Data'].dt.strftime('%Y%m%d').astype(int)

FactVendas = vendas[['IDCliente', 'IDProduto', 'IDTempoDW', 'Quantidade', 'Valor']]

FactVendas = FactVendas.rename(columns={
    'IDCliente': 'IDClienteDW',
    'IDProduto': 'IDProdutoDW'
})

# =====================================================
# 5️⃣ CARREGAMENTO PARA SQL
# =====================================================

DimCliente.to_sql("DimCliente", engine, if_exists="append", index=False)
DimProduto.to_sql("DimProduto", engine, if_exists="append", index=False)
DimTempo.to_sql("DimTempo", engine, if_exists="append", index=False)
FactVendas.to_sql("FactVendas", engine, if_exists="append", index=False)

print("Dados carregados com sucesso no Data Warehouse!")