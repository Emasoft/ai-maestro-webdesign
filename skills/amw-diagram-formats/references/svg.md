# SVG — canonical format reference

This file is the single authoritative spec for SVG within the `ai-maestro-webdesign` plugin. Every skill that creates, modifies, validates, or converts SVG pulls from this file. Format definition, structural primitives, viewport rules, text rendering, rasterization path, validation, and the technique catalog are all below.

**Consumers (cross-references):**
- `../../amw-svg-creator/SKILL.md` — GATED single-SVG producer (icons / logos / patterns / animations)
- `../../amw-diagram-svg/SKILL.md` — freeform node-and-edge SVG
- `../../amw-diagram-architecture/SKILL.md` — layered architecture → JSON / SVG / PNG / Mermaid
- `../../amw-diagram-editorial/SKILL.md` — editorial HTML+SVG producer (13 archetypes)
- `../../amw-ascii-to-svg/SKILL.md` — ASCII → SVG parse/classify/route
- `../../amw-svg-creator/references/advanced-techniques.md` — filter / gradient / animation cookbook
- `../../bin/amw-svg-render.py` — render-verify-finish loop (`render` / `finish` / `status` / `reset`)
- `./ir-schema.md` — when SVG is a source of the diagram IR
- `./conversion-matrix.md` — SVG → {ASCII, HTML, Mermaid, PNG} cells
- `./png.md` — SVG → PNG via cairosvg
- `./validation-dispatcher.md` — SVG validator branch (`xmllint --noout --nonet` + SVG-namespace check)

---

## 1. Format definition

SVG in this plugin is **XML markup, one root `<svg>` element, self-contained, valid XML**.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H"
     role="img" aria-labelledby="svg-title">
  <title id="svg-title">Descriptive title — matches alt text</title>
  <desc id="svg-desc">Optional longer description</desc>
  <defs>
    <!-- gradients, filters, clipPaths, patterns, markers -->
  </defs>
  <g id="background"></g>
  <g id="midground"></g>
  <g id="foreground"></g>
  <g id="effects"></g>
</svg>
```

### 1.1 Non-negotiables

- `xmlns="http://www.w3.org/2000/svg"` on the root element — always
- All tags closed, all `&` escaped as `&amp;`
- **No remote resources**: no `<script>`, no external CSS `<link>`, no `<image href="http...">` to remote URLs, no `@import url(...)` to external stylesheets
- Exception: `mermaid-render` output emits exactly one `@import url('https://fonts.googleapis.com/...Inter...')` for font rendering, documented and strippable for CSP-locked deployment (see `../../skills/amw-mermaid-render/SKILL.md`)

### 1.2 Allowed primitives

`<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<polyline>`, `<line>`, `<path>`, `<text>`, `<tspan>`, `<g>`, `<defs>`, `<filter>`, `<linearGradient>`, `<radialGradient>`, `<pattern>`, `<marker>`, `<symbol>`, `<use>`, `<clipPath>`, `<mask>`, `<animate>`, `<animateTransform>`, `<animateMotion>`, `<mpath>`, `<title>`, `<desc>`, `<style>`.

### 1.3 Forbidden primitives

- `<script>` — zero JavaScript in SVG output
- `<foreignObject>` with HTML content — breaks cairosvg rasterization
- `<image>` with remote `href` — breaks self-containment
- `<video>` / `<audio>` / `<iframe>` — out of scope

---

## 2. Structural primitives (diagram-grade usage)

### 2.1 Node shapes by type

| Node type | Shape | Notes |
|---|---|---|
| Process / Service | `<rect>` with `rx="20" ry="20"` (rounded) | Stroke 4, fill neutral |
| Database | `<ellipse>` top + `<rect>` body + `<ellipse>` bottom (cylinder) | TECH-SV-06 |
| User / Actor | `<circle>` | TECH-SV-07 |
| Decision | `<polygon>` diamond | TECH-SV-08 |
| External system | `<rect>` with dashed stroke `stroke-dasharray="8 4"` | TECH-SV-09 |
| Queue | `<rect>` with squiggle / wavy overlay | TECH-SV-10 |

### 2.2 Edges

```xml
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 10 3, 0 6" fill="currentColor"/>
  </marker>
