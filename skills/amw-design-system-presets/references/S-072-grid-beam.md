---
id: S-072
name: Grid Beam
aesthetic_position: micro-aesthetic ambient-motion hero-background
source_attribution: https://github.com/viernes-ui-starter (MIT) — `grid-beam` component (animated luminous grid lines behind hero)
license: MIT (viernes-ui-starter)
---

# S-072 — Grid Beam

## Identity

Grid Beam is a hero-section background effect that draws a faint geometric grid across the full viewport and animates one or more luminous "beams" of light travelling along the grid lines. The grid itself is rendered with two layered `repeating-linear-gradient` backgrounds (horizontal + vertical hairlines), and beams are short coloured segments translated along a grid axis via CSS keyframes — light entering frame on one edge, traversing the grid, exiting the opposite edge, then looping. The result is a calm, ambient atmosphere that signals "technical product, infrastructure, data" without committing to a Cyberpunk or Neon vocabulary. Intended audience: developer tools, AI products, infrastructure SaaS, observability platforms, devops dashboards, and any landing page whose hero must feel alive without dominating the foreground content.

## Token block

```css
:root {
  /* Surface — Grid Beam expects a dark or near-dark ground */
  --color-bg:          #0A0A0F;
  --color-surface:     #11121A;

  /* Grid lines — barely-visible hairlines */
  --gridbeam-line-color:       rgba(255, 255, 255, 0.06);   /* 4–8% alpha range */
  --gridbeam-line-thickness:   1px;                          /* never thicker than 1px */
  --gridbeam-cell-size:        64px;                         /* 48–96px range */

  /* Beam — luminous travelling segment */
  --gridbeam-beam-color:       #7C3AED;                      /* one vivid accent; match the active preset's primary */
  --gridbeam-beam-glow:        rgba(124, 58, 237, 0.45);     /* same hue, alpha 0.35–0.55 */
  --gridbeam-beam-length:      120px;                        /* short segment, not a full line */
  --gridbeam-beam-thickness:   2px;                          /* 1–3px range; thicker becomes a stripe */
  --gridbeam-beam-blur:        12px;                         /* glow halo around the beam */

  /* Motion */
  --gridbeam-duration:         6s;                           /* 4–10s range; faster reads as anxious */
  --gridbeam-easing:           linear;                       /* must be linear — beam moves at constant velocity */
  --gridbeam-stagger:          1.4s;                         /* delay between successive beams */
  --gridbeam-beam-count:       3;                            /* 2–4 beams max per viewport */

  /* Stacking */
  --gridbeam-z:                0;                            /* sits at hero background, below content */
  --gridbeam-mask-fade:        radial-gradient(ellipse at center, #000 40%, transparent 80%);
}

/* The hero container — establishes the grid + spawns beams */
.gridbeam-hero {
  position: relative;
  overflow: hidden;
  background:
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent calc(var(--gridbeam-cell-size) - var(--gridbeam-line-thickness)),
      var(--gridbeam-line-color) calc(var(--gridbeam-cell-size) - var(--gridbeam-line-thickness)),
      var(--gridbeam-line-color) var(--gridbeam-cell-size)
    ),
    repeating-linear-gradient(
      90deg,
      transparent 0,
      transparent calc(var(--gridbeam-cell-size) - var(--gridbeam-line-thickness)),
      var(--gridbeam-line-color) calc(var(--gridbeam-cell-size) - var(--gridbeam-line-thickness)),
      var(--gridbeam-line-color) var(--gridbeam-cell-size)
    ),
    var(--color-bg);
  -webkit-mask-image: var(--gridbeam-mask-fade);
          mask-image: var(--gridbeam-mask-fade);
}

/* Single beam — duplicated and offset for multi-beam choreography */
.gridbeam-beam {
  position: absolute;
  top: 0;
  left: calc(var(--gridbeam-col, 4) * var(--gridbeam-cell-size));
  width: var(--gridbeam-beam-thickness);
  height: var(--gridbeam-beam-length);
  background: linear-gradient(
    180deg,
    transparent 0%,
    var(--gridbeam-beam-color) 50%,
    transparent 100%
  );
  box-shadow: 0 0 var(--gridbeam-beam-blur) var(--gridbeam-beam-glow);
  filter: blur(0.5px);
  pointer-events: none;
  animation: gridbeam-travel var(--gridbeam-duration) var(--gridbeam-easing) infinite;
  animation-delay: var(--gridbeam-delay, 0s);
}

@keyframes gridbeam-travel {
  0%   { transform: translateY(-100%); opacity: 0; }
  10%  { opacity: 1; }
  90%  { opacity: 1; }
  100% { transform: translateY(100vh); opacity: 0; }
}

/* Respect prefers-reduced-motion — beams freeze at mid-frame, grid remains */
@media (prefers-reduced-motion: reduce) {
  .gridbeam-beam {
    animation: none;
    opacity: 0.5;
    transform: translateY(40vh);
  }
}
```

