# CLAUDE.md

Repo personal de GitHub (perfil `PogloLopez/PogloLopez`, se renderiza en github.com/PogloLopez). No
es una aplicación — son documentos + pipelines que generan el CV y el banner del README.

## Mapa del repo

Dos raíces claras: `assets/` = **productos finales** (lo que muestra el perfil), `builders/` =
**código + materia prima** que los genera.

- `README.md` — bio/perfil de GitHub. Incrusta el banner `assets/header/readme_header.png`.
- `CERTIFICATES.md` — listado completo de certificados, enlazado desde `README.md`.
- `assets/`
  - `assets/cv/` — CV en PDF (ES/EN), generado.
  - `assets/header/` — banner(s) del README en PNG, generados.
  - `assets/img/` — imágenes sueltas usadas por los `.md` (p. ej. `credly_badge.png`).
- `builders/`
  - `builders/cv/` — pipeline del CV (Typst + YAML). Ver `builders/cv/README.md`.
  - `builders/header/` — pipeline del banner del README (Typst + fondo). Ver
    `builders/header/README.md`.
  - `builders/linkedin/` — gemelo del anterior para el banner de LinkedIn (1584×396, texto a
    la derecha, mismo fondo en espejo). Reutiliza los iconos de `builders/header/icons/`.
  - `builders/cv/legacy/` — CVs viejos en Word, solo respaldo, no editar.

## CV (Typst + YAML)

- Contenido: `builders/cv/data/cv_es.yaml` y `cv_en.yaml` — mismo esquema y mismo orden de
  claves a propósito.
- **Regla estricta — los dos CV son reflejos fieles el uno del otro, siempre.** Todo cambio en un
  idioma (contenido, bullets, orden, métricas, fraseo, puntuación) debe reflejarse traducido —no
  copiado— en el otro dentro del mismo cambio, nunca después. Ningún cambio se da por terminado si un
  idioma quedó distinto del otro. La única diferencia admisible entre ambos es el idioma; cualquier
  otra divergencia es un error a corregir. Salvedad: la puntuación sigue la norma de cada idioma
  cuando su gramática difiere (no se copia una coma si en el otro idioma es incorrecta) — el reflejo
  es de contenido y significado, no de caracteres.
- Layout: `builders/cv/template.typ` — puramente estructural, sin texto de ningún idioma.
- Entrypoint de build: `builders/cv/build.py`. Para generar/regenerar el CV:
  `cd builders/cv && uv run build.py` (venv aislado en `.venv/`, gestionado por `uv`, no
  se toca a mano; requiere Typst instalado a nivel de sistema). Compila ambos idiomas, valida que
  `cv_es.yaml`/`cv_en.yaml` tengan la misma estructura, y escribe
  `assets/cv/Pablo-Lopez-CV-{ES,EN}.pdf`. Correr siempre tras editar un YAML o el template, antes
  de dar el cambio por terminado. `--watch` recompila en vivo al guardar.

## Header del README (Typst + fondo)

- Pipeline en `builders/header/` (ver su README). Contenido y estilo en `config.yaml`, layout en
  `template.typ`; el fondo es una imagen intercambiable en `builders/header/background/`, generada
  aparte por una IA de imágenes (prompt en `builders/header/background-prompt.md`).
- `cd builders/header && uv run build.py` (autocontenido: Typst viene en el paquete `typst` vía
  `uv`, no requiere instalación global) escribe `assets/header/readme_header.png`, que es lo que
  incrusta `README.md`. `uv run sync_icons.py` regenera los iconos del stack.

## Git

- Push/pull por SSH normal. `~/.ssh/config` fuerza el puerto 443 para `github.com` — el
  `HostName` de ese bloque debe ser `ssh.github.com`, no `github.com` (si se revierte, el SSH
  handshake falla en seco aunque el puerto esté abierto).
- Antes de crear una rama nueva: `git fetch origin` y partir de `origin/main` real — no asumir que
  el `main` local está al día.
- Nunca mergear a `main` sin confirmación explícita del usuario.
