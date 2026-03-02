-- CREATE DATABASE ShopX
--GO

CREATE TABLE DimCliente (
    IDClienteDW INT PRIMARY KEY,
    IDCliente INT,
    Nome VARCHAR(100),
    Morada VARCHAR(200),
    Cidade VARCHAR(100),
    Pais VARCHAR(100),
    DataRegisto DATE
);

CREATE TABLE DimProduto (
    IDProdutoDW INT PRIMARY KEY,
    IDProduto INT,
    NomeProduto VARCHAR(150),
    Categoria VARCHAR(100),
    Preco DECIMAL(10,2)
);

CREATE TABLE DimTempo (
    IDTempoDW INT PRIMARY KEY,
    Data DATE,
    Ano INT,
    Mes INT,
    Trimestre INT
);

CREATE TABLE FactVendas (
    IDVenda INT IDENTITY(1,1) PRIMARY KEY,
    IDTempoDW INT,
    IDProdutoDW INT,
    IDClienteDW INT,
    Quantidade INT,
    Valor DECIMAL(10,2),

    FOREIGN KEY (IDTempoDW) REFERENCES DimTempo(IDTempoDW),
    FOREIGN KEY (IDProdutoDW) REFERENCES DimProduto(IDProdutoDW),
    FOREIGN KEY (IDClienteDW) REFERENCES DimCliente(IDClienteDW)
);