</defs>
<line x1="200" y1="500" x2="400" y2="500" stroke="currentColor" stroke-width="4"
      marker-end="url(#arrow)"/>
```

- Solid edge = sync call
- Dashed edge (`stroke-dasharray="8 4"`) = async call
- Hollow marker head = dependency (UML-style)

---

## 3. Viewport rules

### 3.1 Canonical viewBoxes

| Use | viewBox | Coordinate center |
|---|---|---|
| Freeform diagram (`diagram-svg`) | `0 0 1000 1000` | `(500, 500)` |
| Icon | `0 0 24 24` | `(12, 12)` |
| Logo (app-icon scale) | `0 0 64 64` | `(32, 32)` |
| Architecture (`diagram-architecture`) | `0 0 1200 800` | `(600, 400)` |
| Editorial / print (`diagram-editorial`) | `0 0 1920 1080` | `(960, 540)` |

### 3.2 `preserveAspectRatio`

Default `xMidYMid meet` works for 95% of cases. Change only if the SVG must crop or stretch:
- `xMidYMid slice` — fill container, crop overflow (full-width hero only)
- `none` — stretch, preserve no aspect (NEVER for diagrams)

### 3.3 Responsive sizing

```xml
<svg viewBox="0 0 1000 1000" width="100%" height="auto"
     style="max-width: 800px;">
```

Drop explicit `width="800"` in favor of `viewBox` + CSS `max-width`. Let the container drive.

### 3.4 Margin reserves

Every diagram reserves ≥ 40 units on all sides. No node touches the canvas edge. Minimum internal node spacing = 120 units on the active axis (120 × 120 for grid layouts).

---

## 4. Text rendering rules

### 4.1 Font stack

```css
font-family: "Inter", ui-sans-serif, system-ui, sans-serif;
```

For `<pre><code>` content inside SVG: `ui-monospace, SFMono-Regular, Menlo, monospace`.

### 4.2 Centering

```xml
<text x="500" y="500" text-anchor="middle" dominant-baseline="central"
      font-size="24" fill="currentColor">Label</text>
```

- `text-anchor="middle"` — horizontal centering
- `dominant-baseline="central"` — vertical centering (more reliable than `alignment-baseline`)
- Font size in viewBox units; at 1920×1080 with viewBox 1000×1000, `font-size=18` renders ≈ 35px (above the 24px slide floor)

### 4.3 Long labels

Split into `<tspan>` lines:

```xml
<text x="500" y="500" text-anchor="middle" font-size="20">
  <tspan x="500" dy="0">First line</tspan>
  <tspan x="500" dy="24">Second line</tspan>
</text>
```

Truncate labels > 20 characters with `...` (TECH-SV-22).

---

## 5. Rasterization path

### 5.1 SVG → PNG via cairosvg

```python
import cairosvg
cairosvg.svg2png(url="diagram.svg", write_to="diagram.png",
                 output_width=1920, dpi=96)
```

`../../bin/amw-svg-render.py` wraps cairosvg with:
- `render <file>` — emit PNG preview, increment iteration counter
- `finish <file> [name]` — finalize; REFUSES if `render` was never called (render-verify-finish guard)
- `status` — show current iteration count
- `reset` — clear state dir

### 5.2 Filter compatibility with cairosvg

cairosvg supports most filter primitives but with caveats:
- `feTurbulence` — supported
- `feGaussianBlur` / `feOffset` / `feComposite` / `feMerge` / `feFlood` — supported
- `feColorMatrix` — supported (all types)
- `feComponentTransfer` — supported (linear, gamma, table, discrete)
- `feDisplacementMap` — supported
- `feSpecularLighting` / `feDiffuseLighting` — partially supported (may differ from browser)
- `feConvolveMatrix` — supported

### 5.3 SMIL in rasterized output

cairosvg rasterizes the first frame. SMIL animations (`<animate>` / `<animateMotion>` / `<animateTransform>`) resolve to their initial state. For animated PNG output, use browser-based renderer (Playwright) via `../../bin/amw-html-export.py` after wrapping the SVG in `<html><body>`.

---

## 6. Validation

### 6.1 Check list

1. **Well-formed XML** — `xmllint --noout --nonet diagram.svg`
2. **SVG namespace** — root element has `xmlns="http://www.w3.org/2000/svg"`
3. **No remote resources** — grep for `http://` / `https://` in `href` / `src` / `url()` attributes (fail with `FIX:` hint)
4. **No `<script>`** — grep for `<script` (fail)
5. **All tags closed** — covered by well-formed check

