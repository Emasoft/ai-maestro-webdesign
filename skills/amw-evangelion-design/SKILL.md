---
name: amw-evangelion-design
description: >-
  Evangelion / NERV-HUD aesthetic skill — original Eva-inspired interface
  language for web and mobile. Severe geometry, amber / red / signal-green
  palette discipline, condensed sans + tabular numerals, mechanical
  state-driven motion. Activates on narrow triggers only: "evangelion ui",
  "NERV hud", "anime control room", "tactical diagnostic overlay", "sync
  monitor", "breach warning ui", "reactor diagnostic screen", "psychograph",
  "title card sci-fi". Does NOT activate on generic "sci-fi", "cyberpunk",
  "dark mode", "tactical dashboard" — those route to amw-design-principles.
author: ai-maestro-webdesign (direct-port from ckorhonen/claude-skills/evangelion-design, MIT, Chris Korhonen)
---

<!-- MIT — adapted from ckorhonen/claude-skills/skills/evangelion-design -->
<!-- Source: https://github.com/ckorhonen/claude-skills (MIT). Reorganised and English-pruned for the ai-maestro-webdesign plugin. -->

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Activated when the user explicitly asks for an
> Evangelion / NERV / anime-control-room aesthetic for a web or mobile
> interface. The orchestrator routes here; do not re-route generic
> "tactical dashboard" or "dark sci-fi" intent back to this skill.

## Scope

Apply an original Evangelion-inspired interface language to product UI without copying franchise assets, exact title cards, or one-to-one screen layouts. The source aesthetic treats UI as STORY PRESSURE — severe geometry, narrow colour signals, dense but legible telemetry, and mechanical motion that behaves like an operating system under stress.

This skill ships:

- The seven canonical **screen roles** the aesthetic supports.
- The disciplined **palette** (one hot accent family per screen).
- **Typography** instrumentation rules (condensed sans + tabular mono).
- **Composition** patterns and the six layout archetypes.
- **Motion** vocabulary (state-driven, not ornamental).
- A pitfalls reference at [TECH-pitfalls](references/TECH-pitfalls.md).
> [TECH-pitfalls.md] Too literal — copying frames instead of extracting principles · Information overload without hierarchy · Missing context cues — users get lost in complexity · Style over function — looks cool, but unusable · Ignoring accessibility — colour and contrast issues · Discipline comparison — NERV UI vs generic sci-fi

It does **not** ship: licensed franchise glyphs, Japanese text as decoration, exact recreations of NERV HQ panels, or generic "neon cyberpunk." The whole point of the skill is the discipline that separates the look from generic sci-fi.

## Quick start

1. **Pick a screen role first.** One of: `hud`, `command-center`, `psychograph`, `sync-ladder`, `reactor-diagnostic`, `breach-monitor`, `title-card`.
2. **Pick one hot accent family** for the screen: `amber`, `red`, or `signal-green`. Add **one** cool support (cyan / blue / teal / magenta) only when separation is genuinely needed.
3. **Compose from frames, rulers, rings, bars, masks, repeated device arrays, and crosshair geometry** before adding decorative texture.
4. **Animate by revealing state**: counters, sweeps, trace plotting, sync steps, panel swaps, alert pulses. Never animate for animation's sake.
5. **Keep the work original.** Echo the language; do not reuse exact logos, title cards, or one-to-one screen compositions.

## Screen roles

Each role has a dramatic job. Choose the role BEFORE choosing components.

| Role                  | Dramatic job                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| `hud`                 | First-person overlay on top of imagery. Wide masks, target brackets, sparse ticks, range markers. |
| `command-center`      | Black-field dashboards with contained modules, status rails, tables, analytic views.               |
| `diagnostic`          | Charts, sync traces, matrices, ring analyzers. Precision and hierarchy over spectacle.             |
| `psychograph`         | Bounded graph surfaces with rulers, sparse cross markers, label boxes, one dense signal trace.     |
| `sync-ladder`         | Repeated capsules / bars / slotted modules stepping across rows or diagonals.                      |
| `reactor-diagnostic`  | Triptych or panoramic board with a dominant central radial analyzer and intentionally sparse bays. |
| `breach-monitor`      | Oversized timers, progress blocks, rack arrays, projected-penetration bars.                        |
| `warning-state`       | Modifier on any role: higher contrast, countdowns, repeated status labels, tighter cadence.        |
| `title-card`          | Near-empty black composition with oversized typography and one dominant accent.                    |

## Palette

A dark structural base + one dominant signal family. Keep **at least 70% of the screen** in dark neutrals.

### Core darks (mandatory on every screen)

| Token             | Hex       | Role                                       |
| ----------------- | --------- | ------------------------------------------ |
| `--eva-bg`        | `#0b090b` | Primary background                         |
| `--eva-panel`     | `#140e0f` | Raised panels, masked overlays             |
| `--eva-panel-2`   | `#221012` | Deep active surfaces                       |
| `--eva-fog`       | `#344642` | Cool atmospheric support for HUD views     |

