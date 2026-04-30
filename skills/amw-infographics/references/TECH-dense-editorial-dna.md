---
name: TECH-dense-editorial-dna
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/style-details.md
---

# Dense editorial DNA — the defining aesthetic

## What it does

Defines the signature visual language for this infographic library:
**dense editorial reference material** — closer to a crypto research
poster or game cheat sheet than a SaaS landing page. The anti-pattern
is producing something that looks like a marketing website.

## The success state

A piece someone would screenshot, save to their phone, and reference
later. Dense with data. Sections connected by arrows. Bullet points,
not paragraphs. Tables with real numbers. Each section structurally
different from the last.

## The failure mode

Uniform card grids, generous breathing room, paragraph descriptions,
no arrows, no tables. Could pass as a Next.js marketing page. Start
over.

## The Anti-Frontend Checklist (run before delivery)

- **No uniform card grids** — each section uses a different layout.
- **No paragraph descriptions** — body text is bullet points. One
  line per fact.
- **No generous whitespace within sections** — whitespace separates
  SECTIONS, within a section content packs tight.
- **No isolated sections** — sections connect via arrows, flow
  lines, or shared color coding.
- **No all-same-component-type** — variety is mandatory. If 3+
  sections use "feature cards", replace at least one.
- **No missing tables** — if data has comparisons / specs / rates /
  tiers / requirements, it lives in a table.
- **No ghost borders** — `rgba(255,255,255,0.08)` is invisible. Use
  `rgba(primary, 0.3)` minimum.

## Density targets by canvas

```
Portrait-medium (1080×1440):   8–15 content blocks
Portrait-tall   (1080×1920):  12–20 content blocks
Landscape       (1200×675):    4–8  content blocks
Square          (1080×1080):   5–10 content blocks
```

A "content block" = table, chart, stat callout, bullet list, flow
diagram, or callout box.

## Spacing rules (THE signature)

```
Between major sections:    24–32px + thin horizontal rule or colored border
Within sections (items):   8–12px gap
Card/panel internal pad:   12–16px   (NOT 24–32px frontend padding)
Section header to content: 8–12px
Body font size:            11–13px dense, 14px max
Table cell padding:        6px 10px  (NOT 12px 16px)
```

## Content format hierarchy (top = prefer)

1. **Tables** — for any comparison, specs, rates, tiers
2. **Bullet lists** — features, rules, steps, conditions
3. **Flow diagrams with arrows** — processes, economies, how-it-works
4. **Stat callouts** — key numbers, oversized hero stats
5. **Badges / pills** — categories, tiers, status, chains
6. **Paragraphs** — LAST RESORT, 1-2 sentence hero only

## Gotchas

- The density is intentional. Don't "simplify" — you'll make it look
  like a SaaS page.
- Generous whitespace is the tell that you're designing a website,
  not an infographic.
- If you're tempted to "add more breathing room", first check —
  are you adding a 3rd feature-cards grid? Replace it with a table.

## Cross-references

- `TECH-section-variety-rule.md` — the mandatory 3+ component types rule.
- `TECH-signature-palette.md` — colors and near-black backgrounds.
- `TECH-arrows-and-connectors.md` — the flow diagram rule.
- `TECH-stacked-reference-archetype.md` — the default canvas architecture.
- [`../SKILL.md`](../SKILL.md) — parent skill

