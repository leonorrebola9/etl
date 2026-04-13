import os
import wave
import subprocess

os.makedirs("output/audio", exist_ok=True)

def run(cmd):
    subprocess.run(cmd, shell=True, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

WAV = r"C:/Programming/2º ano/2º semestre/ETL/etl/etl/lab05/audio.wav"

# ── Inspecionar WAV original ──────────────────────────────
with wave.open(WAV) as wf:
    rate    = wf.getframerate()
    canais  = wf.getnchannels()
    bits    = wf.getsampwidth() * 8
    duracao = wf.getnframes() / rate

print(f"Sample rate : {rate} Hz")
print(f"Canais      : {canais}")
print(f"Bits/sample : {bits} bits")
print(f"Duração     : {duracao:.2f} s")
print(f"Tamanho     : {os.path.getsize(WAV)/1024:.1f} KB")

# ── Converter WAV → MP3 128 kbps e 320 kbps ──────────────
run(f'ffmpeg -i "{WAV}" -codec:a libmp3lame -b:a 128k output/audio/audio_128kbps.mp3 -y')
run(f'ffmpeg -i "{WAV}" -codec:a libmp3lame -b:a 320k output/audio/audio_320kbps.mp3 -y')

# ── Converter WAV → FLAC (lossless) ──────────────────────
run(f'ffmpeg -i "{WAV}" -codec:a flac output/audio/audio_lossless.flac -y')

# ── Tabela de tamanhos ────────────────────────────────────
ficheiros = {
    "WAV original (lossless)" : WAV,
    "MP3 128 kbps (lossy)"    : "output/audio/audio_128kbps.mp3",
    "MP3 320 kbps (lossy)"    : "output/audio/audio_320kbps.mp3",
    "FLAC (lossless)"         : "output/audio/audio_lossless.flac",
}
print(f"\n{'Formato':<26} {'Tamanho (KB)':>12}")
print("-" * 39)
for label, path in ficheiros.items():
    print(f"{label:<26} {os.path.getsize(path)/1024:>11.1f}")

wav_kb  = os.path.getsize(WAV) / 1024
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