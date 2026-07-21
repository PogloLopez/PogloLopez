# CLAUDE.md

Repo personal de GitHub (perfil `PogloLopez/PogloLopez`, se renderiza en github.com/PogloLopez). No
es una aplicación — son documentos + un pipeline de CV.

## Mapa del repo

- `README.md` — bio/perfil de GitHub.
- `CERTIFICATES.md` — listado completo de certificados, enlazado desde `README.md`.
- `assets/cv/` — CV en PDF (ES/EN), generado. Ver `assets/cv/cv-builder/README.md` para el pipeline
  completo (edición, build, fuentes, sincronización ES/EN).
- `assets/cv/legacy/` — versiones antiguas en Word, solo respaldo, no editar.
- `TODO.md` — pendientes activos. Revisar antes de asumir que algo ya está hecho.

## CV (Typst + YAML)

- Contenido: `assets/cv/cv-builder/data/cv_es.yaml` y `cv_en.yaml` — mismo esquema y mismo orden de
  claves a propósito.
- **Regla estricta — los dos CV son reflejos fieles el uno del otro, siempre.** Todo cambio en un
  idioma (contenido, bullets, orden, métricas, fraseo, puntuación) debe reflejarse traducido —no
  copiado— en el otro dentro del mismo cambio, nunca después. Ningún cambio se da por terminado si un
  idioma quedó distinto del otro. La única diferencia admisible entre ambos es el idioma; cualquier
  otra divergencia es un error a corregir. Salvedad: la puntuación sigue la norma de cada idioma
  cuando su gramática difiere (no se copia una coma si en el otro idioma es incorrecta) — el reflejo
  es de contenido y significado, no de caracteres.
- Layout: `assets/cv/cv-builder/template.typ` — puramente estructural, sin texto de ningún idioma.
- Entrypoint de build: `assets/cv/cv-builder/build.py`. Para generar/regenerar el CV:
  `cd assets/cv/cv-builder && uv run build.py` (venv aislado en `.venv/`, gestionado por `uv`, no
  se toca a mano). Compila ambos idiomas, valida que `cv_es.yaml`/`cv_en.yaml` tengan la misma
  estructura, y escribe `assets/cv/Pablo-Lopez-CV-{ES,EN}.pdf`. Correr siempre tras editar un YAML
  o el template, antes de dar el cambio por terminado. `--watch` recompila en vivo al guardar.

## Git

- Push/pull por SSH normal. `~/.ssh/config` fuerza el puerto 443 para `github.com` — el
  `HostName` de ese bloque debe ser `ssh.github.com`, no `github.com` (si se revierte, el SSH
  handshake falla en seco aunque el puerto esté abierto).
- Antes de crear una rama nueva: `git fetch origin` y partir de `origin/main` real — no asumir que
  el `main` local está al día.
- Nunca mergear a `main` sin confirmación explícita del usuario.
