# AGENTS.md

Guía para agentes de IA que trabajen en este repositorio. Para qué es el
proyecto y cómo verlo, lee el [`README.md`](README.md); aquí está lo que hace
falta para cambiarlo sin romperlo.

## En una frase

Una visualización estática, en un solo `index.html` (HTML, CSS y JavaScript sin
compilar ni dependencias), que compara contando ceros a un humano con un modelo
de lenguaje. Se publica en GitHub Pages desde `main`. Tiene un modo vídeo con un
narrador grabado (`audio/`) y música generada en el navegador.

## Reglas del proyecto

- **Todo en español:** textos, comentarios del código, mensajes de commit y
  documentación. El inglés solo como segunda lengua de la página (`T.en`).
- **Sin paso de compilación ni dependencias.** Lo único externo son las fuentes
  de Google Fonts y los iconos de Tabler (`@tabler/icons-webfont@3.19.0`,
  clases `ti ti-*`). No añadas bibliotecas.
- **El rigor manda.** Cada cifra tiene su fuente en la lista «Fuentes» de la
  página. Si cambias una cifra, verifica la fuente y actualiza todos los sitios
  donde aparece (ver «Cambiar una cifra»).
- **Las locuciones dicen lo que se ve.** Cambiar un texto de un paso obliga a
  cambiar su frase en `narracion/guion.json` y a regenerar su audio (ver
  «Narración»). Si no puedes regenerarlo, dilo: la voz no coincidirá con el
  subtítulo.

## Mapa de `index.html`

El script está dividido en secciones con comentarios `/* ---------- … ---------- */`:

| Sección | Qué hay |
|---|---|
| Datos numéricos | `BANDS` (alejamiento), `STEPS` (los 10 pasos: tipo y ceros de cada lado), `ROWS` (la tabla: grupo y ceros) |
| Textos | `T.es` y `T.en`: cada paso (`phase`, `title`, `caption`, `idea`, `warn`, `hu`, `ia`, `label`), filas de la tabla (`rows`), referencias (`bands`) y la interfaz (`ui`) |
| Exponentes | `supify`: convierte ⁰¹²³⁴⁵⁶⁷⁸⁹ de los textos en `<sup>` |
| Fase 1 y 2 | El cara a cara (`renderDuel`) y el alejamiento con zoom (`renderZoom`) |
| Altura fija | `lockHeights`: mide todos los pasos y fija la altura máxima para que nada salte. En móvil (≤ 760 px) no se fija |
| Navegación | `go`, y el modo vídeo: `beatsOf`, `VOICE_S`, `beatMs`, `stepDone` |
| Sonido del modo vídeo | `sound` (estado), `voice` (locuciones), `music` (Web Audio), `renderSound` y los botones |
| Aplicar idioma | `applyLang` y el selector ES/LATAM/EN |

Invariantes que no se ven a simple vista:

- **La interfaz en español sale del HTML.** `T.es.ui` se rellena al cargar con
  el contenido de los elementos `data-i18n` y `data-i18n-aria`. Un texto de la
  interfaz se cambia en el HTML (español) y en `T.en.ui` (inglés).
- **Los índices van alineados.** `T.*.steps[k]` corresponde a `STEPS[k]` y
  `T.*.rows[k]` a `ROWS[k]`. Para añadir o quitar un paso o una fila hay que
  tocarlo en los tres sitios y en los dos idiomas.
- **El modo vídeo tiene tres subtítulos por paso** (`cap`, `idea` y `warn`), y
  cada uno avanza cuando ha pasado su tiempo **y** ha terminado su locución.
  Con la voz puesta, su tiempo es la duración de `VOICE_S` más 900 ms; sin
  ella, `readMs` según la longitud del texto.
- **Pausar no es parar.** `pauseAuto` guarda en `beat` el subtítulo en curso,
  el tiempo que le queda y la locución a medias, y `resumeAuto` sigue desde
  ahí. Salir de pantalla completa también pausa. Parar del todo (`stopAuto`)
  es para lo que cambia de paso, de idioma o de tema. Mientras haya un `beat`
  del paso, un redibujado (`lockHeights` → `backTo`) lo conserva y `stepDone`
  no empieza el paso de nuevo.
- **Idioma y voz son dos cosas.** `lang` (`es` o `en`) elige el texto;
  `voiceEs` (`es-ES` o `es-419`) elige la voz del español. ES y LATAM muestran
  el mismo texto. Los audios están en `audio/<es-ES|es-419|en>/<paso>-<cap|idea|warn>.mp3`.
- **Lo que se guarda en `localStorage`:** `lang`, `voiceEs`, `sound` (voz,
  música, volumen y silencio) y `theme`, siempre dentro de `try`.
- **Los controles de audio solo se ven a pantalla completa** (`.stage.is-fs`).
  En móvil se oculta además la barra de volumen: en iPhone la página no puede
  cambiar el volumen.
- **El audio arranca dentro de un gesto.** `startAuto` llama a `music.start()`
  y `voice.unlock()` dentro del clic o la tecla; todas las locuciones salen del
  mismo elemento de audio para que iPhone las deje sonar.

## Cambiar una cifra

Una cifra suele aparecer en varios sitios, y hay que tocarlos todos, en los dos
idiomas:

