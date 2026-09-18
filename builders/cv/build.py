"""Compila el CV (ES/EN) de YAML+Typst a PDF.

Uso:
    uv run build.py                                 # compila el CV canónico (ambos idiomas, visual + ATS)
    uv run build.py --watch                          # recompila en vivo mientras se edita (Ctrl+C para salir)
    uv run build.py --application loka-ml-engineer   # compila una versión adaptada a UNA postulación
                                                      # puntual, en builders/cv/applications/<slug>/ --
                                                      # no versionado, no toca el CV canónico
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
# Postulaciones puntuales: cada una vive en su propia subcarpeta, ignorada por
# git (ver .gitignore). Nunca se publican en assets/cv/ ni se versionan.
APPLICATIONS_DIR = BUILDER_DIR / "applications"

# (entry .typ, nombre del yaml de datos, nombre de salida del PDF)
LANGUAGES = [
    ("cv_es.typ", "cv_es.yaml", "Pablo-Lopez-CV-ES.pdf"),
    ("cv_en.typ", "cv_en.yaml", "Pablo-Lopez-CV-EN.pdf"),
    ("cv_es_ats.typ", "cv_es.yaml", "Pablo-Lopez-CV-ES-ATS.pdf"),
    ("cv_en_ats.typ", "cv_en.yaml", "Pablo-Lopez-CV-EN-ATS.pdf"),
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


def bootstrap_application_data(data_dir: Path) -> None:
    """Primera vez que se compila una postulación: copia el YAML canónico como
    punto de partida editable. Nunca sobreescribe un archivo que ya exista, para
    no perder ediciones tailored de una corrida anterior."""
    data_dir.mkdir(parents=True, exist_ok=True)
    for name in ("cv_es.yaml", "cv_en.yaml"):
        dest = data_dir / name
        if not dest.exists():
            shutil.copyfile(DATA_DIR / name, dest)
            print(f"  bootstrap: copiado {name} desde data/ canónico")


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


def run_parity_check(data_dir: Path) -> None:
    with open(data_dir / "cv_es.yaml", encoding="utf-8") as f:
        es = yaml.safe_load(f)
    with open(data_dir / "cv_en.yaml", encoding="utf-8") as f:
        en = yaml.safe_load(f)

    warnings = check_parity(es, en)
    if warnings:
        print("Posible desincronización entre cv_es.yaml y cv_en.yaml:")
        for w in warnings:
            print(f"  - {w}")
        print()
    else:
        print("cv_es.yaml y cv_en.yaml tienen la misma estructura. OK.\n")


def compile_all(typst: str, data_dir: Path, output_dir: Path) -> bool:
    fonts = font_path_args()
    output_dir.mkdir(parents=True, exist_ok=True)
    ok = True
    for entry, data_name, output_name in LANGUAGES:
        output_path = output_dir / output_name
        data_arg = (data_dir / data_name).relative_to(BUILDER_DIR).as_posix()
        result = subprocess.run(
            [typst, "compile", *fonts, "--input", f"data={data_arg}", entry, str(output_path)],
            cwd=BUILDER_DIR,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            rel = output_path.relative_to(BUILDER_DIR.parents[1])
            print(f"OK  {entry} -> {rel.as_posix()}")
        else:
            ok = False
            print(f"ERROR compilando {entry}:\n{result.stderr}", file=sys.stderr)
    return ok


def watch_all(typst: str, data_dir: Path, output_dir: Path) -> None:
    fonts = font_path_args()
    output_dir.mkdir(parents=True, exist_ok=True)
    procs = [
        subprocess.Popen(
            [
                typst,
                "watch",
                *fonts,
                "--input",
                f"data={(data_dir / data_name).relative_to(BUILDER_DIR).as_posix()}",
                entry,
                str(output_dir / output_name),
            ],
            cwd=BUILDER_DIR,
        )
        for entry, data_name, output_name in LANGUAGES
    ]
    print("Vigilando cambios en ambos idiomas (Ctrl+C para detener)...")
    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        for p in procs:
            p.terminate()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--watch", action="store_true", help="recompilar en vivo al guardar cambios"
    )
    parser.add_argument(
        "--application",
        metavar="SLUG",
        help=(
            "compila una versión adaptada a una postulación puntual "
            "(builders/cv/applications/SLUG/), en vez del CV canónico"
        ),
    )
    args = parser.parse_args()

    typst = find_typst()

    if args.application:
        data_dir = APPLICATIONS_DIR / args.application / "data"
        output_dir = APPLICATIONS_DIR / args.application
        bootstrap_application_data(data_dir)
        print(
            f"Postulación: {args.application} "
            f"(builders/cv/applications/{args.application}/, no versionado)\n"
        )
    else:
        data_dir = DATA_DIR
        output_dir = CV_DIR

    run_parity_check(data_dir)

    if args.watch:
        watch_all(typst, data_dir, output_dir)
    else:
        if not compile_all(typst, data_dir, output_dir):
            sys.exit(1)


if __name__ == "__main__":
    main()
