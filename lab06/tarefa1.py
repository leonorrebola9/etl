import bleach
import re

# --- Abordagem 1: Bleach (remove/escapa tags HTML) ---
def sanitizar_html(texto):
    # Não permite nenhuma tag HTML — remove tudo
    return bleach.clean(texto, tags=[], attributes={}, strip=True)

# --- Abordagem 2: Regex (permite só alfanuméricos + alguns sinais) ---
def sanitizar_regex(texto, permitidos=r"[^a-zA-Z0-9 _.@\-]"):
    return re.sub(permitidos, "", texto)


# Testes
inputs = [
    "<script>alert('XSS')</script>",
    "<b>Olá</b>, chamo-me João!",
    "email@exemplo.com; DROP TABLE users;--",
    "Texto normal com émojis 🎉 e unicode: café",
    "<img src=x onerror=alert(1)>",
]

print("=" * 60)
for inp in inputs:
    print(f"ORIGINAL : {inp}")
    print(f"BLEACH   : {sanitizar_html(inp)}")
    print(f"REGEX    : {sanitizar_regex(inp)}")
    print("-" * 60)