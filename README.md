# Humano vs IA, contado en ceros

¿Es una IA «más grande» que un cerebro? Depende de lo que contemos. Esta
visualización lo compara todo con una sola regla: **cada punto es un cero**, y
cada punto más multiplica la cifra por diez.

**Verla:** https://jmlopezdona.github.io/human-vs-ai/

## Qué vas a ver

Un viaje en diez pasos:

1. **Cómo leer los puntos:** por qué contamos ceros en lugar de cifras.
2. **Tres comparaciones cara a cara** entre una persona y un modelo de
   lenguaje: palabras, conceptos y hardware. En las dos primeras va por
   delante la IA; en conexiones físicas, el cerebro.
3. **Cinco pasos alejando la cámara:** la edad del universo, los conceptos que
   podría llegar a guardar una IA, los átomos del universo, las formas de
   guardar una palabra y los textos que podría escribir, hasta el millón de
   ceros.
4. **Un resumen** con lo que nos llevamos.

Cada paso tiene un apartado «Para entenderlo mejor», y al final de la página
hay una explicación de los fundamentos, una tabla de magnitudes, advertencias
y las fuentes de cada cifra.

## El modo vídeo

Con **Ver como vídeo** (o la barra espaciadora) el viaje se reproduce solo, a
pantalla completa, como un documental: un narrador lee cada texto y suena una
música de fondo que baja mientras habla. Hay voz de España, de Latinoamérica y
en inglés; se elige con el selector **ES · LATAM · EN** de la cabecera.

A pantalla completa puedes quitar la voz o la música, silenciarlo todo o bajar
el volumen. Sin voz, los textos avanzan a ritmo de lectura. Para salir, Esc.

## Cómo se usa

- Las flechas ← → pasan de un paso a otro, y cada paso tiene su enlace
  (`#paso-3`).
- Está en español y en inglés, con tema claro y oscuro, y se ve bien en el
  móvil.

Para verla en tu ordenador, abre `index.html` en el navegador o sirve la
carpeta:

```bash
python3 -m http.server 8000
# y abre http://localhost:8000
```

## Cómo está hecha

Es una página estática, sin compilar ni instalar nada: todo está en
`index.html`. La música se genera en el propio navegador.

La voz del narrador es sintética y no clona a ninguna persona. Se diseñó a
partir de una descripción con Qwen3-TTS VoiceDesign, y cada frase la dice
IndexTTS-2.5, con las piezas de la
[mesa de doblaje](https://github.com/jmlopezdona/mesa-de-doblaje). Cómo se
generan las locuciones está en [`narracion/`](narracion/README.md).

Si vas a modificar el proyecto, con o sin ayuda de una IA, empieza por
[`AGENTS.md`](AGENTS.md).

## Rigor

Las cifras son órdenes de magnitud aproximados, no medidas exactas, y algunas
comparaciones miden cosas parecidas pero no idénticas. La página dice de dónde
sale cada una: compruébalas antes de citarlas.

## Licencia

Hecho con cariño entre un humano y Claude (una IA).

- **Textos, gráficos e imágenes:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es). Ver [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).
- **Código:** [MIT](LICENSE).
- **Locuciones** (`audio/`): generadas con IndexTTS-2.5, se rigen por la
  bilibili Model Use License Agreement, no por CC BY 4.0. Ver
  [`audio/NOTICE.md`](audio/NOTICE.md).
