---
id: S-082
name: Eight Hand-Extracted Brand Token Sets
aesthetic_position: brand-derived-prescriptive
source_attribution: "blocked-A.md §GRAPHIC STYLES entries #1-8 (A24, Arc, Raycast, Stripe, Aceternity, WIRED, Poolsuite, Polestar); hand-extracted from live brand sites; some upstream repos unlicensed → tokens treated as facts (direct-port) with clean-room synthesis prose."
license: direct-port for token facts (colour hex / type families / radius / spacing — uncopyrightable facts); clean-room for descriptive prose
---

# S-082 — Eight Hand-Extracted Brand Token Sets

## Identity

S-082 ships **eight prescriptive token blocks** hand-extracted from live brand sites — the prescriptive complement to S-081's descriptive corpus. Each block is a ready-to-paste CSS custom-property bundle that captures the visual fingerprint of one specific brand's actual on-site design system. Unlike S-001..S-080 (aesthetic categories with archetypal token blocks) and unlike S-081 (50-entry brand voice reference), S-082 entries are **brand-specific paste-targets**: shipping these tokens verbatim recreates the brand's look pixel-close.

**Legal note:** Colour hex values, font-family names, radius numbers, and spacing values are uncopyrightable facts of the live brand sites. The tokens below transcribe those facts. The brand's typeface licences (NB International, Marlin Soft SQ, Polestar Unica77, sohne-var, WiredDisplay, BreveText, Apercu, Lineage) are NOT included — substitute open-source fallbacks (Inter, IBM Plex Sans, Source Sans 3, Newsreader, etc.) before shipping a non-affiliated product.

Eight brands, eight categories: A24 (editorial film brutalism), Arc Browser (cream-paper mesh), Raycast (macOS dark native), Stripe (premium fintech), Aceternity (aurora motion-first), WIRED (newsstand editorial), Poolsuite (retro pastel), Polestar (luxury EV minimalism).

## Token block — Brand 1: A24 Editorial Film Brutalism

```css
:root {
  /* A24 — pure binary black/white film-poster cinematic */
  --background:        #000000;
  --ink:               #ffffff;
  --text-muted:        #888888;
  --border:            #888888;
  --primary-accent:    #1883fd;  /* hover only — single point of colour */
  --radius-base:       0px;
  --font-display:      "NB International Web", "Helvetica Neue", Arial, sans-serif;
  --tracking-display:  -2.96px;  /* at 74px = -4% em */
  --tracking-large:    -2px;     /* at 50px */
  --line-height-hero:  0.92;
}
```

## Token block — Brand 2: Arc Browser Cream-Paper Mesh

```css
:root {
  /* Arc — cream-paper canvas, electric Arc Blue, pastel mesh blooms */
  --background:        #fffcec;
  --background-warm:   #fffadd;
  --primary:           #3139fb;
  --primary-deep:      #2702c2;
  --brand-dark:        #000354;
  --mesh-peach:        #f5e4d8;
  --mesh-butter:       #f6ecd2;
  --mesh-mint:         #dce8df;
  --mesh-violet:       #e3dcf2;
  --accent-coral:      #d86a73;
  --font-display:      "Marlin Soft SQ", "Marlin", system-ui, sans-serif;
  --tracking-hero:     -1.82px;  /* at 45.5px */
  --line-height-hero:  0.93;
  --radius-card:       16px;
}
```

## Token block — Brand 3: Raycast macOS Dark Native

```css
:root {
  /* Raycast — near-black blue-tinted void, Raycast Red as single accent */
  --background:           #07080a;
  --surface:              #101111;
  --surface-card:         #1b1c1e;
  --ink:                  #f9f9f9;
  --ink-secondary:        #cecece;
  --primary:              #FF6363;       /* Raycast Red */
  --accent-blue:          #55b3ff;
  --border:               #252829;
  --font:                 "Inter", "Inter Fallback", system-ui, sans-serif;
  --font-feature-display: "'liga' 0, 'ss02', 'ss08'";
  --font-feature-body:    "'calt', 'kern', 'liga', 'ss03'";
  --tracking-display:     0px;
  --tracking-body:        0.2px;          /* positive tracking = distinctive */
  --radius-card:          8px;
}
```

