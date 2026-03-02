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

SELECT 
    dT.Ano, 
    dT.Mes, 
    dProd.Categoria,
    SUM(fV.Quantidade) AS TotalQtd,
    SUM(fV.Valor) AS TotalValor
FROM FactVendas fV
JOIN DimTempo dT ON fV.IDTempoDW = dT.IDTempoDW
JOIN DimProduto dProd ON fV.IDProdutoDW = dProd.IDProduto
GROUP BY 
    dT.Ano, 
    dT.Mes, 
    dProd.Categoria
ORDER BY 
    dT.Ano, 
    dT.Mes, 
    dProd.Categoria;

-- top 5 vendas
SELECT TOP 5
    dProd.NomeProduto,
    SUM(fV.Valor) AS TotalVendido
FROM FactVendas fV
JOIN DimProduto dProd 
    ON fV.IDProdutoDW = dProd.IDProduto
GROUP BY dProd.NomeProduto
ORDER BY TotalVendido DESC;

-- distribuição geográfica
SELECT
    dC.Cidade,
    SUM(fV.Valor) AS TotalVendas
FROM FactVendas fV
JOIN DimCliente dC 
    ON fV.IDClienteDW = dC.IDCliente
GROUP BY dC.Cidade
ORDER BY TotalVendas DESC;

-- evolução clientes
WITH PrimeiraCompra AS (
    SELECT
        fV.IDClienteDW,
        MIN(dT.Data) AS DataPrimeiraCompra
    FROM FactVendas fV
    JOIN DimTempo dT 
        ON fV.IDTempoDW = dT.IDTempoDW
    GROUP BY fV.IDClienteDW
)

SELECT
    YEAR(DataPrimeiraCompra) AS Ano,
    MONTH(DataPrimeiraCompra) AS Mes,
    COUNT(IDClienteDW) AS NovosClientes
FROM PrimeiraCompra
GROUP BY 
    YEAR(DataPrimeiraCompra),
    MONTH(DataPrimeiraCompra)
ORDER BY 
    Ano, Mes;
