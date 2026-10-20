# Narración del modo vídeo

La voz del narrador sale de las piezas de la
[mesa de doblaje](https://github.com/jmlopezdona/mesa-de-doblaje), usadas sin la
plataforma, en un PC con Windows y una GPU de NVIDIA (RTX 40):

| Paso | Guion | Qué hace |
|---|---|---|
| 1 | `disenar.cmd` → `disenar.py` | Diseña la voz con el generador `qwen3-voicedesign` (Qwen3-TTS VoiceDesign): la descripción de `guion.json`, dos semillas por idioma |
| 2 | `sintetizar.cmd <voz> <voz.wav>` → `sintetizar.py` | Dice cada frase con el motor `indextts` (IndexTTS-2.5 sobre audio.cpp), con la voz diseñada como timbre; repite las tomas cortadas y recorta los chasquidos del final |
| 3 | `oir.py <voz> <salida>` | Transcribe las tomas con Whisper para comprobar que dicen el guion |
| 3 b | `probar_avisos.py <voz> <voz.wav> <salida>`, `parecido_de_voz.py <salida> <candidatos>` y `oir_avisos.py <voz> <candidatos>` | Genera candidatos del aviso («¡Cuidado!»), mide cuánto se parece su voz a la del narrador (WavLM-base-plus-sv y tono) y los transcribe, para elegir el de `POR_VOZ` |
| 4 | `python3 igualar.py <voz> <carpeta de .wav>` | En el Mac: las pasa a `audio/<voz>/*.mp3` a −18 LUFS e imprime las duraciones, que van en `VOICE_S` de `index.html` |

Hay tres voces, con la misma voz diseñada en los dos españoles:

| Voz | Texto | Modelo de `indextts` |
|---|---|---|
| `es-ES` | Español de España | `ajustado-es-ES`, con `duration_factor` 1 |
| `es-419` | Español de Latinoamérica | `base`, que sesea |
| `en` | Inglés | `base` |

`sintetizar.py` necesita en `lib/` el paquete `motor_indextts`
(`motores/indextts/src`), `mesa_contratos` (`gen/python/src`) y `colas.py` del
spike de vídeo, y los modelos en el almacén de la mesa (`MESA_MODELOS`). Por
SSH, Windows no deja recorrer los enlaces simbólicos de la caché de Hugging
Face (WinError 448): `enlazar.py` deja una copia de la instantánea de Qwen3-TTS
con enlaces duros, en la misma unidad.

Las frases de «Con cuidado» llevan un tercer campo, el aviso («¡Cuidado!»,
«Careful!»): se dice en una toma aparte, con un vector de emoción, y va delante
del resto de la frase con 400 ms de pausa.

El guion (`guion.json`) es el texto de cada subtítulo escrito para decirlo: las
cifras en palabras («diez elevado a ochenta») y sin lo que solo tiene sentido
leyendo («Prueba a mover el control»). Si cambia un texto de la página, hay que
cambiar aquí su frase y volver a generarla.

La licencia de las locuciones está en [`../audio/NOTICE.md`](../audio/NOTICE.md).