## Token block — Brand 4: Stripe Premium Fintech

```css
:root {
  /* Stripe — white canvas, deep navy ink, Stripe Purple, brand-tinted multi-layer shadow */
  --background:            #ffffff;
  --surface-light:         #f6f9fc;
  --primary:               #533afd;       /* Stripe Purple */
  --primary-deep:          #1c1e54;
  --ink:                   #061b31;
  --ink-label:             #273951;
  --ink-body:              #64748d;
  --ruby:                  #ea2261;
  --shadow-blue:           rgba(50,50,93,0.25);   /* brand-tinted layer 1 */
  --shadow-dark:           rgba(3,3,39,0.25);     /* brand-tinted layer 2 */
  --font-display:          "sohne-var", "SF Pro Display", system-ui, sans-serif;
  --weight-display:        300;
  --font-feature-display:  "ss01";
  --tracking-hero:         -1.4px;        /* at 56px */
  --radius-base:           6px;
}
```

## Token block — Brand 5: Aceternity Aurora Motion-First

```css
:root {
  /* Aceternity — near-black, aurora trio violet/pink/blue, intentional non-round radii */
  --background:        #09090b;
  --surface:           #18181b;
  --surface-elevated:  #1c1c22;
  --border:            #27272a;
  --ink:               #fafafa;
  --primary:           #8b5cf6;       /* violet */
  --secondary:         #ec4899;       /* pink */
  --tertiary:          #3b82f6;       /* blue */
  --glow-violet:       rgba(139,92,246,0.1);
  --glow-pink:         rgba(236,72,153,0.2);
  --font:              "Inter", system-ui, sans-serif;
  --tracking-hero:     -1.5px;        /* at 60px */
  --radius-card:       9.6px;         /* intentional non-round — signals craft */
  --radius-button:     7.6px;
}
```

## Token block — Brand 6: WIRED Newsstand Editorial

```css
:root {
  /* WIRED — paper white canvas, ink black, hairline rules, single link blue */
  --background:       #ffffff;
  --ink:              #000000;
  --ink-page:         #1a1a1a;
  --caption:          #757575;
  --hairline:         #e2e8f0;
  --hairline-strong:  #000000;
  --primary:          #057dbc;         /* links only */
  --font-display:     "WiredDisplay", helvetica, serif;
  --font-body:        "BreveText", helvetica, serif;
  --font-ui:          "Apercu", helvetica, sans-serif;
  --tracking-hero:    -0.5px;
  --line-height-hero: 0.93;
  --radius-base:      0px;
}
```

## Token block — Brand 7: Poolsuite Retro Pastel

```css
:root {
  /* Poolsuite — white bg, warm pastel primary, muted rose, pale teal border */
  --background:        #ffffff;
  --primary:           #f9f0e9;       /* warm pastel cream */
  --border:            #afe2e5;       /* pale teal */
  --ink-muted:         #f6d5d5;       /* muted rose */
  --shadow-soft:       #d9d9d9;       /* warm soft shadow */
  --font:              "Lineage", system-ui, sans-serif;
  --weight-display:    400;
  --tracking-display:  -1px;
  --line-height-hero:  1.05;
}
```

## Token block — Brand 8: Polestar Luxury EV Minimalism

```css
:root {
  /* Polestar — pure white, pure black, no accent on primary surface, Swedish-cold restraint */
  --background:        #ffffff;
  --surface:           #3d3d3d;
  --surface-elevated:  #f5f5f5;
  --ink:               #000000;
  --ink-muted:         #a8a8a8;
  --border:            #6e6e6e;
  --font:              "Polestar Unica77", system-ui, sans-serif;
  --weight-display:    400;
  --weight-heading:    500;             /* low contrast range — no bold */
  --size-hero:         96px;
  --tracking-hero:     -1px;
  --radius-base:       2px;             /* hairline near-zero */
}
```

