"""Compila el CV (ES/EN) de YAML+Typst a PDF.

Uso:
    uv run build.py            # compila ambos idiomas una vez
    uv run build.py --watch    # recompila en vivo mientras se edita (Ctrl+C para salir)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

BUILDER_DIR = Path(__file__).resolve().parent
# Los PDF finales se publican en <repo>/assets/cv/ (builders/cv → repo raíz → assets/cv).
CV_DIR = BUILDER_DIR.parents[1] / "assets" / "cv"
DATA_DIR = BUILDER_DIR / "data"

# (entry .typ, datos yaml, nombre de salida del PDF)
LANGUAGES = [
    ("cv_es.typ", "cv_es.yaml", "Pablo-Lopez-CV-ES.pdf"),
    ("cv_en.typ", "cv_en.yaml", "Pablo-Lopez-CV-EN.pdf"),
]


def find_typst() -> str:
    found = shutil.which("typst")
    if found:
        return found

    winget_packages = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    if winget_packages.exists():
        matches = list(winget_packages.glob("Typst.Typst_*/typst-*/typst.exe"))
        if matches:
            return str(matches[0])

    print(
        "No se encontró el ejecutable 'typst'.\n"
        "Instálalo con: winget install --id Typst.Typst\n"
        "Si acabas de instalarlo, abre una terminal nueva para que se actualice el PATH.",
        file=sys.stderr,
    )
    sys.exit(1)


def font_path_args() -> list[str]:
    """Da acceso a Typst a fuentes que Office cachea localmente pero no
    registra como fuente del sistema (p. ej. Bierstadt/Aptos, entregadas vía
    Microsoft 365 "cloud fonts"). No copia ni redistribuye nada: solo apunta
    a lo que Office ya descargó en esta máquina.
    """
    cloud_fonts = Path.home() / "AppData/Local/Microsoft/FontCache/4/CloudFonts"
    if cloud_fonts.exists():
        return ["--font-path", str(cloud_fonts)]
    return []


def check_parity(es, en, path: str = "") -> list[str]:
    """Compara recursivamente la forma (claves/longitudes) de cv_es.yaml y cv_en.yaml.

    No compara contenido (debe diferir, es traducción) — solo detecta bullets,
    certificados o secciones que se agregaron/quitaron en un idioma y no en el otro.
    """
    warnings: list[str] = []

    if es is None or en is None:
        return warnings

    if isinstance(es, dict) and isinstance(en, dict):
        keys_es, keys_en = set(es), set(en)
        if only_es := keys_es - keys_en:
            warnings.append(f"{path or '<root>'}: claves solo en ES: {sorted(only_es)}")
        if only_en := keys_en - keys_es:
            warnings.append(f"{path or '<root>'}: claves solo en EN: {sorted(only_en)}")
        for key in keys_es & keys_en:
            warnings.extend(
                check_parity(es[key], en[key], f"{path}.{key}" if path else key)
            )
    elif isinstance(es, list) and isinstance(en, list):
        if len(es) != len(en):
            warnings.append(
                f"{path}: distinta cantidad de elementos (ES={len(es)}, EN={len(en)})"
            )
        for i, (e_item, n_item) in enumerate(zip(es, en)):
            warnings.extend(check_parity(e_item, n_item, f"{path}[{i}]"))

    return warnings


def run_parity_check() -> None:
    with open(DATA_DIR / "cv_es.yaml", encoding="utf-8") as f:
        es = yaml.safe_load(f)
    with open(DATA_DIR / "cv_en.yaml", encoding="utf-8") as f:
        en = yaml.safe_load(f)

    warnings = check_parity(es, en)
    if warnings:
        print("Posible desincronización entre cv_es.yaml y cv_en.yaml:")
        for w in warnings:
            print(f"  - {w}")
        print()
    else:
        print("cv_es.yaml y cv_en.yaml tienen la misma estructura. OK.\n")


def compile_all(typst: str) -> bool:
    fonts = font_path_args()
    ok = True
    for entry, _, output_name in LANGUAGES:
        output_path = CV_DIR / output_name
        result = subprocess.run(
            [typst, "compile", *fonts, entry, str(output_path)],
            cwd=BUILDER_DIR,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"OK  {entry} -> assets/cv/{output_name}")
        else:
            ok = False
            print(f"ERROR compilando {entry}:\n{result.stderr}", file=sys.stderr)
    return ok


def watch_all(typst: str) -> None:
    fonts = font_path_args()
    procs = [
        subprocess.Popen(
            [typst, "watch", *fonts, entry, str(CV_DIR / output_name)], cwd=BUILDER_DIR
        )
        for entry, _, output_name in LANGUAGES
    ]
    print("Vigilando cambios en ambos idiomas (Ctrl+C para detener)...")
    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        for p in procs:
            p.terminate()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--watch", action="store_true", help="recompilar en vivo al guardar cambios"
    )
    args = parser.parse_args()

    typst = find_typst()
    run_parity_check()

    if args.watch:
        watch_all(typst)
    else:
        if not compile_all(typst):
            sys.exit(1)


if __name__ == "__main__":
    main()
