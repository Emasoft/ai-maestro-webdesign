---
name: amw-tailwind-4
description: Tailwind CSS v4 reference — utilities, variants, @theme, @utility/@custom-variant directives, PostCSS/CLI/Vite tooling, v3-to-v4 migration. Triggers on "tailwind v4", "tailwind config", "tailwind migration", "@theme", "@utility", "@apply", "@source", "@reference", "tailwind variants", "tailwind prefix". Does NOT trigger on generic "style my page", "CSS help", or framework-agnostic layout. Use when looking up Tailwind v4 classes, directives, or migration. Trigger with "tailwind v4" or "@theme".
---

# Tailwind CSS v4 Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Lazy-loaded reference corpus for Tailwind CSS v4. Covers utilities, variants, `@theme`/`@utility`/`@custom-variant`/`@source`/`@reference`/`@apply` directives, PostCSS/CLI/Vite tooling changes, browser compatibility, source-scanning behavior, and the complete v3 → v4 migration path. Two always-available reference files ([gotchas](references/gotchas.md) + [engineering-playbook](references/engineering-playbook.md)) cover the most common migration breakage points and component-abstraction ladder without needing a docs sync. Full authoritative answers require the synced MDX snapshot (`references/docs/`).
> [engineering-playbook.md] Default workflow · Core mindset · The abstraction ladder · What good reuse looks like · Tokens first · Arbitrary values · Custom utilities · Component classes · Variant strategy for component classes · `@apply` · Custom variants · Rich text and uncontrolled markup · Generated DOM and JS-replaced markup · Responsive strategy · File organization · Refactor heuristics · Review checklist · Practical defaults

## Instructions

1. Classify the user's question: migration, utility lookup, config/directive (`@theme`/`@utility`/`@custom-variant`/`@source`/`@reference`/`@apply`), variant, browser compatibility, or refactor/review.
2. Check whether `references/docs/` exists; if not, stop and ask the user to run the sync script (`scripts/sync_tailwind_docs.py --accept-docs-license`) before answering v4-specific questions from the synced snapshot.
3. For migration questions: read [gotchas](references/gotchas.md) first, then `<references/docs/upgrade-guide.mdx>` and `<references/docs/compatibility.mdx>`.
4. For implementation or review: read [engineering-playbook](references/engineering-playbook.md) first, then pull the specific utility/directive MDX only if needed.
> [engineering-playbook.md] Default workflow · Core mindset · The abstraction ladder · What good reuse looks like · Tokens first · Arbitrary values · Custom utilities · Component classes · Variant strategy for component classes · `@apply` · Custom variants · Rich text and uncontrolled markup · Generated DOM and JS-replaced markup · Responsive strategy · File organization · Refactor heuristics · Review checklist · Practical defaults
5. For a specific utility or variant: open the matching MDX file in `references/docs/` directly (e.g. `<references/docs/hover-focus-and-other-states.mdx>`).
6. Extract only the specific answer; do not reload the full snapshot.
7. If the snapshot is absent or stale and the user cannot sync, answer from [gotchas](references/gotchas.md) + [engineering-playbook](references/engineering-playbook.md) for common questions; for anything requiring authoritative doc text, stop and ask the user to sync rather than guessing.
> [engineering-playbook.md] Default workflow · Core mindset · The abstraction ladder · What good reuse looks like · Tokens first · Arbitrary values · Custom utilities · Component classes · Variant strategy for component classes · `@apply` · Custom variants · Rich text and uncontrolled markup · Generated DOM and JS-replaced markup · Responsive strategy · File organization · Refactor heuristics · Review checklist · Practical defaults

See `## Reading strategy` below.

## Output

This skill produces no standalone artifacts — it provides Tailwind v4 lookup answers, migration guidance, and code snippets. Any HTML/CSS output incorporating Tailwind classes is assembled by `amw-ascii-to-html` or `amw-wireframe-builder-agent`.

## Examples

See [gotchas](references/gotchas.md) for v3→v4 migration examples and [engineering-playbook](references/engineering-playbook.md) for `@theme` token design and `@apply` discipline patterns.
> [engineering-playbook.md] Default workflow · Core mindset · The abstraction ladder · What good reuse looks like · Tokens first · Arbitrary values · Custom utilities · Component classes · Variant strategy for component classes · `@apply` · Custom variants · Rich text and uncontrolled markup · Generated DOM and JS-replaced markup · Responsive strategy · File organization · Refactor heuristics · Review checklist · Practical defaults

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during **Phase B** when the target uses Tailwind v4, or pulled in by `shadcn-ui`. Callable directly on Tailwind v4 syntax / migration / directive questions. Skill's techniques are NOT limited to what matching commands expose.