## "Breaks if" invariants (per-brand selection)

- Breaks if multiple brand token blocks are merged into one composite — each block is a complete system; cross-pollinating Stripe's shadow tokens onto an Arc cream-paper bg breaks both brands' coherence.
- Breaks if the brand's proprietary typeface (NB International, Marlin Soft SQ, sohne-var, Polestar Unica77, WiredDisplay, BreveText, Apercu, Lineage) is shipped without a valid licence — substitute the fallback in each block before deploy.
- Breaks if the verbatim brand hex palette is shipped on a non-affiliated commercial product targeting the same audience as the source brand — that's design-trade-dress infringement, not influence.
- Breaks (A24) if a chromatic accent beyond the single `#1883fd` hover-only blue is introduced — A24's binary is the entire aesthetic.
- Breaks (Arc) if the cream-paper canvas is swapped for pure white — the warm `#fffcec` is the brand's full-bleed identity.
- Breaks (Raycast) if positive body tracking (`+0.2px`) is removed — that's a distinctive Raycast signal.
- Breaks (Stripe) if the two-layer brand-tinted shadow is collapsed to a single neutral drop-shadow — the blue-tinted multi-layer is Stripe's premium-fintech fingerprint.
- Breaks (Aceternity) if `--radius-card: 9.6px` and `--radius-button: 7.6px` are rounded to clean integers — the intentional non-round values signal craft.
- Breaks (WIRED) if hairline rules are replaced with soft borders or shadows — the structural ornament is hairline-only.
- Breaks (Poolsuite) if any high-contrast colour or dark surface is introduced — Poolsuite is exclusively daylight-warm.
- Breaks (Polestar) if a bold weight (700+) or a chromatic accent is introduced on the primary surface — Polestar's weight ceiling is 500 and primary surface is monochrome.

## Canonical render-test pointer

Render-test: each block injectable into `references/_test-skeleton.html` substituting the `{{TOKEN}}` markers.
Source render: live brand websites at time of capture — a24films.com, arc.net, raycast.com, stripe.com, ui.aceternity.com, wired.com, poolsuite.net, polestar.com.
Parity threshold: A-class (token-level direct-port; brand sites evolve continuously, so pixel parity drift is expected — token block parity is what we verify).

## Render-test verdict

JOD: A-class (specialized-tokens) — 2026-05-29
Reason: effect / layout / multi-brand token block — defines effect or scene parameters, not the 13-slot landing-page palette (absent slots: accent,bg,font-body,font-mono,primary,radius,shadow,spacing,surface,text). Canonical render uses the effect element/file named in the pointer, not the bare skeleton. Render OK 1440x900, det-JOD 10.00.

## Cross-references

- **Companion presets:** S-081 (50-brand voice-reference corpus from design-for-beauty) — descriptive complement; S-083 (183-brand DESIGN.md corpus from design-swatches) — superset.
- **Related prescriptive presets:** S-014 Editorial Serif (kin to WIRED), S-022 Minimal Pure (kin to Polestar), S-009 Aurora UI (kin to Aceternity), S-026 Soft Pastel (kin to Poolsuite), S-038 Dark Tech (kin to Raycast), S-029 Data Viz Dark (kin to Stripe-on-dark).
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- Source attribution: `reports/batch9-harvest/blocked-A.md` §GRAPHIC STYLES entries #1-8

## Attribution

Token blocks hand-extracted from live brand websites by the upstream `blocked-A.md` author (likely the dembrandt CLI + manual curation). Brand-fact data (colour hex, type family, radius, spacing, font features) is uncopyrightable and ported verbatim. Descriptive prose (vibe / mood / use-case) is paraphrased clean-room. The eight brands span eight distinct categories deliberately — selecting one block teaches a complete category language, not just a single brand's surface. Some upstream repos in the source chain are unlicensed; the licence-of-facts rule applies. Brand typefaces remain the property of their respective foundries and require independent licensing.
