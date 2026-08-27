# Prompt para el FONDO del header

Copiar el bloque completo y pegarlo en la IA de imágenes. Salida **2:1, ≥ 2560×1280 px**.
Sirve tal cual, o adjuntando una imagen de referencia. El fondo **no lleva texto ni logos**:
el pipeline los compone encima.

---

```
ROLE
You are a senior art director specializing in premium, minimal visual branding for
technology professionals. You produce hero imagery with the restraint and polish of the
best modern SaaS brands.

OBJECTIVE
Create a hero-banner BACKGROUND for the GitHub profile of a Data Engineer working in AI and automation.
This is a BACKGROUND ONLY: a large title, a name, a small row of icons and contact details
will be composited on top afterwards. Therefore the image must contain no text and no logos,
and must leave calm, uncluttered space for that overlay. The visual concept is entirely
yours — surprise me — as long as it stays sober, dark and professional.

TECHNICAL SPECIFICATIONS
- Aspect ratio 2:1, horizontal banner. Output resolution >= 2560x1280 px.

COMPOSITION (must obey)
- The LEFT 55-60% of the frame stays dark, calm and nearly empty: clean negative space
  reserved for text, with no strong focal elements there.
- Whatever visual interest you create lives toward the RIGHT, so it balances the empty left.

ART DIRECTION
- Mood: sober, premium, elegant, modern, understated, confident. Never flashy.
- Dark theme: mostly deep blacks and near-blacks. Rich but restrained.
- High production value, generous negative space, calm and balanced — not busy.
- Choose your own visual language, palette accents and technique. Keep it tasteful.

HARD CONSTRAINTS (do not violate)
- No text, letters, numbers or typography. No logos, brand marks, icons, UI or watermark.
- No people, faces or hands.
- Not busy, not cluttered, not gamer-RGB, not sci-fi cliche, not stock-photo.

NEGATIVE PROMPT (for models that support it; in Midjourney pass as --no ...)
text, letters, words, numbers, typography, logo, brand marks, icons, UI, buttons, labels,
watermark, signature, frame, border, busy clutter, neon overload, rainbow, people, faces,
hands, blurry, low resolution, jpeg artifacts, distorted, cartoon

OPTIONAL REFERENCE
If a reference image is attached, follow its style, palette and mood while respecting the
composition and constraints above. If none is attached, invent your own dark, sober concept.
```

---

Regla fija: mantén siempre la **izquierda oscura y despejada** para que el texto sea legible.
Todo lo demás (concepto, técnica, acentos de color) queda a criterio del modelo.
