---
name: amw-generative-backgrounds
description: >-
  GPU shader background catalog for the web — 11 generative background types
  (mesh-gradient, voronoi, liquid-metal, plasma, etc.) plus 17 image-overlay
  effects (ASCII, dither, halftone, glitch, etc.). Activates on narrow
  triggers only: "generative background", "shader background", "WebGL
  background", "mesh gradient background", "voronoi hero", "liquid metal
  background", "fragment-shader hero", "GLSL background", "background effect
  catalog". Does NOT activate on generic "background", "gradient", "hero
  section", "wallpaper" — those route to amw-design-principles.
version: 0.1.0
author: ai-maestro-webdesign (clean-room, no upstream license)
---

<!-- Clean-room — no source library, no upstream license to inherit. -->
<!-- This is a CATALOG skill: it documents the design vocabulary of GPU-rendered backgrounds and image overlays without bundling any third-party shader source. -->

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Activated when the user asks for a generative GPU
> background, a shader-driven hero, or a catalog of image-overlay effects
> (ASCII, dither, halftone, glitch, etc.). The orchestrator routes here;
> do not re-route generic "make the background nicer" intent back to this
> skill.

## Scope

This skill is a **catalog**, not a runtime. It enumerates the canonical generative-background TYPES used in modern web design, documents what each one looks like, the parameters that drive its visual range, the performance envelope on commodity hardware, and the design contexts where each one earns its place. It also documents the parallel catalog of image-overlay EFFECTS (ASCII / dither / halftone / glitch / art) that turn a static raster into an aesthetic surface.

What this skill ships:

- 11 generative background **types**, each with name, visual identity, primary parameters, perf envelope, and use case.
- 17 image-overlay **effects**, same structure.
- A short selection matrix: which type fits which design preset.
- A pitfalls list for shader-heavy backgrounds.

What this skill does **NOT** ship:

- The shader source. There are many MIT-licensed and proprietary shader libraries; this catalog is library-agnostic. Use upstream libs (e.g., Three.js, PixiJS, custom GLSL fragment shaders) or write the shader yourself.
- Image filtering source. Same reason — there are excellent libraries (HyperComp, Glfx, jsfx-pixijs) and this catalog deliberately stays implementation-neutral.
- A WebGL playground / preview server. That is a separate concern.

The 11 + 17 vocabulary below is the **language**; the implementation is downstream of the design choice.

## The 11 generative background types

Each type has a NAME (canonical handle used in design briefs), a one-line visual identity, the parameters that control its visual range, a perf envelope (target FPS on mid-range mobile), and the primary use case.

### 1. `mesh-gradient`

- **Visual identity:** Smooth multi-stop gradient with soft colour blobs flowing across the surface. Reads as "premium SaaS hero" or "Stripe / Linear landing page."
- **Parameters:** colour stops (3–6), blob count (2–6), animation speed (static / slow / medium), seed.
- **Perf envelope:** 60fps on iPhone X equivalents. CPU-cheap.
- **Use case:** Premium product hero, marketing splash, app onboarding background.

### 2. `voronoi`

- **Visual identity:** Cellular tessellation of irregular polygons with subtle edges. Reads as "organic / scientific" or "neural-network-coded."
- **Parameters:** cell density (low / med / high), edge thickness (px), colour palette, drift speed.
- **Perf envelope:** 30..60fps depending on density. GPU-bound at high cell counts.
- **Use case:** Data-visualisation landing pages, AI / ML product splash, biotech / scientific tooling.

### 3. `liquid-metal`

- **Visual identity:** Metallic chrome surface that ripples / reflects light bands. Reads as "Y2K nostalgia" or "premium hardware product page."
- **Parameters:** ripple frequency, light angle, reflection sharpness (matte..mirror), tint hue.
- **Perf envelope:** 30..45fps. Heavy in the fragment stage.
- **Use case:** Hardware-product page, retro / Y2K aesthetic, music landing pages.

### 4. `chrome`

- **Visual identity:** Polished reflective chrome plane (no liquid distortion) with controlled highlight bands. Reads as "luxury automotive" or "minimal premium."
- **Parameters:** highlight count, polish (rough..mirror), tint, light source angle.
- **Perf envelope:** 60fps. Lighter than `liquid-metal`.
- **Use case:** Luxury / automotive splash, premium product landing.

### 5. `pulsar`

- **Visual identity:** Radiating concentric pulses from a central source. Reads as "data / signal / radar."
- **Parameters:** pulse rate (Hz), centre position, decay distance, colour ramp.
- **Perf envelope:** 60fps. Cheap.
- **Use case:** Real-time dashboards, network / telemetry product pages, IoT marketing.

### 6. `black-hole`

