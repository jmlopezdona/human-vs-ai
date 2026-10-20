# Locuciones del modo vídeo / Video mode narration

Los ficheros de `es-ES/`, `es-419/` y `en/` son la voz del narrador del modo
vídeo en español de España, español de Latinoamérica e inglés. Se generaron con
dos modelos, sin clonar a ninguna persona:

1. **La voz**, diseñada a partir de una descripción con
   [Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign)
   (Apache-2.0).
2. **Cada frase**, dicha con esa voz como timbre por
   [IndexTTS-2.5](https://huggingface.co/IndexTeam/IndexTTS-2.5), sobre
   [audio.cpp](https://github.com/0xShug0/audio.cpp) (Apache-2.0). `es-419/` y
   `en/` usan los pesos oficiales (en el GGUF `f16` de audio.cpp). `es-ES/` usa
   una obra derivada de ellos: el GPT ajustado con un LoRA, entrenado con
   doblaje al español de España, y fusionado (el modelo
   `ajustado-es-ES` de la mesa de doblaje).

Lo que produce IndexTTS-2.5 es una obra derivada del modelo según la
**bilibili Model Use License Agreement**, así que estas locuciones **no** se
publican bajo CC BY 4.0 como el resto del contenido: se rigen por ese acuerdo,
cuya copia está en [`LICENSE-IndexTTS.txt`](LICENSE-IndexTTS.txt). Quien las
copie o las redistribuya tiene que cumplirlo y conservar este aviso y esa copia.

> Any modifications made to the original model in this Derivative Work are not
> endorsed, warranted, or guaranteed by the original right-holder of the
> original model, and the original right-holder disclaims all liability related
> to this Derivative Work.

Los textos que dicen son los de la página (CC BY 4.0) y están en
[`../narracion/guion.json`](../narracion/guion.json).

---

The files in `es-ES/`, `es-419/` and `en/` are the narrator's voice for the
video mode (Spain Spanish, Latin American Spanish and English), generated with
Qwen3-TTS VoiceDesign (voice designed from a text description, Apache-2.0) and
IndexTTS-2.5: the official weights for `es-419/` and `en/`, and a fine-tuned
derivative (LoRA trained on Spain Spanish dubbing, merged) for
`es-ES/`. IndexTTS-2.5 outputs
are Derivative Works under the **bilibili Model Use License Agreement**, so
these recordings are **not** licensed under CC BY 4.0: they are governed by
that agreement, a copy of which is in [`LICENSE-IndexTTS.txt`](LICENSE-IndexTTS.txt).
