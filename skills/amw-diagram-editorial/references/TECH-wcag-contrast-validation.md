---
name: TECH-wcag-contrast-validation
category: editorial-brand
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-wcag-contrast-validation

## What it does

Runs WCAG AA contrast validation on every foreground/background pair used
in an editorial diagram, auto-proposes remediation when a pair fails, and
refuses to ship a failing pair silently. Target ratio: **≥4.5:1** at 12px
body copy (the hard threshold for small text). Larger labels (≥18px or
bold 14px) fall under the 3:1 AA-Large rule but editorial diagrams
enforce the stricter 4.5:1 across the board for simplicity.

## When to use

- **Every time** [style-guide](style-guide.md) is written or changed — during brand
  onboarding, manual edits, or template updates.
- **Before returning any generated HTML** when the diagram has overridden
  any token.
- **Never skip** the validation and never allow a failing pair to be
  emitted.

Do not run this on gradients or semi-transparent overlays directly —
compute the effective colour over the canonical `paper` background first,
then check.

## How it works

For each pair `(fg, bg)` in the token table, compute the relative
luminance per WCAG 2.1:

```
luminance(c) = 0.2126*R + 0.7152*G + 0.0722*B
where R,G,B are the sRGB channels linearised:
  linear(c) = (c/255 <= 0.03928) ? c/12.92 : ((c/255 + 0.055)/1.055)^2.4

contrast(fg, bg) = (max(L_fg, L_bg) + 0.05) / (min(L_fg, L_bg) + 0.05)
```

Rules:

| Pair | Required ratio | Rationale |
|---|---|---|
| `ink` on `paper` | ≥4.5:1 | Primary body text |
| `ink` on `paper-2` | ≥4.5:1 | Card-contained body text |
| `accent-fg` on `accent` | ≥4.5:1 | Focal-node label legibility |
| `muted` on `paper` | ≥3.0:1 | Secondary labels only (AA-Large-ish) |
| `muted` on `paper-2` | ≥3.0:1 | Same, inside cards |

Auto-remediation for a failing `ink` on `paper`:

1. Darken `ink` in oklch space by decreasing `L` in 2% steps until the
   ratio passes.
2. If `ink` is already very dark and the issue is actually a too-warm
   `paper`, lighten `paper` by increasing `L` in 2% steps.
3. If neither works within 5 iterations, surface a clear error to the
   user with both the failing pair and the suggested direction.

## Minimal example

Validating an onboarding output against Stripe-style tokens:

```javascript
// paper: #FFFFFF, ink: #0A2540 — expected ratio ~15:1
contrast('#0A2540', '#FFFFFF') === 15.23   // passes

// accent-fg: #FFFFFF, accent: #635BFF — expected ratio ~4.96:1
contrast('#FFFFFF', '#635BFF') === 4.96    // passes 4.5:1

// A failing pair: muted: #B0B0B0, paper: #FFFFFF
contrast('#B0B0B0', '#FFFFFF') === 2.41    // fails even AA-Large 3:1
// Fix: darken muted to oklch(50% 0.01 80) ≈ #777777 → ratio ≈ 4.69:1
```

## Gotchas

- **Linearisation matters.** Using raw RGB skews the contrast ratio and
  produces false passes. Always linearise before computing luminance.
- **AA-Large (3:1) is only for ≥18px or bold 14px.** If the text is at
  10-12px (sublabels, mono mouse-type), the 4.5:1 rule still applies —
  don't relax it just because the text is "decorative".
- **Transparent fills must be resolved first.** `paper-2` at `0.5` opacity
  over `paper` is effectively a fourth colour; compute it before
  validating.
- **Shipping a failing pair is a severe defect.** Never auto-ship. If the
  auto-remediation loop doesn't converge, escalate to the user with both
  the failing ratio and the proposed fix.

## Cross-references

- `../SKILL.md` — orchestrator; contrast validation is non-skippable
- [TECH-brand-url-onboarding](TECH-brand-url-onboarding.md) — onboarding runs this immediately after
  palette extraction
- `../../amw-design-principles/color-system.md` — oklch / WCAG AA reference
- [style-guide](style-guide.md) — the file whose tokens get validated
- [TECH-four-px-grid-snap](TECH-four-px-grid-snap.md) — the other non-negotiable rule
