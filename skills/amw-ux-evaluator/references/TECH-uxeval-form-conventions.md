---
name: TECH-uxeval-form-conventions
category: uxeval-dim
source: SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Position](#position)
  - [Visual weight](#visual-weight)
  - [Spacing](#spacing)
  - [Accessibility floor](#accessibility-floor)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Form conventions (labels / submit / errors / spacing)

## What it does

Component-specific reference for form evaluation. Forms are the highest-intent surface in most products — users are committing information, so label placement, error communication, and spacing matter disproportionately.

## When to use

On every evaluation that includes a form — signup, checkout, contact, settings, search-with-filters.

## How it works

### Position

- **Labels** above or to the left of inputs (not placeholder-only)
- **Submit button** at the bottom — right-aligned for paired actions ([Cancel] [Submit]), full-width for single-action mobile forms
- **Error messages** adjacent to the field that triggered them (inline, not batched at the top)

### Visual weight

- **Required fields** marked clearly (asterisk or "required" label; color alone fails color-blind users)
- **Error state** prominent (red border + red icon + red text — never red alone)
- **Success state** confirmatory (green check + green border when validation passes)
- **Disabled submit** until required fields filled — opacity 0.4, cursor not-allowed, aria-disabled="true"

### Spacing

- **Consistent vertical rhythm** between fields (1-1.5 rem / 16-24 px)
- **Label-to-input gap:** 0.25-0.5 rem (4-8 px) — label belongs to input, so it's tight
- **Field-to-field gap:** 1-1.5 rem (16-24 px) — separates input groups
- **Section-to-section gap:** 2-3 rem (32-48 px) — separates logical sections

### Accessibility floor

- Labels must be visible, not placeholder-only (placeholders vanish when user types)
- `for` / `id` linkage between `<label>` and `<input>`
- Error messages announced via `aria-live="polite"`
- Form errors summarized at top with anchor links to fields (optional but recommended)
- Submit button reachable via keyboard (no onClick-only divs)

## Minimal example

Email signup form done right:

```html
<form class="signup">
  <label for="email">Email address</label>
  <input id="email" name="email" type="email" required aria-describedby="email-error">
  <p id="email-error" class="error" aria-live="polite">Enter a valid email (e.g., name@example.com)</p>

  <label for="password">Password</label>
  <input id="password" name="password" type="password" required minlength="8" aria-describedby="password-hint">
  <p id="password-hint" class="hint">At least 8 characters</p>

  <button type="submit" class="btn btn-primary">Create Account</button>
</form>

<style>
  .signup label { display: block; margin-bottom: 4px; font-weight: 500; }
  .signup input { display: block; margin-bottom: 16px; padding: 12px; min-height: 44px; width: 100%; }
  .signup .error { color: var(--color-error); font-size: 14px; margin-top: -8px; margin-bottom: 16px; }
  .signup .hint  { color: var(--color-muted); font-size: 14px; margin-top: -8px; margin-bottom: 16px; }
  .signup .btn   { margin-top: 16px; }
</style>
```

*Attributed to the ux-evaluator skill — `SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md`.*

## Gotchas

- Placeholder-as-label is the most common form accessibility regression. Always pair with a visible `<label>`.
- "Invalid input" error messages are useless. "Enter a valid email (e.g., name@example.com)" is specific and actionable.
- Red border-only error state fails color-blind users. Pair with an icon (⚠) and text.
- Submit buttons that clear entered data on error are a dark pattern. Preserve all valid input across the error state.
- Asterisks for required fields are understood; "required" text is clearer. Either works; color-only (red label) is wrong.

## Cross-references

- [TECH-uxeval-button-conventions](TECH-uxeval-button-conventions.md), [TECH-uxeval-navigation-conventions](TECH-uxeval-navigation-conventions.md)
  > [TECH-uxeval-navigation-conventions.md] What it does · When to use · How it works · Position (top bar, LTR) · Theme toggle placement (industry cross-check) · Visual weight · Utility control visual weight · Spacing · Mobile patterns · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Position · Visual weight · Spacing · Labels · Minimal example · Gotchas · Cross-references
- [TECH-ux-rule-accessibility](../../amw-ux-designer/references/TECH-ux-rule-accessibility.md)
  > What it does · When to use · How it works · WCAG AA (minimum floor) — four POUR pillars · Inclusive design patterns (beyond compliance) · Testing checklist · Minimal example · Gotchas · Cross-references
- [TECH-ux-rule-interaction](../../amw-ux-designer/references/TECH-ux-rule-interaction.md) — microcopy for errors
  > What it does · When to use · How it works · Flow best practices · Multi-step flows · Error recovery · Microcopy · Specific rules · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
