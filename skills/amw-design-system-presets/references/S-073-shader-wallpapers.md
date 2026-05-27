---
id: S-073
name: Shader Wallpapers / Ambient Interactive
aesthetic_position: micro-aesthetic interactive-background generative-ambient
source_attribution: clean-room summary of `claude-design-aesthetic-workflow-skill-main/references/gallery-cases.md` case #5 "Shader Wallpapers" (license not stated) and `efecto` shader catalogue (license not stated) — generic WebGL/canvas idiom, no proprietary code copied
license: clean-room derivation (no verbatim copy)
---

# S-073 — Shader Wallpapers / Ambient Interactive

## Identity

Shader Wallpapers turn the full viewport into a living material. A WebGL fragment shader (or a 2D canvas particle field as a low-power fallback) renders a generative background that responds to mouse position in real time and to click events as discrete disturbances — plasma washes, field lines, particle clouds, mesh gradients, liquid metal, voronoi cells, pulsar bursts. The screen stops being a window onto static content and becomes an environment. Foreground content sits above the shader on a translucent surface or a transparent layer with sufficient text contrast guaranteed by a colour-stop floor inside the shader itself. Intended audience: hero sections for premium SaaS, AI products, agency portfolios, generative-art landing pages, and any context where "this product is alive" must be the first impression. Best paired with deep-dark grounds — vivid light emissions read brightest against near-black.

## Token block

```css
:root {
  /* Ground — Shader Wallpapers always sit on a deep-dark surface */
  --color-bg:         #050510;
  --color-surface:    rgba(255, 255, 255, 0.02);

  /* Foreground content surface (sits above the shader) */
  --color-text:       #F4F4F5;
  --color-text-muted: #A1A1AA;
  --color-overlay:    rgba(10, 10, 16, 0.45);   /* contrast floor — text must remain WCAG-AA over shader */

  /* Shader configuration tokens (canonical default = plasma-field) */
  --shader-variant:           plasma;            /* plasma | voronoi | mesh-gradient | liquid-metal | particle-field */
  --shader-primary:           #7C3AED;           /* dominant light emission hue */
  --shader-secondary:         #06B6D4;           /* secondary emission hue (cyan, mint, magenta) */
  --shader-tertiary:          #EC4899;           /* rare third hue — used sparingly */
  --shader-intensity:         0.65;              /* 0.0 ambient → 1.0 maximum saturation */
  --shader-mouse-radius:      0.35;              /* viewport-units radius of mouse influence */
  --shader-click-pulse:       1.0;               /* amplitude of click-disturbance ripple */
  --shader-click-decay:       1200ms;            /* ripple fade duration */

  /* Performance budget */
  --shader-fps-target:        60;                /* downgrade to particle-field if sustained < 45fps */
  --shader-resolution-scale:  1.0;               /* drop to 0.5 on devicePixelRatio > 2 mobile */
  --shader-disable-on-lowend: true;              /* skip shader entirely if hardwareConcurrency < 4 */

  /* Motion */
  --shader-base-speed:        0.6;               /* shader uniform time multiplier — 0.4–0.8 ambient range */
  --shader-fade-in:           800ms ease-out;    /* fade shader in on canvas-ready */
}

/* Canvas — full viewport, fixed, behind all content */
.shader-canvas {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;            /* mouse position is read globally; canvas does not intercept clicks */
  opacity: var(--shader-intensity);
  background: var(--color-bg);     /* fallback ground colour while shader compiles */
  transition: opacity var(--shader-fade-in);
}

/* Reduced motion — freeze shader on first frame; mouse and click handlers no-op */
@media (prefers-reduced-motion: reduce) {
  .shader-canvas {
    opacity: 0.25;
    animation-play-state: paused;
  }
}

/* Foreground content — sits above shader with contrast guarantee */
.shader-content {
  position: relative;
  z-index: 1;
  background: linear-gradient(
    180deg,
    transparent 0%,
    var(--color-overlay) 40%,
    var(--color-overlay) 100%
  );
}
```

