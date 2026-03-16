import json

with open("produtos.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)

produtos_ok = []
erros = []

for p in produtos:

    # verificar campos obrigatórios
    if "id" not in p or "nome" not in p or "preco" not in p:
        erros.append({"produto": p, "erro": "campo obrigatório em falta"})
        continue

    # validar preco
    preco = p["preco"]

    if isinstance(preco, str):
        preco = preco.replace(",", ".")
        try:
            preco = float(preco)
        except:
            erros.append({"produto": p, "erro": "preco inválido"})
            continue

    p["preco"] = preco

    # validar categoria
    if "categoria" not in p or p["categoria"] is None:
        p["categoria"] = "Desconhecida"

    # validar variantes
    if "variantes" in p:
        if isinstance(p["variantes"], str):
            p["variantes"] = p["variantes"].split(",")
        elif not isinstance(p["variantes"], list):
            erros.append({"produto": p, "erro": "variantes inválido"})
            continue
    else:
        p["variantes"] = []

    produtos_ok.append(p)

# guardar json final
with open("produtos_ok.json", "w", encoding="utf-8") as f:
    json.dump(produtos_ok, f, indent=2, ensure_ascii=False)

# guardar log
with open("log_erros.json", "w", encoding="utf-8") as f:
    json.dump(erros, f, indent=2, ensure_ascii=False)

print("Processamento concluído!")