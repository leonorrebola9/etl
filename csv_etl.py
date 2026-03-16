import csv

input_file = "clientes.csv"
output_file = "clientes_limpo.csv"
log_file = "erros.log"

colunas_esperadas = 4
dados_limpos = []

salarios_validos = []
idades_validas = []


# Funções de limpeza
def limpar_texto(texto):
    return texto.strip()


def normalizar_numero(valor):
    valor = valor.strip()

    if valor == "":
        return None

    # Converter número europeu para float
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    try:
        return float(valor)
    except:
        return None


def normalizar_inteiro(valor):
    valor = valor.strip()
    if valor.isdigit():
        return int(valor)
    return None


with open(input_file, "r", encoding="latin-1") as f, open(log_file, "w", encoding="utf-8") as log:

    # Usar DictReader ou csv.reader com aspas
    for numero_linha, linha in enumerate(f, start=1):

        linha = linha.strip()

        # Detectar delimitador
        if linha.count(";") > linha.count(","):
            delimitador = ";"
        else:
            delimitador = ","

        try:
            # Usar csv.reader corretamente para lidar com aspas
            reader = csv.reader([linha], delimiter=delimitador, quotechar='"')
            campos = next(reader)

            if len(campos) != colunas_esperadas:
                log.write(f"Linha {numero_linha}: número errado de colunas -> {linha}\n")
                continue

            campos = [c.strip() for c in campos]

            id_cliente = campos[0] if campos[0] else "0"
            nome = limpar_texto(campos[1]) if campos[1] else "N/A"

            idade = normalizar_inteiro(campos[2])
            salario = normalizar_numero(campos[3])

            # Guardar valores válidos
            if idade is not None and idade > 0:
                idades_validas.append(idade)

            if salario is not None and salario > 0:
                salarios_validos.append(salario)

            dados_limpos.append([id_cliente, nome, idade, salario])

        except Exception:
            log.write(f"Linha {numero_linha}: erro de parsing -> {linha}\n")


# Calcular médias
media_idade = sum(idades_validas) / len(idades_validas) if idades_validas else 0
media_salario = sum(salarios_validos) / len(salarios_validos) if salarios_validos else 0


# Substituir valores inválidos
for linha in dados_limpos:
    if linha[2] is None or linha[2] <= 0:
        linha[2] = round(media_idade)
    if linha[3] is None or linha[3] <= 0:
        linha[3] = round(media_salario, 2)


# Guardar CSV limpo
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["ID", "Nome", "Idade", "Salario"])
    writer.writerows(dados_limpos)


print("Processo concluído.")
print("Idade média usada:", round(media_idade))
print("Salário médio usado:", round(media_salario, 2))
print("Ficheiro limpo criado:", output_file)
print("Erros registados em:", log_file)