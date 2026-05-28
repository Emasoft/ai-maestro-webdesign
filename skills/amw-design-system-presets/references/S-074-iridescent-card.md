---
id: S-074
name: Iridescent Card (Material Study)
aesthetic_position: micro-aesthetic single-object-study holographic-material
source_attribution: https://github.com/atelier (MIT) — `gallery-cases.md` case #9 "Iridescent Card"; CSS 3D perspective + conic-gradient holographic membrane technique
license: MIT (atelier)
---

# S-074 — Iridescent Card (Material Study)

## Identity

Iridescent Card is a single-object material study, not a full page aesthetic. The frame is empty space — a dark ambient ground with no competing content — and at its centre sits one card whose surface behaves like a holographic membrane: a `conic-gradient` rainbow rotates across its face, the card tilts on mouse parallax via `transform: perspective() rotateX() rotateY()`, and a specular highlight slides across its surface tracking the cursor. The effect is uncanny because nothing else moves; the card pretends to be a physical object caught in light. Typography on the card is minimal or absent — the composition IS the object. Intended audience: product hero showcases for premium consumer apps, NFT collections, music releases, fashion-tech crossovers, music-visualizer landing pages, and any context where the brief is "show one thing as desirable".

## Token block

```css
:root {
  /* Ambient scene — Iridescent Card requires a dark surrounding void */
  --color-bg:           #0A0A0F;
  --color-bg-vignette:  radial-gradient(ellipse at center, #1A1A28 0%, #0A0A0F 70%);

  /* Card surface — the holographic membrane */
  --iridescent-base:        #1A1A28;                                          /* substrate showing through gradient */
  --iridescent-spectrum:    #FF6B6B, #FFD93D, #6BCF7F, #4ECDC4, #B57EDC, #FF8FB1, #FF6B6B;  /* rainbow stops — last must match first for loop continuity */
  --iridescent-saturation:  0.75;                                             /* 0.5 desaturated holo, 1.0 vivid */
  --iridescent-shimmer:     150%;                                             /* gradient size — larger = subtler hue bands */

  /* Card geometry */
  --iridescent-width:       320px;
  --iridescent-height:      460px;                                            /* portrait ratio canonical; landscape variant 460×320 */
  --iridescent-radius:      24px;                                             /* 16–32px range */
  --iridescent-border:      1px solid rgba(255, 255, 255, 0.18);              /* hairline rim catches the light */

  /* 3D perspective + tilt */
  --iridescent-perspective: 1200px;                                            /* parent container */
  --iridescent-tilt-x:      0deg;                                              /* updated live from mouse Y */
  --iridescent-tilt-y:      0deg;                                              /* updated live from mouse X */
  --iridescent-tilt-max:    14deg;                                             /* clamp — beyond 18° the card reads as overturned */
  --iridescent-lift:        20px;                                              /* translateZ on hover */

  /* Specular highlight — tracks cursor */
  --iridescent-spec-x:      50%;                                               /* updated live from mouse X within card */
  --iridescent-spec-y:      50%;                                               /* updated live from mouse Y within card */
  --iridescent-spec-color:  rgba(255, 255, 255, 0.55);                         /* highlight peak */
  --iridescent-spec-size:   60%;                                               /* highlight radius */

  /* Glow halo — exterior radiance picking up the dominant gradient hue */
  --iridescent-glow:        0 0 80px rgba(180, 130, 220, 0.30);                /* purple-leaning to match spectrum centroid */

  /* Motion */
  --iridescent-tilt-ease:   cubic-bezier(0.16, 1, 0.3, 1);                     /* expo-out for graceful settle */
  --iridescent-tilt-dur:    280ms;                                             /* tilt-follow lag for damped feel */
  --iridescent-hover-dur:   400ms;                                             /* lift-on-hover */
  --iridescent-shimmer-dur: 8s;                                                /* slow ambient rotation when idle */

  /* Optional noise overlay — adds "physical material" tactility */
  --iridescent-noise-url:   url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='0.18'/></svg>");
  --iridescent-noise-blend: overlay;
  --iridescent-noise-opacity: 0.22;
}

/* Stage — the ambient void around the card */
.iridescent-stage {
  display: grid;
  place-items: center;
  min-height: 100vh;
  background: var(--color-bg-vignette);
  perspective: var(--iridescent-perspective);
}

/* The card — holographic membrane */
.iridescent-card {
  width: var(--iridescent-width);
  height: var(--iridescent-height);
  border-radius: var(--iridescent-radius);
  border: var(--iridescent-border);
  background:
    radial-gradient(
      circle at var(--iridescent-spec-x) var(--iridescent-spec-y),
      var(--iridescent-spec-color) 0%,
      transparent var(--iridescent-spec-size)
    ),
    conic-gradient(
      from 0deg at 50% 50%,
      var(--iridescent-spectrum)
    ),
    var(--iridescent-base);
  background-size: 100% 100%, var(--iridescent-shimmer) var(--iridescent-shimmer), 100% 100%;
  background-blend-mode: screen, normal, normal;
  filter: saturate(var(--iridescent-saturation));
  box-shadow: var(--iridescent-glow);
  transform: rotateX(var(--iridescent-tilt-x)) rotateY(var(--iridescent-tilt-y)) translateZ(0);
  transform-style: preserve-3d;
  transition:
    transform var(--iridescent-tilt-dur) var(--iridescent-tilt-ease),
    box-shadow var(--iridescent-hover-dur) var(--iridescent-tilt-ease);
  will-change: transform;
}

.iridescent-card::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background-image: var(--iridescent-noise-url);
  mix-blend-mode: var(--iridescent-noise-blend);
  opacity: var(--iridescent-noise-opacity);
  pointer-events: none;
}

.iridescent-card:hover {
  transform: rotateX(var(--iridescent-tilt-x)) rotateY(var(--iridescent-tilt-y)) translateZ(var(--iridescent-lift));
}

/* Idle shimmer when no mouse — slow gradient rotation keeps the surface alive */
@keyframes iridescent-idle-shimmer {
  to { background-position: 200% 0, 100% 100%, 0 0; }
}

.iridescent-card[data-idle="true"] {
  animation: iridescent-idle-shimmer var(--iridescent-shimmer-dur) linear infinite;
}

/* Reduced motion — freeze tilt, freeze shimmer, keep static iridescent surface */
@media (prefers-reduced-motion: reduce) {
  .iridescent-card,
  .iridescent-card[data-idle="true"] {
    transform: none;
    animation: none;
    transition: none;
  }
}
```

