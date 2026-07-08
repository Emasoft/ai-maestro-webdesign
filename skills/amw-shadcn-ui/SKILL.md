---
name: amw-shadcn-ui
description: shadcn/ui component usage, theming, forms, charts, and framework integration (Next.js / Vite / Remix / Astro / Laravel / Gatsby). Triggers on "shadcn component", "data-table", "shadcn form", "shadcn theme", "dark mode for shadcn", "install shadcn", registry questions, accessibility of Radix-based components, NOT generic "UI library" or "React component". Use when selecting, theming, or integrating a shadcn/ui component into a project. Trigger with explicit "shadcn" phrasing or component name.
---

# shadcn/ui Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Lazy-loaded documentation corpus covering 50+ shadcn/ui components, theming, forms, charts, dark mode, registry, RTL, and per-framework installation (Next.js, Vite, Remix, Astro, Laravel, Gatsby). Reference-only skill — answers shadcn-specific implementation questions once `design-principles` has set intent. 201 MDX files organized under `vendor/`. Does not produce designs; routes general UI intent back to the orchestrator.

## Instructions

1. Identify the specific shadcn/ui component or feature from the user's question (component name, theming, framework install, dark mode, registry, forms, charts, RTL).
2. Read ONLY the relevant MDX file from `vendor/`: component pages live under `vendor/components/radix/<name>.mdx` (Radix-based) or `vendor/components/base/<name>.mdx` (Base UI); install guides under `vendor/installation/<framework>.mdx`.
3. Extract the install command, component source, and usage pattern from that single file.
4. If the question is cross-cutting (theming + a specific component), read the theming page plus the single component page only — never the whole directory.

Full reading strategy, docs-corpus map, activation rules, and detailed notes: see [usage-guide](./references/usage-guide.md).
> Position in flow · Trigger conditions · Activation · Prerequisites · Docs structure (vendor/) · Reading strategy (authoritative 4-step) · Non-negotiables · Error handling

## Prerequisites

- runtime_binaries: none (the docs are static MDX)
- Optional companion skill: [SKILL](../amw-tailwind-4/SKILL.md) — shadcn/ui is Tailwind-native
- Runtime peers (in the user's target project, not the plugin): Radix UI primitives, Tailwind CSS, React Hook Form + Zod (for forms), Recharts (for charts)

## Examples

**Input:** user asks "Show me the shadcn data-table component for Next.js."
**Output:** read `vendor/components/radix/data-table.mdx`, extract the install command (`npx shadcn@latest add data-table`), the component source TSX block, and the usage pattern. Hand back the three pieces without paraphrasing.

See `vendor/components/radix/data-table.mdx`, `vendor/forms/`, `vendor/dark-mode/next.mdx`, and `vendor/installation/next.mdx` for worked code examples per component, framework, and feature.

## Error Handling

Common failure modes and remediation: see [usage-guide](./references/usage-guide.md#error-handling). Summary: requested component missing from corpus → surface the gap rather than invent; user confuses shadcn/ui with another UI library → clarify it's a copy-paste recipe layer over Radix + Tailwind; outdated MDX snapshot → recommend consulting ui.shadcn.com.

## Output

This skill produces no standalone artifacts — it provides component source snippets and guidance. Any HTML/CSS output is assembled by `amw-ascii-to-html` or `amw-wireframe-builder-agent` using the shadcn component source extracted here.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator
- [SKILL](../amw-tailwind-4/SKILL.md) — Tailwind v4 reference pairs naturally with shadcn
- [color-system](../amw-design-principles/color-system.md) — shadcn uses CSS custom properties; align with design-principles' oklch structure where possible
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [SKILL](../amw-design-extract/SKILL.md) — extracted tokens from a shadcn-based site feed here
- [usage-guide](./references/usage-guide.md) — extended usage notes
  > Position in flow · Trigger conditions · Activation · Prerequisites · Docs structure (vendor/) · Reading strategy (authoritative 4-step) · Non-negotiables · Error handling
- `vendor/` — the full shadcn/ui documentation corpus (201 MDX)
