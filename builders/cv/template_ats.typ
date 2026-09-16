// Layout del CV "plano" orientado a parseo ATS. Reutiliza el mismo `data`
// (data/cv_*.yaml) que template.typ, pero renderiza en una sola columna,
// sin grids de layout ni iconos, para maximizar la fidelidad de extracción
// de texto por parsers automáticos. Contiene el mismo texto que la versión
// visual — no es contenido nuevo, es otra proyección del mismo YAML. Un solo
// color de acento para headings/enlaces/divisores es seguro para ATS (los
// parsers leen texto, no color); lo que rompe el parseo son columnas,
// tablas e iconos, no un color de marca. Igual que template.typ: puramente
// estructural, sin texto de ningún idioma propio.

#let ink = rgb("#000000")
#let muted = rgb("#3d434b")
#let accent = rgb("#4b2e6e")
#let rule-stroke = 0.5pt + accent

#let md(body-text) = eval(body-text, mode: "markup")

#let clickable(url, body) = underline(text(fill: accent)[#link(url)[#body]])

#let section(title, body) = {
  block(above: 1.1em, below: 0.5em, breakable: false, sticky: true)[
    #text(size: 10.5pt, weight: "bold", tracking: 0.04em, fill: accent)[#upper(title)]
    #v(0.15em)
    #line(length: 100%, stroke: rule-stroke)
  ]
  body
}

#let header(data) = {
  text(size: 18pt, weight: "bold", fill: accent)[#data.first_name #data.last_name]
  linebreak()
  text(size: 11.5pt, fill: muted)[#data.title]
  v(0.35em)
  let contact = (
    data.location,
    data.phone,
    clickable("mailto:" + data.email, data.email),
    ..data.links.map(l => clickable(l.url, l.label)),
  )
  text(size: 9.5pt)[#contact.join("  |  ")]
  v(0.3em)
  line(length: 100%, stroke: 0.8pt + accent)
  v(0.6em)
}

#let bullet-item(b) = {
  block(below: 0.28em)[
    - #if "lead" in b and b.lead != none [#strong[#b.lead:] ]#md(b.text)
  ]
}

#let experience-entry(data, e) = {
  block(below: 0.65em, breakable: false)[
    #strong[#e.role] #text(fill: muted)[-- #e.company, #e.location]
    #linebreak()
    #text(size: 9.5pt, fill: muted)[#e.start -- #e.end]
    #if "summary" in e and e.summary != none [
      #v(0.18em)
      #text(size: 9.5pt, style: "italic")[#e.summary]
    ]
    #v(0.25em)
    #for b in e.bullets {
      bullet-item(b)
    }
  ]
}

#let skills-block(data) = {
  for s in data.skills {
    block(below: 0.32em)[#strong[#s.category:] #s.items]
  }
}

#let education-block(data) = {
  for e in data.education {
    block(below: 0.3em)[
      #strong[#e.degree] #text(fill: muted)[-- #e.institution, #e.date]
    ]
  }
}

#let projects-block(data) = {
  let p = data.projects
  [#p.note #clickable(p.link, p.link_label).]
  v(0.32em)
  for it in p.items {
    block(below: 0.42em)[#strong[#it.name]: #it.text]
  }
}

#let certificates-block(data) = {
  let c = data.certificates
  [#c.note: #clickable(c.link, c.link_label)]
  v(0.32em)
  for h in c.highlights {
    block(below: 0.3em)[#strong[#h.title] #text(fill: muted)[-- #h.org]]
  }
}

#let references-block(data) = {
  for r in data.references {
    let parts = (r.role,)
    if "phone" in r and r.phone != none { parts += (r.phone,) }
    parts += (clickable("mailto:" + r.email, r.email),)
    block(below: 0.3em)[#strong[#r.name] #text(fill: muted)[-- #parts.join(", ")]]
  }
}

#let render(data) = {
  set page(paper: "us-letter", margin: (x: 2cm, y: 1.8cm))
  set text(font: ("Arial", "Liberation Sans", "Calibri", "Segoe UI"), size: 10.5pt, fill: ink, lang: "en")
  set par(justify: false, leading: 0.6em)

  header(data)

  section(data.labels.profile, [#data.profile])
  section(data.labels.skills, skills-block(data))
  section(data.labels.experience, {
    for e in data.experience {
      experience-entry(data, e)
    }
  })
  section(data.labels.projects, projects-block(data))
  section(data.labels.education, education-block(data))
  section(data.labels.certificates, certificates-block(data))
  section(data.labels.references, references-block(data))
}
