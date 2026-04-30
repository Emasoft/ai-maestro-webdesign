---
name: TECH-designlang-responsive
category: designlang-url-extract
source: SKILLS-TO-INTEGRATE/web-design/designlang-design-extract/SKILL.md
also-in:
---

# TECH: `--responsive` — breakpoint capture

## What it does

Captures computed styles at four viewport breakpoints — mobile (375px), tablet (768px), desktop (1024px), and wide (1440px) — and emits a dedicated "Responsive Design" section in the Markdown report documenting which properties change across breakpoints.

## When to use

- Reverse-engineering a site whose layout, type scale, or spacing shifts noticeably between mobile and desktop (most modern sites).
- Building a Tailwind config that correctly models `sm:` / `md:` / `lg:` / `xl:` overrides rather than a single desktop-only token set.
- Auditing a site's responsive discipline — consistent ratios, container widths, and type ramps.

Skip on static landing pages where the only change between breakpoints is a single hamburger toggle — the extra three renders dominate runtime without new signal.

## How it works

designlang runs four sequential page loads, resizing the viewport before each one. For each element observed in the DOM, computed-style diffs are recorded per breakpoint. The Markdown output gains a "Responsive Design" section listing properties that changed and their per-breakpoint values. The Tailwind config gains responsive variants for type sizes and container widths when the source site uses them.

## Minimal example

```bash
npx designlang https://stripe.com --responsive
```

Resulting Markdown includes:

```markdown
## 11. Responsive Design

### Type scale (font-size)
- h1: 48px (mobile) → 60px (tablet) → 72px (desktop)
- body: 16px (mobile) → 16px (tablet) → 18px (desktop)

### Container
- max-width: 100% (mobile) → 720px (tablet) → 1200px (desktop)
```

*Attributed to designlang — `designlang-design-extract/SKILL.md`.*

## Gotchas

- Pages with JavaScript-driven layout (container queries + ResizeObserver, masonry via JS) may produce inconsistent diffs because the resize event races against layout computation. Add `--wait 1500` between breakpoints via upstream support if available.
- Not all breakpoints will be meaningful — a desktop-only marketing page will show mobile/tablet values that are simply the "unstyled" defaults. Cross-reference with the actual site's CSS `@media` rules before trusting the ramp.

## Cross-references

- `TECH-designlang-full-mode.md`
- `../SKILL.md`
