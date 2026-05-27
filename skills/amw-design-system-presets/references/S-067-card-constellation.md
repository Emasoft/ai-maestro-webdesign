---
id: S-067
name: Card Constellation
aesthetic_position: motion-defined-3d-cards
source_attribution: >
  styles-A.md Category 10 "Motion-Defined Aesthetics #30 — Card Constellation";
  blocked-B.md #67 Card Constellation Hero (CSS perspective, per-card transform vars,
  GSAP mouse parallax, depth-sorted opacity).
  Upstream licence not stated — this preset is a clean-room derivation of the
  documented technique; no verbatim copy of any source's CSS or JS.
license: clean-room derivation (no verbatim copy)
---

# S-067 — Card Constellation

**Filename:** `skills/amw-design-system-presets/references/S-067-card-constellation.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Card Constellation is a motion-defined aesthetic where the *layout* itself carries the brand: a hero (or feature row) of 5–9 cards arranged in 3D space, each with its own depth, rotation, and atmospheric blur, responding to mouse parallax. The aesthetic is neither colour nor typography — it is *spatial arrangement*. The visual fingerprint is a darker neutral canvas that lets each card's lighting matter, cards floating at different `--z` depths with depth-correlated opacity and `filter: blur()`, and a single accent reserved for the foreground card. Typography stays restrained (one display + one body) because the cards do the loud work. Intended audience: product hero sections, agency portfolios, case-study galleries, conference site speaker grids, "what we built" showcase blocks.

## Token block

```css
/* S-067 Card Constellation — CSS custom properties */
:root {
  /* Colors — restrained palette so 3D cards carry the visual weight */
  --color-bg:          #0F1116;   /* deep neutral charcoal — lets card lighting register */
  --color-surface:     #1A1D24;   /* card base */
  --color-surface-2:   #232730;   /* elevated / foreground card */
  --color-text:        #F2F4F8;   /* cool light grey */
  --color-text-muted:  #8A92A3;
  --color-primary:     #F2F4F8;
  --color-accent:      #8B5CF6;   /* violet — reserved for foreground card / CTA */
  --color-border:      #2A2F3A;

  /* Typography */
  --font-display: 'Space Grotesk', 'Inter', 'Helvetica Neue', sans-serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Geometry */
  --spacing:      8px;
  --radius:       12px;          /* generous radius — softens 3D edge under perspective */
  --border-width: 1px;

  /* Shadow — strong enough that depth reads even on still card */
  --shadow:       0 12px 40px rgba(0, 0, 0, 0.45);
  --shadow-card-foreground: 0 20px 60px rgba(0, 0, 0, 0.55);

  /* 3D arena — applied to the parent container of all cards */
  --perspective:        1400px;
  --transform-style:    preserve-3d;

  /* Per-card transform vars — defaults overridden per card */
  --x:    0px;
  --y:    0px;
  --z:    0px;            /* depth: negative pushes back, positive forward */
  --rx:   0deg;
  --ry:   0deg;
  --rz:   0deg;
  --blur: 0;              /* dimensionless multiplier; 0 = sharp, 1 = max blur */

  /* Motion — slow, deliberate, parallax-friendly */
  --motion-duration: 280ms;
  --motion-easing:   cubic-bezier(0.22, 0.61, 0.36, 1);
}

/* Reference card pattern (consumer copies, adjusts per-card --x/--y/--z/--rx/--ry/--blur) */
.constellation-card {
  transform: translate3d(var(--x), var(--y), var(--z))
             rotateX(var(--rx))
             rotateY(var(--ry))
             rotateZ(var(--rz));
  filter: blur(calc(var(--blur, 0) * 4px));
  opacity: calc(1 - var(--blur, 0) * 0.08);
  transition: transform var(--motion-duration) var(--motion-easing),
              filter   var(--motion-duration) var(--motion-easing);
}

.constellation-arena {
  perspective: var(--perspective);
  transform-style: var(--transform-style);
}

