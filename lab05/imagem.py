import os
from PIL import Image, ExifTags

# ── Define o caminho uma vez só ───────────────────────────
IMG = r"C:/Programming/2º ano/2º semestre/ETL/etl/etl/lab05/original.jpg"

img = Image.open(IMG)
print(f"Resolução : {img.width} x {img.height} px")
print(f"Modo cor  : {img.mode}")
print(f"Tamanho   : {os.path.getsize(IMG) / 1024:.1f} KB")

os.makedirs("output/imagens", exist_ok=True)

# ── Converter para PNG (lossless) ─────────────────────────
img.save("output/imagens/imagem_lossless.png", format="PNG")

# ── Converter para JPEG em 3 qualidades ──────────────────
for q in [90, 70, 50]:
    img.save(f"output/imagens/imagem_q{q}.jpg", format="JPEG", quality=q)

# ── Tabela de tamanhos ────────────────────────────────────
ficheiros = {
    "original.jpg" : IMG,
    "PNG lossless"  : "output/imagens/imagem_lossless.png",
    "JPEG 90%"      : "output/imagens/imagem_q90.jpg",
    "JPEG 70%"      : "output/imagens/imagem_q70.jpg",
    "JPEG 50%"      : "output/imagens/imagem_q50.jpg",
}
print(f"\n{'Ficheiro':<25} {'Tamanho (KB)':>12}")
print("-" * 38)
for label, path in ficheiros.items():
    print(f"{label:<25} {os.path.getsize(path)/1024:>11.1f}")

# ── Metadados EXIF ────────────────────────────────────────
print("\nMetadados EXIF:")
exif = img._getexif()
if exif:
    tags_interesse = ["Make", "Model", "DateTime", "GPSInfo", "Software"]
    for tag_id, valor in exif.items():
        nome = ExifTags.TAGS.get(tag_id, str(tag_id))
        if nome in tags_interesse:
            print(f"  {nome:<20}: {valor}")
else:
    print("  (sem dados EXIF)")