// Capa de composición del header. NO contiene contenido ni estilo propio:
// todo se lee de config.yaml. El fondo se pone como imagen a pantalla completa
// y encima se colocan velo, texto e iconos en posiciones absolutas.

#let cfg = yaml("config.yaml")
#let u = 1pt
#let W = cfg.canvas.width * u
#let H = cfg.canvas.height * u
#let L = cfg.layout
#let P = cfg.palette

#set page(
  width: W,
  height: H,
  margin: 0pt,
  background: image(cfg.background, width: W, height: H, fit: "cover"),
)

// ── Velo de legibilidad (izquierda opaca → derecha transparente) ─────────────
#if cfg.scrim.enabled {
  let base = rgb(cfg.scrim.color)
  let solid = base.transparentize((1 - cfg.scrim.opacity) * 100%)
  let clear = base.transparentize(100%)
  place(top + left, rect(
    width: W,
    height: H,
    fill: gradient.linear(
      (solid, 0%),
      (solid, 6%),
      (clear, cfg.scrim.width * 100%),
      (clear, 100%),
      angle: 0deg,
    ),
  ))
}

// ── Tagline ──────────────────────────────────────────────────────────────────
#place(top + left, dx: L.margin_x * u, dy: L.tagline_y * u,
  text(font: cfg.fonts.body, size: L.tagline_size * u, style: "italic",
    fill: rgb(P.subtitle))[#cfg.content.tagline])

// ── Título (varias líneas) ───────────────────────────────────────────────────
#place(top + left, dx: L.margin_x * u, dy: L.title_y * u, {
  set par(leading: L.title_leading * u)
  set text(font: cfg.fonts.title, size: L.title_size * u, weight: 800,
    fill: rgb(P.title), tracking: L.title_tracking * u)
  for (i, ln) in cfg.content.title_lines.enumerate() {
    if i > 0 { linebreak() }
    ln
  }
})

// ── Nombre ───────────────────────────────────────────────────────────────────
#place(top + left, dx: L.margin_x * u, dy: L.name_y * u,
  text(font: cfg.fonts.body, size: L.name_size * u, fill: rgb(P.subtitle))[
    #cfg.content.name])

// ── Fila de iconos del stack ─────────────────────────────────────────────────
#place(top + left, dx: L.margin_x * u, dy: L.icons_y * u,
  stack(dir: ltr, spacing: cfg.icons.gap * u,
    ..cfg.icons.list.map(n => image("icons/" + n + ".svg", height: cfg.icons.size * u))))

// ── Contacto ─────────────────────────────────────────────────────────────────
#place(top + left, dx: L.margin_x * u, dy: L.contact_y * u, {
  set par(leading: L.contact_leading * u)
  set text(font: cfg.fonts.body, size: L.contact_size * u, fill: rgb(P.text))
  for (i, c) in cfg.content.contact.enumerate() {
    if i > 0 { linebreak() }
    c
  }
})