### Hot signal family (PICK ONE per screen)

| Token                 | Hex       | Role                                         |
| --------------------- | --------- | -------------------------------------------- |
| `--eva-alert`         | `#8f1507` | Critical alerts, outlines, emphasis (red)    |
| `--eva-alert-2`       | `#bb622d` | Warm linework, secondary highlight           |
| `--eva-warning`       | `#f19e1f` | Timers, warning numerals (amber)             |
| `--eva-warning-soft`  | `#cca552` | Filled charts, inactive caution blocks       |

### Support signals (use sparingly)

| Token                | Hex       | Role                                         |
| -------------------- | --------- | -------------------------------------------- |
| `--eva-signal-green` | `#549f58` | Normal state, active confirmations           |
| `--eva-cool`         | `#6f9b95` | Secondary graph lines                        |
| `--eva-sync-cyan`    | `#65e6d1` | Sync ladders, psychographic grid             |
| `--eva-sync-blue`    | `#7088ff` | Capsule rows, compatibility rails            |
| `--eva-magenta`      | `#c45484` | Wireframe callout separation                 |
| `--eva-ink`          | `#f3ece2` | Title-card type, rare bright text            |
| `--eva-muted`        | `#9c8a78` | Secondary labels, noncritical captions       |

### Ready-made colour modes

- `command-red` — bg + panel + alert + warning.
- `hud-fog` — bg + fog + warning + tiny alert.
- `bio-scan` — bg + deep crimson + signal-green + restrained warning.
- `sync-array` — bg + panel + sync-cyan + sync-blue + a little warning.
- `orbital-callout` — bg + warning + magenta + restrained alert.
- `title-card` — bg + ink + one muted hot accent.

### Token block (copy verbatim)

```css
:root {
  --eva-bg:           #0b090b;
  --eva-panel:        #140e0f;
  --eva-panel-2:      #221012;
  --eva-fog:          #344642;
  --eva-alert:        #8f1507;
  --eva-alert-2:      #bb622d;
  --eva-warning:      #f19e1f;
  --eva-warning-soft: #cca552;
  --eva-signal-green: #549f58;
  --eva-cool:         #6f9b95;
  --eva-sync-cyan:    #65e6d1;
  --eva-sync-blue:    #7088ff;
  --eva-magenta:      #c45484;
  --eva-ink:          #f3ece2;
  --eva-muted:        #9c8a78;
}
```

## Typography

Use type as instrumentation, not editorial chrome.

- **Condensed sans** for labels and headers: `IBM Plex Sans Condensed`, `Archivo Narrow`, `League Gothic`, or a `DIN Condensed` analog.
- **Mono** for timers, telemetry, and numerical tables: `IBM Plex Mono`, `JetBrains Mono`, `Space Mono`.
- **Rare display serif** for title-card moments ONLY: `Cormorant Garamond`, `Bodoni Moda`, or another severe high-contrast serif.

Rules:

- Default to **UPPERCASE** for labels and section headers.
- Keep labels short and concrete: `SYNC RATE`, `TARGET`, `PHASE`, `LOCK`, `INTERNAL`, `LAYER 01`.
- Use **tabular numerals** everywhere numbers animate or align.
- Body copy is sparse. Communicate through labels, figures, and states — not paragraphs.
- Treat the serif mode as exceptional. Most screens live in condensed sans + mono.

## Composition

### Structural patterns to draw from

- Panoramic masks for HUD overlays.
- Thin ruled frames with hard corners.
- Framed boards with notched tabs or edge registrations.
- Circular analyzers, reticles, sweep arcs.
- Stacked status rails and numbered layers.
- Waveform traces, sine curves, graph axes.
- Wireframe spheres / bodies / volumes surrounded by callouts.
- Repeated capsules / cartridges / sync slots in strict rows.
- Grid-backed data tables with strong alignment.
- Asymmetric placement with one dominant anchor.

### Six layout archetypes

| Archetype             | Anatomy                                                                                          |
| --------------------- | ------------------------------------------------------------------------------------------------ |
| `reactor-triptych`    | One large central radial instrument, two sparse framed side panels, tiny seam connectors.        |
| `panoramic-merge`     | Mirrored device banks around a geometric field pattern in the centre.                            |
| `matrix-rail`         | Repeated capsules / slots with one warning column at the edge.                                   |
| `breach-board`        | Left-aligned timer block, central histogram / penetration bar, right-side rack array.            |
| `psychograph-panel`   | Y-axis ruler, x-axis baseline, sparse cross markers, boxed labels, one aggressive trace.        |
| `orbital-model`       | Central wireframe volume with external annotation shards and coordinate-like labels.             |

### Composition rules

- Start with a black field; place only the modules the story needs.
- Make one module the main event. Everything else supports it.
- Use **scale contrast** aggressively: large number or chart, then tiny labels.
- Keep **line weights thin and precise**. Heavy borders feel chunky.
- Use tiny registration dots, ruler ticks, and corner notches to make the canvas feel instrumented.
- Favour **long horizontal canvases** for system boards.
- Prefer clipping, masking, and hard containment over drop shadows.
- Allow photographic imagery behind HUDs, but desaturate it so the overlay owns the hierarchy.

