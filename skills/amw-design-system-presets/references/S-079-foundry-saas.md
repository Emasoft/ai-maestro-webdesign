---
id: S-079
name: Foundry (Hard-bordered SaaS)
aesthetic_position: developer-terminal-monospace
source_attribution: "styles-A §Foundry (Hard-bordered SaaS); upstream: `claude-design-mode-main/README.md` 'Foundry' design example. LICENSE: MIT."
license: MIT
---

# S-079 — Foundry (Hard-bordered SaaS)

## Identity

Foundry is the "pricing table that means business" idiom — a deep black field with white text, Space Grotesk display (tabular numbers for prices that line up across tiers) sitting above Space Mono for data, code excerpts, and feature ledger entries. Each feature row reads like a ledger line in a terminal — `+` glyphs for included items, `-` glyphs for excluded items, never checkmarks or X-marks (icon-heavy lists kill the typographic ledger rhythm). Borders are hard 1px `#333` rules on a `#000` ground. The featured pricing tier inverts: solid black inside a thick white border, becoming a flat island against the otherwise grey-bordered grid. No drop shadows, no gradients, no rounded pill buttons. Reach for it when the brief is a developer-tool pricing page, an open-source project's "pro tier" disclosure, a B2B infrastructure landing where the audience is engineers who buy on spec-readability not visual polish. Avoid for consumer SaaS, marketing-led products — Foundry is unfriendly on purpose.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary:      #FFFFFF;   /* white text on black */
  --accent:       #FFFFFF;   /* Foundry has no chromatic accent — featured tier inverts to solid black-on-white */
  --bg:           #000000;   /* deep black field */
  --surface:      #0A0A0A;   /* card surface — almost imperceptible step from bg */
  --surface-elev: #FFFFFF;   /* inverted featured-tier surface — solid white */
  --text:         #FFFFFF;   /* primary text */
  --text-muted:   #999999;   /* secondary text — grey-500 */
  --text-faint:   #555555;   /* faint label / disabled ledger row */
  --text-inv:     #000000;   /* text on inverted featured tier */
  --border:       #333333;   /* hard 1px ledger border */
  --border-strong:#FFFFFF;   /* featured-tier wrapping border — thick white */
  --font-display: 'Space Grotesk', 'Helvetica Neue', system-ui, sans-serif;
  --font-body:    'Space Grotesk', 'Helvetica Neue', system-ui, sans-serif;
  --font-mono:    'Space Mono', 'JetBrains Mono', 'Menlo', monospace;
  --radius:       0px;       /* 0 or 2px maximum — Foundry is hard-edge */
  --radius-max:   2px;
  --shadow:       none;      /* no drop shadows ever */
  --spacing:      16px;
  --motion-duration: 0ms;    /* motion is none — the ledger does not animate */

  /* Ledger glyphs — used in :before / content for feature rows */
  --glyph-included:  "+";    /* never a checkmark */
  --glyph-excluded:  "-";    /* never an X */
  --glyph-na:        "~";    /* "not applicable" tier-specific */
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#FFFFFF',
        bg: '#000000',
        surface: '#0A0A0A',
        'surface-elev': '#FFFFFF',
        text: '#FFFFFF',
        'text-muted': '#999999',
        'text-faint': '#555555',
        'text-inv': '#000000',
        border: '#333333',
        'border-strong': '#FFFFFF',
      },
      fontFamily: {
        display: ['"Space Grotesk"', '"Helvetica Neue"', 'system-ui', 'sans-serif'],
        body:    ['"Space Grotesk"', '"Helvetica Neue"', 'system-ui', 'sans-serif'],
        mono:    ['"Space Mono"', '"JetBrains Mono"', 'Menlo', 'monospace'],
      },
      borderRadius: { DEFAULT: '0px', max: '2px' },
      boxShadow: { DEFAULT: 'none' },
    }
  }
}
```

**Light variant token override (Foundry's defining ground is dark; light variant is offered for completeness, rarely correct):**
```css
[data-theme="light"] {
  --primary:      #000000;
  --bg:           #FFFFFF;
  --surface:      #FAFAFA;
  --surface-elev: #000000;
  --text:         #000000;
  --text-muted:   #666666;
  --text-faint:   #AAAAAA;
  --text-inv:     #FFFFFF;
  --border:       #CCCCCC;
  --border-strong:#000000;
}
```

## "Breaks if" invariants

- Breaks if checkmark icons (✓) or X-marks (✗) replace `+` / `-` / `~` typographic glyphs in feature ledger rows — Foundry's vocabulary is character-based, not icon-based.
- Breaks if `border-radius` exceeds 2px — pill buttons, rounded cards, soft tiers all destroy the ledger-rule fingerprint.
- Breaks if any gradient (linear, radial, conic) appears on a tier card or button — Foundry is flat by definition.
- Breaks if a drop shadow lifts the featured tier — featured tier MUST be a flat inversion (black-on-white island), never elevated.
- Breaks if Space Grotesk or Space Mono are replaced — the display/mono pairing IS the typographic ledger signature.
- Breaks if the featured tier's price column does not use tabular-number alignment (Space Grotesk's tabular figures must line up vertically across all tiers).
- Breaks if motion / hover transitions exceed an instant state-flip (no fades, no spring scale, no glow).
- Breaks if a saturated chromatic accent (blue, green, brand-color) is introduced anywhere — Foundry is strictly black / white / grey.
- Breaks if feature rows exceed ~20 chars before wrapping — the ledger reads as a compact column, not a paragraph.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — token interpretation of `styles-A.md §Foundry (Hard-bordered SaaS)` prose; upstream `claude-design-mode-main/README.md` describes vocabulary but does not ship HTML.
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 79108 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-002 Brutalism (also hard borders + 0px radius, but uses raw primary colors not pure black/white), S-003 Neo-Brutalism (decorative-Brutalism with offset shadows — Foundry has no shadows), S-012 Retro Terminal (also Space Mono territory, but green-on-black CRT signal), S-013 Industrial (also mono + monochrome, but functional-yellow accent which Foundry rejects).
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: reports/batch9-harvest/styles-A.md §Foundry (Hard-bordered SaaS) — upstream claude-design-mode-main/README.md, MIT.

## Attribution

Visual vocabulary (ledger-row features, `+`/`-` glyphs, inverted featured tier, hard 1px borders) and font pairing (Space Grotesk + Space Mono) ported from styles-A.md §Foundry. Token hex values are clean-room interpretations of the upstream prose ("deep black background, white text, `border: 1px solid #333`, zero or 2px radius, featured tier uses flat `background: #000` inversion"). Upstream source repo `claude-design-mode-main` is MIT-licensed; this reference inherits MIT.