```js
// iridescent-card.js — skeleton; mouse parallax + specular tracking
const card  = document.querySelector('.iridescent-card');
const stage = document.querySelector('.iridescent-stage');
const root  = document.documentElement;

function clamp(v, min, max) { return Math.min(Math.max(v, min), max); }

stage.addEventListener('mousemove', (e) => {
  const rect = card.getBoundingClientRect();
  const x = (e.clientX - rect.left) / rect.width;   // 0..1 within card
  const y = (e.clientY - rect.top)  / rect.height;
  const tiltMax = parseFloat(getComputedStyle(root).getPropertyValue('--iridescent-tilt-max'));

  root.style.setProperty('--iridescent-tilt-y',  clamp((x - 0.5) *  tiltMax * 2, -tiltMax, tiltMax) + 'deg');
  root.style.setProperty('--iridescent-tilt-x',  clamp((0.5 - y) *  tiltMax * 2, -tiltMax, tiltMax) + 'deg');
  root.style.setProperty('--iridescent-spec-x',  (x * 100) + '%');
  root.style.setProperty('--iridescent-spec-y',  (y * 100) + '%');
  card.dataset.idle = 'false';
});

stage.addEventListener('mouseleave', () => {
  root.style.setProperty('--iridescent-tilt-x', '0deg');
  root.style.setProperty('--iridescent-tilt-y', '0deg');
  card.dataset.idle = 'true';
});
```

## "Breaks if" invariants

