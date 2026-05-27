---
name: TECH-registry-lookup
category: shadcn-ui-registry
source: shadcn-ui official registry documentation (https://ui.shadcn.com/docs/registry); synthesized for plugin from MIT-licensed sources
license: MIT (plugin license)
also-in: globalCC skill `tailwindcss`; `react` for the consuming components
---

# shadcn registry lookup — finding and adding custom variants

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [The official 50+ components vs. registry variants](#the-official-50-components-vs-registry-variants)
- [The `pnpm dlx shadcn@latest add <variant-url>` pattern](#the-pnpm-dlx-shadcnlatest-add-variant-url-pattern)
- [Custom registry config in `components.json`](#custom-registry-config-in-componentsjson)
- [Evaluating community variants for plugin-relevance](#evaluating-community-variants-for-plugin-relevance)
- [Common community registries](#common-community-registries)
- [Safety checklist before adding a registry component](#safety-checklist-before-adding-a-registry-component)
- [Cross-references](#cross-references)

## What it does

Documents how the shadcn CLI installs **custom variants** that extend beyond the 50+ default components. The shadcn registry is an OpenAPI-style HTTP endpoint that returns a manifest describing the files, dependencies, and Tailwind config a component needs. The CLI fetches the manifest, copies source files into the consumer project at `components/ui/`, and updates `components.json` to track what was installed.

This reference is for the agent and the user when the standard 50+ shadcn components do not cover the design's needs — e.g., a multi-select combobox, a date-range picker with timezone support, a rich-text editor, a kanban board, a sortable data table. Many community-maintained registries expose these as drop-in shadcn variants.

## When to use

- The wireframe-builder agent or the component-library-architect agent needs a component the default shadcn catalog does not ship (date-range, time-picker, multi-select, file-uploader-with-progress, code-editor, kanban, scheduler, charts beyond Recharts wrappers, command-palette extensions).
- The user explicitly asks to install a shadcn variant they found in a tweet, a blog post, or a third-party registry.
- The agent is evaluating whether a community variant is safe to adopt, or whether to author a new component from primitives.

## The official 50+ components vs. registry variants

The default shadcn registry (`https://ui.shadcn.com/r/styles/default`) ships ~50 components covering most general-purpose UI needs — accordion, alert, avatar, badge, button, card, carousel, chart, checkbox, collapsible, combobox, command, context-menu, dialog, dropdown-menu, form, hover-card, input, label, menubar, navigation-menu, pagination, popover, progress, radio-group, resizable, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, switch, table, tabs, textarea, toast, toggle, toggle-group, tooltip, breadcrumb, calendar, drawer, input-otp, aspect-ratio, and a few more.

**Components NOT in the default registry** (must come from custom registries or be authored from primitives):
- Date-range picker (the default `calendar` is single-date)
- Time picker, datetime picker with timezone
- Multi-select with chips/tags
- Rich-text editor (markdown / WYSIWYG)
- File uploader with progress
- Kanban board (drag-and-drop columns)
- Tree view (hierarchical list with expand/collapse)
- Image cropper
- Color picker (use `amw-react-colorful` instead — already in this plugin)
- Code editor (Monaco / CodeMirror wrappers)
- Spreadsheet / grid
- Mention input (@-mentions with autocomplete)
- Phone-number input with country selector
- Credit-card input with brand detection

For any of those, the user has three options:
1. **Find a community registry variant** (this reference).
2. **Compose from Radix primitives** (`@radix-ui/react-*`) and Tailwind styles directly.
3. **Use a non-shadcn library** wrapped to match the shadcn design tokens (e.g., `react-day-picker` + custom shadcn-themed wrapper for date-range).

## The `pnpm dlx shadcn@latest add <variant-url>` pattern

The shadcn CLI accepts a registry component URL as the `add` argument. The URL points to a JSON manifest the registry serves.

**Default registry component (using the short name):**

```bash
pnpm dlx shadcn@latest add button card dialog
# Equivalent to:
pnpm dlx shadcn@latest add https://ui.shadcn.com/r/styles/default/button.json
```

**Custom registry component (using the full URL):**

```bash
pnpm dlx shadcn@latest add https://magicui.design/r/marquee.json
pnpm dlx shadcn@latest add https://shadcnui-expansions.typeart.cc/r/multi-select.json
pnpm dlx shadcn@latest add https://originui.com/r/calendar-with-time.json
```

The CLI:
1. Fetches the JSON manifest.
2. Validates the schema (`shadcn` registry schema version 1).
3. For each file in the manifest, copies it into the configured destination (`components/ui/` or the path declared by the manifest).
4. For each `dependencies` entry, runs the package manager install.
5. For each `registryDependencies` entry, recursively fetches and installs (e.g., a multi-select that depends on `command` and `popover` pulls those in if missing).
6. Updates `components.json` to record what was installed.

**npm / yarn / bun equivalents:**

```bash
npx shadcn@latest add <url>
yarn dlx shadcn@latest add <url>
bunx shadcn@latest add <url>
```

## Custom registry config in `components.json`

To configure a project to look up component **short names** in a custom registry (instead of full URLs every time), add a `registries` field to `components.json`:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "registries": {
    "@magic-ui": "https://magicui.design/r/{name}.json",
    "@expansions": "https://shadcnui-expansions.typeart.cc/r/{name}.json",
    "@origin": "https://originui.com/r/{name}.json"
  }
}
```

After this config exists, the user can install short-named components from the custom registries:

```bash
pnpm dlx shadcn@latest add @magic-ui/marquee
pnpm dlx shadcn@latest add @expansions/multi-select
pnpm dlx shadcn@latest add @origin/calendar-with-time
```

The CLI substitutes `{name}` into the registry URL template and fetches as usual.

## Evaluating community variants for plugin-relevance

Before the wireframe-builder agent adds a community variant to a generated project, it MUST evaluate the variant against three signals:

### 1. License signal

- **MIT, Apache-2.0, BSD-3-Clause, ISC** — safe to include in plugin-generated output.
- **GPL-2.0, GPL-3.0, AGPL, SSPL** — copyleft; the variant cannot be added to a project the agent is generating if the project itself is not GPL-compatible. The agent declines and explains.
- **No license** or **proprietary** — decline; the agent does not install code without an explicit license grant.
- **CC-BY-NC / non-commercial** — decline for commercial projects; ask the user.

The variant's repository (linked from the registry manifest) MUST contain a `LICENSE` or `LICENSE.md` file. Variants with no license are NOT acceptable, even if they look correct.

### 2. Test signal

The variant repository SHOULD have:
- A `tests/` directory or test files alongside source (`*.test.tsx`, `*.spec.tsx`).
- A CI workflow that runs tests on PR.
- At least one published version (a recent commit count > 1 is the minimum acceptable signal).

A variant with no tests, no CI, and one commit is **toy-grade**, not production-grade. The agent flags this and offers two alternatives: (a) install with a warning, (b) author the component from primitives instead.

### 3. Maintenance signal

- Last commit within the last 12 months → actively maintained.
- 12-24 months → low maintenance; check for open issues / unaddressed PRs; usually acceptable for stable components.
- > 24 months stale → likely abandoned; do not install without confirming the variant still works against current shadcn / Radix versions.

The agent reports the three signals as a one-line summary before installing:

```
Variant: @expansions/multi-select
License: MIT  Tests: 14 specs  Last commit: 6 weeks ago  Stars: 1.4k
→ Safe to install.
```

If any signal is red, the agent does NOT install silently; it surfaces the conflict to main-agent for user confirmation.

## Common community registries

A non-exhaustive list of community shadcn registries the plugin has seen used in practice. The list is descriptive, not endorsing — the agent applies the safety checklist above to every entry regardless of popularity.

| Registry | URL pattern | Specialty |
|---|---|---|
| **Magic UI** | `https://magicui.design/r/{name}.json` | Animated components (marquee, particles, blur-fade, ripple) |
| **shadcn/ui expansions** | `https://shadcnui-expansions.typeart.cc/r/{name}.json` | Variants of default components (multi-select, infinite-scroll, autocomplete) |
| **Origin UI** | `https://originui.com/r/{name}.json` | Date/time pickers, calendar variants, form components |
| **Aceternity UI** | `https://ui.aceternity.com/registry/{name}.json` | Marketing-page animated components (3D cards, beams, lamp) |
| **Tremor** | `https://tremor.so/r/{name}.json` | Dashboard / chart primitives |
| **CredoUI** | (varies) | Auth flows, billing screens |

Each registry maintains its own component schema. The CLI handles the differences via the manifest format; the agent does not need to know per-registry quirks.

## Safety checklist before adding a registry component

The agent (typically `amw-wireframe-builder-agent` or `amw-component-library-architect-agent`) runs this checklist before any `shadcn@latest add <url>` call:

- [ ] The variant URL resolves and returns valid JSON matching the shadcn registry schema.
- [ ] The variant's source repository is linked and contains a `LICENSE` file with an OSS-compatible license.
- [ ] The variant has tests or a stated test-coverage status; if neither, the agent surfaces "this variant is not production-tested" to the user.
- [ ] The variant's last commit is within 24 months.
- [ ] The variant's dependencies (in the manifest) are all OSS-licensed and current (no peer-dep conflict with the project's React / Radix / Tailwind versions).
- [ ] The variant's design tokens are compatible with the project's `globals.css` color variables. If the variant ships its own color palette, the agent confirms with the user before letting it override the project's tokens.
- [ ] After install, the agent runs `npm run typecheck` (or project equivalent) and confirms zero new errors.

Failing any check means the agent EITHER installs with explicit warning surfaced to main-agent, OR declines and offers an alternative (compose from primitives; pick a different registry; ask the user to vet manually).

## Cross-references

- [SKILL.md](../SKILL.md) — shadcn-ui top-level skill; routes here when registry lookup is needed
- [skills/amw-shadcn-ui/references/usage-guide.md](./usage-guide.md) — non-registry usage of the default 50+ components
- [agents/amw-wireframe-builder-agent.md](../../../agents/amw-wireframe-builder-agent.md) — agent that consumes this reference when picking variants
- [agents/amw-component-library-architect-agent.md](../../../agents/amw-component-library-architect-agent.md) — Tier-4 specialist that owns design-token alignment when registry variants ship their own tokens
- [skills/amw-tailwind-4/SKILL.md](../../amw-tailwind-4/SKILL.md) — Tailwind v4 reference for the CSS variables the variants must align with
- Official shadcn registry docs: `https://ui.shadcn.com/docs/registry`
