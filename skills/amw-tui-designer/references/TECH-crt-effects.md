<!--
ai-maestro-webdesign / skills / amw-tui-designer / references / TECH-crt-effects.md
Adapted from Chris Korhonen's `tui-designer` skill in https://github.com/ckorhonen/claude-skills
Original work © 2025 Chris Korhonen — MIT License.
Adaptation © 2026 Emasoft — MIT License.
SwiftUI / Metal-shader content removed — out of scope for ai-maestro-webdesign.
-->

# TECH-crt-effects — CSS recipes for CRT, scanlines, neon glow, flicker

## Table of Contents

- [Scanlines overlay](#scanlines-overlay)
- [Neon glow — text and borders](#neon-glow-text-and-borders)
- [CRT curvature](#crt-curvature)
- [Flicker animation](#flicker-animation)
- [WebGL CRT (when CSS is insufficient)](#webgl-crt-when-css-is-insufficient)
- [Effect-pattern reference](#effect-pattern-reference)
- [Performance considerations](#performance-considerations)
- [Accessibility — non-negotiable](#accessibility-non-negotiable)
- [Pitfalls and prevention](#pitfalls-and-prevention)
- [When CRT effects backfire](#when-crt-effects-backfire)

All recipes are vanilla CSS; none requires a framework. Pair with [palettes](TECH-palettes.md) and apply via wrapper classes (e.g. `.crt-container`, `.neon-text`).

## Scanlines overlay

The subtle horizontal stripe pattern over the entire screen. Implemented as a `::after` pseudo-element so it sits above content without affecting layout.

```css
.crt-container {
  position: relative;
  background: #001100;          /* phosphor green BG */
  overflow: hidden;
}

.crt-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.15),
    rgba(0, 0, 0, 0.15) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none;          /* never blocks clicks */
}
```

**Tuning:**

- Stripe alpha 0.10–0.18. Below 0.10 invisible; above 0.20 reduces readability.
- Stripe period 2 px (1 dark + 1 transparent). Larger periods become decorative dashed lines, not scanlines.
- `pointer-events: none` is mandatory — without it, the overlay swallows every click.

## Neon glow — text and borders

The signature retro/cyberpunk text effect. Multiple `text-shadow` layers stack from a white core outward through the accent color.

```css
.neon-text {
  color: #00ffff;                /* cyan core */
  text-shadow:
    /* white inner core */
    0 0 5px  #ffffff,
    0 0 10px #ffffff,
    /* cyan glow layers */
    0 0 20px #00ffff,
    0 0 40px #00ffff;
}

.neon-border {
  border: 1px solid #00ffff;
  box-shadow:
    0 0 5px  #00ffff,
    0 0 10px #00ffff,
    inset 0 0 5px #00ffff;
}
```

**Tuning:**

- **Max 4 `text-shadow` layers** — every layer is a separate GPU pass. > 5 layers blurs the text core and degrades mobile performance.
- White inner core (5–10 px) is what makes the glow look hot rather than fuzzy. Without it, the text reads as dim/blurred.
- For headings, scale glow up to 40 px outer. For body text, cap outer glow at 20 px — beyond that, letters merge.
- Match the glow color to the chosen palette (cyan for cyberpunk, green for phosphor, amber for CRT). Do not mix palettes.

## CRT curvature

Subtle perspective transform + inset glow simulates the convex CRT glass.

```css
.crt-screen {
  border-radius: 20px;
  transform: perspective(1000px) rotateX(2deg);
  box-shadow:
    inset 0 0 50px rgba(0, 255, 0, 0.10),   /* inner phosphor glow */
    0 0 20px       rgba(0, 255, 0, 0.20);   /* outer halo */
}
```

**Rules:**

- `rotateX` ≤ 3deg. Beyond that, content visibly skews and forms feel broken.
- **Decorative only.** Never apply CRT curvature to surfaces with critical layout (forms, tables, dense data) — users will think the UI is misaligned.
- Border-radius 16–24 px reads as a CRT bezel; below 12 px reads as a generic rounded card.

## Flicker animation

A near-imperceptible opacity wobble for atmosphere. CSS-only — never JavaScript.

```css
@keyframes flicker {
  0%, 100% { opacity: 1; }
  50%      { opacity: 0.95; }
  52%      { opacity: 1; }
  54%      { opacity: 0.90; }
}

.flicker {
  animation: flicker 3s infinite;
}
```

**Rules:**

- `@keyframes` only. **Never** `setInterval(() => el.style.opacity = ...)` — main-thread opacity changes cause stutter and battery drain.
- Opacity range 0.88–1.0. Below 0.85, the element visibly disappears; above 0.95, no visible flicker.
- Period 2–5 s. Faster than 1 s reads as a broken element; slower than 8 s loses the effect.
- **Disable via `prefers-reduced-motion: reduce`.** This is mandatory — see Accessibility below.

## WebGL CRT (when CSS is insufficient)

For fully-correct chromatic aberration, screen barrel distortion, or animated retrace lines, use the WebGL backend:

```html
<canvas id="crt-canvas"></canvas>
<script type="module">
import { CRTFilterWebGL } from 'crtfilter';

const canvas = document.getElementById('crt-canvas');
const crt = new CRTFilterWebGL(canvas, {
  scanlineIntensity: 0.15,
  glowBloom: 0.30,
  chromaticAberration: 0.002,
  barrelDistortion: 0.10,
  staticNoise: 0.03,
  flicker: true,
  retraceLines: true
});

crt.start();
</script>
```

CRTFilter.js is hardware-accelerated and has minimal CPU cost on modern hardware. **Throttle on mobile** — full-screen CRT shaders at 120 fps drain battery instantly. Use `prefers-reduced-motion` to disable the start entirely.

## Effect-pattern reference

| Effect | CSS implementation |
|---|---|
| Scanlines | `repeating-linear-gradient` on `::after` pseudo-element |
| Bloom / glow | Multiple `text-shadow` / `box-shadow` with increasing blur (max 4 layers) |
| Chromatic aberration | Three overlapping copies with per-channel color offset (expensive — prefer WebGL) |
| Flicker | `@keyframes` opacity wobble (never JS) |
| Phosphor decay | `transition: opacity 200ms ease-out` on element exit |
| Static noise | `repeating-linear-gradient` of 1 px noise dots at low alpha |

## Performance considerations

- **`box-shadow` and `text-shadow` are GPU-accelerated** but expensive with many layers. Cap at 4 layers for glow.
- Use `will-change: transform` (or `opacity`) on elements that flicker, **sparingly** — `will-change` on every element actually slows rendering.
- Avoid layout-affecting effects (`box-shadow` that overflows the parent without `overflow: visible`). Keep glow inside a wrapper.
- Profile on real mobile devices, not desktop dev tools. Glow + scanlines + flicker compounds quickly.

## Accessibility — non-negotiable

The retro aesthetic is a *visual* layer, not a functional one. Every accessibility gate the orchestrator imposes still applies.

```css
/* Hard requirement — disable all decorative motion under reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .flicker,
  .neon-text,
  .crt-container::after {     /* scanlines */
    animation: none;
    text-shadow: none;         /* keep base color readable */
  }
  .crt-container::after {
    display: none;             /* remove scanline overlay */
  }
}

/* Focus indicators — mandatory on every interactive element */
.neon-button:focus,
.crt-container button:focus,
.crt-container input:focus,
.crt-container a:focus {
  outline: 2px solid #00ffff;
  outline-offset: 2px;
}
```

**Hard gates the design MUST pass:**

| Gate | Requirement | Why |
|---|---|---|
| WCAG AA contrast | ≥ 4.5:1 body, ≥ 3:1 large text | Glow on text reduces effective contrast — measure the *unglowed* base color |
| Keyboard navigation | Tab / Shift+Tab / Enter / Esc / Arrow keys all functional | Mouse-only is a non-starter |
| Focus indicators | Visible outline on every interactive element | Without it, keyboard users lose their place |
| `prefers-reduced-motion` | Flicker + scanlines + bloom disabled when set | Photosensitive-epilepsy + motion-sickness safety |
| Screen-reader labels | `aria-label` on icon-only buttons | VoiceOver/NVDA/JAWS announce affordances |
| Color-only status | Pair with text/icon — never red-only / green-only | 8 % of males are color-blind |
| Font size | Body ≥ 14 px, headers ≤ 32 px (glow becomes illegible past 32) | Glow + small text = unreadable |

## Pitfalls and prevention

| Symptom | Root cause | Fix |
|---|---|---|
| Scanlines kill readability | Stripe alpha > 0.18, or stripe period > 2 px | Cap alpha at 0.15; keep period at 2 px |
| Glow blurs the text into illegibility | > 4 `text-shadow` layers, or outer glow > 20 px on body text | Cap at 4 layers; outer glow ≤ 20 px for body, ≤ 40 px for headings |
| CRT curvature breaks form alignment | `rotateX` > 3deg, or applied to a surface with critical layout | Cap at 2–3 deg; never on forms/tables |
| Flicker triggers motion sickness | No `prefers-reduced-motion` escape hatch | Mandatory `@media (prefers-reduced-motion: reduce) { animation: none; }` |
| Flicker is choppy / janky | JS-driven (`setInterval` opacity) | Replace with `@keyframes` |
| Performance tanks on mobile | Too many `box-shadow` layers, or full-screen WebGL shaders unthrottled | Cap layers; throttle WebGL to 30 fps on mobile |
| Forms feel broken on CRT-curved screens | Barrel distortion applied to inputs/buttons | Apply curvature to the container, never to interactive children |
| `box-shadow` clips at parent edges | Wrapper has `overflow: hidden` | Use `overflow: visible` on glow wrappers, or expand the wrapper padding |
| Box-drawing chars render as `?` | Legacy terminal (VT100) — not a web concern | Fallback to `+-\|` only when targeting terminal emulators; modern browsers render Unicode reliably |

## When CRT effects backfire

Some honest pushback to give the user:

- **Scanlines reduce readability for low-vision users.** Pair with a settings toggle or `prefers-contrast: more`.
- **Heavy glow hides text edges.** If you must glow body text, keep the white inner core at 5 px minimum.
- **Barrel distortion makes content look misaligned.** Users with no retro context will think the UI is broken.
- **Flicker is a safety risk.** Photosensitive epilepsy is real. The `prefers-reduced-motion` gate is not optional.

If the user pushes back on accessibility ("we want it cool, not accessible"), defer to the orchestrator — the ai-slop-avoid checklist will reject the result regardless.

<!--
Original sources adapted under MIT License.
ckorhonen/claude-skills · skills/tui-designer · © 2025 Chris Korhonen.
Adaptation © 2026 Emasoft. Both upstream and adaptation are MIT-licensed.
SwiftUI / Metal-shader content from upstream removed — out of scope for this plugin.
-->
