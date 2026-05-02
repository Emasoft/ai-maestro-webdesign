---
name: TECH-designlang-dark-mode
category: designlang-url-extract
source: SKILLS-TO-INTEGRATE/web-design/designlang-design-extract/SKILL.md
also-in:
---

# TECH: `--dark` — dark-mode extraction

## What it does

Re-renders the target URL with `prefers-color-scheme: dark` emulated so designlang captures dark-theme colors, backgrounds, and component surfaces alongside (or instead of) the default light mode.

## When to use

- Sites that ship both light and dark themes (Vercel, Linear, GitHub, Stripe-internal). Running without `--dark` silently loses half the palette.
- Brand-reverse engineering where the dark variant is the canonical surface (dashboards, dev tools).
- When downstream output targets `shadcn.theme.css` or Figma Variables, both of which model light and dark as sibling token sets.

Skip `--dark` on pages that have no dark theme — the extra run adds noise without new signal.

## How it works

designlang uses Playwright's `page.emulateMedia({ colorScheme: 'dark' })` to flip the media query. If the site toggles theme via `class="dark"` on `<html>` or a `data-theme="dark"` attribute, designlang attempts that path as a second strategy. Colors, backgrounds, and surface shadows are captured into a `dark` block within the W3C tokens file and rendered as a second `:root[data-theme="dark"]` selector in the CSS output.

## Minimal example

```bash
npx designlang https://vercel.com --dark
```

The generated shadcn theme CSS gains a sibling `.dark { --background: ...; --foreground: ...; }` block mirroring the light mode.

*Attributed to designlang — `designlang-design-extract/SKILL.md`.*

## Gotchas

- Some sites only ship dark mode via JavaScript runtime toggles that `emulateMedia` does not trigger. If the dark block comes back identical to light, run with `--wait 3000` so client-side theme hydration has time to complete.
- Sites with `prefers-color-scheme: dark` but no actual styling (still default) produce misleading output. Cross-check against a manual browser preview.

## Cross-references

- [TECH-designlang-full-mode](TECH-designlang-full-mode.md) — `--full` enables this plus three more modes
- `../SKILL.md`
