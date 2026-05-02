---
name: TECH-ux-rule-accessibility
category: ux-rule-a11y
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/accessibility.md
also-in: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
---

# TECH: Rule — Accessibility & Inclusive Design (WCAG AA)

## What it does

The CRITICAL-priority rule covering WCAG 2.1 AA compliance plus inclusive-design patterns (motor / visual / cognitive / situational accommodations). Accessibility is legally required in many jurisdictions (ADA in the US, EN 301 549 in the EU, AODA in Ontario) and is a moral imperative everywhere else.

## When to use

On every deliverable. There is no "non-accessible" phase of a UX project. Specific triggers: "WCAG audit", "accessibility review", "a11y check", "screen-reader support", "keyboard navigation review".

## How it works

### WCAG AA (minimum floor) — four POUR pillars

**Perceivable**
- Color contrast 4.5:1 normal text, 3:1 large text (18px bold or 24px+)
- Descriptive alt text on images; decorative images use `alt=""`
- Synchronized captions on video
- Content preserved when CSS is disabled

**Operable**
- Keyboard-reachable for every interactive element
- Focus indicators visible (min 2px, high contrast)
- Skip links ("Skip to main content") for keyboard users
- 44×44 CSS px minimum touch targets
- No time traps; user can extend / disable time limits
- No seizure-inducing content (> 3 flashes/sec)

**Understandable**
- Visible form labels, not placeholder-as-label
- Error messages in text (not color alone)
- Confirm destructive actions; provide undo
- Consistent navigation across pages
- `lang` attribute on `<html>`

**Robust**
- Semantic HTML (`<button>`, `<nav>`, `<main>`, `<header>`) before ARIA
- ARIA only when semantic HTML is insufficient
- Test with VoiceOver + NVDA (minimum)

### Inclusive design patterns (beyond compliance)

- **Motor:** one-handed mobile use (thumb zone); 48×48 generous target; no hover-only interactions
- **Visual:** color never the only signal; light + dark mode; text resize to 200% without breakage
- **Cognitive:** plain language (6th-8th grade reading level); small steps; minimize choices
- **Situational:** offline + loading states; RTL-friendly layouts; no culturally specific metaphors / colors

### Testing checklist

- [ ] Automated audit (Axe, Lighthouse)
- [ ] Keyboard-only walkthrough (Tab, Enter, Esc, Arrow keys)
- [ ] Screen-reader walkthrough (VoiceOver or NVDA)
- [ ] 200% zoom — no content loss or overlap
- [ ] High-contrast mode — still visible
- [ ] `prefers-reduced-motion` — animations reduced or removed

## Minimal example

Button inaccessible → compliant:

```html
<!-- ✗ Inaccessible -->
<div class="btn" onclick="save()">Save</div>

<!-- ✓ Compliant -->
<button type="button" class="btn" onClick="save()" aria-label="Save draft">Save</button>

<style>
.btn { min-height: 44px; min-width: 44px; padding: 0.75rem 1.5rem; }
.btn:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
</style>
```

*Attributed to the ux-designer rule file — `SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/accessibility.md`.*

## Gotchas

- `outline: none` without a replacement focus style is the most common a11y regression. If you must remove the default, replace it with `:focus-visible` styling.
- Placeholder text as label fails screen readers and disappears when the user types.
- Color-only error states ("field turned red") fail color-blind users. Pair with an icon or text marker.
- Automated tools (Axe, Lighthouse) catch ~30% of issues. The other 70% require manual testing with a screen reader.

## Cross-references

- [TECH-ux-rule-research](TECH-ux-rule-research.md), [TECH-ux-rule-ia](TECH-ux-rule-ia.md), [TECH-ux-rule-interaction](TECH-ux-rule-interaction.md), [TECH-ux-rule-visual](TECH-ux-rule-visual.md)
- `../../amw-ui-ux-reasoning/references/TECH-uiux-pre-delivery-checklist.md` — shared a11y checklist
- `../SKILL.md`
