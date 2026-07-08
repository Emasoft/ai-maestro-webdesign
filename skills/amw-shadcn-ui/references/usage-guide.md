# shadcn/ui — Usage Guide (extended)

Routing surface and quick instructions live in the parent `SKILL.md`. This reference holds the docs-corpus map, reading strategy, activation rules, prerequisites, and error-handling notes that previously sat inline.

## Table of Contents

- [Position in flow](#position-in-flow)
- [Trigger conditions](#trigger-conditions)
- [Activation](#activation)
- [Prerequisites](#prerequisites)
- [Docs structure (vendor/)](#docs-structure-vendor)
- [Reading strategy (authoritative 4-step)](#reading-strategy-authoritative-4-step)
- [Non-negotiables](#non-negotiables)
- [Error handling](#error-handling)

## Position in flow

REFERENCE. Lazy-loaded docs corpus (201 MDX); answers shadcn-specific implementation questions once design-principles has set intent.

## Trigger conditions

Activates when the user explicitly names shadcn/ui, when extracted tokens (from `/amw-extract-style`) indicate a shadcn-based target, or when the user asks about a component by its shadcn identifier (data-table, dropdown-menu, sheet, toast, etc.). General "how do I build a UI" goes to design-principles / ascii-sketch.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when extracted design tokens or explicit user request indicate a shadcn/ui-based implementation target. Also callable directly when the user names a specific shadcn component, theming question, or registry workflow.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Prerequisites

- runtime_binaries: none (the docs are static MDX)
- Optional companion skill: `../amw-tailwind-4/SKILL.md` — shadcn/ui is Tailwind-native
- Runtime peers (in the user's target project, not the plugin): Radix UI primitives, Tailwind CSS, React Hook Form + Zod (for forms), Recharts (for charts)

## Docs structure (vendor/)

- `vendor/installation/` — per-framework install guides (Next.js, Vite, Remix, Astro, Laravel, Gatsby, TanStack Start, manual)
- `vendor/components/` — 50+ component guides documented across the 201 MDX files in this corpus, split into two variant roots: `vendor/components/radix/` (Radix-primitive-based) and `vendor/components/base/` (Base UI variant). For the authoritative component-slug list, list `vendor/components/radix/` and `vendor/components/base/` at runtime; the slug = the MDX filename without extension (e.g. `data-table.mdx` → component "data-table").
- `vendor/forms/` — Form + Zod schemas, validation, accessibility patterns
- `vendor/dark-mode/` — dark-mode recipes per framework (Next.js, Vite, Remix, Astro)
- `vendor/registry/` — registry schema, namespacing, custom component publishing
- `vendor/rtl/` — right-to-left layout guidance
- `vendor/changelog/` — version history
- `vendor/(root)/` — top-level pages (theming, CLI, monorepo, MCP, JavaScript usage, v4 migration, etc.)

## Reading strategy (authoritative 4-step)

Input: a user question naming a specific shadcn component / feature / framework.
Output: install command + component source + usage pattern, extracted from a single MDX file.

1. Identify the component / feature from the question.
2. Read ONLY the relevant MDX (e.g. `vendor/components/radix/data-table.mdx`, `vendor/installation/next.mdx`, `vendor/dark-mode/next.mdx`).
3. Extract install command, component source, usage pattern.
4. Cross-cutting (theming + component): read theming page + single component page only.

## Non-negotiables

- Does NOT claim generic design / UI work — design-principles orchestrates general design intent; this skill answers shadcn-specific questions.
- Docs are read-only; do not modify the MDX files.
- When emitting shadcn component source, use the copy-paste CLI pattern (install via `npx shadcn@latest add <component>`), not npm-imported monolithic components.

## Error handling

- Requested component is not in the docs corpus — surface the gap rather than invent.
- Framework-specific question outside the installation guides (e.g. SolidStart, SvelteKit) — defer to design-principles or the user.
- User confuses shadcn/ui with Material UI / Chakra / Radix UI primitives directly — clarify that shadcn/ui is a copy-paste recipe layer on top of Radix + Tailwind, not an npm component library.
- Outdated MDX vs. a newer upstream release — acknowledge the docs snapshot date and recommend consulting ui.shadcn.com for post-snapshot changes.
