# /// script
# requires-python = ">=3.11"
# dependencies = ["typst", "pyyaml"]
# ///
"""Compila el banner de LinkedIn (fondo + capa Typst) a PNG.

Uso:
    uv run build.py            # genera assets/header/linkedin_banner.png

Mismo motor que el header de GH: Typst incluido en el paquete `typst` (sin instalación
global), cloud fonts de Office enlazadas sin copiarlas.
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
    # root = builders/ para que el template pueda leer ../header/icons sin "escapar".
    typst.compile(
        str(BASE / "template.typ"),
        root=str(BASE.parent),
        output=str(out),
        ppi=ppi,
        font_paths=font_paths(),
    )
    print(f"OK  linkedin -> {out}  (ppi={ppi:g})")


if __name__ == "__main__":
    main()
