import os
import subprocess

os.makedirs("output/video", exist_ok=True)

def run(cmd):
    subprocess.run(cmd, shell=True, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def ffprobe(path, entry):
    r = subprocess.run(
        f'ffprobe -v quiet -show_entries {entry} '
        f'-print_format default=noprint_wrappers=1 "{path}"',
        shell=True, capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if '=' in line:
            return line.split('=', 1)[1].strip()
    return 'N/A'

VIDEO = r"C:/Programming/2º ano/2º semestre/ETL/etl/etl/lab05/video.mp4"

# ── Inspecionar vídeo original ────────────────────────────
print("Vídeo original:")
print(f"  Codec     : {ffprobe(VIDEO, 'stream=codec_name')}")
print(f"  Resolução : {ffprobe(VIDEO, 'stream=width')}x{ffprobe(VIDEO, 'stream=height')}")
print(f"  FPS       : {ffprobe(VIDEO, 'stream=r_frame_rate')}")
print(f"  Bitrate   : {int(ffprobe(VIDEO, 'format=bit_rate'))//1000} kbps")
print(f"  Tamanho   : {os.path.getsize(VIDEO)/1024:.1f} KB")

# ── Converter para H.264 e H.265 ─────────────────────────
run(f'ffmpeg -i "{VIDEO}" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output/video/video_h264.mp4 -y')
run(f'ffmpeg -i "{VIDEO}" -c:v libx265 -crf 28 -preset medium -c:a aac -b:a 128k output/video/video_h265.mp4 -y')

# ── Tabela de comparação ──────────────────────────────────
videos = {
    "Original"       : VIDEO,
    "H.264 (CRF 23)" : "output/video/video_h264.mp4",
    "H.265 (CRF 28)" : "output/video/video_h265.mp4",
}
print(f"\n{'Formato':<20} {'Tamanho (KB)':>13} {'Bitrate (kbps)':>15} {'Pixel fmt':>10}")
print("-" * 61)
for label, path in videos.items():
    kb      = os.path.getsize(path) / 1024
    bitrate = int(ffprobe(path, 'format=bit_rate')) // 1000
    pix_fmt = ffprobe(path, 'stream=pix_fmt')
    print(f"{label:<20} {kb:>13.1f} {bitrate:>15} {pix_fmt:>10}")

# ── Subsampling de croma ──────────────────────────────────
print("\nSubsampling de croma:")
for label, path in videos.items():
    fmt = ffprobe(path, 'stream=pix_fmt')
    if   "420" in fmt: sub = "4:2:0 — chroma reduzida em X e Y (streaming)"
    elif "422" in fmt: sub = "4:2:2 — chroma reduzida em X"
    elif "444" in fmt: sub = "4:4:4 — sem subsampling (máxima qualidade)"
    else:              sub = fmt
    print(f"  {label:<20}: {sub}")