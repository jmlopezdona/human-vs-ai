"""Dice con IndexTTS, el motor `indextts` de la mesa de doblaje, las frases
de `guion.json` en una de sus voces, con la voz diseñada como timbre.

Usa el motor sin la mesa: su runtime, su receta de fábrica y su unión de
referencias. El español de España va con el modelo `ajustado-es-ES`, con
`duration_factor` 1 (el motor le recomienda 1,10, que lo deja más lento); el de Latinoamérica
y el inglés, con el modelo `base`, que en español sesea. Una entrada del
guion con tercer campo se dice en dos tomas unidas con una pausa: delante, ese
campo, que es el título del paso en el primer subtítulo y el aviso
(«¡Cuidado!») en el de «Con cuidado»; detrás, el texto. Leídos de corrido, el
modelo no hace la pausa. Cómo se dice el aviso de cada voz sale de
`probar_avisos.py` y `parecido_de_voz.py`; el título va igual. Una toma que acaba cortada se repite
con la semilla siguiente, y un chasquido tras el final se recorta. Reanudable:
lo que ya está en la salida no se repite.

Para rehacer una frase que no ha quedado bien: borrar su .wav de la salida y
volver a llamar con otra semilla, un número que se suma a la de las tomas que
se rehacen, también a la de su título o su aviso. Si sale bien, apúntala en
`semillas` de su voz en POR_VOZ, para que una regeneración completa la repita.

Uso (con MESA_MODELOS, y el paquete del motor y `colas.py` en el PYTHONPATH):
  python sintetizar.py <es-ES|es-419|en> <voz.wav> <salida> [semilla]
"""
import io
import json
import sys
import time
import wave
from pathlib import Path

import numpy as np
from motor_indextts import audio, modelos, runtime
from motor_indextts.manifiesto import EMOCION_DEL_TIMBRE, EMOCIONES, MODELO_AJUSTADO, MODELO_BASE, manifiesto
from motor_indextts.receta import peticion_de_audiocpp

import colas

SEMILLA = 20261020
INTENTOS = 3
PICO = 0.89  # -1 dBFS
# La pausa tras lo que va delante, por subtítulo: tras el título, algo más larga
PAUSAS_S = {"cap": 0.6, "warn": 0.4}
PAUSA_S = PAUSAS_S["warn"]  # la del aviso, que usa probar_avisos.py
# Un texto muy largo se le estropea al modelo hacia el final (en inglés, pasados
# unos 25 s): en el guion se parte con « | », y cada parte va en su toma
CORTE = " | "
PAUSA_CORTE_S = 0.35
SILENCIO_DB = -40.0  # por debajo, respecto al pico, el aviso no suena: se recorta
# Por voz: el texto de `guion.json` que dice, con qué modelo, cómo dice el
# aviso (su vector de emoción, vacío para la del timbre, y lo que se suma a la
# semilla) y las tomas que salieron mal con la semilla de siempre, con lo que
# se suma a la suya para que salgan bien
POR_VOZ = {
    "es-ES": {"guion": "es", "idioma": "es-ES", "modelo": MODELO_AJUSTADO, "duration_factor": 1.0,
              "aviso": {"vector": {}, "semilla": 0},
              # 3-cap: un «el» suelto antes de «Aquí»; 9-cap: partía el título en dos
              # preguntas; 9-idea: «unos» sonaba a «uno»
              "semillas": {"3-cap": 10, "9-cap": 70, "9-idea": 10}},
    "es-419": {"guion": "es", "idioma": "es-419", "modelo": MODELO_BASE, "duration_factor": 1.0,
               "aviso": {"vector": {}, "semilla": 0},
               # 4-idea: decía «Su cerebro»; 8-idea: un chasquido antes de «unos»
               "semillas": {"4-idea": 10, "8-idea": 30}},
    "en": {"guion": "en", "idioma": "en-US", "modelo": MODELO_BASE, "duration_factor": 1.0,
           "aviso": {"vector": {}, "semilla": 0},
           "semillas": {"8-idea": 10}},  # se comía «positions each»
}


