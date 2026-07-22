# CV builder

Genera los PDF del CV (español e inglés) a partir de texto plano (YAML) + [Typst](https://typst.app),
en vez de editar `.docx` a mano. El resultado (`Pablo-Lopez-CV-ES.pdf` / `-EN.pdf`) se publica en la
carpeta de productos del repo, `assets/cv/`.

## Requisitos (una sola vez)

- [Typst](https://typst.app) instalado y accesible (`winget install --id Typst.Typst`).
- [uv](https://docs.astral.sh/uv/) instalado (gestiona el entorno Python de este build, aislado en
  `builders/cv/.venv/` — no toca nada fuera de esta carpeta).

## Uso día a día

Desde esta carpeta (`builders/cv/`):

```
uv run build.py
```

La primera vez, `uv` crea el entorno virtual e instala las dependencias automáticamente. Cada corrida:

1. Compara la estructura de `data/cv_es.yaml` y `data/cv_en.yaml` y avisa si un idioma tiene
   secciones/bullets/certificados que el otro no tiene (posible desincronización).
2. Compila ambos PDFs a `assets/cv/`.

Para editar en vivo (recompila automáticamente al guardar):

```
uv run build.py --watch
```

## Qué editar

Todo el contenido vive en `data/cv_es.yaml` y `data/cv_en.yaml`. `template.typ` es puramente
estructural — no contiene ningún texto de idioma, así que nunca hace falta tocarlo para actualizar
el contenido del CV.

- **Bullets de la experiencia actual**: `experience[0].bullets` en cada YAML. El campo `text`
  admite énfasis con la sintaxis nativa de Typst (`*así se pone en negrita*`).
- **Certificados destacados**: `certificates.highlights`. Reordenar o reemplazar esta lista es la
  forma de destacar certificados distintos; el listado completo sigue viviendo en
  [`CERTIFICATES.md`](../../CERTIFICATES.md).

## Mantener ES y EN sincronizados (con un agente de IA)

`cv_es.yaml` y `cv_en.yaml` comparten exactamente el mismo esquema y el mismo orden de claves/listas
a propósito. Esto hace que un `git diff` sobre uno de los dos sea una referencia posicional exacta
para el otro (ej. `experience[0].bullets[2]`).

Flujo recomendado:

1. Editar y compilar un solo idioma (ej. `cv_es.yaml`), revisar el PDF, hacer commit.
2. Abrir una sesión de Claude Code (u otro agente) y pedir algo como:
   > Revisa el último cambio de git en `builders/cv/data/cv_es.yaml` y replícalo,
   > traducido, en `cv_en.yaml`, manteniendo el mismo orden de claves y bullets.
3. Correr `uv run build.py` de nuevo y revisar que ambos PDFs quedaron equivalentes.

El chequeo de paridad de estructura que corre `build.py` antes de compilar sirve como red de
seguridad: si algún día un idioma queda con más/menos bullets, secciones o certificados que el otro,
te avisa antes de generar el PDF.

## Fuente

`template.typ` pide la fuente en este orden: `Bierstadt` (la del CV original en Word) → `Calibri` →
`Segoe UI` → `Arial`.

Bierstadt/Aptos no se "instalan" como fuente del sistema aunque tengas Microsoft 365 — Office las
descarga como _cloud font_ y las cachea en
`%LOCALAPPDATA%\Microsoft\FontCache\4\CloudFonts\`, visibles solo para apps de Office, no para el
resto de programas (Typst incluido). No hace falta instalar nada a mano ni con `uv` (los venvs de
Python no tienen forma de gestionar fuentes, son una capa completamente distinta al sistema de
fuentes del SO): `build.py` ya apunta a esa carpeta con `typst ... --font-path`, así que si Word
alguna vez descargó Bierstadt en tu máquina, Typst la encuentra sola. No copiamos ni versionamos el
archivo de fuente (es de Microsoft, no nuestro para redistribuir) — solo lo referenciamos donde ya
vive.

Si esa carpeta no existe (otra máquina, sin Office, u otro SO) Typst cae automáticamente a
`Calibri` → `Segoe UI` → `Arial` sin romper nada; en Linux/Mac lo más probable es que ninguna de las
cuatro esté disponible y use la fuente por defecto de Typst — para instalar una fuente de verdad ahí
sí aplica lo de siempre: instalarla a nivel de sistema operativo (no hay atajo por `uv`/Python).

## Respaldo del CV anterior

Los `.docx`/`.pdf` originales (hechos a mano en Word) quedaron en `builders/cv/legacy/` como respaldo.
