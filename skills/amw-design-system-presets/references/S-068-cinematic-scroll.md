---
id: S-068
name: Cinematic Scroll
aesthetic_position: motion-defined-scroll-film-reel
source_attribution: >
  styles-A.md Category 10 "Motion-Defined Aesthetics #31 — Cinematic Scroll (L3)";
  blocked-B.md #66 "L3 cinematic scroll — 4 required patterns: Pin-Scrub,
  Container-swap, Convergence, WebGL".
  Upstream license not stated — clean-room derivation; no verbatim copy of any
  source's GSAP/Three.js implementation.
license: clean-room derivation (no verbatim copy)
---

# S-068 — Cinematic Scroll

**Filename:** `skills/amw-design-system-presets/references/S-068-cinematic-scroll.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Cinematic Scroll is a level-3 motion-defined aesthetic in which the *page IS a film reel* — scroll progress becomes the timeline scrubber, and the visual identity is movement itself rather than colour or type. The fingerprint is composed of four mandatory scroll patterns layered through a single long-scroll experience: **Pin-Scrub** (a section pins to the viewport while its inner content animates against scroll progress), **Container-swap** (a sticky outer container while inner "scenes" cross-fade or slide on enter/leave breakpoints), **Convergence** (elements that begin at corners or off-canvas and converge toward a central focal point), and **WebGL** (a Three.js or similar scene tied to scroll progress, used sparingly — one scene per page max). Static colour, typography, and chrome stay quiet so the choreography reads. Intended audience: agency case-study pages, product launch sites, conference/film/festival landings, narrative editorial — anywhere the brand needs to *unfold* rather than be presented.

## Token block

```css
/* S-068 Cinematic Scroll — CSS custom properties */
:root {
  /* Colors — deliberately quiet so motion choreography reads as the brand */
  --color-bg:          #0B0B0E;   /* near-black cinematic canvas */
  --color-surface:     #14141A;
  --color-surface-2:   #1E1E27;
  --color-text:        #F4F4F6;
  --color-text-muted:  #8A8A95;
  --color-primary:     #F4F4F6;
  --color-accent:      #E0FF00;   /* signal-yellow — reserved for moments, not chrome */
  --color-border:      #25252F;

  /* Typography — single restrained pair; motion does the loud work */
  --font-display: 'Tobias', 'Editorial New', 'Playfair Display', Georgia, serif;
  --font-body:    'Inter', 'Helvetica Neue', 'system-ui', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Geometry — minimal; no decorative shapes */
  --spacing:      8px;
  --radius:       0px;            /* hard edges read cleaner under motion */
  --border-width: 1px;

  /* Shadow — used only on convergence focal-point cards */
  --shadow:       0 24px 60px rgba(0, 0, 0, 0.55);

  /* Motion — base contract; pattern-specific overrides below */
  --motion-duration: 600ms;
  --motion-easing:   cubic-bezier(0.16, 1, 0.3, 1);

  /* Scroll-timeline tuning */
  --scroll-section-length:   200vh;   /* pin-scrub section height in viewport units */
  --scroll-scene-count:      3;       /* container-swap scenes per outer pin */
  --scroll-convergence-px:   240px;   /* corner-to-center travel distance */
  --webgl-degrade-threshold: 4;       /* navigator.hardwareConcurrency floor */
}
```

```ts
// S-068 Cinematic Scroll — Tailwind theme extension
const cinematicScroll = {
  colors: {
    bg:           '#0B0B0E',
    surface:      '#14141A',
    'surface-2':  '#1E1E27',
    text:         '#F4F4F6',
    'text-muted': '#8A8A95',
    primary:      '#F4F4F6',
    accent:       '#E0FF00',
    border:       '#25252F',
  },
  fontFamily: {
    display: ['Tobias', '"Editorial New"', '"Playfair Display"', 'Georgia', 'serif'],
    body:    ['Inter', '"Helvetica Neue"', 'system-ui', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
  },
  borderRadius: { DEFAULT: '0px' },
  boxShadow: { DEFAULT: '0 24px 60px rgba(0,0,0,0.55)' },
  transitionDuration: { DEFAULT: '600ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.16,1,0.3,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if fewer than 2 of the 4 patterns are implemented (Pin-Scrub, Container-swap, Convergence, WebGL) — single-pattern pages do not register as "L3 cinematic"
- breaks if WebGL is used without a `navigator.hardwareConcurrency < 4` graceful-degradation fallback — performance regression on low-core devices
- breaks if more than ONE WebGL scene runs simultaneously on a page — GPU contention destroys frame rate
- breaks if `prefers-reduced-motion: reduce` does not collapse every animation to its end state (no movement, content still readable in correct order)
- breaks if Pin-Scrub section height drops below 150vh — there is not enough scroll runway for the inner animation to register
- breaks if Container-swap scene count exceeds 5 — readers lose track of scene transitions
- breaks if Convergence travel distance is shorter than 120px — the converge motion reads as a glitch, not a deliberate move
- breaks if the colour palette adopts more than one chromatic accent — quiet palette is structural
- breaks if border-radius exceeds 4px — soft edges blur under motion blur and read as artifact
- breaks if scroll progress is decoupled from the timeline (e.g. autoplay timelines that ignore scroll) — the cinema-as-page metaphor fails
- breaks if no scroll-progress indicator (numeric percent OR scaleX bar) is provided — readers lose narrative position

## Implementation note (consumer obligation)

Cinematic Scroll is a *protocol* — this preset specifies tokens and the invariants the motion layer must honour, but does not bundle GSAP/Three.js. Consumers MUST:

1. Implement Pin-Scrub via `IntersectionObserver` + `position: sticky` (or GSAP `ScrollTrigger` with `pin: true, scrub: true`) — clean-room implementation.
2. Implement Container-swap via a sticky outer wrapper containing N absolutely-positioned scenes, each driven by `requestAnimationFrame`-throttled scroll progress.
3. Implement Convergence via CSS variables `--converge-x` and `--converge-y` updated by scroll handler.
4. Implement WebGL (if used) via a `<canvas>` with a Three.js scene whose camera or material parameters are driven by scroll progress; gate behind `navigator.hardwareConcurrency >= 4` AND `!matchMedia('(prefers-reduced-motion: reduce)').matches`.
5. Provide scroll progress indicator: either a top-of-viewport `scaleX(pct)` bar or a numeric `XX%` overlay.

Reference observer pattern (clean-room):

```js
const pin = document.querySelector('.pin-scrub');
const inner = pin.querySelector('.inner');
window.addEventListener('scroll', () => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const r = pin.getBoundingClientRect();
  const len = pin.offsetHeight - window.innerHeight;
  const progress = Math.max(0, Math.min(1, -r.top / len));
  inner.style.setProperty('--progress', String(progress));
}, { passive: true });
```

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#0B0B0E`, `{{SURFACE}}` = `#14141A`, `{{TEXT}}` = `#F4F4F6`, `{{TEXT_MUTED}}` = `#8A8A95`, `{{PRIMARY}}` = `#F4F4F6`, `{{ACCENT}}` = `#E0FF00`, `{{BORDER}}` = `#25252F`, `{{FONT_DISPLAY}}` = `'Tobias', 'Editorial New', serif`, `{{FONT_BODY}}` = `'Inter', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `0px`, `{{SHADOW}}` = `0 24px 60px rgba(0,0,0,0.55)`, `{{SPACING}}` = `8px`). The skeleton verifies palette + type only; the four scroll patterns require the implementation notes above.

Upstream parity source: styles-A.md Category 10 #31 + blocked-B.md #66 — clean-room derivation; no verbatim copy.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 113996 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-067 Card Constellation (motion-defined but mouse-parallax, not scroll), S-036 Cinematic Dark (cinematic palette + type, but no scroll choreography), S-009 Aurora (atmospheric motion via blurred fields, not timeline)
- **Differentiators:** S-068 is *scroll-as-timeline*; S-067 is *mouse-as-camera*; S-036 is *static cinematic mood* without motion contract; S-009 is ambient atmosphere without narrative beats
- **Source:** styles-A.md Category 10 #31 + blocked-B.md #66 (clean-room derivation; upstream licence unknown)
