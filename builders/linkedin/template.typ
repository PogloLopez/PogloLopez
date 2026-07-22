// Banner de LinkedIn: fondo (opcionalmente en espejo) + capa de texto/iconos a la
// DERECHA. Todo el contenido y estilo se lee de config.yaml. Iconos reutilizados de
// builders/header/icons.

#let cfg = yaml("config.yaml")
#let u = 1pt
#let W = cfg.canvas.width * u
#let H = cfg.canvas.height * u
#let L = cfg.layout
#let P = cfg.palette
#let zonew = cfg.canvas.width * 0.60 * u

// Fondo a pantalla completa, con espejo horizontal opcional.
#let bg = image(cfg.background, width: W, height: H, fit: "cover")
#set page(
  width: W,
  height: H,
  margin: 0pt,
  background: if cfg.flip_h { scale(x: -100%, reflow: false, bg) } else { bg },
)
#set text(font: cfg.fonts.body, fill: rgb(P.text))

// Velo de legibilidad: transparente a la izquierda → opaco a la DERECHA.
#if cfg.scrim.enabled {
  let base = rgb(cfg.scrim.color)
  let solid = base.transparentize((1 - cfg.scrim.opacity) * 100%)
  let clear = base.transparentize(100%)
  place(top + left, rect(
    width: W, height: H,
    fill: gradient.linear(
      (clear, 0%),
      (clear, (1 - cfg.scrim.width) * 100%),
      (solid, 100%),
      angle: 0deg,
    ),
  ))
}

// Bloque anclado a la derecha, con líneas alineadas a la derecha.
#let R(y, body) = place(top + right, dx: -L.margin_r * u, dy: y * u,
  box(width: zonew, align(right, body)))

// Tagline
#R(L.tagline_y, text(font: cfg.fonts.body, size: L.tagline_size * u, style: "italic",
  fill: rgb(P.subtitle))[#cfg.content.tagline])

// Título (varias líneas)
#R(L.title_y, {
  set par(leading: L.title_leading * u)
  set text(font: cfg.fonts.title, size: L.title_size * u, weight: 800,
    fill: rgb(P.title), tracking: L.title_tracking * u)
  for (i, ln) in cfg.content.title_lines.enumerate() {
    if i > 0 { linebreak() }
    ln
  }
})

// Nombre
#R(L.name_y, text(font: cfg.fonts.body, size: L.name_size * u, fill: rgb(P.subtitle))[
  #cfg.content.name])

// Fila de iconos (anclada a la derecha)
#place(top + right, dx: -L.margin_r * u, dy: L.icons_y * u,
  stack(dir: ltr, spacing: cfg.icons.gap * u,
    ..cfg.icons.list.map(n => image(cfg.icons.dir + "/" + n + ".svg", height: cfg.icons.size * u))))

// Contacto
#R(L.contact_y, {
  set par(leading: L.contact_leading * u)
  set text(font: cfg.fonts.body, size: L.contact_size * u, fill: rgb(P.text))
  for (i, c) in cfg.content.contact.enumerate() {
    if i > 0 { linebreak() }
    c
  }
})
