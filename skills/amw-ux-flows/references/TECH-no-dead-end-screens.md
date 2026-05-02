---
name: TECH-no-dead-end-screens
category: ux-flow-wireframe
source: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Validation check](#validation-check)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-no-dead-end-screens

## What it does

Enforces that **every wireframe HTML file has at least one outgoing
navigation link** — back button, tab bar, or action button. The rule
prevents the "user is stuck" failure mode where the prototype reaches a
screen and stakeholders can't continue clicking through the flow.

## When to use

- **Every wireframe** emitted in Phase 3. Non-negotiable.
- **Every time a new wireframe is added** to an existing `ux-flows`
  output directory.
- **Never skip** the rule — even terminal screens (success, error,
  confirmation) need a way back.

## How it works

For every `.html` wireframe, verify at least one of:

1. **Back button** in the `.wf-nav` bar pointing to the previous screen
   (`<a href="previous.html" class="wf-link wf-back">&larr; Back</a>`).
2. **Tab bar** at the bottom with at least 2 tabs linking to other screens.
3. **Action button** in the content area pointing somewhere
   (`<a href="next.html" class="wf-link"><div class="wf-button">Continue</div></a>`).
4. **Tappable card or list item** linking to a detail view.

Terminal screens (success, error, thank-you) always need at least a
"back to home" link — usually as an action button:

```html
<!-- Success screen pattern -->
<div class="wf-content">
  <div class="wf-title">Order placed</div>
  <div class="wf-subtitle">Confirmation #42</div>
  <div class="wf-spacer"></div>

  <a href="home.html" class="wf-link">
    <div class="wf-button">Back to home</div>
  </a>
  <a href="orders.html" class="wf-link">
    <div class="wf-button-secondary">View orders</div>
  </a>
</div>
```

## Minimal example

Dead-end screen (❌ violates the rule):

```html
<div class="wf-screen">
  <div class="wf-header">Thanks!</div>
  <div class="wf-content">
    <div class="wf-title">Your feedback has been submitted.</div>
  </div>
  <!-- No outgoing link — user is stuck -->
</div>
```

Fixed version (✅ satisfies the rule):

```html
<div class="wf-screen">
  <div class="wf-nav">
    <a href="home.html" class="wf-link wf-back">&larr; Back to home</a>
    <span>Feedback</span>
    <span></span>
  </div>
  <div class="wf-content">
    <div class="wf-title">Your feedback has been submitted.</div>
    <div class="wf-spacer"></div>
    <a href="feedback.html" class="wf-link">
      <div class="wf-button-secondary">Leave more feedback</div>
    </a>
  </div>
  <div class="wf-footer">thanks.html — UC-007</div>
</div>
```

## Validation check

When building the wireframe index (see [TECH-wireframe-index-inventory](TECH-wireframe-index-inventory.md)),
the "Outgoing links" column must be non-empty for every row. A row with
an empty or zero outgoing-links list is a bug.

```markdown
| Screen name | File link | UCs | Outgoing links |
|---|---|---|---|
| Thanks | thanks.html | UC-007 | home.html, feedback.html |  ← ✅
| Sad dead-end | error.html | UC-005 |                     |  ← ❌ violates
```

## Gotchas

- **Tab bar alone is sufficient** — a screen with a tab bar has at least
  3 outgoing links (each tab). No need to add an explicit back button
  to screens that live under the tab bar.
- **`onclick` handlers do NOT satisfy the rule.** No JavaScript. The
  link must be a real `<a href="...">`. See
  [TECH-clickable-prototype-navigation](TECH-clickable-prototype-navigation.md).
- **Modal wireframes are still screens.** A modal is a separate `.html`
  file in this skill's convention (clickable prototypes don't overlap
  screens). The modal must have an "X close" link to its parent screen
  AND a confirmation link to wherever the action routes.
- **Login-required screens** route the user to `login.html` if not
  authenticated — that is a valid outgoing link even if it's a
  redirect-like pattern.
- **Error screens are not terminal either.** A 500-error wireframe
  needs a "try again" link (back to the source screen) and a "home"
  link at minimum.

## Cross-references

- `../SKILL.md` — Phase 3 of the workflow
- [TECH-wireframe-html-mobile-first](TECH-wireframe-html-mobile-first.md) — the HTML scaffold
- [TECH-clickable-prototype-navigation](TECH-clickable-prototype-navigation.md) — the link pattern
- [TECH-wireframe-index-inventory](TECH-wireframe-index-inventory.md) — the index that audits this rule