def muestras(wav: bytes) -> tuple[np.ndarray, int]:
    with wave.open(io.BytesIO(wav), "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels()).mean(axis=1), w.getframerate()


def recortar(m: np.ndarray, hz: int) -> np.ndarray:
    """Sin el silencio del principio ni del final, para que la pausa sea la pedida."""
    db = colas.envolvente(m, hz)
    suena = np.flatnonzero(db > SILENCIO_DB)
    paso = int(colas.TRAMO_S * hz)
    return colas.fundir(m[suena[0] * paso : (suena[-1] + 1) * paso], hz)


def guardar(m: np.ndarray, hz: int, ruta: Path) -> None:
    m = m * (PICO / max(float(np.abs(m).max()), 1e-6))
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(hz)
        w.writeframes((m * 32767).astype("<i2").tobytes())


class Motor:
    """El servidor de audio.cpp con el modelo y el timbre de una voz."""

    def __init__(self, variante: str, voz: Path, salida: Path) -> None:
        self.ajuste = POR_VOZ[variante]
        guion = json.loads((Path(__file__).parent / "guion.json").read_text(encoding="utf-8"))
        self.frases = guion[self.ajuste["guion"]]
        fabrica = {q.nombre: q.valor_de_fabrica for q in manifiesto().parametros}
        self.receta = {**fabrica, "emo_audio_prompt": EMOCION_DEL_TIMBRE,
                       "duration_factor": self.ajuste["duration_factor"]}
        self.servidor = runtime.Servidor(
            modelos.exigir(modelos.raiz_del_almacen(), self.ajuste["modelo"]), salida / "servidor")
        self.servidor.arrancar()
        self.timbre = audio.escribir_referencia_unida([voz], salida / "timbre")

    def receta_con(self, vector: dict[str, float]) -> dict:
        """La receta con ese vector de emoción; sin vector, la emoción del timbre."""
        if not vector:
            return self.receta
        r = {**self.receta, "use_emo_vector": True}
        return r | {f"emo_vector_{e}": vector.get(e, 0.0) for e in EMOCIONES}

    def decir(self, texto: str, receta: dict, semilla: int = 0) -> tuple[np.ndarray, int, str | None, int]:
        """Una toma: se repite si acaba cortada, y se le quita el chasquido final."""
        for intento in range(INTENTOS):
            peticion = peticion_de_audiocpp(
                receta, texto=texto, idioma=self.ajuste["idioma"], semilla=SEMILLA + semilla + intento,
                timbre=str(self.timbre), original=None)
            m, hz = muestras(self.servidor.sintetizar(peticion))
            final = colas.analizar(m, hz)
            if final["clase"] != "cortada":
                break
        if final["clase"] == "chasquido":
            m = colas.fundir(m[: final["corte"]], hz)
        return m, hz, final["clase"], intento + 1

    def terminar(self) -> None:
        self.servidor.terminar()


def main() -> None:
    variante, voz, salida = sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    otra_semilla = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    (salida / "wav").mkdir(parents=True, exist_ok=True)
    motor = Motor(variante, voz, salida)
    como = motor.ajuste["aviso"]
    avisos: dict[str, np.ndarray] = {}
    try:
        for clave, texto, *antes in motor.frases:
            destino = salida / "wav" / f"{clave}.wav"
            if destino.is_file():
                continue
            t0 = time.monotonic()
            semilla = otra_semilla or motor.ajuste["semillas"].get(clave, 0)
            partes = [motor.decir(t, motor.receta, semilla) for t in texto.split(CORTE)]
            m, hz, final, intentos = partes[0]
            if len(partes) > 1:
                corte = np.zeros(int(PAUSA_CORTE_S * hz), np.float32)
                trozos = [recortar(p[0], hz) for p in partes]
                m = np.concatenate([x for t in trozos for x in (t, corte)][:-1])
                final, intentos = partes[-1][2], max(p[3] for p in partes)
            if antes:
                if antes[0] not in avisos:
                    a, _, _, _ = motor.decir(antes[0], motor.receta_con(como["vector"]), como["semilla"] + semilla)
                    avisos[antes[0]] = recortar(a, hz)
                pausa = np.zeros(int(PAUSAS_S[clave.split("-")[1]] * hz), np.float32)
                m = np.concatenate([avisos[antes[0]], pausa, recortar(m, hz)])
            guardar(m, hz, destino)
            fila = {"clave": clave, "toma_s": round(len(m) / hz, 2), "gpu_s": round(time.monotonic() - t0, 2),
                    "intentos": intentos, "final": final}
            print(json.dumps(fila, ensure_ascii=False), flush=True)
    finally:
        motor.terminar()
    print("FIN", flush=True)


if __name__ == "__main__":
    main()
