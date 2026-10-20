# Humano vs IA, contado en ceros

Visualización interactiva que compara, contando ceros, lo que maneja un ser humano, lo que maneja un modelo de lenguaje (LLM) y el espacio teórico en el que trabaja ese modelo. Cada punto es un cero: cada punto más multiplica la cifra por diez.

Sitio 100 % estático (HTML, CSS y JavaScript), sin paso de compilación.

## Estructura

```
.
├── index.html      La visualización completa (HTML, CSS y JS en un solo archivo)
├── audio/          Locuciones del narrador del modo vídeo (es-ES/, es-419/ y en/) y su licencia
├── narracion/      Guion hablado y guiones para generar las locuciones
├── LICENSE         Licencia MIT del código
├── LICENSE-CONTENT.md  Licencia CC BY 4.0 de textos e imágenes
├── og-image.png    Imagen para compartir en redes (1200×630)
├── README.md
└── .nojekyll       Evita que GitHub Pages procese el sitio con Jekyll
```

## Qué incluye

- **10 pasos:** una introducción interactiva para entender la escala de ceros, tres comparaciones cara a cara (palabras, conceptos y hardware), cinco pasos de alejamiento hasta el millón de ceros y un resumen final.
- **Alejamiento con zoom continuo:** todo lo anterior se queda fijo en la esquina. Cada bola lleva un anillo por cada referencia que cuenta ese cero, y al tocar una referencia de la leyenda se resaltan todos sus ceros. En los pasos más grandes, una lupa amplía la esquina.
- **Modo vídeo:** a pantalla completa, con el texto de cada paso, «La idea» y «Con cuidado» como subtítulos y una cuenta atrás en la barra de progreso. Un narrador lee cada subtítulo, con voz de España o de Latinoamérica en español (ES y LATAM en el selector de idioma) o en inglés, y suena una música de fondo que baja mientras habla. La voz y la música se quitan por separado con sus botones, y hay un botón de silencio y un control de volumen para las dos (en móvil, solo el silencio). Estos controles solo aparecen a pantalla completa, y todo se recuerda. Silenciar no quita la voz: los subtítulos siguen su ritmo; sin voz, cada subtítulo dura según su longitud. La duración que muestra el botón se calcula a partir de las locuciones. Esc para salir.
- **Narración:** la voz se diseñó con Qwen3-TTS VoiceDesign y cada frase la dice IndexTTS-2.5, con las piezas de la mesa de doblaje (ver [`narracion/`](narracion/README.md)). La música no es un fichero: se genera en el navegador con Web Audio.
- **Navegación:** con el teclado (← → y espacio) y enlaces directos a cada paso (`#paso-3` o `#step-3`).
- **«Para entenderlo mejor»** en cada paso, y en la página: fundamentos, tabla de magnitudes, advertencias de rigor y fuentes.
- **Bilingüe español/inglés:** se muestra en español si el navegador está en español y en inglés en cualquier otro caso. El selector ES/LATAM/EN de la cabecera permite cambiarlo y la elección se recuerda. ES y LATAM muestran el mismo texto; cambian la voz del narrador, que por defecto es la de España si el navegador está en `es` o `es-ES` y la de Latinoamérica con cualquier otro español.
- **Tema claro/oscuro**, diseño adaptado a móvil, textos alternativos y respeto por la opción de reducir movimiento.

## Verlo en local

Abre `index.html` en el navegador, o sirve la carpeta:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Publicar en GitHub Pages

```bash
git init
git add .
git commit -m "Primera versión"
git branch -M main
git remote add origin https://github.com/jmlopezdona/human-vs-ai.git
git push -u origin main
```

En GitHub: **Settings → Pages → Build and deployment → Deploy from a branch**, rama `main`, carpeta `/ (root)`. En uno o dos minutos estará en `https://jmlopezdona.github.io/human-vs-ai/`.

Las etiquetas para compartir (`og:url`, `og:image` y `twitter:image` en `index.html`) apuntan a `https://jmlopezdona.github.io/human-vs-ai/`. Si publicas el repositorio con otro nombre o en otra cuenta, actualízalas.

## Rigor

Las cifras son órdenes de magnitud aproximados. Consulta la sección de fuentes de la página y verifica cada dato antes de citarlo.

## Licencia

Hecho con cariño entre un humano y Claude (una IA).

- **Contenido** (textos, gráficos e imágenes): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es). Ver [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).
- **Código** (HTML, CSS y JavaScript): [MIT](LICENSE).
- **Locuciones** (`audio/`): generadas con IndexTTS-2.5, se rigen por la bilibili Model Use License Agreement, no por CC BY 4.0. Ver [`audio/NOTICE.md`](audio/NOTICE.md).
