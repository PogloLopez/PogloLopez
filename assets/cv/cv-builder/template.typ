// Shared CV layout. Contains no language-specific text — every string comes
// from the `data` dict loaded from data/cv_*.yaml. Section labels live under
// data.labels so this file works identically for any language.

#let accent = rgb("#4b2e6e")
#let muted = rgb("#3d434b")
#let rule-stroke = 0.6pt + accent

#let md(body-text) = eval(body-text, mode: "markup")

// Styled hyperlink: colored + underlined so it visibly reads as clickable,
// unlike Typst's unstyled default link (plain inherited text color).
#let clickable(url, body) = underline(text(fill: accent)[#link(url)[#body]])

#let section(title, body) = {
  block(above: 1.3em, below: 0.6em, breakable: false)[
    #text(size: 10.5pt, weight: "bold", tracking: 0.06em, fill: accent)[#upper(title)]
    #v(0.2em)
    #line(length: 100%, stroke: rule-stroke)
  ]
  body
}

#let contact-block(data) = {
  set text(size: 9pt)
  set align(right)
  [#data.location]
  linebreak()
  [#data.phone]
  linebreak()
  clickable("mailto:" + data.email, data.email)
  for l in data.links {
    linebreak()
    clickable(l.url, l.label)
  }
}

#let header(data) = {
  grid(
    columns: (1fr, auto),
    align: (left, right),
    [
      #text(size: 22pt, weight: "bold")[
        #upper(data.first_name) \
        #text(fill: accent)[#upper(data.last_name)]
      ]
      #v(0.15em)
      #text(size: 12pt, fill: muted)[#data.title]
    ],
    contact-block(data),
  )
  v(0.5em)
  line(length: 100%, stroke: 1pt + accent)
  v(0.7em)
}

#let bullet-item(b) = {
  grid(
    columns: (0.9em, 1fr),
    column-gutter: 0.3em,
    [•],
    [
      #if "lead" in b and b.lead != none [#strong[#b.lead:] ]
      #md(b.text)
    ],
  )
  v(0.35em)
}

#let experience-entry(data, e) = {
  block(below: 0.8em, breakable: false)[
    #grid(
      columns: (1fr, auto),
      align: (left, right),
      [
        #strong[#e.role] \
        #emph[#e.company -- #e.location]
      ],
      text(fill: muted, size: 9.5pt)[#e.start -- #e.end],
    )
    #if "summary" in e and e.summary != none [
      #v(0.25em)
      #text(style: "italic", size: 9.5pt)[#e.summary]
    ]
    #v(0.4em)
    #for b in e.bullets {
      bullet-item(b)
    }
  ]
}

#let skills-block(data) = {
  grid(
    columns: (auto, 1fr),
    column-gutter: 1em,
    row-gutter: 0.9em,
    align: (left + top, left + top),
    ..data.skills.map(s => (strong[#s.category:], [#s.items])).flatten()
  )
}

#let education-block(data) = {
  for e in data.education {
    block(below: 0.4em)[
      #strong[#e.degree] \
      #emph[#e.institution] -- #e.date
    ]
  }
}

#let certificates-block(data) = {
  let c = data.certificates
  [#c.note #clickable(c.link, c.link_label).]
  v(0.5em)
  for h in c.highlights {
    block(below: 0.55em)[
      #strong[#h.title] \
      #text(fill: muted, size: 9.5pt)[#h.org]
    ]
  }
}

#let references-block(data) = {
  grid(
    columns: (1fr,) * calc.min(data.references.len(), 3),
    column-gutter: 1.2em,
    ..data.references.map(r => [
      #strong[#r.name] \
      #text(size: 9pt)[#r.role]
      #if "phone" in r and r.phone != none [\ #text(size: 9pt)[#r.phone]]
      \ #text(size: 9pt)[#clickable("mailto:" + r.email, r.email)]
    ])
  )
}

#let render(data) = {
  set page(paper: "us-letter", margin: (x: 1.9cm, y: 1.7cm))
  set text(font: ("Bierstadt", "Calibri", "Segoe UI", "Arial"), size: 9.8pt, lang: "en")
  set par(justify: false, leading: 0.62em)

  header(data)

  section(data.labels.profile, [#data.profile])
  section(data.labels.skills, skills-block(data))
  section(data.labels.experience, {
    for e in data.experience {
      experience-entry(data, e)
    }
  })
  section(data.labels.education, education-block(data))
  section(data.labels.certificates, certificates-block(data))
  section(data.labels.references, references-block(data))
}
