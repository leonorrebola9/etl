CREATE DATABASE CatalogoMediaDB;
GO

USE CatalogoMediaDB;
GO

CREATE TABLE Titulos (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    titulo        NVARCHAR(255)  NOT NULL,
    tipo          NVARCHAR(10)   NOT NULL CHECK (tipo IN ('filme', 'serie')),
    genero        NVARCHAR(100)  NOT NULL,
    ano           INT            NOT NULL,
    classificacao DECIMAL(3,1)   NULL CHECK (classificacao BETWEEN 0 AND 10),
    descricao     NVARCHAR(MAX)  NULL,
    ativo         BIT            NOT NULL DEFAULT 1,
    criado_em     DATETIME       NOT NULL DEFAULT GETDATE(),
    atualizado_em DATETIME       NOT NULL DEFAULT GETDATE()
);
GO

select * from Titulos;