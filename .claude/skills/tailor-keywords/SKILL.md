---
name: tailor-keywords
description: "Use this skill when the user wants to tailor Pablo's CV (builders/cv/) to a specific job posting/vacante. Triggers: 'adapta mi CV a esta vacante', 'tailor my resume for this job', a pasted job posting URL or job description text alongside a request to update the CV, or 'busca las keywords de esta oferta y méteselas al CV'. Weaves the job posting's exact terminology into the CV's  real narrative (skills list, experience bullets, project descriptions)"
argument-hint: "[job posting URL or pasted text]"
allowed-tools: Read Edit Bash Glob Grep WebFetch
license: MIT
---

# tailor-keywords

Adapta `builders/cv/data/cv_es.yaml` y `cv_en.yaml` a una oferta de trabajo puntual, reescribiendo
frases que ya son ciertas con la terminología exacta que usa esa oferta. Ejemplo del objetivo: si la oferta pide "LangChain" y el CV dice "frameworks agénticos" en el proyecto donde el candidato usó LangChain, el resultado dice "LangChain" ahí. Si la oferta pide "orquestación" y el CV dice "Dagster" a secas, el resultado dice "orquestación con Dagster". La narrativa no cambia de forma, solo de vocabulario.

## Regla dura: nunca inventar

Cada término que se agrega al CV tiene que corresponder a algo que el candidato **ya hace o ya usó**, solo que estaba descrito con otras palabras. Si una keyword de la oferta no tiene  respaldo real, no se fuerza — se reporta como gap al usuario (Stage 4) en vez de metérsela.

## Stage 1 — Obtener la oferta

Si el usuario pasó una URL, usa `WebFetch` para extraer: título del puesto, stack técnico,
metodologías, responsabilidades, requisitos obligatorios vs. deseables — todo verbatim, no
parafraseado (los términos exactos son los que importan para el parseo ATS). Si pegó texto, usa ese
texto directamente.

## Stage 2 — Leer el CV actual

Lee `builders/cv/data/cv_es.yaml` y `builders/cv/data/cv_en.yaml` completos. Presta atención a:
`skills` (por categoría), `experience[].bullets[].text`, `projects.items[].text`. Esas tres zonas son
donde se puede insertar terminología sin alterar el significado.

## Stage 3 — Cruzar keywords contra la narrativa real

Para cada keyword/tecnología/metodología de la oferta, busca en el CV, en memoria o en otros proyectos un punto donde ya se describe lo mismo con otro término (sinónimo, marca genérica, nombre de categoría en vez de la herramienta específica). Arma una tabla mental (o literal, si ayuda) de:

| Keyword de la oferta | Dónde ya vive esa idea en el CV | Cambio propuesto |
|---|---|---|

Ejemplos del tipo de sustitución que aplica:
- Oferta pide **LangChain/LangGraph** → si el proyecto de RAG/agentes dice "frameworks agénticos" o
  "orquestación de agentes" de forma genérica, se vuelve
  explícita: "LangChain/LangGraph".
- Oferta pide **orquestación** → "Dagster" a secas pasa a "orquestación con Dagster" (o similar),
  para que el término de la oferta aparezca literal, no solo el nombre de la herramienta.
- Oferta pide **MLOps** → si ya se describe "arquitectura MLOps completa", no hace falta tocarlo, ya
  está.
- Oferta pide **vector search / embeddings** pero el candidato nunca ha trabajado con eso → **no se
  agrega**. Va a la lista de gaps, se pregunta al usuario y definen juntos si se debe incluir. Si no está en el CV, puede estar en otros proyectos, así que preguntale.

## Stage 4 — Reportar antes de escribir

Antes de editar los YAML, muestra al usuario:
1. **Keywords que sí se van a tejer** — keyword → ubicación exacta (archivo + campo) → redacción
   actual → redacción propuesta.
2. **Keywords sin respaldo real** — las que no se pueden meter honestamente, para que el usuario
   decida si quiere ajustar el enfoque de alguna experiencia o simplemente aceptar el gap.

No edites nada hasta que el usuario confirme la lista (o pida ajustes).

## Stage 5 — Editar ES y EN juntos, en el mismo cambio

Regla estricta de este repo (ver `CLAUDE.md`): `cv_es.yaml` y `cv_en.yaml` son reflejos fieles — todo
cambio en un idioma se traduce (no se copia) al otro en el mismo paso. Nunca dejes un idioma
actualizado y el otro pendiente. Usa `Edit` sobre ambos archivos, campo por campo.

## Stage 6 — Rebuild y validar

```bash
cd builders/cv && uv run build.py
```

Confirma que el chequeo de paridad estructural pase y que los 4 PDFs se regeneraron sin error. Lee al
menos uno de los PDFs generados para confirmar que las frases nuevas se leen naturales, no forzadas.

## Stage 7 — Recordar el alcance del cambio

Esto modifica el YAML "maestro" que también alimenta el CV visual y el del README/perfil público.
Antes de terminar, pregúntale al usuario si esta redacción tailored:
- (a) es una mejora genuina que quiere dejar permanente en el CV, o
- (b) es un ajuste puntual solo para esta postulación, que debería revertirse
  (`git checkout -- builders/cv/data/cv_es.yaml builders/cv/data/cv_en.yaml`) después de generar y
  enviar el PDF, para no acumular reformulaciones específicas de una empresa en el CV general.

## Qué NO hacer

- No inventar herramientas, métricas o proyectos que el candidato no mencionó.
- No dejar un idioma sin actualizar mientras el otro sí cambió.
- No saltarte Stage 4 (reporte y confirmación) aunque el input parezca obvio.
