---
name: TECH-designlang-interactions
category: designlang-url-extract
source: SKILLS-TO-INTEGRATE/web-design/designlang-design-extract/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: `--interactions` — hover / focus / active state capture

## What it does

For every interactive element (buttons, links, inputs), designlang simulates `:hover`, `:focus`, and `:active` pseudo-states and records the computed-style deltas — color shifts, shadow adds, scale transforms, border changes. The output Markdown gains an "Interaction States" section documenting these deltas.

## When to use

- Reverse-engineering a site with a distinctive interaction language (Linear's subtle hover shadows, Stripe's gradient hover sweeps, Apple's scale-down active states).
- Building a shadcn/ui or React theme that models states as token variants.
- Auditing whether a site's hover/focus/active states are differentiated enough for WCAG 2.2 focus-visible compliance.

Skip on dashboards where every interactive element uses the same utility-class hover (Tailwind `hover:bg-...`) — the captured deltas are identical to the default state.

## How it works

designlang iterates over every element matching `a, button, input, select, textarea, [tabindex], [role="button"]`. For each, Playwright triggers hover (cursor move), focus (tab key), and active (mousedown) in sequence, capturing computed styles after each event. Differences from the default state are recorded as a per-selector delta map.

## Minimal example

```bash
npx designlang https://linear.app --interactions
```

Output includes:

```markdown
## 12. Interaction States

### .button-primary
- hover: box-shadow +0 4px 12px rgba(0,0,0,0.15), transform scale(1.02)
- focus: outline 2px solid var(--color-primary), outline-offset 2px
- active: transform scale(0.98), box-shadow reduced
```

*Attributed to designlang — `designlang-design-extract/SKILL.md`.*

## Gotchas

- Sites that use JavaScript for hover effects (intersection-observer-driven parallax, GSAP tweens) will not register via `:hover` CSS. The captured deltas underreport the real interaction design.
- Some focus states require keyboard tab sequencing which Playwright's focus-by-click does not emulate. For WCAG 2.2 focus-visible audits, pair this with a manual keyboard-navigation check via `../amw-dev-browser/`.
- Active states captured via mousedown can miss long-press or touch interactions on mobile-first sites.

## Cross-references

- [TECH-designlang-full-mode](TECH-designlang-full-mode.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
