---
name: TECH-uxeval-navigation-conventions
category: uxeval-dim
source: SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Position (top bar, LTR)](#position-top-bar-ltr)
  - [Theme toggle placement (industry cross-check)](#theme-toggle-placement-industry-cross-check)
  - [Visual weight](#visual-weight)
  - [Utility control visual weight](#utility-control-visual-weight)
  - [Spacing](#spacing)
  - [Mobile patterns](#mobile-patterns)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Navigation conventions (logo / primary / utilities)

## What it does

Component-specific reference for navigation evaluation. Navigation is the spine of a site's IA — getting it wrong means every downstream screen inherits the error.

## When to use

On every evaluation that includes a navbar, sidebar nav, or mobile bottom bar.

## How it works

### Position (top bar, LTR)

- **Logo** → LEFT
- **Primary nav** → CENTER or immediately after logo
- **Utility items** (search, auth, theme toggle) → RIGHT

### Theme toggle placement (industry cross-check)

| Site | Placement |
|---|---|
| GitHub | Far right, after user menu |
| VS Code Docs | Far right |
| Stripe Docs | Far right |
| Discord | In settings, not navbar |

Verdict: theme toggle is far right after auth, or hidden in settings. Never compete with primary CTAs.

### Visual weight

- **Active state** clearly distinguished (underline, background, color shift)
- **Current page** visible to both mouse + keyboard + screen-reader users
- **Navigation does not compete with page content** — nav items are sans, smaller, lower saturation than hero content

### Utility control visual weight

| Control | Expected weight |
|---|---|
| Theme toggle | Icon-only, subtle, doesn't compete with CTAs |
| Search | Icon trigger or compact input; expandable |
| Language selector | Icon or compact dropdown |

Rule: utilities are subordinate to primary actions. If the theme toggle has the same visual weight as the "Sign Up" CTA, the hierarchy has failed.

### Spacing

- Group related items (logo + primary nav) tightly
- Clear separation between nav groups (24 px+ between primary group and utility group)
- Adequate click/tap targets (44 × 44 px mobile)

### Mobile patterns

- Bottom bar for 3-5 primary actions on mobile apps (thumb-reachable)
- Hamburger for secondary navigation only — primary nav behind a hamburger is a usability regression on desktop
- Current section visibly highlighted

## Minimal example

Desktop navbar done right:

```html
<nav style="display:flex; align-items:center; padding:16px 24px;">
  <a class="logo" href="/">Brand</a>
  <ul class="nav-primary" style="display:flex; gap:24px; margin-left:48px;">
    <li><a href="/product" class="active">Product</a></li>
    <li><a href="/pricing">Pricing</a></li>
    <li><a href="/docs">Docs</a></li>
  </ul>
  <div class="nav-utilities" style="margin-left:auto; display:flex; gap:12px; align-items:center;">
    <button class="icon-btn" aria-label="Search">🔍</button>
    <button class="icon-btn" aria-label="Toggle theme">☾</button>
    <a class="btn btn-ghost" href="/login">Sign in</a>
    <a class="btn btn-primary" href="/signup">Sign up</a>
  </div>
</nav>
```

*Attributed to the ux-evaluator skill — `SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md`.*

## Gotchas

- Logo on the right is rare and almost always wrong in LTR. If a brand insists, document it as a known deviation, don't naturalize it.
- Hamburger menus on desktop hide 100% of navigation — bad. Only acceptable for small secondary surfaces (editor tool panels, not product nav).
- Theme toggle inside primary nav reads as a product feature, not a chrome utility. Move to far right.
- Sticky navigation that covers > 10% of the viewport on mobile is a usability regression. Collapse on scroll or reduce height.

## Cross-references

- [TECH-uxeval-button-conventions](TECH-uxeval-button-conventions.md), [TECH-uxeval-form-conventions](TECH-uxeval-form-conventions.md)
  > What it does · When to use · How it works · Position · Visual weight · Spacing · Labels · Minimal example · Gotchas · Cross-references
- [TECH-ux-rule-ia](../../amw-ux-designer/references/TECH-ux-rule-ia.md)
  > What it does · When to use · How it works · Navigation structure · Navigation patterns · Mobile specifics · Content organization · Information scent · Search as navigation · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