- **Visual identity:** Gravitational-lens distortion with accretion-disk colour bands. Reads as "sci-fi / physics-themed" or "data infinity."
- **Parameters:** disk thickness, lens strength, rotation speed, hue (orange / blue / multi).
- **Perf envelope:** 24..30fps. Fragment-heavy.
- **Use case:** Scientific / academic product splash, sci-fi entertainment, data / analytics products.

### 7. `glass`

- **Visual identity:** Faceted glass tessellation with refraction at the seams. Reads as "premium 3D / spatial."
- **Parameters:** facet count, refraction strength, tint, light angle.
- **Perf envelope:** 30..45fps.
- **Use case:** AR / VR / spatial-UI product pages, premium SaaS, luxury brand splash. Cross-references the `amw-liquid-glass` skill for component-level glass.

### 8. `spiral`

- **Visual identity:** Logarithmic / golden-spiral patterning with controlled banding. Reads as "geometric / mathematical."
- **Parameters:** spiral tightness, band thickness, rotation, colour stops.
- **Perf envelope:** 60fps. Cheap.
- **Use case:** Educational / mathematical product pages, abstract corporate splash.

### 9. `particles`

- **Visual identity:** Many small drifting points (stars / dust / pollen). Reads as "ambient atmospheric."
- **Parameters:** particle count (100..10000), drift speed, size variation, fade duration.
- **Perf envelope:** 60fps below 2000 particles; degrades above.
- **Use case:** Ambient SaaS hero, game / entertainment splash, AI / generative tools.

### 10. `fireworks`

- **Visual identity:** Punctuated bursts of radiating particles. Reads as "celebratory / event."
- **Parameters:** burst frequency, burst size, particle count per burst, hue palette.
- **Perf envelope:** 30..60fps. Spikes during bursts.
- **Use case:** Launch / event landing pages, celebration moments, success-state full-screen treatments.

### 11. `plasma`

- **Visual identity:** Soft sine-wave colour fields layered to produce shifting cloud-like patterns. Reads as "classic demo-scene / retro-modern."
- **Parameters:** wave count, frequency, palette, animation speed.
- **Perf envelope:** 60fps. Trivially cheap.
- **Use case:** Retro / demo-scene aesthetic, music / entertainment landing, nostalgic SaaS hero.

## The 17 image-overlay effects

Apply on top of a raster (photo / illustration / screenshot) to convert it into an aesthetic surface. Each effect has the same five-axis description.

### Text / pattern conversions

| Effect      | Identity                                              | Parameters                              | Perf       | Use case                                             |
| ----------- | ----------------------------------------------------- | --------------------------------------- | ---------- | ---------------------------------------------------- |
| `ascii`     | Image rendered as monospaced characters by luminance. | char set, density, font size, colour     | 60fps      | Terminal / hacker aesthetic, retro UI                |
| `braille`   | Image rendered as Unicode Braille (2x4 dot blocks).   | density, threshold                       | 60fps      | Dense terminal art, tiny-resolution previews         |
| `dither`    | 1-bit / 2-bit Bayer / Floyd-Steinberg dither.         | algorithm, palette                       | 60fps      | Game Boy aesthetic, low-res print zine               |
| `halftone`  | Photo dot-screen at varying density.                  | dot size, angle, palette                 | 60fps      | Print / editorial / poster aesthetic                 |
| `crosshatch`| Layered diagonal-line shading by luminance.            | line density, angle, weight              | 60fps      | Engraving / sketch aesthetic                          |

### Glitch / distortion

| Effect       | Identity                                                | Parameters                                  | Perf      | Use case                                             |
| ------------ | ------------------------------------------------------- | ------------------------------------------- | --------- | ---------------------------------------------------- |
| `glitch`     | RGB-channel-split + horizontal-band displacement.       | shift amplitude, band count, rate           | 60fps     | Hacker / cyberpunk / event hero                       |
| `vhs`        | Scan-lines + chromatic aberration + slight blur.        | scan density, aberration px, vignette       | 60fps     | Retro / Y2K / nostalgia                               |
| `data-mosh`  | Block-shifted compression artefacts.                    | block size, shift rate                      | 30..45fps | Music / glitch-art landing                            |
| `bit-crush`  | Posterised colour reduction to N steps.                 | colour bits (1..8)                          | 60fps     | Lo-fi / retro / pixel-art aesthetic                   |

### Art filters

| Effect         | Identity                                              | Parameters                          | Perf    | Use case                                              |
| -------------- | ----------------------------------------------------- | ----------------------------------- | ------- | ----------------------------------------------------- |
| `oil-paint`    | Local-region brush-stroke smoothing.                  | radius, intensity                   | 30fps   | Artistic / editorial hero                              |
| `watercolour`  | Soft edge bleed + wet-on-wet blending.                | bleed radius, paper texture amount  | 30fps   | Editorial / illustration brand                         |
| `pencil`       | Edge-detection + crosshatch shading.                  | edge weight, hatch density          | 60fps   | Sketch / wireframe aesthetic                           |
| `posterise`    | Hard-cell colour quantisation.                        | colour count, edge weight           | 60fps   | Pop-art / screen-print aesthetic                       |

