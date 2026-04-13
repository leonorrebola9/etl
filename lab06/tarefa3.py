import hashlib
import hmac
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

# ================================================================
# PARTE 1 — Hash SHA-256
# ================================================================
print("=" * 60)
print("PARTE 1 — SHA-256")
print("=" * 60)

conteudo_original = b"Este e o meu contrato importante."
conteudo_alterado = b"Este e o meu contrato importanteX"  # 1 byte diferente

hash_original = hashlib.sha256(conteudo_original).hexdigest()
hash_alterado  = hashlib.sha256(conteudo_alterado).hexdigest()

print(f"Conteúdo original : {conteudo_original}")
print(f"Hash original     : {hash_original}")
print(f"Conteúdo alterado : {conteudo_alterado}")
print(f"Hash alterado     : {hash_alterado}")
print(f"Hashes iguais?    : {hash_original == hash_alterado}")

# ================================================================
# PARTE 2 — HMAC
# ================================================================
print("\n" + "=" * 60)
print("PARTE 2 — HMAC")
print("=" * 60)

chave_secreta = b"chave-super-secreta"

def gerar_hmac(chave, mensagem):
    return hmac.new(chave, mensagem, hashlib.sha256).hexdigest()

hmac_original = gerar_hmac(chave_secreta, conteudo_original)
hmac_alterado  = gerar_hmac(chave_secreta, conteudo_alterado)
hmac_chave_errada = gerar_hmac(b"chave-errada", conteudo_original)

print(f"HMAC (original)      : {hmac_original}")
print(f"HMAC (conteúdo alt.) : {hmac_alterado}")
print(f"HMAC (chave errada)  : {hmac_chave_errada}")
print(f"Verificação OK?      : {hmac.compare_digest(hmac_original, gerar_hmac(chave_secreta, conteudo_original))}")
print(f"Chave errada OK?     : {hmac.compare_digest(hmac_original, hmac_chave_errada)}")

# ================================================================
# PARTE 3 — Assinatura Digital RSA
# ================================================================
print("\n" + "=" * 60)
print("PARTE 3 — Assinatura Digital RSA")
print("=" * 60)

# Gerar par de chaves
chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
chave_publica = chave_privada.public_key()

# Assinar
assinatura = chave_privada.sign(
    conteudo_original,
    padding.PKCS1v15(),
    hashes.SHA256()
)
print(f"Assinatura gerada (primeiros 32 bytes): {assinatura[:32].hex()}...")

# Verificar — conteúdo original
try:
    chave_publica.verify(assinatura, conteudo_original, padding.PKCS1v15(), hashes.SHA256())
    print("Verificação (original)  : ✅ Assinatura válida!")
except InvalidSignature:
    print("Verificação (original)  : ❌ Assinatura inválida!")

# Verificar — conteúdo alterado
try:
    chave_publica.verify(assinatura, conteudo_alterado, padding.PKCS1v15(), hashes.SHA256())
    print("Verificação (alterado)  : ✅ Assinatura válida!")
except InvalidSignature:
    print("Verificação (alterado)  : ❌ Assinatura inválida!")