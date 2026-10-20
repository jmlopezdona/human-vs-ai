"""Genera candidatos del aviso («¡Cuidado!») de una voz, para elegir uno de
oído y medir cuáles conservan el timbre del narrador (`parecido_de_voz.py`).

Cada candidato es una toma aparte con un vector de emoción (o sin él) y una
semilla, y se guarda suelto y montado en una frase con aviso, como irá en la
página. Además se dice esa frase entera en una sola toma, con «!» y con «!...»,
para oír la pausa que mete el propio modelo. Salen en `<salida>/candidatos`
(sueltos) y `<salida>/candidatos-en-frase`.

Uso (como sintetizar.py): python probar_avisos.py <es-ES|es-419|en> <voz.wav> <salida>
"""
import sys
from pathlib import Path

import numpy as np

import sintetizar as s

variante, voz, salida = sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
CANDIDATOS = {
    **{f"sin-{n + 1}": ({}, n) for n in range(6)},
    "sorpresa-015": ({"sorpresa": 0.15}, 0),
    "alarma-mitad": ({"sorpresa": 0.12, "miedo": 0.1}, 0),
    "alarma": ({"sorpresa": 0.25, "miedo": 0.2}, 0),
    "sorpresa-035": ({"sorpresa": 0.35}, 0),
}
motor = s.Motor(variante, voz, salida)
sueltos, en_frase = salida / "candidatos", salida / "candidatos-en-frase"
sueltos.mkdir(parents=True, exist_ok=True)
en_frase.mkdir(parents=True, exist_ok=True)
clave, texto, aviso = next(f for f in motor.frases if len(f) == 3)
try:
    m, hz, _, _ = motor.decir(texto, motor.receta)
    resto = s.recortar(m, hz)
    pausa = np.zeros(int(s.PAUSA_S * hz), np.float32)
    for nombre, (vector, semilla) in CANDIDATOS.items():
        m, hz, _, _ = motor.decir(aviso, motor.receta_con(vector), semilla)
        a = s.recortar(m, hz)
        s.guardar(a, hz, sueltos / f"{nombre}.wav")
        s.guardar(np.concatenate([a, pausa, resto]), hz, en_frase / f"{nombre}.wav")
        print(nombre, flush=True)
    for nombre, union in {"frase-entera": " ", "frase-puntos": "... "}.items():
        m, hz, _, _ = motor.decir(f"{aviso}{union}{texto}", motor.receta)
        s.guardar(s.recortar(m, hz), hz, en_frase / f"{nombre}.wav")
        print(nombre, flush=True)
finally:
    motor.terminar()
