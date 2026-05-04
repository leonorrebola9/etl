# pip install fastapi uvicorn sqlalchemy pyodbc
# uvicorn app:app --reload
# http://127.0.0.1:8000/docs
# Dataset extraído de: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?resource=download

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import pyodbc

app = FastAPI(
    title="API de Filmes e Séries",
    description="Catálogo unificado de Filmes e Séries",
    version="1.0"
)

# -----------------------
# Base de dados SQL Server
# -----------------------

def get_conn():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-VG0H1U7H\\SQLEXPRESS;"
        "DATABASE=CatalogoMediaDB;"
        "UID=sa;PWD=sa"
    )

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Titulos' AND xtype='U')
        CREATE TABLE Titulos (
            id            INT IDENTITY(1,1) PRIMARY KEY,
            titulo        NVARCHAR(255) NOT NULL,
            tipo          NVARCHAR(10)  NOT NULL CHECK (tipo IN ('filme', 'serie')),
            genero        NVARCHAR(100) NOT NULL,
            ano           INT           NOT NULL,
            classificacao DECIMAL(3,1)  NULL,
            descricao     NVARCHAR(MAX) NULL,
            ativo         BIT           NOT NULL DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------
# Modelos Pydantic
# -----------------------
# 1º — Enum
class TipoEnum(str, Enum):
    filme = "filme"
    serie = "serie"

class TituloInput(BaseModel):
    titulo:        str             = Field(...)
    tipo:          TipoEnum        = Field(...)
    genero:        str             = Field(...)
    ano:           int             = Field(...)
    classificacao: Optional[float] = Field(None)
    descricao:     Optional[str]   = Field(None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "titulo":        "Inception",
                "tipo":          "filme",
                "genero":        "Ficção Científica",
                "ano":           2010,
                "classificacao": 8.8,
                "descricao":     "Um ladrão que rouba segredos..."
            }
        }
    }

class TituloPatch(BaseModel):
    titulo: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "example": {"titulo": "Novo Título"}
        }
    }

class TituloOutput(BaseModel):
    id:            int
    titulo:        str
    tipo:          str
    genero:        str
    ano:           int
    classificacao: Optional[float]
    descricao:     Optional[str]
    ativo:         bool

class BulkInput(BaseModel):
    titulos: List[TituloInput]

# -----------------------
# Funções auxiliares
# -----------------------

def row_to_dict(row):
    return {
        "id":            row[0],
        "titulo":        row[1],
        "tipo":          row[2],
        "genero":        row[3],
        "ano":           row[4],
        "classificacao": float(row[5]) if row[5] else None,
        "descricao":     row[6],
        "ativo":         bool(row[7]),
    }

def get_titulo_by_id(cursor, id: int):
    cursor.execute("SELECT * FROM Titulos WHERE id=? AND ativo=1", id)
    return cursor.fetchone()

# -----------------------
# GET (2 endpoints)
# -----------------------

@app.get("/titulos", response_model=List[TituloOutput])
def get_all_titulos(tipo: Optional[str] = None, genero: Optional[str] = None,
                    pagina: int = 1, limite: int = 10):
    """GET 1 – Listar todos os títulos (com filtros e paginação)"""
    offset = (pagina - 1) * limite
    query  = "SELECT * FROM Titulos WHERE ativo=1"
    params = []
    if tipo:
        query += " AND tipo=?";   params.append(tipo)
    if genero:
        query += " AND genero=?"; params.append(genero)
    query += f" ORDER BY id OFFSET {offset} ROWS FETCH NEXT {limite} ROWS ONLY"

    conn   = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

@app.get("/titulos/{titulo_id}", response_model=TituloOutput)
def get_titulo(titulo_id: int):
    """GET 2 – Obter um título específico pelo ID"""
    conn   = get_conn()
    cursor = conn.cursor()
    row    = get_titulo_by_id(cursor, titulo_id)
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Título não encontrado")
    return row_to_dict(row)

# -----------------------
# POST (2 endpoints)
# -----------------------