- breaks if the ambient scene is light (`--color-bg` lighter than `#1A1A1A`) — the holographic spectrum requires a dark void to register as luminous; on light grounds the card reads as a faded sticker
- breaks if any other content (cards, copy, ornament) sits within the stage region — the technique is a single-object study; surrounding elements destroy the illusion
- breaks if `--iridescent-tilt-max` exceeds 18° — the card reads as overturning, not as tilting; the holographic illusion requires subtle perspective
- breaks if the conic gradient is replaced by a linear gradient — linear holos read as a flat foil sticker; the rainbow must circulate around the card centre
- breaks if the first and last stops of `--iridescent-spectrum` do not match — the idle shimmer animation will hitch at the loop seam
- breaks if `--iridescent-saturation` exceeds 1.0 — the surface becomes a vivid candy stripe, not a holographic membrane
- breaks if `--iridescent-saturation` falls below 0.4 — the surface reads as grey noise; the hues must remain visible
- breaks if the specular highlight is omitted — the surface goes flat; the moving highlight is what sells the "physical object" reading
- breaks if `transform-style: preserve-3d` is omitted on the card or `perspective` on the stage — tilt becomes flat-skew, not 3D rotation
- breaks if typography or icons are placed centred on the card surface — they fight the rotating gradient; copy belongs around the card, not on it
- breaks if the noise overlay is omitted on devices with HiDPI displays — the gradient bands become visible and the surface reads as a CSS demo rather than a material
- breaks if multiple iridescent cards stack in the same viewport — the technique relies on scarcity (one card per page hero)
- breaks if `prefers-reduced-motion` is not respected — the tilt animation triggers vestibular reactions; static iridescent surface is the reduced-motion fallback

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html`, substituting `{{TOKEN}}` markers. Wrap the hero region in `<div class="iridescent-stage"><div class="iridescent-card" data-idle="true"></div></div>`. The canonical parity capture is a static screenshot at idle (no mouse interaction) — this gives a reproducible holographic surface frame without depending on cursor position.
Upstream parity source: `atelier-main/references/gallery-cases.md` case #9 "Iridescent Card" (MIT) — distilled in `reports/batch9-harvest/styles-A.md` line 318. The implementation in this preset adapts the documented behaviour (perspective tilt + specular shift + glow on hover + noise texture) into a token contract; no proprietary atelier code is copied verbatim.

## Render-test verdict

JOD: A-class (specialized-tokens) — 2026-05-29
Reason: effect / layout / multi-brand token block — defines effect or scene parameters, not the 13-slot landing-page palette (absent slots: accent,border,font-body,font-display,font-mono,primary,radius,shadow,spacing,surface,text,text-muted). Canonical render uses the effect element/file named in the pointer, not the bare skeleton. Render OK 1440x900, det-JOD 10.00.

## Cross-references

- **Companion presets:** S-034 Liquid Glass (Apple visionOS spatial UI — Iridescent Card is its single-object cousin), S-036 Cinematic Dark (immersive near-black ambient surrounding — Iridescent Card is the centred hero), S-035 21st.dev / Aceternity (dark cinematic SaaS surface — Iridescent Card replaces the bento grid hero with a single material study)
- **Sibling micro-aesthetics:** S-067 Card Constellation (multiple 3D-tilted cards with mouse parallax — Iridescent Card is the singular counterpart), S-069 Abstract Gradient Art (static blurred-blob ambient — Iridescent Card is the kinetic-on-hover counterpart), S-070 Dynamic Island UI (small physical-object UI element — Iridescent Card is the hero-scale equivalent)
- **Source attribution:** `atelier-main/references/gallery-cases.md` case #9 "Iridescent Card" (MIT — atelier repo). Visual reference and behaviour spec; this preset is a token contract for the technique. The conic-gradient spectrum stops are a clean-room composition (rainbow rotation around the card centre is a standard CSS idiom).
- **Note:** Iridescent Card is a hero-only single-object study. It does not scale to product grids, marketing pages with multiple sections, or any layout where attention is divided. The technique is high-impact, high-restraint — one card, one hero, one page. Pair with minimal typography around the card (large heading + short subhead + single CTA) and nothing else in the viewport.