```js
// shader-wiring.js — skeleton; the actual fragment shader code is variant-specific
// and lives in the host project. the token block above defines the contract the
// shader must implement.
const canvas = document.querySelector('.shader-canvas');
const gl = canvas.getContext('webgl2', { antialias: false, alpha: true });

// performance gate — bail to particle-field fallback if shader compilation fails
// or the device is low-end.
const lowEnd = navigator.hardwareConcurrency < 4 || !gl;
if (lowEnd) {
  canvas.classList.add('shader-fallback-particle-field');
} else {
  initShader(gl, {
    variant:        getComputedStyle(document.documentElement).getPropertyValue('--shader-variant').trim(),
    primary:        getComputedStyle(document.documentElement).getPropertyValue('--shader-primary').trim(),
    secondary:      getComputedStyle(document.documentElement).getPropertyValue('--shader-secondary').trim(),
    tertiary:       getComputedStyle(document.documentElement).getPropertyValue('--shader-tertiary').trim(),
    intensity:      parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--shader-intensity')),
    mouseRadius:    parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--shader-mouse-radius')),
    clickPulse:     parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--shader-click-pulse')),
    clickDecay:     parseInt(getComputedStyle(document.documentElement).getPropertyValue('--shader-click-decay'), 10),
    baseSpeed:      parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--shader-base-speed')),
  });
}
```

## "Breaks if" invariants

- breaks if the ground is light (`--color-bg` lighter than `#1A1A1A`) — vivid emissions read as muddy stains on light grounds; the technique is dark-only
- breaks if foreground text contrast against the live shader falls below WCAG-AA 4.5:1 at any frame — the contrast floor (`--color-overlay`) must guarantee legibility across the shader's full animation cycle
- breaks if the shader covers content that requires reading (body copy, dense tables, forms) — Shader Wallpapers are hero-region only
- breaks if `--shader-intensity` exceeds 0.85 — the shader competes with foreground content; intensity must remain ambient
- breaks if more than one shader region runs simultaneously on a single page — the technique relies on scarcity (one shader region max)
- breaks if `prefers-reduced-motion` is not respected — animated emissions trigger vestibular reactions for sensitive users; shader must freeze at intensity ≤ 0.3
- breaks if `pointer-events: auto` is set on the canvas — the canvas intercepts clicks and breaks the foreground click targets
- breaks if a low-end fallback (particle field, static gradient, plain dark ground) is not provided — devices with `hardwareConcurrency < 4` or WebGL2-unsupported browsers must degrade gracefully
- breaks if the shader runs at sustained < 45fps without downgrading `--shader-resolution-scale` — sluggish shader animation reads as broken software
- breaks if shader hues exceed three accent colours — the technique reverts to a Maximalism vocabulary above three hues
- breaks if a click-disturbance ripple decays faster than 400ms — the interaction feels nervous; minimum 800ms decay for the "fidgetable" quality

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html`, substituting `{{TOKEN}}` markers, and wrap the hero region in `<canvas class="shader-canvas"></canvas>` + foreground in `.shader-content`. A static screenshot at frame `t = 2.4s` is the parity capture point (chosen because it is past the fade-in but before the first click disturbance — gives a representative ambient frame).
Upstream parity source: `claude-design-aesthetic-workflow-skill-main/references/gallery-cases.md` case #5 "Shader Wallpapers" (license not stated — visual reference only, no code copied) and the `efecto` shader catalogue (license not stated — catalogue of 11 generative types). Both are surveyed in `reports/batch9-harvest/styles-A.md` line 623. The implementation distilled in this preset is a clean-room contract — variant-agnostic tokens, no shader source code.

## Render-test verdict

JOD: pending

## Cross-references

- **Companion presets:** S-035 21st.dev / Aceternity (dark cinematic surface with one accent — canonical Shader Wallpapers ground), S-036 Cinematic Dark (immersive near-black with film-grade — Shader as the "scene"), S-010 Cyberpunk (multi-hue neon vocabulary — Shader emissions stay within the cyber palette)
- **Sibling micro-aesthetics:** S-072 Grid Beam (non-interactive static-grid counterpart — use when WebGL is unavailable or motion budget is tight), S-069 Abstract Gradient Art (static blurred-blob ambient layer — Shader is its kinetic counterpart), S-068 Cinematic Scroll (page-as-film-reel — Shader is the always-on hero alternative)
- **Future skill:** T-021 `amw-generative-backgrounds` (GPU shader background catalogue: 11 generative types — meshGradient, voronoi, liquidMetal, chrome, pulsar, blackHole, glass, spiral, particles, fireworks; this preset is the design-system contract that catalogue will satisfy)
- **Source attribution:** Clean-room derivation. No source code copied from either `claude-design-aesthetic-workflow-skill-main` or `efecto`. The tokens defined here describe behaviour and constraints; the host project supplies its own fragment shader implementing the contract.
- **Note:** Shader Wallpapers carry an explicit performance and accessibility budget. The `--shader-disable-on-lowend` token MUST be honoured — devices that cannot sustain 45fps fall back to particle field or static gradient. The `prefers-reduced-motion` media query MUST freeze emissions at low intensity. Without these guarantees the technique is excluded by an accessibility-auditor veto (RULE: WCAG 2.1 AA — pause/stop animation).
