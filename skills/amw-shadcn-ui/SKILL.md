---
name: amw-shadcn-ui
description: shadcn/ui component usage, theming, forms, charts, and framework integration (Next.js / Vite / Remix / Astro / Laravel / Gatsby). Triggers on "shadcn component", "data-table", "shadcn form", "shadcn theme", "dark mode for shadcn", "install shadcn", registry questions, accessibility of Radix-based components, NOT generic "UI library" or "React component".
version: 0.1.0
---

# shadcn/ui Reference

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when extracted design tokens or explicit user request indicate a shadcn/ui-based implementation target. Also callable directly when the user names a specific shadcn component, theming question, or registry workflow.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow
REFERENCE. Lazy-loaded documentation corpus of 201 MDX files covering 50+ components, theming, forms, charts, accessibility, registry, and framework installation guides. Does not produce designs — answers shadcn-specific implementation questions once design-principles has set intent.

## Trigger conditions
Specific shadcn/ui questions. The orchestrator routes general "how do I build a UI" to the design-principles / ascii-sketch pipeline; this skill only activates when the user explicitly names shadcn/ui, or when extracted tokens (from /amw-extract-style) indicate a shadcn-based target, or when the user asks about a component by its shadcn identifier (e.g. "data-table", "dropdown-menu", "sheet", "toast").

## Dependencies
- runtime_binaries: none (the docs are static MDX)
- Optional companion skill: `../amw-tailwind-4/SKILL.md` — shadcn/ui is Tailwind-native
- Runtime peers (in the user's target project, not the plugin): Radix UI primitives, Tailwind CSS, React Hook Form + Zod (for forms), Recharts (for charts)

## Docs structure (docs/)
- `docs/installation/` — per-framework install guides (Next.js, Vite, Remix, Astro, Laravel, Gatsby, TanStack Start, manual)
- `docs/components/` — 50+ component guides documented across the 201 MDX files in this corpus, split into two variant roots: `docs/components/radix/` (Radix-primitive-based) and `docs/components/base/` (Base UI variant). Enumerated component slugs (snapshot — see `docs/components/` for the authoritative list as the snapshot may include newer components): accordion, alert, alert-dialog, avatar, badge, breadcrumb, button, calendar, card, carousel, checkbox, collapsible, combobox, command, context-menu, data-table, date-picker, dialog, drawer, dropdown-menu, form, hover-card, input, input-otp, label, menubar, navigation-menu, pagination, popover, progress, radio-group, resizable, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, switch, table, tabs, textarea, toast, toggle, toggle-group, tooltip, typography, etc.
- `docs/forms/` — Form + Zod schemas, validation, accessibility patterns
- `docs/dark-mode/` — dark-mode recipes per framework (Next.js, Vite, Remix, Astro)
- `docs/registry/` — registry schema, namespacing, custom component publishing
- `docs/rtl/` — right-to-left layout guidance
- `docs/changelog/` — version history
- `docs/(root)/` — top-level pages (theming, CLI, monorepo, MCP, JavaScript usage, v4 migration, etc.)

## Reading strategy
Do NOT load the entire docs/ corpus. When invoked:
1. Identify the specific component / feature from the user's question.
2. Read ONLY the relevant MDX file. Component pages live under the two variant roots — `docs/components/radix/<name>.mdx` (Radix-primitive-based variant) or `docs/components/base/<name>.mdx` (Base UI variant). Example: `docs/components/radix/data-table.mdx`, `docs/installation/next.mdx`, `docs/dark-mode/next.mdx`.
3. Extract the install command, component source, and usage pattern.
4. If the question is cross-cutting (theming + a specific component), read the theming page plus the single component page — never the whole directory.

## Cross-references
- `../amw-design-principles/SKILL.md` — orchestrator
- `../amw-tailwind-4/SKILL.md` — Tailwind v4 reference pairs naturally with shadcn
- `../amw-design-principles/color-system.md` — shadcn uses CSS custom properties; align with design-principles' oklch structure where possible
- `../amw-design-extract/SKILL.md` — extracted tokens from a shadcn-based site feed here
- `docs/` — the full shadcn/ui documentation corpus (201 MDX)

## Non-negotiables
- Does NOT claim generic design / UI work — design-principles orchestrates general design intent; this skill answers shadcn-specific questions.
- Docs are read-only; do not modify the MDX files.
- When emitting shadcn component source, use the copy-paste CLI pattern (install via `npx shadcn@latest add <component>`), not npm-imported monolithic components.

## Failure modes
- Requested component is not in the docs corpus — surface the gap rather than invent.
- Framework-specific question outside the installation guides (e.g. SolidStart, SvelteKit) — defer to design-principles or the user.
- User confuses shadcn/ui with Material UI / Chakra / Radix UI primitives directly — clarify that shadcn/ui is a copy-paste recipe layer on top of Radix + Tailwind, not an npm component library.
- Outdated MDX vs. a newer upstream release — acknowledge the docs snapshot date and recommend consulting ui.shadcn.com for post-snapshot changes.
