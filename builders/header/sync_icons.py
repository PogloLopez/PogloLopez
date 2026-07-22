# /// script
# requires-python = ">=3.11"
# dependencies = ["simpleicons", "pyyaml"]
# ///
"""Genera icons/<nombre>.svg a partir de la lista en config.yaml.

Tres orígenes por icono, en este orden de prioridad:
  1. icons/_src/<nombre>.svg  → SVG oficial que dejaste tú (Claude, Dagster, etc.).
     Se recolorea al color de config.icons (o se deja tal cual en modo "brand").
  2. simpleicons                → logos oficiales de marca (MIT).
  3. error                      → si no está en ninguno, avisa qué hacer.

Para usar un logo oficial cualquiera: deja su .svg en icons/_src/<nombre>.svg y
añade <nombre> a config.icons.list. Nada más.

Uso:  uv run sync_icons.py
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent
ICONS_DIR = BASE / "icons"
SRC_DIR = ICONS_DIR / "_src"

SLUG_ALIAS: dict[str, str] = {"sqlserver": "microsoftsqlserver"}


def recolor(svg: str, color: str) -> str:
    """Pinta todo el SVG de un solo color, respetando fill/stroke = none."""
    svg = re.sub(r'fill="(?!none")[^"]*"', f'fill="{color}"', svg)
    svg = re.sub(r'stroke="(?!none")[^"]*"', f'stroke="{color}"', svg)
    return svg


def simpleicon_svg(slug: str, color: str | None) -> str:
    from simpleicons.all import icons

    ic = icons.get(slug)
    if ic is None:
        raise SystemExit(
            f"'{slug}' no está en simpleicons ni en icons/_src/. "
            f"Deja su SVG oficial en icons/_src/{slug}.svg y reintenta."
        )
    fill = f"#{ic.hex}" if color is None else color
    d = re.search(r'\sd="([^"]+)"', ic.svg).group(1)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        f'<path fill="{fill}" d="{d}"/></svg>'
    )


def main() -> None:
    cfg = yaml.safe_load((BASE / "config.yaml").read_text(encoding="utf-8"))
    color_mode = str(cfg["icons"]["color"])
    global_brand = color_mode.lower() == "brand"
    keep_brand = set(cfg["icons"].get("keep_brand", []))

    ICONS_DIR.mkdir(exist_ok=True)
    for name in cfg["icons"]["list"]:
        as_brand = global_brand or name in keep_brand
        src = SRC_DIR / f"{name}.svg"
        if src.exists():
            svg = src.read_text(encoding="utf-8")
            if not as_brand:
                svg = recolor(svg, color_mode)
            origin = "oficial (_src)"
        else:
            slug = SLUG_ALIAS.get(name, name)
            svg = simpleicon_svg(slug, None if as_brand else color_mode)
            origin = "simpleicons"
        (ICONS_DIR / f"{name}.svg").write_text(svg, encoding="utf-8")
        tag = "brand" if as_brand else color_mode
        print(f"OK  icons/{name}.svg  [{origin}]  {tag}")


if __name__ == "__main__":
    main()
