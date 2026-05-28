---
id: S-080
name: Tempo (Dark Tech App Landing)
aesthetic_position: dark-cinematic-cyber
source_attribution: "styles-A §Tempo (Dark Tech App Landing); upstream: `claude-design-mode-main/README.md` 'Tempo' design example. LICENSE: MIT."
license: MIT
---

# S-080 — Tempo (Dark Tech App Landing)

## Identity

Tempo is the "dark-mode app promo with a single iPhone mockup" idiom — a near-black field, Geist running both display and body (Vercel's clean grotesque providing the entire typographic stack), a centered iPhone device frame containing one app screen as the sole hero subject, and very sparse surrounding chrome (headline above, sub-line and one CTA below — that is the entire fold). The accent is a single restrained tint (cyan, lime, or a brand color) used on the CTA and nothing else; no gradients on backgrounds, no glow halos, no aurora-effect blobs. The device frame carries the only depth signal — a standard subtle drop shadow grounding the iPhone against the dark field. Reach for it when the brief is a single-product mobile-app launch, a Vercel-adjacent developer tool with a mobile companion, a Linear-style minimalist promo, or any case where the message is "here is one beautiful app, look at it." Avoid for multi-product platforms, marketing-heavy enterprises, content-rich landings — Tempo's restraint requires you to have only one thing to say.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary:      #FFFFFF;   /* white text on near-black */
  --accent:       #00D9C0;   /* single restrained cyan accent — swap to lime #A5F23D or brand color */
  --bg:           #0A0A0A;   /* near-black field — NOT pure #000, slightly warmer for screen comfort */
  --surface:      #141414;   /* card / footer panel surface */
  --surface-elev: #1F1F1F;   /* very rarely used — Tempo is single-layer */
  --text:         #FFFFFF;   /* primary text */
  --text-muted:   #A1A1AA;   /* secondary text — sub-headline / metadata */
  --text-faint:   #71717A;   /* faint label / legal */
  --border:       #27272A;   /* near-imperceptible hairline (rarely visible — Tempo barely uses borders) */
  --font-display: 'Geist', 'Inter', system-ui, sans-serif;
  --font-body:    'Geist', 'Inter', system-ui, sans-serif;
  --font-mono:    'Geist Mono', 'JetBrains Mono', 'Menlo', monospace;
  --radius:       8px;       /* CTA pill and card chrome — 6–10px range, 8px canonical */
  --radius-cta:   100px;     /* fully rounded CTA button */
  --radius-device:48px;      /* iPhone frame corner radius */

  /* Device-mockup shadow — the only depth signal in Tempo */
  --shadow-device: 0 24px 64px -16px rgba(0, 0, 0, 0.6), 0 8px 24px -8px rgba(0, 0, 0, 0.4);
  --shadow:        none;     /* general chrome has no shadow */

  --spacing:         8px;
  --motion-duration: 250ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#FFFFFF',
        accent: '#00D9C0',
        bg: '#0A0A0A',
        surface: '#141414',
        'surface-elev': '#1F1F1F',
        text: '#FFFFFF',
        'text-muted': '#A1A1AA',
        'text-faint': '#71717A',
        border: '#27272A',
      },
      fontFamily: {
        display: ['Geist', 'Inter', 'system-ui', 'sans-serif'],
        body:    ['Geist', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"Geist Mono"', '"JetBrains Mono"', 'Menlo', 'monospace'],
      },
      borderRadius: { DEFAULT: '8px', cta: '100px', device: '48px' },
      boxShadow: {
        DEFAULT: 'none',
        device:  '0 24px 64px -16px rgba(0,0,0,0.6), 0 8px 24px -8px rgba(0,0,0,0.4)',
      },
      transitionDuration: { DEFAULT: '250ms' },
    }
  }
}
```

**Light variant token override (Tempo's natural ground is dark; light is rarely correct but offered for completeness):**
```css
[data-theme="light"] {
  --primary:     #0A0A0A;
  --accent:      #00A693;
  --bg:          #FAFAFA;
  --surface:     #F4F4F5;
  --surface-elev:#FFFFFF;
  --text:        #0A0A0A;
  --text-muted:  #52525B;
  --text-faint:  #A1A1AA;
  --border:      #E4E4E7;
}
```

## "Breaks if" invariants

- Breaks if any gradient appears on the background, hero text, or CTA — Tempo is strictly flat fills, the device shadow is the only depth.
- Breaks if a warm-toned palette (cream, amber, terracotta accent) replaces the cool near-black + cyan/lime — Tempo's restraint is cold.
- Breaks if more than one device mockup appears in the hero fold — Tempo's whole conceit is "one phone, one app, one message"; a laptop + phone or three-phone fan destroys the rhythm.
- Breaks if the screen content inside the device frame is mocked rather than a real product screen — Tempo's promise is "this is the app".
- Breaks if more than one chromatic accent is used at full saturation — a single cyan OR lime OR brand-color, nothing else.
- Breaks if the headline + sub-line + CTA exceed three lines of text combined — Tempo's density is "very low" by spec.
- Breaks if Geist is replaced by a serif, a monospace, or a heavier grotesque (Inter is the only acceptable Geist substitute; Helvetica is too neutral).
- Breaks if the device frame is exaggerated (oversized shadow, glow halo, neon perimeter) — the device shadow must read as natural product photography.
- Breaks if the page is responsive only at one breakpoint — Tempo is mobile-marketing first; desktop + tablet + mobile responsiveness is mandatory.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — tokens interpreted from `styles-A.md §Tempo (Dark Tech App Landing)` prose; upstream `claude-design-mode-main/README.md` carries the description without a published HTML file.
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 100328 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-038 Dark Tech (broader dark-mode tech palette without the single-iPhone constraint), S-035 21st Aceternity (also Geist territory, but more decorative / animation-led), S-009 Aurora (dark cinematic with gradient halos — Tempo strictly forbids the gradient halo), S-029 Data Viz Dark (also near-black, but high-density data layouts which Tempo rejects).
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-A.md §Tempo (Dark Tech App Landing)` — upstream `claude-design-mode-main/README.md`, MIT.

## Attribution

Visual vocabulary (centered iPhone mockup, sparse hero chrome, single accent, very low density) and font choice (Geist) ported from styles-A.md §Tempo. Token hex values are clean-room interpretations of the upstream prose ("dark background near-black, single accent, no gradients, device frame has standard shadow"). Upstream source repo `claude-design-mode-main` is MIT-licensed; this reference inherits MIT.
