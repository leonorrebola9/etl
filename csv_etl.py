import csv
import os

input_file = "clientes.csv"
output_file = "clientes_limpo.csv"
log_file = "erros.log"

colunas_esperadas = 4
dados_limpos = []

salarios_validos = []
idades_validas = []


# --- Funções de limpeza ---
def limpar_texto(texto):
    # remover vírgulas e aspas do nome, normalizar espaços
    texto = texto.replace(",", " ")
    texto = texto.replace('"', "")
    return " ".join(texto.strip().split())


def normalizar_numero(valor):
    valor = valor.strip()
    if valor == "":
        return None
    valor = valor.replace(".", "").replace(",", ".")
    try:
        return float(valor)
    except:
        return None


def normalizar_inteiro(valor):
    valor = valor.strip()
    return int(valor) if valor.isdigit() else None


with open(input_file, "r", encoding="latin-1") as f, open(log_file, "w", encoding="utf-8") as log:

    for numero_linha, linha in enumerate(f, start=1):

        linha = linha.strip()

        if not linha:
            log.write(f"Linha {numero_linha}: vazia.\n")
            continue

        # ignorar header
        if numero_linha == 1:
            continue

        # detectar delimitador
        delimitador = ";" if linha.count(";") > linha.count(",") else ","

        try:
            reader = csv.reader([linha], delimiter=delimitador, quotechar='"')
            campos = next(reader)

            if len(campos) < colunas_esperadas:
                while len(campos) < 4:
                    campos.append("")
                log.write(f"Linha {numero_linha}: colunas a menos.\n")

            if len(campos) > colunas_esperadas:
                # juntar as partes do nome
                id_v = campos[0]
                salario = campos[-1]
                idade = campos[-2]
                nome_partes = campos[1:-2]
                nome = " ".join(nome_partes)
                campos = [id_v, nome, idade, salario]
                log.write(f"Linha {numero_linha}: colunas a mais detectadas, nome corrigido.\n")

            # ---------------- ID ----------------
            id_v = campos[0].strip()

            # ---------------- NOME ----------------
            nome = limpar_texto(campos[1])
            if not nome:
                nome = "N/A"
                log.write(f"Linha {numero_linha}: nome vazio corrigido.\n")

            # ---------------- IDADE ----------------
            idade = "".join(filter(str.isdigit, campos[2]))
            if not idade:
                idade = None
                log.write(f"Linha {numero_linha}: idade inválida corrigida.\n")
            else:
                idade = int(idade)
                idades_validas.append(idade)

            # ---------------- SALARIO ----------------
            sal_raw = campos[3].replace('"', "").strip()
            if "." in sal_raw and "," in sal_raw:
                sal_raw = sal_raw.replace(".", "")
            sal_raw = sal_raw.replace(",", ".")
            try:
                salario = float(sal_raw)
                salarios_validos.append(salario)
            except:
                salario = None
                log.write(f"Linha {numero_linha}: salário inválido corrigido.\n")

            dados_limpos.append([id_v, nome, idade, salario])

        except Exception:
            log.write(f"Linha {numero_linha}: erro de parsing -> {linha}\n")


# calcular médias
media_idade = sum(idades_validas) / len(idades_validas) if idades_validas else 0
media_salario = sum(salarios_validos) / len(salarios_validos) if salarios_validos else 0

# substituir valores inválidos pela média
for linha in dados_limpos:
    if linha[2] is None or linha[2] <= 0:
        linha[2] = round(media_idade)
    if linha[3] is None or linha[3] <= 0:
        linha[3] = round(media_salario, 2)

# escrever CSV limpo
with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["ID", "Nome", "Idade", "Salario"])
    writer.writerows(dados_limpos)

print("Processo concluído.")
print(f"Idade média usada: {round(media_idade)}")
print(f"Salário médio usado: {round(media_salario, 2)}")
print("Ficheiro limpo criado:", output_file)
print("Log criado:", log_file)