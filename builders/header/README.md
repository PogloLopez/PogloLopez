# header — generador del banner del README

Mismo patrón que el pipeline del CV: **contenido + estilo en `config.yaml`**, **layout
en Typst**, salida PNG. El header se compone como dos capas:

```
FONDO (imagen, la genera una IA especialista)  +  CAPA (texto + iconos + datos)
        background/…                                    template.typ
                         └──────── build.py ───────┘
                                     ↓
                       assets/header/readme_header.png
```

La idea es no depender de "dibujar" bien una imagen, solo de **componer con precisión**
sobre un fondo intercambiable.

## Estructura

```
builders/header/
├── config.yaml          ← ÚNICA fuente de verdad: textos, colores, posiciones, iconos, fondo
├── template.typ         ← layout (no tiene contenido propio; todo lo lee de config.yaml)
├── build.py             ← compila a PNG (Typst incluido vía uv, no requiere instalación global)
├── sync_icons.py        ← regenera icons/ según config.icons
├── background-prompt.md ← prompt para que una IA de imágenes genere el fondo
├── background/          ← fondos disponibles (header.svg, maieutik_background.svg, …)
├── icons/               ← SVGs listos (generados; no editar a mano)
│   └── _src/            ← SVGs oficiales crudos (Claude, Dagster) que sync_icons recolorea
```

Salida: `assets/header/readme_header.png` (carpeta de productos del repo).

## Uso

```bash
cd builders/header
uv run build.py            # → assets/header/readme_header.png
```

- **Cambiar textos, colores o posiciones:** editar `config.yaml` y `uv run build.py`.
- **Cambiar el fondo:** poner la imagen en `background/`, apuntar `config.background` a ella
  y rebuild. Se recorta con `fit: cover` al lienzo (2:1 por defecto).
- **Cambiar iconos:** editar `config.icons.list`, luego `uv run sync_icons.py` y `build.py`.

## Iconos

- `python`, `docker`, `postgresql`, `github` → `simpleicons` (logos oficiales, MIT).
- `claude`, `dagster` → SVG oficial en `icons/_src/<nombre>.svg`, recoloreado por `sync_icons.py`.
- **Color:** `config.icons.color` = un hex (monocromo) o `"brand"` (colores de marca).
  `config.icons.keep_brand` lista los que conservan su color aunque el resto sea monocromo.
- **Añadir un logo oficial cualquiera:** deja su `.svg` en `icons/_src/<nombre>.svg`, añade
  `<nombre>` a `config.icons.list`, y `uv run sync_icons.py`. Si no está ahí, `sync_icons`
  lo busca en `simpleicons` (slugs en https://simpleicons.org).

## Dimensiones

Lienzo por defecto **1280×640** (2:1) a `ppi: 144` → PNG **2560×1280** (nítido en retina;
GitHub lo reescala). Todo configurable en `config.canvas`.

## Enganche en el README

Ya está enganchado: `README.md` apunta a `/assets/header/readme_header.png`. Al cambiar de
fondo o contenido, basta regenerar ese archivo; el README no se toca.

## Fondo

Ver `background-prompt.md` para el prompt con el que generar el fondo. Regla de oro: **el
fondo NO lleva texto ni logos** — esos los pone esta capa encima.