### 6.2 Output contract

Per `./validation-dispatcher.md`: `PASS|FAIL: line: message [FIX: hint]`. Example:

```
FAIL: 42: <script> forbidden in SVG. FIX: remove <script> and move interactivity to host page
FAIL: 18: missing xmlns. FIX: add xmlns="http://www.w3.org/2000/svg" to <svg>
PASS
```

### 6.3 Render-verify as final gate

`svg-creator` and `diagram-svg` both run `bin/amw-svg-render.py render → view PNG → finish` as mandatory — passing the XML validator is not enough; Claude must visually inspect the PNG before shipping.

---

## 7. Per-source breakdown of the technique catalog

| Src | Source material | TECH range | Focus |
|---|---|---|---|
| S1 | `skills/amw-svg-creator/references/advanced-techniques.md` | TECH-SV-01 .. TECH-SV-14 | Filter chains (drop / inner / glow / specular / glassmorphism / noise / vignette / emboss) |
| S2 | `skills/amw-diagram-svg/SKILL.md` + `SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md` | TECH-SV-15 .. TECH-SV-22 | Node shapes, arrow markers, viewBox, spacing, labels |
| S3 | `skills/amw-diagram-svg/SKILL.md` animations + `advanced-techniques.md` §9 | TECH-SV-23 .. TECH-SV-29 | Animation primitives, SMIL, CSS, reduced motion |
| S4 | `SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md` | TECH-SV-30 .. TECH-SV-36 | Editorial SVG: 13 archetypes, self-contained, brand tokens |
| S5 | `SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/` | TECH-SV-37 .. TECH-SV-41 | Layered arch on canvas, zone labels, component stacks |
| S6 | `advanced-techniques.md` §4 Material + §7 Icons + §8 Logos + §10 Data-vis + §11 Patterns + §12 Power features | TECH-SV-42 .. TECH-SV-54 | Materials, icons-with-depth, logos, bar/donut charts, patterns, paint-order, `pathLength` |

Total: **54 techniques**, 6 sources.

---

## 8. Technique catalog

Format: `TECH-SV-NN <name>: <description> | source: <path>:<section> | applies-to: <use-case>`

### S1 — svg-creator filter cookbook

