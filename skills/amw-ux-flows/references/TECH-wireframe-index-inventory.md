---
name: TECH-wireframe-index-inventory
category: ux-flow-wireframe
source: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/SKILL.md
also-in:
---

# TECH-wireframe-index-inventory

## What it does

Generates `docs/ux-flows/wireframes/INDEX.md` — a **screen inventory
table** cataloging every wireframe in the output directory with its
purpose, related use cases, key UI elements, and outgoing navigation
links. The index is the map of the clickable prototype.

## When to use

- **End of Phase 3** of the `ux-flows` workflow. Mandatory.
- **After any wireframe edit** — regenerate the index so the catalog
  stays in sync.
- **Before generating the Phase 4 handoff document** — the handoff
  references this index's entries.

## How it works

Fixed table schema:

| Column | Description |
|---|---|
| `Screen name` | Human-readable name (e.g. "Login", "Home", "Order Detail") |
| `File link` | Relative link to the `.html` file |
| `Related use cases` | UC-IDs this screen participates in |
| `Key elements` | Main components on the screen (3-6 items, comma-separated) |
| `Outgoing links` | Every screen this one links to (comma-separated) |

The `Outgoing links` column is the audit trail for
`TECH-no-dead-end-screens.md` — any row with an empty value is a bug.

## Minimal example

Four-screen inventory:

```markdown
# Wireframes — Screen Inventory

| Screen name | File link | Related UCs | Key elements | Outgoing links |
|---|---|---|---|---|
| Splash | [splash.html](./splash.html) | UC-001 | Logo, tagline | home.html, login.html |
| Login | [login.html](./login.html) | UC-002 | Email input, Password input, Sign in button, Forgot link, Register link | home.html, forgot.html, register.html |
| Home | [home.html](./home.html) | UC-003 UC-004 | Recent orders card, Invoice card, Tab bar | orders.html, invoice.html, search.html, profile.html |
| Profile | [profile.html](./profile.html) | UC-004 | Avatar, Edit button, Settings link, Logout | edit-profile.html, settings.html, login.html |
```

## Gotchas

- **Relative links, not absolute.** `[my-screen.html](<./my-screen.html>)`, not
  `[my-screen.html](</docs/ux-flows/wireframes/my-screen.html>)`. Absolute paths
  break when the directory moves.
- **Related UCs are space-separated**, not comma-separated — so a single
  cell can enumerate multiple UCs without ambiguity when the UCs
  themselves have "and" in their names.
- **Key elements lists 3–6 items.** Fewer doesn't convey what's on the
  screen; more turns the table into a component listing. If the screen
  has 20+ elements, pick the 6 most important for orientation.
- **Outgoing links list the unique TARGET screens**, not every anchor
  tag. If the Login screen has 3 buttons that all go to `home.html`,
  `home.html` appears ONCE.
- **Empty `Outgoing links` = dead-end = bug.** The inventory is a
  mechanical audit of `TECH-no-dead-end-screens.md`; empty values must
  be fixed before shipping.
- **Sort by natural flow order**, not alphabetical. Splash → Login →
  Home → everything-else — matches the reader's mental traversal.

## Validation pass

After emitting `INDEX.md`, run a quick sanity check:

1. Every `.html` file in the directory has a row in the index.
2. Every row has a non-empty `Outgoing links` column.
3. Every target named in `Outgoing links` is itself a row in the index
   (no phantom targets).
4. The `Related UCs` column references only UC-IDs that exist in
   `docs/ux-flows/use-cases.md`.

## Cross-references

- `../SKILL.md` — Phase 3 step 3 (index generation)
- `TECH-wireframe-html-mobile-first.md` — the HTML files being indexed
- `TECH-no-dead-end-screens.md` — the rule this index audits
- `TECH-clickable-prototype-navigation.md` — source of the link data
- `TECH-4-phase-mandatory-workflow.md` — Phase 4 consumes this index
