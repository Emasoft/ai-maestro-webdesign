# TECH — Named Color, Shadow, Near-Black, Mesh Gradients, Optical Letter-Spacing

**License:** Clean-room original. No upstream source.
**Audience:** `amw-wireframe-builder-agent`, `amw-component-library-architect-agent`, `amw-asset-generator-agent`, `amw-infographic-builder-agent`, `amw-email-designer-agent`.
**Purpose:** Four bundled "taste" techniques that separate competent visual output from generic AI-slop output. Each rule has a numeric threshold that can be checked mechanically.

These rules apply to every HTML/SVG/PNG artifact the plugin produces. They are enforced post-generation by `bin/amw-ai-slop-check.py` against the patterns listed below, and they should also be checked at authoring time before delivery.

---

## 1. Colored shadows (never pure black shadows)

A pure-black shadow (`box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3)`) is the single fastest tell for AI-slop output. Real designers tint shadows toward the element's own hue, darkened by ~30-50% lightness and desaturated by ~20-30%. The result reads as light + ambient occlusion, not as a black cloud floating under the element.

### Rule

For any non-neutral element (card, button, badge, panel), the shadow color MUST be derived from the element's surface color:

```
shadow.h = surface.h                    # keep hue
shadow.s = max(0, surface.s - 20)       # desaturate ~20%
shadow.l = max(8, surface.l - 35)       # darken ~35%, floor at 8%
shadow.a = 0.18 – 0.32                  # never above 0.4
```

### Before / after

```css
/* Slop: black shadow on a blue card */
.card-bad {
  background: #3b82f6;             /* blue-500 */
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.30);
}

/* Tasteful: shadow tinted toward the card's hue */
.card-good {
  background: #3b82f6;
  box-shadow: 0 8px 24px rgba(29, 78, 216, 0.28); /* blue-700 alpha */
}
```

### Neutrals exception

Pure-grey cards on pure-white backgrounds may use a neutral shadow (`rgba(15, 23, 42, 0.10)`). The rule applies only to chromatic surfaces.

### Stacked shadows (production-grade)

For elevated surfaces (modals, popovers, the hovered card in a grid), stack two tinted shadows — one tight for contact, one wide for ambience:

```css
box-shadow:
  0 1px 2px  rgba(29, 78, 216, 0.18),    /* contact */
  0 12px 32px rgba(29, 78, 216, 0.22);   /* ambient */
```

The contact shadow stays small (≤4 px blur) and grounds the element. The ambient shadow carries the elevation reading.

---

## 2. Near-black (never `#000` for backgrounds or large surfaces)

`#000000` is a flat absence of pigment. It has no warmth and no recession — on a screen it reads as a dead hole. Real "black" surfaces in print and product photography are warm dark greys, typically between `#1a1a1a` and `#2d2d2d`.

### Rule

The darkest background color used anywhere in an artifact MUST satisfy `min(R, G, B) >= 0x18` (24 decimal). Borders, glyph outlines, and 1-px decorative strokes may use `#000` — they are too thin for the dead-hole effect to register.

### Warm-dark palette (recommended)

