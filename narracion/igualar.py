"""Pasa a .mp3 las tomas de `sintetizar.py`, todas a la misma sonoridad, y
escribe sus duraciones, que `index.html` lleva en `VOICE_S`.

Con el mismo pico, una toma se oye más alta que otra: lo que se iguala es la
sonoridad (LUFS), y un limitador sujeta los picos que la subida saca del tope.

Uso: python3 igualar.py <es-ES|es-419|en> <carpeta con los .wav>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

LUFS = -18.0
TOPE_DB = 6.0
PICO = 0.84  # -1,5 dBFS: el mp3 se pasa un poco del pico de su wav


def sonoridad(wav: Path) -> float:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, check=True).stderr
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", r[r.rindex("Summary:"):])[1])


def duracion(ruta: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ruta)],
                       capture_output=True, text=True, check=True).stdout
    return round(float(r), 2)


lengua, carpeta = sys.argv[1], Path(sys.argv[2])
destino = Path(__file__).resolve().parent.parent / "audio" / lengua
destino.mkdir(parents=True, exist_ok=True)
duraciones = {}
for wav in sorted(carpeta.glob("*.wav"), key=lambda p: [int(p.stem.split("-")[0]), p.stem]):
    sube = min(LUFS - sonoridad(wav), TOPE_DB)
    filtro = f"volume={sube:.2f}dB,alimiter=limit={PICO}:level=false:attack=5:release=50:latency=true"
    mp3 = destino / f"{wav.stem}.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", filtro, "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", "64k", str(mp3)], check=True)
    duraciones[wav.stem] = duracion(mp3)
print(json.dumps(duraciones, separators=(",", ":")))
