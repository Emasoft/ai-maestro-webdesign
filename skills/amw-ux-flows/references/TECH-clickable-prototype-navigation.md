---
name: TECH-clickable-prototype-navigation
category: ux-flow-wireframe
source: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Navigation wrapper class](#navigation-wrapper-class)
  - [Patterns](#patterns)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-clickable-prototype-navigation

## What it does

Wires every navigable element in a wireframe with **`<a href="...">`
links** wrapped in a `.wf-link` class, producing a clickable prototype
navigable in any browser with zero JavaScript. Every button, tab, card,
and list item that logically navigates becomes an anchor tag.

## When to use

- **Every wireframe** emitted in Phase 3 of the `ux-flows` workflow.
- **Whenever a stakeholder needs to click through the UX** before
  committing to visual design — the anchor-based approach works in
  email, on GitHub Pages, on a shared file system.
- **Never use JavaScript** for wireframe navigation — no onclick, no
  form submits, no JS state transitions. See Gotchas.

## How it works

### Navigation wrapper class

```css
a.wf-link {
  color: inherit;
  text-decoration: none;
  display: contents;    /* critical: makes the <a> behave as a transparent wrapper */
}
a.wf-link:hover {
  opacity: 0.7;
}
a.wf-link:active {
  opacity: 0.5;
}
```

The `display: contents` on `.wf-link` is the key — it makes the anchor
tag visually invisible, preserving the parent's flex/grid layout, while
still capturing the click.

### Patterns

**Button linking to another screen:**

```html
<a href="home.html" class="wf-link">
  <div class="wf-button">Sign In</div>
</a>
```

**Tab bar (each tab is a link):**

```html
<div class="wf-tab-bar">
  <a href="home.html" class="wf-link">
    <div class="wf-tab-item active">
      <div class="wf-icon-placeholder"></div>
      Home
    </div>
  </a>
  <a href="search.html" class="wf-link">
    <div class="wf-tab-item">
      <div class="wf-icon-placeholder"></div>
      Search
    </div>
  </a>
  <a href="profile.html" class="wf-link">
    <div class="wf-tab-item">
      <div class="wf-icon-placeholder"></div>
      Profile
    </div>
  </a>
</div>
```

**Back button in nav bar:**

```html
<div class="wf-nav">
  <a href="previous.html" class="wf-link wf-back">&larr; Back</a>
  <span>SCREEN_NAME</span>
  <span></span>
</div>
```

**Tappable list item linking to detail screen:**

```html
<a href="detail.html" class="wf-link">
  <div class="wf-list-item">
    <div class="wf-icon-placeholder"></div>
    <span>Item label</span>
  </div>
</a>
```

**Tappable card linking to another screen:**

```html
<a href="detail.html" class="wf-link">
  <div class="wf-card">Card content here</div>
</a>
```

## Minimal example

Home screen with tab bar + navigable cards:

```html
<div class="wf-screen">
  <div class="wf-header">Home</div>

  <div class="wf-content">
    <a href="orders.html" class="wf-link">
      <div class="wf-card">
        <div class="wf-label">Recent orders</div>
        <div class="wf-title">3 shipped, 1 pending</div>
      </div>
    </a>

    <a href="invoice.html" class="wf-link">
      <div class="wf-card">
        <div class="wf-label">Invoice</div>
        <div class="wf-title">$420 due Aug 1</div>
      </div>
    </a>
  </div>

  <div class="wf-tab-bar">
    <a href="home.html" class="wf-link">
      <div class="wf-tab-item active">Home</div>
    </a>
    <a href="search.html" class="wf-link">
      <div class="wf-tab-item">Search</div>
    </a>
    <a href="profile.html" class="wf-link">
      <div class="wf-tab-item">Profile</div>
    </a>
  </div>
</div>
```

## Gotchas

- **`display: contents` is non-negotiable.** Without it, the anchor
  becomes a block-level element that breaks the parent's flex/grid
  layout. Every wireframe template must ship this rule.
- **No JavaScript.** The wireframe must work when saved as a `.html`
  file and opened from the desktop. JS breaks this expectation and
  eliminates the browser-as-preview loop.
- **Tab bar must be consistent across screens.** If the "Home" tab
  links to `home.html` on one screen, it must link to `home.html` on
  every screen. Tab-bar divergence breaks the clickable-prototype
  illusion.
- **Back buttons point to the actual previous screen**, not always to
  `home.html`. The "back" meaning differs per flow; wire each back
  button to the screen it came from.
- **`:hover` and `:active` opacity changes** are the visual affordance
  that the element is clickable. Without them, stakeholders hover and
  don't realise they should click.
- **No form submits.** If a screen has a form, the "submit" button is
  an `<a href="next.html" class="wf-link">` like any other button —
  the wireframe doesn't actually process inputs. See
  [TECH-no-dead-end-screens](TECH-no-dead-end-screens.md).

## Cross-references

- [SKILL](../SKILL.md) — Phase 3 of the workflow
- [TECH-wireframe-html-mobile-first](TECH-wireframe-html-mobile-first.md) — the full HTML scaffold
  > What it does · When to use · How it works · Scaffold · Aesthetic tokens · Utility classes · Minimal example · Gotchas · Cross-references
- [TECH-no-dead-end-screens](TECH-no-dead-end-screens.md) — companion rule (every screen has ≥1
  > What it does · When to use · How it works · Minimal example · Validation check · Gotchas · Cross-references
  outgoing link)
- [TECH-wireframe-index-inventory](TECH-wireframe-index-inventory.md) — the inventory that tracks
  > What it does · When to use · How it works · Minimal example · Gotchas · Validation pass · Cross-references
  link targets
