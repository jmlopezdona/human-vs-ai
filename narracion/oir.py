"""Transcribe con Whisper las tomas de una salida y anota cuánto se parecen al guion.

Uso: python oir.py <es-ES|es-419|en> <salida>
"""
import difflib
import json
import re
import sys
from pathlib import Path

import whisper

lengua, salida = sys.argv[1].split("-")[0], Path(sys.argv[2])
# Una frase con aviso se oye con él delante
guion = {clave: " ".join([*antes, texto.replace(" | ", " ")]) for clave, texto, *antes in
         json.loads((Path(__file__).parent / "guion.json").read_text(encoding="utf-8"))[lengua]}
norma = lambda t: re.sub(r"[^\w\s]", "", t.lower()).split()
modelo = whisper.load_model("turbo", device="cuda")
for clave, texto in guion.items():
    oido = modelo.transcribe(str(salida / "wav" / f"{clave}.wav"), language=lengua, temperature=0.0)["text"].strip()
    parecido = difflib.SequenceMatcher(None, norma(texto), norma(oido)).ratio()
    print(json.dumps({"clave": clave, "parecido": round(parecido, 3), "oido": oido}, ensure_ascii=False), flush=True)