TECH-SV-01 drop-shadow-filter: `feGaussianBlur → feOffset → feFlood → feComposite → feMerge`; `color-interpolation-filters="linearRGB"` on `<filter>` | source: svg-creator/references/advanced-techniques.md:28-38 | applies-to: card / chrome / hero shadow
TECH-SV-02 inner-shadow-filter: `feComponentTransfer type="table" tableValues="1 0"` to invert alpha, then blur+offset, composite `in` | source: advanced-techniques.md:62-76 | applies-to: inset effects, pressed-button look
TECH-SV-03 soft-glow-filter: `feGaussianBlur stdDeviation="8"` + feMerge with SourceGraphic last | source: advanced-techniques.md:48-57 | applies-to: halo around logos, key elements
TECH-SV-04 salt-pepper-texture: pepper (multiply) + salt (overlay) fractal-noise blend for tactile grain | source: advanced-techniques.md:82-96 | applies-to: poster/plate textures, non-digital feel
TECH-SV-05 subtle-paper-texture: `feTurbulence baseFrequency="0.9"` + `feComponentTransfer` normalized at ~0.5 + multiply blend | source: advanced-techniques.md:100-110 | applies-to: editorial backgrounds, print-ready pieces
TECH-SV-06 specular-lighting: `feSpecularLighting surfaceScale="5" specularConstant="0.75"` + `fePointLight x y z` | source: advanced-techniques.md:114-127 | applies-to: glossy UI elements, chrome surfaces
TECH-SV-07 diffuse-lighting: `feDiffuseLighting` + `feDistantLight azimuth="225" elevation="45"` | source: advanced-techniques.md:131-140 | applies-to: matte materials, natural lighting
TECH-SV-08 emboss-filter: `feConvolveMatrix order="3" kernelMatrix="-2 -1 0 -1 1 1 0 1 2"` | source: advanced-techniques.md:143-147 | applies-to: debossed badges, raised glyphs
TECH-SV-09 glassmorphism-filter: `feTurbulence` + `feDisplacementMap scale="12"` + `feSpecularLighting` for frosted glass | source: advanced-techniques.md:152-170 | applies-to: glass cards (limited per ai-slop-avoid TECH-23)
TECH-SV-10 vignette-radial: `<radialGradient>` black-to-transparent with `mix-blend-mode: multiply` | source: advanced-techniques.md:173-179 | applies-to: photograph-style edge darkening
TECH-SV-11 feturbulence-parameter-guide: baseFrequency 0.01-0.05 = clouds; 0.5-0.8 = paper grain; numOctaves=3 sweet spot | source: advanced-techniques.md:185-204 | applies-to: texture scale tuning
TECH-SV-12 feturbulence-stitch: always `stitchTiles="stitch"` for pattern fills (seamless tiling) | source: advanced-techniques.md:204 | applies-to: repeating backgrounds
TECH-SV-13 duotone-component-transfer: `feColorMatrix saturate 0` + `feFuncR/G/B type="table"` with 2-value tables | source: advanced-techniques.md:252-260 | applies-to: editorial duotone photos, brand-tinted images
TECH-SV-14 gamma-curve: `feFuncR/G/B type="gamma" amplitude="1" exponent="0.7"` to lighten midtones | source: advanced-techniques.md:263-268 | applies-to: shadow lifting, brightness correction

### S2 — diagram-svg + baybee-diagram

TECH-SV-15 rect-rounded-process: `<rect rx="20" ry="20">` for Process/Service nodes, stroke 4, flat fill | source: diagram-svg/SKILL.md:60-66 | applies-to: any Process/Service node
TECH-SV-16 cylinder-database: `<ellipse>` top + `<rect>` body + `<ellipse>` bottom for DB nodes | source: diagram-svg/SKILL.md:63 | applies-to: any Database node
TECH-SV-17 circle-actor: `<circle>` for User/Actor nodes | source: diagram-svg/SKILL.md:64 | applies-to: end-user / human agent nodes
TECH-SV-18 polygon-diamond-decision: `<polygon>` 4-point for decision diamonds | source: diagram-svg/SKILL.md:65 | applies-to: yes/no gates, flow branches
TECH-SV-19 dashed-external: `stroke-dasharray="8 4"` on rect for External-System nodes | source: diagram-svg/SKILL.md:66 | applies-to: 3rd-party APIs, out-of-scope systems
TECH-SV-20 arrow-marker-defs: `<marker id="arrow" refX="8" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6"/>` in `<defs>`; apply via `marker-end="url(#arrow)"` | source: diagram-svg/SKILL.md:91-100 | applies-to: all directional edges
TECH-SV-21 minimum-spacing-120: minimum 120-unit spacing on the active axis, 40-unit margin reserve | source: diagram-svg/SKILL.md:108-116 | applies-to: every multi-node layout
TECH-SV-22 label-truncate-20: labels > 20 chars truncate with `...`, or split with `<tspan>` | source: baybee-diagram/SKILL.md:259-261 | applies-to: long node names, endpoint URLs

### S3 — animations (SMIL + CSS)

