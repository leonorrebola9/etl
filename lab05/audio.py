import os
from pydub import AudioSegment

os.makedirs("output/audio", exist_ok=True)

AUDIO = r"C:/Programming/2º ano/2º semestre/ETL/etl/etl/lab05/audio.mp4"

# ── Converter AAC/MP4 para WAV base ──────────────────────
audio = AudioSegment.from_file(AUDIO)
audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
audio.export("output/audio/audio_base.wav", format="wav")

# ── Inspecionar WAV gerado ────────────────────────────────
print(f"Sample rate : {audio.frame_rate} Hz")
print(f"Canais      : {audio.channels} (estéreo)")
print(f"Bits/sample : {audio.sample_width * 8} bits")
print(f"Duração     : {len(audio)/1000:.2f} s")

# ── Converter WAV → MP3 128 kbps e 320 kbps ──────────────
audio.export("output/audio/audio_128kbps.mp3", format="mp3", bitrate="128k")
audio.export("output/audio/audio_320kbps.mp3", format="mp3", bitrate="320k")

# ── Converter WAV → FLAC (lossless) ──────────────────────
audio.export("output/audio/audio_lossless.flac", format="flac")

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