## Position in flow

REFERENCE. Loaded when the orchestrator (or a sub-skill like `shadcn-ui`) needs authoritative Tailwind v4 guidance: migration, utility lookup, `@theme` tokens, custom variants, detection rules, or tooling changes.

## Trigger conditions

Invoke this skill when the question is specifically about Tailwind v4:

- migrating a v3 project to v4 (`@tailwind` directives, PostCSS plugin move, CLI move, Vite plugin)
- writing or reading `@theme`, `@utility`, `@custom-variant`, `@source`, `@reference`, `@apply` blocks
- disambiguating v3 vs v4 syntax (prefix placement, important modifier position, arbitrary CSS variable syntax, stacked variant order, transform reset utilities)
- looking up a specific utility, variant, or directive and confirming it exists / behaves as expected in v4
- checking browser support, detection rules, or source-scanning behavior

Do NOT invoke this skill for generic "style my page" requests, framework-agnostic CSS questions, or design-intent work — those belong to the orchestrator or to `design-principles` sub-skills (color-system, spacing-rhythm, typography-system).

## Prerequisites

- `runtime_binaries`: `python3`, `git`, network access (all three are required only for the first-use docs sync; after sync, this skill works fully offline).
- The full Tailwind v4 docs snapshot (~194 MDX files) is NOT bundled with this skill. The upstream repo at `https://github.com/tailwindlabs/tailwindcss.com` is source-available but not open-source, so the user must sync the snapshot locally and accept the upstream license.

## Setup (first use)

Before the first use of this skill, sync the Tailwind v4 docs snapshot into `references/docs/`:

```bash
# From the plugin root:
python3 skills/amw-tailwind-4/scripts/sync_tailwind_docs.py --accept-docs-license
```

This clones the tailwindcss.com repo (shallow), copies `src/docs/` into `references/docs/`, copies the docs sidebar index into `<references/docs-index.tsx>`, and writes commit metadata into `references/docs-source.txt`.

Optional flags:

- `--local-repo /path/to/tailwindcss.com` — reuse an existing local clone instead of cloning a temp copy.
- `--ref main` — pin to a different git ref.
- `--accept-docs-license` is **required**; the script refuses to run without it.

**License note:** the Tailwind docs are source-available, not open-source. Review `https://github.com/tailwindlabs/tailwindcss.com#license` before syncing and keep the snapshot local (never redistribute).

**Refresh cadence:** re-run the sync when the snapshot in `references/docs-source.txt` is more than a week old or when you need a recent Tailwind release's docs. Pass `--local-repo` to speed up repeat syncs.

## Structure

- [gotchas](references/gotchas.md) — v3 to v4 migration pitfalls, quick-scan list. Small and always available (does not need the sync).
- [engineering-playbook](references/engineering-playbook.md) — implementation / refactor / review guide covering the abstraction ladder, tokens, custom utilities, component classes, `@apply` discipline, responsive strategy, and review checklist. Always available (does not need the sync).
> [engineering-playbook.md] Default workflow · Core mindset · The abstraction ladder · What good reuse looks like · Tokens first · Arbitrary values · Custom utilities · Component classes · Variant strategy for component classes · `@apply` · Custom variants · Rich text and uncontrolled markup · Generated DOM and JS-replaced markup · Responsive strategy · File organization · Refactor heuristics · Review checklist · Practical defaults
- `references/docs-source.txt` — sync metadata (upstream repo, commit SHA, commit date, snapshot date). Ships with a pre-populated sentinel commit; gets overwritten by the sync script on each run.
- `references/docs/` — synced Tailwind v4 MDX snapshot. **Not present until the user runs the sync script.**
- `<references/docs-index.tsx>` — synced sidebar index mapping categories to doc slugs. **Not present until the user runs the sync script.**
- `scripts/sync_tailwind_docs.py` — the sync script itself.

## Reading strategy

When invoked:

1. Parse the user's question to classify it: migration, utility lookup, config/directive, variant, compatibility, review, or refactor.
2. Check whether `references/docs/` exists. If it does not, stop and ask the user to run the sync command from the Setup section — do not attempt to answer v4-specific docs questions from memory.
3. For migration questions: read [gotchas](references/gotchas.md) first (fast), then `<references/docs/upgrade-guide.mdx>` and `<references/docs/compatibility.mdx>` from the synced snapshot.
4. For implementation, refactor, or review: read [engineering-playbook](references/engineering-playbook.md) first, then pull the specific utility/directive doc only if needed.
> [engineering-playbook.md] Default workflow · Core mindset · The abstraction ladder · What good reuse looks like · Tokens first · Arbitrary values · Custom utilities · Component classes · Variant strategy for component classes · `@apply` · Custom variants · Rich text and uncontrolled markup · Generated DOM and JS-replaced markup · Responsive strategy · File organization · Refactor heuristics · Review checklist · Practical defaults
5. For a specific utility or variant: open the matching MDX file in `references/docs/` (for example `<references/docs/hover-focus-and-other-states.mdx>`, `<references/docs/theme.mdx>`, `<references/docs/functions-and-directives.mdx>`).
6. Treat MDX exports (`export const title`, `export const description`) as metadata. Treat JSX callouts (`<TipInfo>`, `<TipBad>`) as guidance text.
7. Extract the specific answer; do not reload the whole snapshot.

