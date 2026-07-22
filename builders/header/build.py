# /// script
# requires-python = ">=3.11"
# dependencies = ["typst", "pyyaml"]
# ///
"""Compila el header (fondo + capa Typst) a PNG.

Uso:
    uv run build.py            # genera assets/header/readme_header.png

El compilador de Typst viene incluido en el paquete `typst` (no requiere
instalación global). Las cloud fonts de Office (Aptos, etc.) se enlazan igual
que en el pipeline del CV, sin copiar ni redistribuir nada.
"""

from __future__ import annotations

from pathlib import Path

import typst
import yaml

BASE = Path(__file__).resolve().parent


def font_paths() -> list[str]:
    cloud = Path.home() / "AppData/Local/Microsoft/FontCache/4/CloudFonts"
    return [str(cloud)] if cloud.exists() else []


def main() -> None:
    cfg = yaml.safe_load((BASE / "config.yaml").read_text(encoding="utf-8"))
    out = (BASE / cfg["output"]).resolve()
    ppi = float(cfg["canvas"]["ppi"])

    typst.compile(
        str(BASE / "template.typ"),
        output=str(out),
        ppi=ppi,
        font_paths=font_paths(),
    )
    print(f"OK  header -> {out}  (ppi={ppi:g})")


if __name__ == "__main__":
    main()