## Motion

### Principles

- **Mechanical, not playful.** Linear or stepped, never springy.
- **State-driven, not ornamental.** Every animation reveals a state change.
- **Fast, but readable.** 80..320ms for most reveals.
- **Localised to active elements**, not the whole page.

### Motion vocabulary

| Pattern              | Duration              | Usage                                                       |
| -------------------- | --------------------- | ----------------------------------------------------------- |
| `line-draw`          | `80-160ms`            | Frames, rulers, brackets drawing on                         |
| `scan-sweep`         | `180-320ms`           | Horizontal or radial scanner pass                           |
| `counter-tick`       | `40-70ms` per step    | Timers and telemetry increments                             |
| `trace-plot`         | `240-800ms`           | Psychographic lines / analytic curves writing across a graph |
| `ladder-step`        | `60-120ms` per unit   | Sync slots / capsule arrays / repeated indicators advancing |
| `lock-on`            | `120-220ms`           | Brackets converging on a target                             |
| `wireframe-precess`  | `1200-2400ms`         | Slow linear rotation / sectional reveal for volume model    |
| `panel-swap`         | `80-140ms`            | Hard state change between modules                           |
| `alert-pulse`        | `700-1200ms`          | Ongoing critical-state indicator                            |

### Motion rules

- Use `linear`, `ease-out`, or `steps(2-6, end)`. Avoid spring / bounce / overshoot.
- Stagger as a system boot cue: frame, then labels, then numbers.
- Countdowns visibly tick. They should feel procedural.
- Animate plotted traces as if data is being written by a machine.
- Advance repeated sync modules one unit at a time.
- Keep wireframe models slow and clinical. They precess or reveal slices — they do not "spin."
- Use opacity, transform, clip, and mask reveals instead of large blurs.

### Reduced-motion fallback

- Every state change must be readable with motion disabled.
- Replace sweeps with instant reveals.
- Freeze looping alert motion into static high-contrast states.
- Preserve countdown meaning via text and colour, not motion alone.

## Adapting for web and mobile

### Web

- Lean into wide hero canvases for HUD / command views.
- Allow secondary telemetry to live in rails, overlays, and side modules.
- Use framed panoramic boards for dashboards with repeated devices / counters / breach projections.
- Favour CSS variables for the palette so the tokens compose with existing design systems.
- Primary actions stay obvious; style the STATE display around them, never bury them in it.

### Mobile

- Promote ONE active module per screen.
- Stack supporting metrics into narrow bands, tabs, or drawers.
- Convert triptychs to a central hero analyzer with collapsible side panels.
- Convert matrix rails to paged slices or horizontal scrollers with a fixed summary.
- Reserve tiny telemetry for non-interactive support text.
- Respect safe areas; hard-edged frames must not collide with the notch or home indicator.
- Use motion sparingly. One scan or lock-on reads better than five concurrent loops.

## Guardrails (hard rules)

- Do not default to purple gradients, glassmorphism, soft blur, or playful spring motion.
- Do not make every surface glow. Most of the screen stays matte, dark, controlled.
- Do not use Japanese text or franchise symbols as decoration.
- Do not sacrifice accessibility for density; hierarchy must read with motion disabled.
- Do not copy Evangelion assets or layouts literally. Produce an original interpretation with the same tension and rigor.
- Pass WCAG AA contrast (4.5:1 body text, 3:1 large) on every hot-on-dark pairing.
- Add label / icon / shape cues to every colour-coded signal — never rely on red-vs-green alone.

See [TECH-pitfalls](references/TECH-pitfalls.md) for the five common failure modes (too literal / information overload / missing context / style-over-function / accessibility) with worked examples.
> [TECH-pitfalls.md] Too literal — copying frames instead of extracting principles · Information overload without hierarchy · Missing context cues — users get lost in complexity · Style over function — looks cool, but unusable · Ignoring accessibility — colour and contrast issues · Discipline comparison — NERV UI vs generic sci-fi

## Review checklist

- Does the screen communicate a clear system state or mission context?
- Is one module obviously primary?
- Is the palette limited and intentional?
- Would the interface still read if all motion stopped?
- Are the numbers aligned and easy to scan?
- Is the mobile version simplified rather than compressed?
- Does the result feel original rather than copied from a specific Evangelion frame?

## Cross-references

- **Sibling aesthetic skill:** [amw-liquid-glass](../amw-liquid-glass/SKILL.md) — the polar-opposite aesthetic (soft / translucent / spatial).
- **Generic colour / type / layout reference:** [amw-design-principles](../amw-design-principles/SKILL.md).
- **Design-system encoding companion:** [amw-design-system-presets](../amw-design-system-presets/SKILL.md) — if a one-shot preset is needed instead of the full encoded aesthetic.
