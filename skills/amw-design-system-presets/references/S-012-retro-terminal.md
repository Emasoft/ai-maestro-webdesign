---
id: S-012
name: Retro Terminal / Green-on-Black
aesthetic_position: developer-terminal-monospace
source_attribution: batch9 harvest corpus — `styles-A` "Retro Terminal", `styles-B` "Developer Native", `frontend-design-engineer` #8 (no public upstream URL recorded)
license: original summary; color values and typography choices in the public domain
---

## Identity

Retro Terminal recreates the phosphor-green CRT display of early Unix workstations and command-line interfaces from the late 1970s through the 1990s. The sole chromatic value is `#00FF41` — Matrix-green phosphor — rendered against a near-black `#0D0208` that simulates aged CRT glass. Every text element uses `Fira Code` monospaced font exclusively; no proportional typeface is permitted anywhere in the UI. The aesthetic is strictly information-dense and utilitarian: no decorative graphics, no rounded corners, no drop-shadows. Interactivity is communicated through a blinking block cursor (`▌`) and typewriter-reveal character animations. The overall effect is a terminal emulator running on physical 1970s hardware — designed for developer tools, CLI documentation sites, hacker aesthetic landing pages, and security / CTF competition interfaces.

## Token block

```css
/* S-012 Retro Terminal / Green-on-Black — token block */
:root {
  /* Colors — single phosphor chromatic */
  --color-bg:           #0D0208;   /* near-black, slight warm tint mimics aged CRT glass */
  --color-surface:      #111810;   /* elevated panel — barely distinguishable from bg */
  --color-text:         #00FF41;   /* phosphor green — primary text */
  --color-text-muted:   #007A20;   /* dimmed phosphor — muted/secondary text */
  --color-primary:      #00FF41;   /* same phosphor — interactive primary */
  --color-accent:       #00CC33;   /* slightly deeper green for hover/active states */
  --color-border:       #004B16;   /* very dark green — hairline separator */

  /* Typography — monospace ONLY */
  --font-display: 'Fira Code', 'Courier New', 'Lucida Console', monospace;
  --font-body:    'Fira Code', 'Courier New', 'Lucida Console', monospace;
  --font-mono:    'Fira Code', 'Courier New', 'Lucida Console', monospace;

  /* Layout */
  --spacing:  8px;
  --radius:   0px;   /* hard pixels only */

  /* Shadow / Glow — phosphor text-shadow, no box-shadow */
  --shadow:          none;
  --glow-text:       0 0 4px #00FF41, 0 0 12px rgba(0,255,65,0.6);
  --glow-text-muted: 0 0 3px rgba(0,255,65,0.3);

  /* Motion — instant or very fast; no easing curves */
  --motion-duration: 0ms;    /* most state transitions are immediate */
  --motion-easing:   steps(1);

  /* Typing animation — use for text-reveal effects */
  --typing-speed:    60ms;   /* per-character delay in JS typewriter loops */
  --cursor-blink:    700ms;  /* cursor blink interval */
}
```

```ts
// Tailwind theme extension — S-012 Retro Terminal
export default {
  theme: {
    extend: {
      colors: {
        terminal: {
          bg:      '#0D0208',
          surface: '#111810',
          green:   '#00FF41',
          muted:   '#007A20',
          border:  '#004B16',
          cursor:  '#00FF41',
        },
      },
      fontFamily: {
        display: ['Fira Code', 'Courier New', 'monospace'],
        body:    ['Fira Code', 'Courier New', 'monospace'],
        mono:    ['Fira Code', 'Courier New', 'monospace'],
      },
      borderRadius: {
        terminal: '0px',
      },
      boxShadow: {
        terminal: 'none',
      },
      transitionDuration: {
        terminal: '0ms',
      },
      animation: {
        blink: 'blink 700ms steps(1) infinite',
      },
      keyframes: {
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%':       { opacity: '0' },
        },
      },
    },
  },
};
```

## "Breaks if" invariants

- Breaks if any proportional typeface (sans-serif, serif, display, handwritten) appears anywhere — the monospace-only contract is the style's entire typographic identity.
- Breaks if `border-radius` exceeds `0px` — terminal UIs are pixel-grid aligned; rounded corners signal a modern GUI, which is the antithesis of this style.
- Breaks if a second chromatic color is introduced (e.g. red error text, blue links) — the single-phosphor constraint is load-bearing; multi-color breaks the monochromatic authenticity.
- Breaks if `box-shadow` is applied to cards or panels — depth in this style is communicated only through foreground phosphor glow (`text-shadow`), never through drop-shadows on containers.
- Breaks if background color is set lighter than `#0D0208` — the contrast ratio between phosphor green and background must remain extreme; lighter backgrounds destroy the CRT illusion.
- Breaks if smooth CSS transitions (non-zero `transition-duration` with easing) are applied to text visibility or element entry — terminal state changes are instant (step-function); smooth fades read as a modern SPA, not a terminal.
- Breaks if the blinking cursor (`▌` or `|` with `animation: blink`) is removed from interactive input elements — the cursor is the primary interactivity affordance in this context.

## Canonical render-test pointer

Render-test: inject tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` with the token block above. Parity source: styles-A "Retro Terminal" + styles-B "Developer Native" + frontend-design-engineer #8 (batch9 harvest).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 103557 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-011 Retro-Futuristic / Synthwave — shares monospace font requirement; Synthwave uses dual-neon palette on deep-space bg vs. Terminal's single-phosphor purism.
- S-013 Industrial / Utilitarian — shares 0 radius, extreme information density, monospace-only fonts; Industrial adds a signal color and accepts amber variant; Terminal is strictly green.
- S-038 Dark Tech — shares dark background + monospace code font; Dark Tech is a contemporary clean dark UI; Terminal specifically emulates physical 1970s–1990s hardware.

## Attribution

Tokens derived from batch9 harvest: `styles-A` "Retro Terminal", `styles-B` "Developer Native", `frontend-design-engineer` #8. Color values (`#00FF41`, `#0D0208`) are long-established conventions in terminal emulator design, in the public domain as color specifications.