### Noise / atmosphere

| Effect          | Identity                                            | Parameters                              | Perf      | Use case                                             |
| --------------- | --------------------------------------------------- | --------------------------------------- | --------- | ---------------------------------------------------- |
| `film-grain`    | Animated luminance noise overlay.                   | grain size, intensity, animation        | 60fps     | Cinematic / editorial mood                            |
| `scan-lines`    | Horizontal raster lines at CRT-style spacing.       | spacing, opacity, scroll speed          | 60fps     | Terminal / retro / Evangelion-style HUD               |
| `noise-static`  | TV-static random pixels.                            | intensity, animation                    | 60fps     | Glitch / transition / loading state                   |
| `vignette`      | Radial darkening at frame edges.                    | radius, intensity, colour               | 60fps     | Cinematic mood, focus framing                         |

## Selection matrix — which type fits which preset

| Aesthetic                                      | Recommended backgrounds                                  |
| ---------------------------------------------- | -------------------------------------------------------- |
| Premium SaaS / understated elegance (S-018)    | `mesh-gradient`, `chrome` (subtle), `plasma`             |
| Liquid glass / spatial UI (S-034)              | `glass`, `mesh-gradient`, `liquid-metal`                  |
| Evangelion / NERV-HUD                          | NONE generative — flat black + `scan-lines` overlay only |
| Brutalist / industrial                          | flat colour fields + `noise-static` or `film-grain`      |
| Y2K / retro-modern                              | `liquid-metal`, `chrome`, `vhs` overlay                  |
| Cyberpunk / hacker                              | `pulsar`, `particles`, `glitch` overlay                  |
| Editorial / print                               | flat colour + `halftone`, `crosshatch`, or `oil-paint`   |
| Scientific / data / AI                          | `voronoi`, `pulsar`, `black-hole`                         |
| Celebratory / launch                            | `fireworks` (event-driven, not idle)                      |

## Pitfalls for shader-heavy backgrounds

- **Never animate a heavy fragment shader at 60Hz on every page.** Pause when the tab is not visible (`document.visibilityState`). Pause when `prefers-reduced-motion: reduce` is set.
- **Always test on a mid-range mobile.** Desktop dev hardware will hide a 15fps stutter that real users will notice.
- **Never put body text on top of an animated shader** without a solid backdrop (90%+ opaque card). Text contrast against a moving surface fails accessibility AND legibility.
- **Provide a static-image fallback** for browsers without WebGL (`<noscript>` poster, or a captured PNG / WebP first frame).
- **Avoid stacking multiple shaders.** Two heavy backgrounds on the same page compound GPU load and battery drain. Pick one.
- **Image-overlay effects (ascii / dither / halftone / glitch) work on STATIC rasters too.** Don't pay shader cost for an aesthetic that a one-time canvas pass can produce.

## Selection checklist

- [ ] Confirmed the brief calls for a generative/animated background (not a static asset).
- [ ] Chose one of the 11 background **types** using the selection matrix (type ↔ preset).
- [ ] Chose any needed image-overlay **effect(s)** from the 17-effect catalog.
- [ ] Reviewed the shader-heavy pitfalls (perf envelope, contrast, reduced-motion).
- [ ] Handed the chosen type/effect vocabulary to the downstream implementer (this catalog ships the language, not the shader source).

## Cross-references

- **Orchestrator:** [amw-design-principles](../amw-design-principles/SKILL.md).
- **Aesthetic presets that select among these backgrounds:**
  [amw-design-system-presets](../amw-design-system-presets/SKILL.md).
- **Glass component skill (for spatial-UI use cases):**
  [amw-liquid-glass](../amw-liquid-glass/SKILL.md).
- **Image-overlay implementation primitives (when ready to ship):** the
  [amw-hypercomp](../amw-hypercomp/SKILL.md) skill ships a TS / SVG-filter compiler for image effects; it is the recommended runtime for the 17 overlays catalogued here.
- **Shader-type-specific deep dive:** see [TECH-shader-types](references/TECH-shader-types.md).
> [TECH-shader-types.md] `mesh-gradient` · `voronoi` · `liquid-metal` · `chrome` · `pulsar` · `black-hole` · `glass` · `spiral` · `particles` · `fireworks` · `plasma` · Library / runtime choice · Accessibility checklist · The mathematical / geometric primitive that drives the look. · The default-tasteful parameter range (what to suggest as a starting point). · The dial that, when overdriven, ruins the effect. · Library-agnostic implementation hints.
