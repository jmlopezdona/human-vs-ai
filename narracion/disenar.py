"""Diseña la voz del narrador con Qwen3-TTS VoiceDesign, el generador
`qwen3-voicedesign` de la mesa de doblaje, en español y en inglés.

Lee la descripción, los textos de muestra y las semillas de `guion.json`.
Reanudable: lo que ya está en `voces/` no se repite.

Uso (en el entorno de qwen-tts):
  python disenar.py
"""
import json
from pathlib import Path

import soundfile as sf
import torch

from qwen_tts import Qwen3TTSModel

# La revisión que fija el generador (5ecdb67), del almacén de modelos de la
# mesa. Por SSH, Windows no deja recorrer sus enlaces simbólicos (WinError
# 448): `enlazar.py` deja una copia con enlaces duros a los mismos ficheros.
MODELO = r"D:\humano-ia-voces-modelo\qwen3-voicedesign"
IDIOMAS = {"es": "Spanish", "en": "English"}
AQUI = Path(__file__).parent
SALIDA = AQUI / "voces"
SALIDA.mkdir(exist_ok=True)
voz = json.loads((AQUI / "guion.json").read_text(encoding="utf-8"))["voz"]

modelo = Qwen3TTSModel.from_pretrained(
    MODELO, device_map="cuda:0", dtype=torch.bfloat16, attn_implementation="sdpa")
for idioma, nombre in IDIOMAS.items():
    for semilla in voz["semillas"]:
        destino = SALIDA / f"narrador-{idioma}-s{semilla}.wav"
        if destino.exists():
            continue
        torch.manual_seed(semilla)
        torch.cuda.manual_seed_all(semilla)
        ondas, frecuencia = modelo.generate_voice_design(
            text=voz["muestra"][idioma], language=nombre, instruct=voz["descripcion"])
        sf.write(destino, ondas[0], frecuencia)
        print(destino.name, round(len(ondas[0]) / frecuencia, 2), "s", flush=True)
print("FIN", flush=True)
