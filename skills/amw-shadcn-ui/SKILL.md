---
name: amw-shadcn-ui
description: shadcn/ui component usage, theming, forms, charts, and framework integration (Next.js / Vite / Remix / Astro / Laravel / Gatsby). Triggers on "shadcn component", "data-table", "shadcn form", "shadcn theme", "dark mode for shadcn", "install shadcn", registry questions, accessibility of Radix-based components, NOT generic "UI library" or "React component". Use when selecting, theming, or integrating a shadcn/ui component into a project. Trigger with explicit "shadcn" phrasing or component name.
version: 0.1.0
---

# shadcn/ui Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Lazy-loaded documentation corpus covering 50+ shadcn/ui components, theming, forms, charts, dark mode, registry, RTL, and per-framework installation (Next.js, Vite, Remix, Astro, Laravel, Gatsby). Reference-only skill — answers shadcn-specific implementation questions once `design-principles` has set intent. 201 MDX files organized under `docs/`. Does not produce designs; routes general UI intent back to the orchestrator.

## Instructions

1. Identify the specific shadcn/ui component or feature from the user's question (component name, theming, framework install, dark mode, registry, forms, charts, RTL).
2. Read ONLY the relevant MDX file from `docs/`: component pages live under `docs/components/radix/<name>.mdx` (Radix-based) or `docs/components/base/<name>.mdx` (Base UI); install guides under `docs/installation/<framework>.mdx`.
3. Extract the install command, component source, and usage pattern from that single file.
4. If the question is cross-cutting (theming + a specific component), read the theming page plus the single component page only — never the whole directory.

See the `## Reading strategy` section below for the authoritative 4-step approach to loading only the relevant MDX file.

## Examples

See `docs/components/radix/data-table.mdx`, `docs/forms/`, `docs/dark-mode/next.mdx`, and `docs/installation/next.mdx` for worked code examples per component, framework, and feature.

## Output

This skill produces no standalone artifacts — it provides component source snippets and guidance. Any HTML/CSS output is assembled by `amw-ascii-to-html` or `amw-wireframe-builder-agent` using the shadcn component source extracted here.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when extracted design tokens or explicit user request indicate a shadcn/ui-based implementation target. Also callable directly when the user names a specific shadcn component, theming question, or registry workflow.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

REFERENCE. Lazy-loaded docs corpus (201 MDX); answers shadcn-specific implementation questions once design-principles has set intent.

## Trigger conditions

Activates when the user explicitly names shadcn/ui, when extracted tokens (from /amw-extract-style) indicate a shadcn-based target, or when the user asks about a component by its shadcn identifier (data-table, dropdown-menu, sheet, toast, etc.). General "how do I build a UI" goes to design-principles / ascii-sketch.

## Prerequisites
- runtime_binaries: none (the docs are static MDX)
- Optional companion skill: [SKILL](../amw-tailwind-4/SKILL.md) — shadcn/ui is Tailwind-native
- Runtime peers (in the user's target project, not the plugin): Radix UI primitives, Tailwind CSS, React Hook Form + Zod (for forms), Recharts (for charts)

## Docs structure (docs/)
- `docs/installation/` — per-framework install guides (Next.js, Vite, Remix, Astro, Laravel, Gatsby, TanStack Start, manual)
- `docs/components/` — 50+ component guides documented across the 201 MDX files in this corpus, split into two variant roots: `docs/components/radix/` (Radix-primitive-based) and `docs/components/base/` (Base UI variant). For the authoritative component-slug list, list `docs/components/radix/` and `docs/components/base/` at runtime; the slug = the MDX filename without extension (e.g. `data-table.mdx` → component "data-table").
- `docs/forms/` — Form + Zod schemas, validation, accessibility patterns
- `docs/dark-mode/` — dark-mode recipes per framework (Next.js, Vite, Remix, Astro)
- `docs/registry/` — registry schema, namespacing, custom component publishing
- `docs/rtl/` — right-to-left layout guidance
- `docs/changelog/` — version history
- `docs/(root)/` — top-level pages (theming, CLI, monorepo, MCP, JavaScript usage, v4 migration, etc.)

## Reading strategy

Input: a user question naming a specific shadcn component / feature / framework. Output: install command + component source + usage pattern, extracted from a single MDX file.

1. Identify the component / feature from the question.
2. Read ONLY the relevant MDX (e.g. `docs/components/radix/data-table.mdx`, `docs/installation/next.mdx`, `docs/dark-mode/next.mdx`).
3. Extract install command, component source, usage pattern.
4. Cross-cutting (theming + component): read theming page + single component page only.

## Resources
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator
- [SKILL](../amw-tailwind-4/SKILL.md) — Tailwind v4 reference pairs naturally with shadcn
- [color-system](../amw-design-principles/color-system.md) — shadcn uses CSS custom properties; align with design-principles' oklch structure where possible
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [SKILL](../amw-design-extract/SKILL.md) — extracted tokens from a shadcn-based site feed here
- `docs/` — the full shadcn/ui documentation corpus (201 MDX)

## Non-negotiables
- Does NOT claim generic design / UI work — design-principles orchestrates general design intent; this skill answers shadcn-specific questions.
- Docs are read-only; do not modify the MDX files.
- When emitting shadcn component source, use the copy-paste CLI pattern (install via `npx shadcn@latest add <component>`), not npm-imported monolithic components.

## Error Handling
- Requested component is not in the docs corpus — surface the gap rather than invent.
- Framework-specific question outside the installation guides (e.g. SolidStart, SvelteKit) — defer to design-principles or the user.
- User confuses shadcn/ui with Material UI / Chakra / Radix UI primitives directly — clarify that shadcn/ui is a copy-paste recipe layer on top of Radix + Tailwind, not an npm component library.
- Outdated MDX vs. a newer upstream release — acknowledge the docs snapshot date and recommend consulting ui.shadcn.com for post-snapshot changes.