| Token | Hex | When |
|---|---|---|
| `--surface-dark-0` | `#0f0f10` | Pure-dark mode page background, but only if every accent is warm |
| `--surface-dark-1` | `#1a1a1d` | Default dark-mode page background |
| `--surface-dark-2` | `#23232a` | Dark-mode card / panel surface |
| `--surface-dark-3` | `#2d2d36` | Dark-mode raised element, modal background |
| `--ink-dark-strong` | `#e5e5ea` | Body text on dark backgrounds (never #fff) |
| `--ink-dark-soft` | `#9ca0aa` | Secondary text on dark backgrounds |

These hexes carry a subtle red+blue warmth that prevents the flat-black look. For a cool-dark aesthetic (true blacks with a blue cast), use `#11151c` / `#1a212e` / `#2a323f` — same principle, different temperature.

### Pure-white parallel

The same rule applies in reverse: `#FFFFFF` body text on `#000000` background is visually harsh and the bane of phototypesetting. Use `#FAFAFA` / `#F5F5F7` for "white" backgrounds and `#E5E5EA` / `#D2D2D7` for "white" text.

---

## 3. Gradient meshes (never single-stop linear gradients on hero surfaces)

Single-stop linear gradients (`background: linear-gradient(135deg, #6366f1, #a855f7)`) are the second-fastest tell for AI-slop output. They flatten any hero or feature surface into a stock-photo banner. A 4-to-6-layer radial-gradient mesh produces depth, atmospheric perspective, and a sense of light direction.

### Rule

Any hero, feature panel, or call-to-action surface larger than 480×240 SHOULD use a stacked radial-gradient mesh, NOT a single linear gradient. Small surfaces (badges, buttons, icon backdrops) may keep linear gradients — the dead-flatness only registers at scale.

### Mesh recipe

```css
.hero-mesh {
  background-color: #0f1a2e;                 /* base color = darkest stop */
  background-image:
    radial-gradient(at 12% 18%, hsla(252, 80%, 60%, 0.55) 0px, transparent 50%),
    radial-gradient(at 88% 22%, hsla(199, 86%, 55%, 0.40) 0px, transparent 50%),
    radial-gradient(at 24% 82%, hsla(322, 70%, 60%, 0.30) 0px, transparent 55%),
    radial-gradient(at 78% 78%, hsla(168, 76%, 50%, 0.28) 0px, transparent 55%);
}
```

### Composition rules

1. 4-6 layers. Fewer than 4 looks accidental; more than 6 muddies into beige.
2. Focal points in opposite quadrants. Two top-left + two top-right + two bottom-something distribute the "light sources" across the surface.
3. Decreasing opacity outward. The first 1-2 layers carry 50-60% alpha; the later layers stay under 35%.
4. The base color matches the darkest stop. Without this, the corners read as black holes between the radial bursts.
5. Each layer's hue stays within ±60° of the surface's primary token. Wider hue range becomes carnival.

### Mobile fallback

Mesh gradients are GPU-cheap but cognitively expensive. On mobile breakpoints (< 768 px), reduce to 2-3 layers or fall back to a single tinted background color.

---

## 4. Optical letter-spacing (tighten as fonts grow)

Display type optically appears looser than body type at the same letter-spacing setting because the eye reads counters and side-bearings at a larger angular size. To compensate, real typographers tighten tracking as type grows. AI-default `letter-spacing: 0` everywhere produces "open" headlines that look amateurish.

### Rule (the four-step tracking ramp)

| Font size | `letter-spacing` |
|---|---|
| ≥ 64 px (hero display) | `-0.025em` to `-0.04em` |
| 48–63 px (page-title display) | `-0.02em` |
| 32–47 px (section heading) | `-0.01em` to `-0.015em` |
| 20–31 px (subheadings, lead paragraphs) | `0` (default) |
| < 20 px (body, caption) | `0` to `+0.01em` (slightly loosen long body) |

### Font-specific exceptions

- **Geometric sans (Futura, Avenir, Poppins, Geist)** — apply the full ramp; geometric counters need the tightening to feel solid at scale.
- **Humanist sans (Inter, Source Sans, IBM Plex)** — use 70% of the recommended values; humanist designs already include optical sizing in the glyph design.
- **Serifs with optical sizes (Source Serif, Georgia)** — use 50% of the recommended values, OR rely on the font's built-in optical-size axis if it exists.
- **Monospace (JetBrains Mono, IBM Plex Mono)** — NEVER tighten. Monospace tracking is structural; reducing it breaks the grid.

### Implementation pattern

Encode the ramp as a single utility class set in the design tokens:

```css
.display-xl  { font-size: 72px; line-height: 1.05; letter-spacing: -0.035em; }
.display-lg  { font-size: 56px; line-height: 1.08; letter-spacing: -0.02em;  }
.heading-1   { font-size: 40px; line-height: 1.15; letter-spacing: -0.012em; }
.heading-2   { font-size: 28px; line-height: 1.2;  letter-spacing: 0;        }
.body-lg     { font-size: 18px; line-height: 1.55; letter-spacing: 0;        }
.body-md     { font-size: 16px; line-height: 1.6;  letter-spacing: 0;        }
.caption     { font-size: 13px; line-height: 1.4;  letter-spacing: 0.005em;  }
```

The ramp lives in `design-tokens.json` under `typography.tracking-ramp` and is regenerated into CSS by `bin/amw-design-md-emit-companions.py`.

---

## Mechanical post-output check

`bin/amw-ai-slop-check.py` flags violations of all four techniques:

| Pattern | Detector |
|---|---|
| Black shadow on chromatic surface | regex on `box-shadow.*rgba\(0,\s*0,\s*0` near non-neutral `background:` |
| `#000`/`#000000`/`black` background | regex on `background(-color)?:\s*(#000(0{3})?\|black)\b` |
| Single-stop linear gradient on hero-sized container | DOM-aware check: container ≥ 480×240 AND only one `linear-gradient` in `background-image` |
| `letter-spacing: 0` on font-size ≥ 32 px | computed-style heuristic; warns if size ≥ 32 AND tracking unset or > -0.005em |

The checker emits warnings only — the agent decides whether to suppress (rare; document the rationale) or fix. Suppressing all four in the same artifact is treated as a hard fail.

---

## Cross-references

- `component-taste.md` — broader taste catalog this file extends.
- `TECH-css-variable-discipline.md` — colors used here must come from DESIGN.md tokens, not raw hex literals in markup.
- `bin/amw-ai-slop-check.py` — mechanical enforcement entry point.
- `skills/amw-design-principles/ai-slop-avoid.md` — full slop catalog (this file is the visual-foundation subset).
