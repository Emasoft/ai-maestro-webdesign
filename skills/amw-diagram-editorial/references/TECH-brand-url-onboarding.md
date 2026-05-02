---
name: TECH-brand-url-onboarding
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


# TECH-brand-url-onboarding

## What it does

Matches a generated editorial diagram's palette and typography to the
user's live website in roughly 60 seconds. The agent fetches the user's
homepage, extracts the dominant palette + font stack, maps everything to
six semantic token roles (`paper`, `ink`, `muted`, `paper-2`, `accent`,
`accent-fg`), runs WCAG AA contrast checks, and writes the result to
`references/style-guide.md`.

## When to use

- **First use** of the skill in a new project. If [style-guide](style-guide.md) still
  holds the default stone + rust tokens, pause and ask the user: "Run
  onboarding, paste tokens manually, or proceed with default?"
- **Brand refresh** — the user has updated their site and wants diagrams
  to follow along.
- **Explicit invocation** — the user types `"onboard editorial diagrams
  to https://<site>"`.

Do not run onboarding silently or without explicit user consent — palette
changes are load-bearing on every diagram downstream.

## How it works

Five fixed steps:

1. **Fetch.** Route through `../../amw-dev-browser/` (never raw WebFetch) to
   load the homepage and serialize the DOM. The dev-browser primitive is
   the only authorised path for reading live pages in this plugin; raw
   WebFetch loses computed-style data that the palette extractor needs.
2. **Extract.** Pull dominant palette + font stack from computed styles.
3. **Map to semantic roles.**

   | Detected from site | Becomes token |
   |---|---|
   | `<body>` background | `paper` |
   | Primary text color | `ink` |
   | Secondary / caption text | `muted` |
   | Cards / container fills | `paper-2` |
   | Most-used brand color (CTA, link, heading) | `accent` |
   | `<h1>` font family | `title` font |
   | `<body>` font family | `node-name` font |
   | `<code>` / `<pre>` font | `sublabel` font |

4. **WCAG AA validation.** Run `4.5:1` contrast check on every
   foreground/background pair at 12px. Auto-propose adjustments (darker
   `ink`, lighter `paper`) for failures. Never silently ship a failing
   pair.
5. **Write + confirm.** Show a proposed diff to the user; on confirmation,
   overwrite `references/style-guide.md` with the new oklch token
   block and update the font-stack section.

## Minimal example

User invocation:

```
onboard editorial diagrams to https://stripe.com
```

Expected resulting tokens (approximate, stripe has a widely-known brand):

```markdown
| Role | Value | Source |
|---|---|---|
| paper | #FFFFFF | body background |
| ink | #0A2540 | primary text |
| muted | #425466 | secondary text |
| paper-2 | #F6F9FC | card fill |
| accent | #635BFF | brand purple |
| accent-fg | #FFFFFF | text on accent |
```

And a fonts block:

```
Title: "Inter", ui-sans-serif, system-ui
Body:  "Inter", ui-sans-serif, system-ui
Code:  ui-monospace, "SF Mono", Menlo, monospace
```

## Gotchas

- **dev-browser only.** Raw WebFetch silently loses computed-style data
  (it returns initial HTML, not rendered CSS). Palette extraction
  against WebFetch returns nonsense tokens.
- **Every color must pass WCAG AA at 12px.** Failing pairs must be
  auto-adjusted and shown in the diff; shipping a failing pair silently
  is a severe defect.
- **Fonts are advisory, not mandatory.** The editorial three-family rule
  (`Instrument Serif` / `Geist Sans` / `Geist Mono`) is preserved for
  the type-role mapping even after brand onboarding — the brand fonts
  override only if the user explicitly opts in.
- **Preserve the default fallback.** If onboarding fails, [style-guide](style-guide.md)
  must fall back to stone + rust, not to empty tokens. Every diagram
  downstream depends on the tokens being resolvable.

## Cross-references

- `../SKILL.md` — orchestrator; onboarding is step 1 before any diagram
- `../../amw-dev-browser/SKILL.md` — the only authorised browser-automation
  primitive
- `../../amw-design-principles/color-system.md` — oklch / WCAG AA reference
- [style-guide](style-guide.md) — the file onboarding writes
- [TECH-wcag-contrast-validation](TECH-wcag-contrast-validation.md) — the contrast-check step in detail
