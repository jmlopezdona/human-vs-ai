"""Cuánto se parece cada candidato del aviso a la voz del narrador.

La referencia son las frases normales de esa voz (`<salida>/wav/*-cap.wav`).
Para cada audio da la similitud de hablante (coseno de los x-vectors de
WavLM-base-plus-sv con la media de la referencia) y su tono medio (F0, pyin).
Para saber qué es «la misma voz», da también la similitud de cada frase
normal con la media de las demás.

Uso (en un entorno con transformers, librosa y soundfile):
  python parecido_de_voz.py <salida> <carpeta de candidatos>
"""
import json
import sys
from pathlib import Path

import librosa
import numpy as np
import torch
from transformers import AutoFeatureExtractor, WavLMForXVector

MODELO = "microsoft/wavlm-base-plus-sv"
salida, candidatos = Path(sys.argv[1]), Path(sys.argv[2])
extractor = AutoFeatureExtractor.from_pretrained(MODELO)
modelo = WavLMForXVector.from_pretrained(MODELO).eval()


def cargar(ruta: Path) -> np.ndarray:
    return librosa.load(str(ruta), sr=16000, mono=True)[0]


def vector(x: np.ndarray) -> np.ndarray:
    with torch.no_grad():
        e = modelo(**extractor(x, sampling_rate=16000, return_tensors="pt")).embeddings[0].numpy()
    return e / np.linalg.norm(e)


def tono(x: np.ndarray) -> float:
    f0, voz, _ = librosa.pyin(x, fmin=60, fmax=400, sr=16000)
    return round(float(np.nanmedian(f0[voz])), 1) if voz.any() else float("nan")


normales = sorted((salida / "wav").glob("*-cap.wav"))
v = {r.stem: vector(cargar(r)) for r in normales}
media = np.mean(list(v.values()), axis=0)
media /= np.linalg.norm(media)
for r in normales:
    otras = np.mean([e for k, e in v.items() if k != r.stem], axis=0)
    print(json.dumps({"referencia": r.stem, "parecido": round(float(v[r.stem] @ (otras / np.linalg.norm(otras))), 3),
                      "f0": tono(cargar(r))}), flush=True)
for c in sorted(candidatos.glob("*.wav")):
    x = cargar(c)
    print(json.dumps({"candidato": c.stem, "s": round(len(x) / 16000, 2),
                      "parecido": round(float(vector(x) @ media), 3), "f0": tono(x)}), flush=True)
