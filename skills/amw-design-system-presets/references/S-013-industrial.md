---
id: S-013
name: Industrial / Utilitarian
aesthetic_position: developer-terminal-monospace
source_attribution: batch9 harvest corpus — `styles-B` "Industrial", `styles-A` "Industrial/Utilitarian", `frontend-design` Anchor 2 (no public upstream URL recorded)
license: original summary; color and typography values in the public domain
---

## Identity

Industrial Utilitarian applies the visual vocabulary of factory signage, technical manuals, and engineering diagrams to web UI: near-black backgrounds with near-black surfaces (the classic "black-on-black" layering that creates depth through tone alone), a single high-visibility signal color in either amber (`#FFB300`) or safety-green (`#39FF14`) for all interactive and status elements, and IBM Plex Mono or JetBrains Mono as the exclusive typeface for every role. Information density is extreme — no whitespace is decorative. Border-radius is `0px` (cut-steel aesthetic); shadows are entirely absent (no softening, no depth illusion). The result reads like a hardened operator console for industrial control systems, server monitoring dashboards, CLI documentation, or developer-productivity tools where function is the only aesthetic value.

## Token block

```css
/* S-013 Industrial / Utilitarian — token block (amber signal variant) */
:root {
  /* Colors — black-on-black + 1 signal color */
  --color-bg:           #0A0A0A;   /* near-black base */
  --color-surface:      #141414;   /* panel surface, barely distinguishable */
  --color-text:         #C8C8C8;   /* cool grey — readable without glow */
  --color-text-muted:   #666666;   /* dim grey for secondary labels */
  --color-primary:      #FFB300;   /* amber signal — interactive + status */
  --color-accent:       #E09A00;   /* darker amber for pressed/active states */
  --color-border:       #2A2A2A;   /* dark steel divider */

  /* Typography — mono ONLY */
  --font-display: 'IBM Plex Mono', 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  --font-body:    'IBM Plex Mono', 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  --font-mono:    'IBM Plex Mono', 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Layout — dense grid */
  --spacing:  6px;   /* tighter than default — extreme density */
  --radius:   0px;

  /* Shadow — none */
  --shadow:   none;

  /* Motion — functional, no easing flourish */
  --motion-duration: 100ms;
  --motion-easing:   linear;

  /* Green signal variant (swap --color-primary + --color-accent to use) */
  --color-primary-green: #39FF14;
  --color-accent-green:  #28CC0A;
}
```

```ts
// Tailwind theme extension — S-013 Industrial / Utilitarian
export default {
  theme: {
    extend: {
      colors: {
        industrial: {
          bg:       '#0A0A0A',
          surface:  '#141414',
          text:     '#C8C8C8',
          muted:    '#666666',
          amber:    '#FFB300',   // signal (amber variant)
          green:    '#39FF14',   // signal (green variant)
          border:   '#2A2A2A',
        },
      },
      fontFamily: {
        display: ['IBM Plex Mono', 'JetBrains Mono', 'Fira Code', 'monospace'],
        body:    ['IBM Plex Mono', 'JetBrains Mono', 'Fira Code', 'monospace'],
        mono:    ['IBM Plex Mono', 'JetBrains Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: {
        industrial: '0px',
      },
      boxShadow: {
        industrial: 'none',
      },
      spacing: {
        'ind-unit': '6px',
      },
      transitionDuration: {
        industrial: '100ms',
      },
    },
  },
};
```

## "Breaks if" invariants

- Breaks if any proportional typeface (sans-serif humanist, serif, display, handwritten) is introduced — the monospace-only contract enforces the machine-readout aesthetic throughout every text role.
- Breaks if `border-radius` exceeds `0px` — industrial systems use straight-edge panel construction; rounded corners signal consumer-UI softening.
- Breaks if `box-shadow` is applied to any element — depth in this style is created only through background-tone layering (`--color-bg` vs `--color-surface`); shadows are incompatible.
- Breaks if a second chromatic color is introduced alongside the signal color — the visual vocabulary relies on a single high-contrast signal against neutral grey; adding a second chromatic element turns a utilitarian console into a branded product UI.
- Breaks if padding / line-height is increased to match editorial conventions — extreme density is definitional; generous whitespace is the editorial aesthetic, not the industrial one.
- Breaks if the signal color is a mid-saturation hue (e.g. slate blue, muted teal) — the signal must be maximum-chroma for the single-color rule to function as a visual alarm; desaturated signals dissolve into the neutral base.
- Breaks if background is set lighter than `#1A1A1A` — the black-on-black depth effect requires very dark surfaces; light backgrounds produce a completely different style (Swiss, Editorial Serif, etc.).

## Canonical render-test pointer

Render-test: inject tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` with the amber signal token block above. Parity source: styles-B "Industrial" + styles-A "Industrial/Utilitarian" + frontend-design Anchor 2 (batch9 harvest).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 85442 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-012 Retro Terminal / Green-on-Black — shares monospace-only and 0-radius; Terminal is strictly phosphor-green on near-black with CRT nostalgia cues; Industrial is neutral-grey with an amber or green signal, no retro-specific texture.
- S-022 Minimal Pure / Ultra-Minimal — shares 0-radius and no-shadow; Minimal Pure uses pure black/white on a light background with a single proportional typeface; Industrial stays dark and monospace.
- S-038 Dark Tech — adjacent aesthetic but Dark Tech uses Space Grotesk (proportional) and 2px radius; Industrial is stricter (mono-only, 0-radius, no shadow).

## Attribution

Tokens derived from batch9 harvest: `styles-B` "Industrial", `styles-A` "Industrial/Utilitarian", `frontend-design` Anchor 2. Color and typography values are conventional industrial-UI palette choices in the public domain.
