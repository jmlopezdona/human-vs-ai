"""Transcribe con Whisper los candidatos del aviso de una carpeta, con su duración.

Uso: python oir_avisos.py <es-ES|es-419|en> <carpeta>
"""
import json
import sys
from pathlib import Path

import wave

import whisper

lengua, carpeta = sys.argv[1].split("-")[0], Path(sys.argv[2])
modelo = whisper.load_model("turbo", device="cuda")
for wav in sorted(carpeta.glob("*.wav")):
    oido = modelo.transcribe(str(wav), language=lengua, temperature=0.0)["text"].strip()
    print(json.dumps({"aviso": wav.stem, "s": round((w := wave.open(str(wav))).getnframes() / w.getframerate(), 2), "oido": oido}, ensure_ascii=False), flush=True)
