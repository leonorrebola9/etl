import os
import wave
import subprocess

os.makedirs("output/audio", exist_ok=True)

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

# ── Converter gravação (AAC/MP4) para WAV base ────────────
# O ficheiro original é uma gravação do WhatsApp em AAC.
# Convertemos para WAV 16 bits, 44.1 kHz, estéreo.
AUDIO = r"C:/Programming/2º ano/2º semestre/ETL/etl/etl/lab05/audio.mp4"

run(f'ffmpeg -i "{AUDIO}" -ar 44100 -ac 2 -sample_fmt s16 output/audio/audio_base.wav -y')

# ── Inspecionar WAV gerado ────────────────────────────────
with wave.open("output/audio/audio_base.wav") as wf:
    rate    = wf.getframerate()
    canais  = wf.getnchannels()
    bits    = wf.getsampwidth() * 8
    duracao = wf.getnframes() / rate

print(f"Sample rate : {rate} Hz")
print(f"Canais      : {canais} (estéreo)")
print(f"Bits/sample : {bits} bits")
print(f"Duração     : {duracao:.2f} s")

# ── Converter WAV → MP3 128 kbps e 320 kbps ──────────────
run("ffmpeg -i output/audio/audio_base.wav -codec:a libmp3lame -b:a 128k output/audio/audio_128kbps.mp3 -y")
run("ffmpeg -i output/audio/audio_base.wav -codec:a libmp3lame -b:a 320k output/audio/audio_320kbps.mp3 -y")

# ── Converter WAV → FLAC (lossless) ──────────────────────
run("ffmpeg -i output/audio/audio_base.wav -codec:a flac output/audio/audio_lossless.flac -y")

# ── Tabela de tamanhos ────────────────────────────────────
ficheiros = {
    "WAV base (lossless)"   : "output/audio/audio_base.wav",
    "MP3 128 kbps (lossy)"  : "output/audio/audio_128kbps.mp3",
    "MP3 320 kbps (lossy)"  : "output/audio/audio_320kbps.mp3",
    "FLAC (lossless)"       : "output/audio/audio_lossless.flac",
}
print(f"\n{'Formato':<25} {'Tamanho (KB)':>12}")
print("-" * 38)
for label, path in ficheiros.items():
    print(f"{label:<25} {os.path.getsize(path)/1024:>11.1f}")

wav_kb  = os.path.getsize("output/audio/audio_base.wav") / 1024
flac_kb = os.path.getsize("output/audio/audio_lossless.flac") / 1024
print(f"\nTaxa de compressão FLAC vs WAV: {wav_kb/flac_kb:.2f}x")

# ── Tags ID3 ──────────────────────────────────────────────
run('ffmpeg -i output/audio/audio_320kbps.mp3 '
    '-metadata title="Lab 05 Audio" '
    '-metadata artist="ETD @ UBI" '
    '-metadata album="Lab Multimedia" '
    '-codec copy output/audio/audio_tagged.mp3 -y')

result = subprocess.run(
    'ffprobe -v quiet -show_entries format_tags -print_format flat output/audio/audio_tagged.mp3',
    shell=True, capture_output=True, text=True)
print("\nTags ID3:")
for line in result.stdout.splitlines():
    if "tag" in line:
        print(f"  {line.strip()}")