TECH-SV-23 animate-motion-on-path: `<circle><animateMotion dur="2s" repeatCount="indefinite"><mpath href="#flow-a-b"/></animateMotion></circle>` | source: diagram-svg/SKILL.md:140-148 | applies-to: data-flow pulse on connector
TECH-SV-24 animate-opacity-pulse: `<animate attributeName="opacity" values="1;0.4;1" dur="1.5s" repeatCount="indefinite"/>` | source: diagram-svg/SKILL.md:155-158 | applies-to: gentle pulse on focal node
TECH-SV-25 reduced-motion-guard: `@media (prefers-reduced-motion: reduce) { * { animation: none !important; } animate, animateMotion, animateTransform { display: none; } }` — MANDATORY on every animated SVG | source: diagram-svg/SKILL.md:166-172 | applies-to: every animation-bearing SVG
TECH-SV-26 transform-box-fill: `transform-box: fill-box; transform-origin: center;` on every animated element | source: advanced-techniques.md:584-587 | applies-to: CSS-animated SVG elements
TECH-SV-27 stroke-dasharray-draw: `stroke-dasharray: 1; stroke-dashoffset: 1; animation: reveal 2s ease forwards;` + `pathLength="1"` on path | source: advanced-techniques.md:602-612 | applies-to: line-drawing reveal animations
TECH-SV-28 staggered-entrance: `:nth-child(N) { animation-delay: N*0.15s; }` with fadeUp keyframes | source: advanced-techniques.md:616-628 | applies-to: staggered reveals, multi-node entrances
TECH-SV-29 animation-timing: pulses 1.2-1.8s; spinners 0.8-1.2s; progress fills 0.4-0.8s; walk 1-1.2s; run 0.5-0.7s | source: svg-creator/SKILL.md:85 + advanced-techniques.md:872-874 | applies-to: duration selection per motion type

### S4 — diagram-design-editorial

TECH-SV-30 editorial-13-archetypes: Architecture / Flowchart / Sequence / StateMachine / ER / Timeline / Swimlane / Quadrant / Nested / Tree / Layer-stack / Venn / Pyramid — pick one | source: diagram-design-editorial/SKILL.md:45-60 | applies-to: editorial diagram type selection
TECH-SV-31 no-build-inline-only: emit single-file with inline CSS+SVG, no CDN CSS, no npm | source: diagram-design-editorial/SKILL.md:18 | applies-to: every editorial SVG output
TECH-SV-32 minimal-palette-2-3: 2-3 colors per diagram (accent + neutral + 1 semantic max) | source: diagram-design-editorial/SKILL.md:68 | applies-to: diagram-region coloring
TECH-SV-33 brand-tokens-first: derive tokens from brand site (60s scrape) before picking defaults | source: diagram-design-editorial/SKILL.md:19 | applies-to: brand-bound editorial pieces
TECH-SV-34 reader-value-test: "would a reader learn more than from a paragraph?" — if no, delete | source: diagram-design-editorial/SKILL.md:63 | applies-to: decorative diagram removal gate
TECH-SV-35 4px-grid-align: every coordinate divisible by 4 prevents AI-jitter | source: diagram-design-editorial/SKILL.md:139 | applies-to: node positioning / grid layouts
TECH-SV-36 one-accent-rule: exactly 1 accent node per diagram, rest neutral | source: diagram-design-editorial/SKILL.md:152-154 | applies-to: highlighting discipline

### S5 — architecture-canvas (layered arch patterns)

TECH-SV-37 layered-zones: horizontal bands (frontend / backend / data) with `<rect>` zone backgrounds at low opacity | source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas (inferred from layout) | applies-to: tiered architecture diagrams
TECH-SV-38 zone-label-left: zone names right-justified in 120px left gutter, vertical center of the band | source: architecture-canvas patterns | applies-to: layered system naming
TECH-SV-39 component-stack: multiple `<rect>` nodes horizontally inside a zone band, uniform width | source: architecture-canvas patterns | applies-to: multi-service layers
TECH-SV-40 external-zone-dashed: outer `<rect stroke-dasharray="8 4">` around external systems on the canvas | source: ASCII-STYLES.md analog + architecture-canvas | applies-to: 3rd-party integration zones
TECH-SV-41 cross-zone-edge-markers: edges crossing zone boundaries get `marker-start` + `marker-end` both set for clarity | source: architecture-canvas patterns | applies-to: inter-zone flow

### S6 — advanced cookbook (materials / icons / logos / data-vis / patterns / power)