1. `STEPS` o `ROWS` (los ceros que se dibujan).
2. El paso en `T.es.steps` y `T.en.steps`: `hu`/`ia`/`label`, y los textos que
   la citan.
3. La fila de la tabla (`T.*.rows`) y las conclusiones del final (`take*` en el
   HTML y en `T.en.ui`).
4. Las fuentes (`s1`…`s14` en el HTML y en `T.en.ui`) y las advertencias (`w*`).
5. La frase hablada en `narracion/guion.json`, y su audio regenerado.

Busca el valor antiguo con `grep` para no dejarte ninguno.

## Narración

El detalle está en [`narracion/README.md`](narracion/README.md). Lo esencial:

- **El guion hablado** (`narracion/guion.json`) tiene una entrada por subtítulo
  e idioma: `[clave, texto]` o `[clave, texto, delante]`. Dice todo lo que se ve, con
  las cifras y fórmulas en palabras («diez elevado a ochenta»), «IA» y «LLM»
  desarrolladas, y los nombres ingleses escritos como suenan en el texto
  español («Golden Gueit», «Clod tres Sónet», «Jáiku»). El tercer campo se
  dice en una toma aparte y se une al texto con una pausa, porque leído de
  corrido el modelo no la hace: en el primer subtítulo de cada paso es el
  **título** del paso (600 ms), para que el oyente siga el hilo, y en «Con
  cuidado» es el **aviso**, «¡Cuidado!» o «Careful!» (400 ms). Van sin vector
  de emoción, porque un vector cambia el timbre. Si cambias el título de un
  paso, cambia también su tercer campo.
- **Las locuciones se generan en el PC de juegos** de la persona usuaria
  (`ssh pc-juegos`, Windows, RTX 4090), con las piezas de la
  [mesa de doblaje](https://github.com/jmlopezdona/mesa-de-doblaje): voz
  diseñada con Qwen3-TTS VoiceDesign y frases con IndexTTS-2.5
  (`ajustado-es-ES` para España, `base` para Latinoamérica e inglés, todo con
  `duration_factor` 1). La carpeta de trabajo es
  `C:\Users\Jose\Development\humano-ia-voces`.
- **Antes de usar la GPU**, comprueba con `nvidia-smi` que está libre: en ese
  PC trabajan otros proyectos y otros agentes. No mates procesos ajenos. El
  almacén de modelos de la mesa (`D:\mesa-modelos`) solo se lee.
- **Para rehacer una frase:** cambia `guion.json`, copia lo que cambie al PC,
  borra el `.wav` de esa clave en `tomas-<voz>\wav`, vuelve a ejecutar
  `sintetizar.cmd <voz> <voz.wav> [semilla]` (es reanudable), compruébala con
  `oir.py`, y en el Mac pásala a MP3 con `igualar.py` y copia las duraciones
  que imprime en `VOICE_S`. Si Whisper oye otra cosa (palabras cambiadas,
  finales raros, una pregunta partida en dos), repite con otra semilla y, si
  sale bien, apúntala en `semillas` de su voz en `POR_VOZ`
  (`narracion/sintetizar.py`), para que una regeneración completa la repita.
- **Whisper escribe las cifras con dígitos**, así que la similitud con el guion
  baja aunque la toma esté bien. Lee la transcripción; no te fíes solo del número.

## Licencias

- Código: MIT (`LICENSE`). Textos e imágenes: CC BY 4.0 (`LICENSE-CONTENT.md`).
- **Las locuciones no son CC BY.** Lo que produce IndexTTS-2.5 es obra derivada
  según la bilibili Model Use License Agreement: `audio/NOTICE.md` y
  `audio/LICENSE-IndexTTS.txt` tienen que acompañarlas siempre. La voz de
  España sale de un modelo ajustado con doblaje de videojuegos; la decisión de
  publicarla es de la persona usuaria.

## Verificar un cambio

No hay batería de pruebas. Como mínimo:

```bash
# Sintaxis del script
node -e "const s=require('fs').readFileSync('index.html','utf8');new Function(s.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/)[1]);console.log('ok')"
# Servirlo, como en GitHub Pages
python3 -m http.server 8000
```

Y en un navegador sin interfaz (Playwright con Chromium), comprobar que no hay
errores en la consola, que el paso tocado se ve bien en claro y en oscuro, a
1440 px y a 375 px, sin desplazamiento horizontal, y, si tocaste el modo vídeo,
que las locuciones suenan en orden. El único 404 esperado es `favicon.ico`.

## Git

- Commits en español, con un título corto y una lista de cambios, como los del
  historial. Añade las rutas explícitas, nunca `git add -A`.
- `main` se publica sola en GitHub Pages (Settings → Pages: rama `main`,
  carpeta raíz; `.nojekyll` evita que Jekyll procese el sitio). Haz commit y
  push solo cuando la persona usuaria lo pida.
- Las etiquetas para compartir (`og:url`, `og:image`, `twitter:image`) y
  `og-image.png` apuntan a `https://jmlopezdona.github.io/human-vs-ai/`: si
  cambia la dirección, actualízalas.
- No subas nada temporal: las tomas `.wav`, los candidatos y las pruebas se
  quedan en el PC o en una carpeta temporal.