```html
<!-- usage — 3 beams, staggered, on a hero ground -->
<section class="gridbeam-hero">
  <span class="gridbeam-beam" style="--gridbeam-col: 4; --gridbeam-delay: 0s;"></span>
  <span class="gridbeam-beam" style="--gridbeam-col: 9; --gridbeam-delay: 1.4s;"></span>
  <span class="gridbeam-beam" style="--gridbeam-col: 14; --gridbeam-delay: 2.8s;"></span>
  <div class="hero-content"><!-- foreground content sits above --></div>
</section>
```

## "Breaks if" invariants

- breaks if the ground is light (`--color-bg` lighter than `#1A1A1A`) — beams require a dark surface to register as luminous; on light grounds they read as muddy stripes
- breaks if `--gridbeam-line-color` alpha exceeds 0.10 — the grid becomes the foreground and the hero content has to fight it
- breaks if `--gridbeam-line-thickness` exceeds 1px — hairlines are the defining quality; 2px lines read as a graph paper, not as ambient atmosphere
- breaks if `--gridbeam-cell-size` falls below 48px — the grid becomes a mesh and visually noisy; above 96px it stops reading as a grid and becomes a sparse cross
- breaks if `--gridbeam-beam-count` exceeds 4 — the effect tips from ambient to anxious, and the eye loses the grid-as-substrate reading
- breaks if `--gridbeam-easing` is not `linear` — non-linear easings break the "constant-velocity light" illusion and the beam reads as a particle effect
- breaks if `--gridbeam-duration` is shorter than 4s — beams feel hurried and anxious; the effect must read as patient and ambient
- breaks if the radial fade mask is removed — beams travelling past the viewport edge create hard edges that break immersion
- breaks if more than one accent hue is used across beams — multi-hue beams compete and the technique reverts to a Cyberpunk vocabulary
- breaks if foreground content lacks sufficient contrast against the ground (WCAG-AA fail) — the ambient beams make the contrast judgement harder, not easier
- breaks if the grid extends edge-to-edge without a fade mask on a long page — the effect must be confined to the hero region, not bleed into body content

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html`, substituting `{{TOKEN}}` markers, and wrap the hero region in `.gridbeam-hero` with three `.gridbeam-beam` spans at columns 4/9/14 with staggered delays.
Upstream parity source: `viernes-ui-starter-master` — `grid-beam` component (MIT). Canonical visual reference: hero sections on 21st.dev / Aceternity / Linear (which use the same idiom in production landing pages).

## Render-test verdict

JOD: A-class (specialized-tokens) — 2026-05-29
Reason: effect / layout / multi-brand token block — defines effect or scene parameters, not the 13-slot landing-page palette (absent slots: accent,border,font-body,font-display,font-mono,primary,radius,shadow,spacing,text,text-muted). Canonical render uses the effect element/file named in the pointer, not the bare skeleton. Render OK 1440x900, det-JOD 10.00.

## Cross-references

- **Companion presets:** S-035 21st.dev / Aceternity (dark cinematic surface with violet accent — Grid Beam is the canonical hero-background pairing), S-010 Cyberpunk (deeper neon vocabulary, beams turn cyan/magenta), S-038 Dark Tech (terminal-without-retro — beams stay one hue, no multi-colour drift)
- **Sibling micro-aesthetics:** S-071 Ghost Title (typographic depth on the same hero), S-068 Cinematic Scroll (full page-as-film-reel — Grid Beam is the still-hero counterpart), S-073 Shader Wallpapers (interactive generative bg — Grid Beam is the non-interactive static-grid counterpart)
- **Source attribution:** `viernes-ui-starter-master` repo, `grid-beam` component (MIT) — recorded in `reports/batch9-harvest/blocked-B.md` entry #87. CSS implementation distilled from the public component; no JavaScript runtime is required (pure CSS keyframes + custom properties).
- **Note:** Grid Beam is a hero-only effect — do not extend the grid into body content. Maximum one Grid Beam region per page. Beams should not animate when `prefers-reduced-motion: reduce` is set; the grid alone is sufficient ambient atmosphere.