TECH-SV-42 metal-gradient-7-stops: `<linearGradient>` with 7 stops `#e8e8e8 #6b6b6b #d4d4d4 #888 #e0e0e0 #555 #b0b0b0`; `spreadMethod="reflect"` for brushed repeat | source: advanced-techniques.md:278-287 | applies-to: metallic logos, chrome surfaces
TECH-SV-43 glass-layers: low-opacity base (0.12) + highlight streak (0.5 angled linear) + dark stroke (0.3) + bottom reflected ellipse | source: advanced-techniques.md:297-308 | applies-to: transparent UI elements
TECH-SV-44 wood-grain-turbulence: `baseFrequency="0.02 0.2"` directional turbulence + brown `feColorMatrix` | source: advanced-techniques.md:314-318 | applies-to: natural-material backgrounds
TECH-SV-45 icon-stroke-24: 24×24 viewBox, `stroke-width="2"`, `stroke-linecap="round"`, `stroke-linejoin="round"`, `fill="none"`, `stroke="currentColor"`, coords 2-22 | source: svg-creator/SKILL.md:19 | applies-to: every stroke icon
TECH-SV-46 icon-shine-overlay: 64×64 app icons: `<rect x="4" y="4" width="56" height="28" rx="10" fill="white" opacity="0.12"/>` top shine | source: advanced-techniques.md:542 | applies-to: app-icon glossy finish
TECH-SV-47 logo-cast-shadow: `<circle cx="103" cy="106" r="72" fill="#1e1b4b" opacity="0.15" filter="url(#soft)"/>` offset 3px under the main shape | source: advanced-techniques.md:566-568 | applies-to: polished logos
TECH-SV-48 bar-gradient-3-stop: `<linearGradient y1=0 y2=1>` with 3 stops light-mid-dark + `filter="url(#drop-shadow)"` | source: advanced-techniques.md:689-698 | applies-to: bar-chart bars, KPI columns
TECH-SV-49 donut-dasharray: `stroke-dasharray="<percent × circumference> <circumference>"`, `transform="rotate(-90 cx cy)"`, `stroke-linecap="round"` | source: advanced-techniques.md:701-707 | applies-to: donut/pie segments
TECH-SV-50 pattern-userspace: `<pattern patternUnits="userSpaceOnUse" width="20" height="20"><circle cx="10" cy="10" r="1.5"/></pattern>` | source: advanced-techniques.md:742-744 | applies-to: dotted backgrounds, tile fills
TECH-SV-51 pattern-rotate: `patternTransform="rotate(45)"` on a pattern for diagonal lines | source: advanced-techniques.md:747-750 | applies-to: diagonal hatching backgrounds
TECH-SV-52 paint-order-stroke-first: `paint-order="stroke fill"` renders stroke behind fill → outlined text / halo effects without duplicate elements | source: advanced-techniques.md:762-764 | applies-to: outlined icons, halo text
TECH-SV-53 vector-effect-non-scaling: `vector-effect="non-scaling-stroke"` keeps stroke width constant under transforms/zoom | source: advanced-techniques.md:767-768 | applies-to: icons at multiple scales, technical illustrations
TECH-SV-54 path-length-normalize: `pathLength="1"` + `stroke-dasharray="0.5 0.5"` = 50% dashed regardless of path length | source: advanced-techniques.md:771-773 | applies-to: line-drawing animations, dash patterns across multi-path groups

---

## 9. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| SVG fails to parse | Unclosed tag, stray `&`, missing `xmlns` | Close all tags, escape `&` → `&amp;`, add `xmlns="http://www.w3.org/2000/svg"` |
| Labels overflow nodes | Font too large or label too long | Split via `<tspan>` or shorten before dropping below 18 viewBox units |
| Arrowheads invisible | `<marker>` absent or `marker-end` URL typo | Verify `<marker id="arrow">` in `<defs>` matches |
| Edges tangle | Spacing < 120 units | Increase spacing, reflow, or switch to grid |
| `cairosvg` blank output | Content outside viewBox, or filter cairosvg doesn't support | Reposition inside viewBox, simplify filters |
| Animation off-centre | Missing `transform-box: fill-box; transform-origin: center;` | Add both CSS properties to animated elements |