@app.post("/titulos", response_model=TituloOutput, status_code=201)
def create_titulo(titulo: TituloInput):
    """POST 1 – Criar um novo título"""
    conn   = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM Titulos WHERE titulo=? AND tipo=? AND ano=?",
        titulo.titulo, titulo.tipo, titulo.ano
    )
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Título já existe com o mesmo nome, tipo e ano")

    cursor.execute(
        """INSERT INTO Titulos (titulo, tipo, genero, ano, classificacao, descricao)
           OUTPUT INSERTED.*
           VALUES (?, ?, ?, ?, ?, ?)""",
        titulo.titulo, titulo.tipo, titulo.genero,
        titulo.ano, titulo.classificacao, titulo.descricao
    )
    novo = cursor.fetchone()
    conn.commit()
    conn.close()
    return row_to_dict(novo)

@app.post("/titulos/bulk", response_model=List[TituloOutput], status_code=201)
def create_bulk(bulk: BulkInput):
    """POST 2 – Criar múltiplos títulos em lote (bulk create)"""
    if not bulk.titulos:
        raise HTTPException(status_code=400, detail="Lista de títulos vazia")

    conn    = get_conn()
    cursor  = conn.cursor()
    criados = []
    for item in bulk.titulos:
        cursor.execute(
            """INSERT INTO Titulos (titulo, tipo, genero, ano, classificacao, descricao)
               OUTPUT INSERTED.*
               VALUES (?, ?, ?, ?, ?, ?)""",
            item.titulo, item.tipo, item.genero,
            item.ano, item.classificacao, item.descricao
        )
        criados.append(row_to_dict(cursor.fetchone()))
    conn.commit()
    conn.close()
    return criados

# -----------------------
# PUT (2 endpoints)
# -----------------------

@app.put("/titulos/{titulo_id}", response_model=TituloOutput)
def update_titulo(titulo_id: int, titulo: TituloInput):
    """PUT 1 – Atualizar completamente um título (substituição total)"""
    conn   = get_conn()
    cursor = conn.cursor()
    if not get_titulo_by_id(cursor, titulo_id):
        conn.close()
        raise HTTPException(status_code=404, detail="Título não encontrado")

    cursor.execute(
        """UPDATE Titulos
           SET titulo=?, tipo=?, genero=?, ano=?, classificacao=?, descricao=?
           OUTPUT INSERTED.*
           WHERE id=?""",
        titulo.titulo, titulo.tipo, titulo.genero,
        titulo.ano, titulo.classificacao, titulo.descricao, titulo_id
    )
    atualizado = cursor.fetchone()
    conn.commit()
    conn.close()
    return row_to_dict(atualizado)

@app.put("/titulos/{titulo_id}/titulo", response_model=TituloOutput)
def update_titulo_nome(titulo_id: int, patch: TituloPatch):
    """PUT 2 – Atualizar parcialmente (apenas o nome do título)"""
    conn   = get_conn()
    cursor = conn.cursor()
    if not get_titulo_by_id(cursor, titulo_id):
        conn.close()
        raise HTTPException(status_code=404, detail="Título não encontrado")

    cursor.execute(
        "UPDATE Titulos SET titulo=? OUTPUT INSERTED.* WHERE id=?",
        patch.titulo, titulo_id
    )
    atualizado = cursor.fetchone()
    conn.commit()
    conn.close()
    return row_to_dict(atualizado)

# -----------------------
# DELETE (2 endpoints)
# -----------------------

@app.delete("/titulos/{titulo_id}", status_code=204)
def delete_titulo(titulo_id: int):
    """DELETE 1 – Remover um título pelo ID"""
    conn   = get_conn()
    cursor = conn.cursor()
    if not get_titulo_by_id(cursor, titulo_id):
        conn.close()
        raise HTTPException(status_code=404, detail="Título não encontrado")

    cursor.execute("UPDATE Titulos SET ativo=0 WHERE id=?", titulo_id)
    conn.commit()
    conn.close()

@app.delete("/titulos", status_code=200)
def delete_all_titulos():
    """DELETE 2 – Remover todos os títulos (endpoint administrativo)"""
    conn   = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE Titulos SET ativo=0 WHERE ativo=1")
    afetados = cursor.rowcount
    conn.commit()
    conn.close()
    return {"message": f"{afetados} título(s) removido(s)"}