from bs4 import BeautifulSoup
import json

with open("pagina.xml", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

produtos = []
erros = []

for p in soup.find_all("div", class_="produto"):

    nome_tag = p.find("span", class_="nome")
    preco_tag = p.find("span", class_="preco")

    if not nome_tag or not preco_tag:
        erros.append("Produto ignorado: dados incompletos")
        continue

    nome = nome_tag.text.strip()
    preco = preco_tag.text.strip()

    try:
        preco = float(preco)
    except:
        erros.append(f"Preço inválido: {preco}")
        continue

    produtos.append({
        "nome": nome,
        "preco": preco
    })

with open("produtos.json", "w", encoding="utf-8") as f:
    json.dump(produtos, f, indent=2, ensure_ascii=False)

with open("erros.log", "w", encoding="utf-8") as f:
    for e in erros:
        f.write(e + "\n")