## Graceful degradation (when docs snapshot is absent or stale)

If the user is offline or cannot run the sync:

- [gotchas](references/gotchas.md) alone covers the most common v3 to v4 breakage points (directive move, PostCSS plugin rename, prefix syntax, important modifier placement, arbitrary CSS variable syntax, stacked variant order, transform reset utility names, `space-*`/`divide-*` selector change, `@theme` placement rules).
- [engineering-playbook](references/engineering-playbook.md) alone covers the abstraction ladder, when to create tokens vs utilities vs component classes, `@apply` discipline, and the review checklist.
> [engineering-playbook.md] Default workflow · Core mindset · The abstraction ladder · What good reuse looks like · Tokens first · Arbitrary values · Custom utilities · Component classes · Variant strategy for component classes · `@apply` · Custom variants · Rich text and uncontrolled markup · Generated DOM and JS-replaced markup · Responsive strategy · File organization · Refactor heuristics · Review checklist · Practical defaults
- For anything that requires authoritative doc text (exact utility flag names, exact variant syntax, full upgrade-guide steps), stop and ask the user to sync the docs rather than guessing.

## Resources

- [SKILL](../amw-shadcn-ui/SKILL.md) — shadcn/ui ships Tailwind-based components; migration and `@theme` token design should stay aligned.
- [color-system](../amw-design-principles/color-system.md) — the oklch token approach can be expressed as `@theme` variables (`--color-*`) auto-promoted into utilities.
> [color-system.md] I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [spacing-rhythm](../amw-design-principles/spacing-rhythm.md) — Tailwind's spacing scale (`--spacing-*`) aligns with the 8pt grid.
> [spacing-rhythm.md] I. 8pt grid system · II. Fibonacci spacing rhythm (large-scale) · III. Vertical rhythm (baseline grid) · IV. Hit targets (tappable areas) · V. Alignment · VI. Three principles of whitespace · VII. Border radius · VIII. Shadow system · IX. Self-check
- [typography-system](../amw-design-principles/typography-system.md) — Tailwind's type scale (`--text-*`, `--font-*`) maps to the typography tokens documented there.
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)

## Non-negotiables

- Does NOT own broad design intent. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether Tailwind is the right execution surface; this skill only answers Tailwind-specific questions.
- Docs under `references/docs/` are reference-only: never edit the synced MDX files. If they look wrong, re-sync — do not patch.
- Never paraphrase utility names, directive names, or breaking-change lists from memory. Either the synced docs confirm it or the skill asks for a re-sync.
- The sync command is the single source of truth for docs freshness. When a Tailwind v4 release changes behavior, the fix is to re-run sync, not to edit this SKILL.md.
- English-only content across the skill. No third-language characters in any file.

## Error Handling

- **Sync fails (network/git error):** report the exact command and error to the user; fall back to [gotchas](references/gotchas.md) + [engineering-playbook](references/engineering-playbook.md) for non-doc-lookup questions.
> [engineering-playbook.md] Default workflow · Core mindset · The abstraction ladder · What good reuse looks like · Tokens first · Arbitrary values · Custom utilities · Component classes · Variant strategy for component classes · `@apply` · Custom variants · Rich text and uncontrolled markup · Generated DOM and JS-replaced markup · Responsive strategy · File organization · Refactor heuristics · Review checklist · Practical defaults
- **Upstream repo structure changes (docs moved out of `src/docs/`):** the sync script raises a clear error; update `scripts/sync_tailwind_docs.py` and re-test. Do not silently adapt to stale paths.
- **User asks a v3-specific question:** answer from [gotchas](references/gotchas.md) (v3→v4 deltas) and note that v3 docs are outside this skill's scope.
- **Offline environment, docs not synced:** acknowledge the constraint, answer what `gotchas.md` + `engineering-playbook.md` cover, and defer authoritative utility lookups until the user can sync.
- **User asks about a post-snapshot Tailwind release:** re-run the sync and retry. If the release is so recent that upstream docs lag, say so instead of guessing.
