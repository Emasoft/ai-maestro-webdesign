---
name: TECH-inline-token-coloring
category: infographic-template
source: image-generation/create-infographics/resources/copy-guide.md
also-in: image-generation/create-infographics/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [The two patterns](#the-two-patterns)
  - [Pattern 1: Color-only](#pattern-1-color-only)
  - [Pattern 2: Color + background tint](#pattern-2-color-background-tint)
- [HTML](#html)
- [What gets colored](#what-gets-colored)
- [The 2-per-bullet cap](#the-2-per-bullet-cap)
- [The `highlight` class vs `.accent`](#the-highlight-class-vs-accent)
- [The token-pill variant (standalone)](#the-token-pill-variant-standalone)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Inline token coloring — `$TOKEN` names always colored

## What it does

Token names mentioned inline in any body text MUST be wrapped in an
accent-colored span. This is a core signature — differentiates the
piece from generic marketing copy.

## The two patterns

### Pattern 1: Color-only

```css
/* source: image-generation/create-infographics/resources/copy-guide.md */
.highlight {
  color: var(--primary);
  font-weight: 600;
}
```

### Pattern 2: Color + background tint

```css
.highlight-bg {
  background: rgba(var(--primary-rgb), 0.15);
  color: var(--primary);
  padding: 1px 5px;
  border-radius: 3px;
  font-weight: 600;
}
```

Use `.highlight-bg` when tokens appear in dense lists where they'd
otherwise blend in; use `.highlight` in flowing body text.

## HTML

```html
<!-- source: image-generation/create-infographics/resources/copy-guide.md -->
<li>Hold <span class="highlight">500 $TKN</span> before snapshot</li>
<li>Earn <span class="highlight">$ARENA</span> + <span class="highlight">$ENERGY</span> daily</li>

<!-- With background -->
<p>Your <span class="highlight-bg">$TKN</span> balance determines tier.</p>
```

## What gets colored

- **Token names** — always: `$TKN`, `$ARENA`, `$ETH`, `BTC`
- **Key numbers** in body text — sometimes: percentages, dates
- **Critical terms** — sometimes: "SNAPSHOT DATE", "TGE"

## The 2-per-bullet cap

Max 2 highlights per bullet / sentence. More than 2 and the emphasis
loses meaning — everything becomes noise.

```
✅ Hold <span class="highlight">500 $TKN</span> before
   <span class="highlight">March 31st</span>.

❌ Hold <span class="highlight">500 $TKN</span> before
   <span class="highlight">March 31st</span> to earn
   <span class="highlight">8% APY</span> on
   <span class="highlight">staked tokens</span>.
```

## The `highlight` class vs `.accent`

```
.highlight          — Inline text in body copy (bullet, paragraph)
.accent             — Dense table cells (see dense-table component)
.token-pill         — Stand-alone token identifier
```

Don't use them interchangeably — different contexts.

## The token-pill variant (standalone)

```css
.token-pill {
  display: inline-block;
  padding: 2px 8px;
  background: rgba(var(--primary-rgb), 0.15);
  border: 1px solid rgba(var(--primary-rgb), 0.35);
  color: var(--primary);
  border-radius: 3px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
```

For use when `$TOKEN` needs to be a standalone label, not inline
with body text.

## Gotchas

- Uncolored `$TOKEN` in body text is an anti-pattern — it reads as
  marketing, not dense editorial.
- Don't color every occurrence — once per paragraph / bullet is
  enough. Re-coloring the 3rd mention adds no information.
- Background tint (`.highlight-bg`) is stronger than color-only —
  use it only where emphasis really matters.

## Cross-references

- [TECH-copy-guide-bullets](TECH-copy-guide-bullets.md) — Rule 4 mandates this pattern.
- [TECH-signature-palette](TECH-signature-palette.md) — where `var(--primary)` comes from.
- [TECH-dense-table-component](TECH-dense-table-component.md) — the `.accent` table-cell variant.
- [`../SKILL.md`](../SKILL.md) — parent skill