@media (prefers-reduced-motion: reduce) {
  .constellation-card {
    transform: none;
    filter:    none;
    opacity:   1;
    transition: none;
  }
}
```

```ts
// S-067 Card Constellation — Tailwind theme extension
const cardConstellation = {
  colors: {
    bg:           '#0F1116',
    surface:      '#1A1D24',
    'surface-2':  '#232730',
    text:         '#F2F4F8',
    'text-muted': '#8A92A3',
    primary:      '#F2F4F8',
    accent:       '#8B5CF6',
    border:       '#2A2F3A',
  },
  fontFamily: {
    display: ['"Space Grotesk"', 'Inter', '"Helvetica Neue"', 'sans-serif'],
    body:    ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
  },
  borderRadius: { DEFAULT: '12px' },
  boxShadow: {
    DEFAULT:  '0 12px 40px rgba(0,0,0,0.45)',
    'card-fg':'0 20px 60px rgba(0,0,0,0.55)',
  },
  perspective: { arena: '1400px' },
  transitionDuration: { DEFAULT: '280ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.22,0.61,0.36,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if perspective is dropped below 800px or raised above 2000px — outside this band cards either flatten or distort
- breaks if `transform-style: preserve-3d` is omitted on the arena container — the 3D space collapses to 2D
- breaks if depth-correlated opacity (`opacity = 1 - blur * 0.08`) is replaced by uniform opacity — cards lose atmospheric reading
- breaks if cards lack the `--x / --y / --z / --rx / --ry / --blur` CSS variable contract — mouse-parallax handler cannot target them
- breaks if `prefers-reduced-motion: reduce` does NOT zero all transforms and filters — accessibility regression
- breaks if more than 9 cards are placed in a single constellation — depth perception collapses; spatial parsing fails above 9
- breaks if cards adopt full saturation or high-chroma fills — busy faces destroy the depth illusion (the cards must read as planes, not paintings)
- breaks if the canvas is white/light — strong 3D shadow needs a darker field to register
- breaks if a second accent is introduced — only the foreground card carries chromatic accent
- breaks if `border-radius` drops below 8px — sharp edges + perspective look like broken render rather than intentional depth

## Implementation note (consumer obligation)

Consumers MUST implement a `pointermove` handler that updates `--x` and `--y` on each card with a parallax coefficient proportional to its `--z` (deeper cards = larger displacement, mimicking real-camera parallax). The handler MUST short-circuit when `matchMedia('(prefers-reduced-motion: reduce)').matches` is true. A reference handler signature (clean-room, no upstream copy):

```js
arena.addEventListener('pointermove', (ev) => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const r = arena.getBoundingClientRect();
  const nx = (ev.clientX - r.left) / r.width  - 0.5;   // -0.5 .. 0.5
  const ny = (ev.clientY - r.top)  / r.height - 0.5;
  arena.querySelectorAll('.constellation-card').forEach(card => {
    const depth = parseFloat(getComputedStyle(card).getPropertyValue('--z')) || 0;
    const k = depth / -200;                              // tune per project
    card.style.setProperty('--x', `${nx * k * 16}px`);
    card.style.setProperty('--y', `${ny * k * 16}px`);
  });
});
```

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#0F1116`, `{{SURFACE}}` = `#1A1D24`, `{{TEXT}}` = `#F2F4F8`, `{{TEXT_MUTED}}` = `#8A92A3`, `{{PRIMARY}}` = `#F2F4F8`, `{{ACCENT}}` = `#8B5CF6`, `{{BORDER}}` = `#2A2F3A`, `{{FONT_DISPLAY}}` = `'Space Grotesk', 'Inter', sans-serif`, `{{FONT_BODY}}` = `'Inter', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `12px`, `{{SHADOW}}` = `0 12px 40px rgba(0,0,0,0.45)`, `{{SPACING}}` = `8px`). The skeleton alone shows the palette; the constellation layout requires the 3D-arena and per-card variables documented above.

Upstream parity source: styles-A.md Category 10 + blocked-B.md #67 — clean-room derivation; no verbatim copy.

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling styles:** S-009 Aurora (atmospheric depth via blurred colour fields, no 3D transform), S-038 Dark Tech (dark restrained palette, no 3D), S-068 Cinematic Scroll (motion-defined, but timeline-driven rather than mouse-driven)
- **Differentiators:** S-067 is mouse-parallax + still-image depth; S-068 is scroll-timeline cinematic; S-009 uses blurred colour for depth not transform; S-038 has no spatial depth at all
- **Source:** styles-A.md Category 10 + blocked-B.md #67 (clean-room derivation; upstream licence unknown)
