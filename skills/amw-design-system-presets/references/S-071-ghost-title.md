---
id: S-071
name: Ghost Title
aesthetic_position: micro-aesthetic typographic-depth pseudo-element
source_attribution: blocked-A/B "Ghost Title" — CSS `::before` depth-without-image pattern (no single upstream repo; recurring idiom; MIT-equivalent CSS technique)
license: MIT (CSS idiom, no proprietary code copied)
---

# S-071 — Ghost Title

## Identity

Ghost Title is a typographic depth effect that adds a single layer of atmospheric weight behind a heading without resorting to background images, gradients, or illustration. The mechanism is a `::before` pseudo-element that duplicates the heading text via `content: attr(data-ghost)`, scales it up dramatically (≈3×), drops its opacity to 0.2–0.4, and blurs it (`filter: blur(6–12px)`). The result is a soft halo of the same word(s) sitting behind the crisp foreground heading — depth without imagery, identical at any zoom, fully selectable for the foreground while the ghost is decorative. Intended audience: editorial landing pages, premium SaaS hero sections, technical product mastheads, any context where a single heading must feel weighted without competing visual elements.

## Token block

```css
:root {
  /* Foreground heading colour (style-agnostic — inherit from active preset) */
  --color-text:        #111111;
  --color-bg:          #FFFFFF;

  /* Ghost-title effect tokens */
  --ghost-opacity:     0.30;          /* 0.20 minimum visible, 0.40 maximum subtle */
  --ghost-blur:        8px;           /* 6–12px range — outside this it stops reading as halo */
  --ghost-scale:       3.0;           /* font-size multiplier vs the real heading */
  --ghost-offset-x:    0;             /* horizontal nudge from heading centre */
  --ghost-offset-y:    -0.15em;       /* vertical nudge — slightly above is conventional */
  --ghost-color:       currentColor;  /* inherits heading colour by default */
  --ghost-z:           -1;            /* sits behind the heading */
  --ghost-letter-spacing: -0.04em;    /* tighten ghost to keep silhouette compact */
  --ghost-font-weight: 900;           /* heaviest available weight maximises halo presence */

  /* Stacking context — the heading needs `position: relative` to host the ::before */
  --ghost-stacking-strategy: relative;
}

/* Canonical implementation */
.ghost-title {
  position: relative;
  display: inline-block;
  isolation: isolate;                  /* contains ::before z-index inside this element */
}

.ghost-title::before {
  content: attr(data-ghost);
  position: absolute;
  left: 50%;
  top: var(--ghost-offset-y);
  transform: translateX(calc(-50% + var(--ghost-offset-x))) scale(var(--ghost-scale));
  transform-origin: center center;
  font-weight: var(--ghost-font-weight);
  letter-spacing: var(--ghost-letter-spacing);
  color: var(--ghost-color);
  opacity: var(--ghost-opacity);
  filter: blur(var(--ghost-blur));
  z-index: var(--ghost-z);
  pointer-events: none;
  user-select: none;
  white-space: nowrap;
}

/* Reduced-motion + reduced-transparency users */
@media (prefers-reduced-transparency: reduce) {
  .ghost-title::before { display: none; }
}
```

```html
<!-- usage — the foreground heading text and the ghost text must match -->
<h1 class="ghost-title" data-ghost="Velocity">Velocity</h1>
```

```ts
// tailwind plugin — register the effect as a single utility class
import plugin from 'tailwindcss/plugin';

export default plugin(({ addUtilities }) => {
  addUtilities({
    '.ghost-title': {
      position: 'relative',
      display: 'inline-block',
      isolation: 'isolate',
    },
    '.ghost-title::before': {
      content: 'attr(data-ghost)',
      position: 'absolute',
      left: '50%',
      top: '-0.15em',
      transform: 'translateX(-50%) scale(3)',
      'font-weight': '900',
      'letter-spacing': '-0.04em',
      color: 'currentColor',
      opacity: '0.3',
      filter: 'blur(8px)',
      'z-index': '-1',
      'pointer-events': 'none',
      'user-select': 'none',
      'white-space': 'nowrap',
    },
  });
});
```

## "Breaks if" invariants

- breaks if `--ghost-opacity` exceeds 0.4 — the halo competes with the foreground heading instead of supporting it
- breaks if `--ghost-opacity` drops below 0.2 — the halo becomes invisible and the technique is pointless overhead
- breaks if `--ghost-blur` exceeds 12px — the halo dissolves into a coloured smudge and loses its typographic origin
- breaks if `--ghost-blur` falls below 4px — the duplicated text reads as a misregistered second heading rather than a ghost
- breaks if `--ghost-scale` exceeds 4.0 — the halo overflows its container and creates layout instability
- breaks if `--ghost-scale` falls below 2.0 — the halo cannot establish atmospheric weight and reads as an artefact
- breaks if the foreground heading text does not match `data-ghost` — the duplication illusion fails and the halo reads as unrelated decoration
- breaks if `pointer-events: none` is omitted on `::before` — the halo intercepts clicks and breaks selection of the real heading
- breaks if the ghost is given a chromatic colour different from the foreground heading — the effect becomes a chromatic outline, not a ghost
- breaks if multiple ghost titles stack on a single page section — the technique relies on scarcity (1–2 ghosts per viewport maximum)

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html`, substituting `{{TOKEN}}` markers, and place a single `<h1 class="ghost-title" data-ghost="Sample">Sample</h1>` element in the hero region.
Upstream parity source: no single proprietary upstream — the technique is a recurring CSS idiom documented in `reports/batch9-harvest/blocked-B.md` entries #74 (technique catalogue) and #34 (component-defined micro-aesthetic section). Visual reference baselines: any premium-SaaS landing page hero using the `::before content: attr()` pattern.

## Render-test verdict

JOD: A-class (specialized-tokens) — 2026-05-29
Reason: effect / layout / multi-brand token block — defines effect or scene parameters, not the 13-slot landing-page palette (absent slots: accent,border,font-body,font-display,font-mono,primary,radius,shadow,spacing,surface,text-muted). Canonical render uses the effect element/file named in the pointer, not the bare skeleton. Render OK 1440x900, det-JOD 10.00.

## Cross-references

- **Companion presets:** S-022 Minimal Pure (clean foreground heading that benefits most from ghost depth), S-014 Editorial Serif (serif headings + ghost halo amplifies editorial weight), S-035 21st.dev / Aceternity (dark-cinematic surface where ghost halo provides atmospheric tint)
- **Sibling micro-aesthetics:** S-072 Grid Beam (background-layer ambient effect), S-069 Abstract Gradient Art (large blurred gradient blob as ambient colour source)
- **Source attribution:** `reports/batch9-harvest/blocked-B.md` #74 + #34 (technique catalogue; no upstream code copied — CSS idiom only). License: MIT-equivalent (CSS technique, no proprietary implementation).
- **Note:** Ghost Title is an overlay effect, not a full preset. Combine with any base preset whose foreground colour palette is high-contrast (Swiss, Editorial Serif, Minimal Pure, 21st.dev). It does NOT compose with presets that already carry decorative background atmosphere (Aurora, Shader Wallpapers, Memphis, Cinematic Dark) — the ghost halo will compete with the existing ambient layer.
