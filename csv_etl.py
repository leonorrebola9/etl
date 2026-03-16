import csv

input_file = "clientes.csv"
output_file = "clientes_limpo.csv"
log_file = "erros.log"

colunas_esperadas = 4
dados_limpos = []


# --- Funções de limpeza ---
def limpar_texto(texto):
    return texto.strip()


def normalizar_numero(valor):
    valor = valor.strip()

    if valor == "":
        return 0

    # converter número europeu para formato padrão
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    try:
        return float(valor)
    except:
        return 0


def normalizar_inteiro(valor):
    valor = valor.strip()
    return int(valor) if valor.isdigit() else 0


with open(input_file, "r", encoding="latin-1") as f, open(log_file, "w", encoding="utf-8") as log:

    for numero_linha, linha in enumerate(f, start=1):

        linha = linha.strip()

        # Detectar delimitador
        if linha.count(";") > linha.count(","):
            delimitador = ";"
        else:
            delimitador = ","

        try:
            reader = csv.reader([linha], delimiter=delimitador)
            campos = next(reader)

            # Verificar número de colunas
            if len(campos) != colunas_esperadas:
                log.write(f"Linha {numero_linha}: número errado de colunas -> {linha}\n")
                continue

            # Remover espaços extra
            campos = [c.strip() for c in campos]

            # Corrigir campos vazios
            id_cliente = campos[0] if campos[0] else "0"

            nome = limpar_texto(campos[1]) if campos[1] else "N/A"

            idade = normalizar_inteiro(campos[2])

            salario = normalizar_numero(campos[3])

            dados_limpos.append([id_cliente, nome, idade, salario])

        except Exception as e:
            log.write(f"Linha {numero_linha}: erro de parsing -> {linha}\n")


# Guardar CSV limpo
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Nome", "Idade", "Salario"])
    writer.writerows(dados_limpos)

print("Processo concluído.")
print("Ficheiro limpo criado:", output_file)
print("Erros registados em:", log_file)