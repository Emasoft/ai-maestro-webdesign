---
id: S-069
name: Abstract Gradient Art
aesthetic_position: motion-defined-gradient-blob-industrial
source_attribution: >
  styles-A.md Category 10 "Motion-Defined Aesthetics #32 — Abstract Gradient Art";
  blocked-B.md #71 "Abstract Gradient Art top section — large blurred gradient blob"
  + #69 "Rivet decoration — 6px rotated square".
  Upstream license not stated — clean-room derivation; no verbatim copy.
license: clean-room derivation (no verbatim copy)
---

# S-069 — Abstract Gradient Art

**Filename:** `skills/amw-design-system-presets/references/S-069-abstract-gradient-art.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Abstract Gradient Art is an industrial-craft fusion aesthetic: a single oversized, heavily blurred gradient blob anchored at the top of the page becomes the ambient colour source for the entire layout — every other surface borrows tints from this one painted mass — and small "rivet" decorations (6×6px squares rotated 45° to render as diamonds) sit at card corners to introduce a hand-built industrial texture. The blob is positioned absolutely at `z-index: -1` so foreground content overlays it without competing. Typography is restrained (geometric sans display + neutral sans body) so the colour field reads as art rather than chrome. Intended audience: design-conscious SaaS, creative-studio sites, product launches that want a painterly hero without commissioning an illustrator, software targeted at makers/engineers (the rivet motif signals "built, not assembled").

## Token block

```css
/* S-069 Abstract Gradient Art — CSS custom properties */
:root {
  /* Colors — quiet neutral surface so the blob carries the chroma */
  --color-bg:          #FAFAF7;   /* warm-neutral off-white — picks up blob tints */
  --color-surface:     #FFFFFF;   /* card / panel sits on top of blob */
  --color-surface-2:   #F2F0EA;
  --color-text:        #15151A;
  --color-text-muted:  #5A5A66;
  --color-primary:     #15151A;
  --color-accent:      #FF6B35;   /* rust orange — echoes industrial palette */
  --color-border:      #DEDCD3;
  --color-rivet:       #8A8A95;   /* matte metal for decorative rivets */

  /* Gradient blob — composed of 3 colours mixing across the blob */
  --blob-c1: #FFB4A2;    /* warm coral */
  --blob-c2: #B5DEFF;    /* sky-blue */
  --blob-c3: #C8B6FF;    /* lilac */

  /* Typography */
  --font-display: 'General Sans', 'Inter', 'Helvetica Neue', sans-serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Geometry */
  --spacing:      8px;
  --radius:       8px;            /* moderate radius — pairs cleanly with rivets */
  --border-width: 1px;

  /* Shadow — paper-light so foreground panels float on the blob */
  --shadow:       0 4px 16px rgba(0, 0, 0, 0.06);
  --shadow-card:  0 8px 24px rgba(0, 0, 0, 0.08);

  /* Blob geometry */
  --blob-width:  120vw;            /* oversize, extends past viewport edges */
  --blob-height: 90vh;
  --blob-blur:   120px;            /* heavy gaussian — blob reads as colour field */
  --blob-top:    -20vh;            /* anchored above fold; partial visibility */
  --blob-opacity: 0.55;

  /* Rivet — 6px diamond at card corners */
  --rivet-size:   6px;
  --rivet-inset:  10px;            /* distance from card corner */

  /* Motion */
  --motion-duration: 220ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reference patterns — consumers paste into their stylesheet */
.ag-blob {
  position: absolute;
  top: var(--blob-top);
  left: 50%;
  transform: translateX(-50%);
  width: var(--blob-width);
  height: var(--blob-height);
  background:
    radial-gradient(40% 50% at 30% 40%, var(--blob-c1), transparent 60%),
    radial-gradient(45% 55% at 70% 30%, var(--blob-c2), transparent 60%),
    radial-gradient(40% 50% at 50% 70%, var(--blob-c3), transparent 60%);
  filter: blur(var(--blob-blur));
  opacity: var(--blob-opacity);
  z-index: -1;
  pointer-events: none;
}

.ag-card { position: relative; }   /* host for rivets */
.ag-card::before,
.ag-card::after {
  content: '';
  position: absolute;
  width:  var(--rivet-size);
  height: var(--rivet-size);
  background: var(--color-rivet);
  transform: rotate(45deg);
}
.ag-card::before { top: var(--rivet-inset);    left: var(--rivet-inset); }
.ag-card::after  { top: var(--rivet-inset);    right: var(--rivet-inset); }
/* Consumers may extend with bottom-corner rivets via additional pseudo-classes
   on inner wrappers or extra DOM nodes — keep 4 rivets max per card. */
```

```ts
// S-069 Abstract Gradient Art — Tailwind theme extension
const abstractGradientArt = {
  colors: {
    bg:           '#FAFAF7',
    surface:      '#FFFFFF',
    'surface-2':  '#F2F0EA',
    text:         '#15151A',
    'text-muted': '#5A5A66',
    primary:      '#15151A',
    accent:       '#FF6B35',
    border:       '#DEDCD3',
    rivet:        '#8A8A95',
    'blob-c1':    '#FFB4A2',
    'blob-c2':    '#B5DEFF',
    'blob-c3':    '#C8B6FF',
  },
  fontFamily: {
    display: ['"General Sans"', 'Inter', '"Helvetica Neue"', 'sans-serif'],
    body:    ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
  },
  borderRadius: { DEFAULT: '8px' },
  boxShadow: {
    DEFAULT: '0 4px 16px rgba(0,0,0,0.06)',
    card:    '0 8px 24px rgba(0,0,0,0.08)',
  },
  transitionDuration: { DEFAULT: '220ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #0F0F12;
  --color-surface:    #18181D;
  --color-surface-2:  #232328;
  --color-text:       #F5F4F0;
  --color-text-muted: #8A8A95;
  --color-border:     #2A2A30;
  --color-rivet:      #5A5A66;
  --blob-opacity:     0.35;        /* dim the blob on dark to preserve contrast */
}
```

## "Breaks if" invariants

- breaks if the blob is rendered without `filter: blur()` ≥80px — sharp gradient reads as artifact, not ambient art
- breaks if the blob's `z-index` is ≥0 — it must sit BEHIND content
- breaks if the blob occupies less than 80vw — small blobs read as decoration, not as colour source
- breaks if more than ONE blob is placed in the same viewport — two blobs cancel each other and read as muddy
- breaks if more than 4 rivets appear on a single card — the industrial motif tips into kitsch above 4
- breaks if rivets are sized outside the 4–8px range — outside this band they read as buttons or as noise
- breaks if rivets are NOT rotated 45° — un-rotated squares lose the rivet/diamond reading
- breaks if rivet colour matches the accent colour — rivets must remain matte metal grey to read as hardware, not as branding
- breaks if the page bg is high-chroma — the blob needs a quiet field to register
- breaks if the body font is serif — the industrial-craft register requires neutral sans
- breaks if `pointer-events: none` is omitted on the blob — the blob will intercept clicks and break interactivity
- breaks if border-radius on rivet-bearing cards drops to 0 — sharp corners + rivets read as broken render

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#FAFAF7`, `{{SURFACE}}` = `#FFFFFF`, `{{TEXT}}` = `#15151A`, `{{TEXT_MUTED}}` = `#5A5A66`, `{{PRIMARY}}` = `#15151A`, `{{ACCENT}}` = `#FF6B35`, `{{BORDER}}` = `#DEDCD3`, `{{FONT_DISPLAY}}` = `'General Sans', 'Inter', sans-serif`, `{{FONT_BODY}}` = `'Inter', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `8px`, `{{SHADOW}}` = `0 4px 16px rgba(0,0,0,0.06)`, `{{SPACING}}` = `8px`). The skeleton verifies the quiet base palette; the blob + rivets require the patterns above on a real layout.

Upstream parity source: styles-A.md Category 10 #32 + blocked-B.md #71 (blob) and #69 (rivet) — clean-room derivation; no verbatim copy.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 104149 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-009 Aurora (also blob-blur, but as page-wide atmosphere not localised top-of-fold), S-027 Maximalism (multi-accent painterly, but flat not blurred), S-013 Industrial (industrial register but flat colour, no rivet motif)
- **Differentiators:** S-069 is *single-blob ambient source* + *rivet hardware accents*; S-009 spreads blobs across whole canvas with no rivets; S-027 paints flat overlapping shapes; S-013 leans industrial typography without colour blob
- **Source:** styles-A.md Category 10 #32 + blocked-B.md #71/#69 (clean-room derivation; upstream licence unknown)
