-- consultar base de dados toda
select * from wikipedia;

-- top 10 artigos com mais conteúdo
SELECT TOP 10
    title,
    LEN(CAST(text AS VARCHAR(MAX))) AS tamanho_texto
FROM wikipedia
ORDER BY tamanho_texto DESC;

-- top 5 páginas com mais links
SELECT TOP 5
    title,
    LEN(CAST(links AS VARCHAR(MAX))) 
    - LEN(REPLACE(CAST(links AS VARCHAR(MAX)), ';', '')) + 1 AS numero_links
FROM wikipedia
ORDER BY numero_links DESC;

-- top 10 páginas com mais imagens
SELECT TOP 10
    title,
    LEN(CAST(images AS VARCHAR(MAX))) 
    - LEN(REPLACE(CAST(images AS VARCHAR(MAX)), ';', '')) + 1 AS numero_imagens
FROM wikipedia
ORDER BY numero_imagens DESC;

-- estatísticas do tamanho do conteúdo
SELECT
    AVG(LEN(CAST(text AS VARCHAR(MAX)))) AS media_tamanho_texto,
    MIN(LEN(CAST(text AS VARCHAR(MAX)))) AS menor_texto,
    MAX(LEN(CAST(text AS VARCHAR(MAX)))) AS maior_texto
FROM wikipedia;