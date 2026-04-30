---
name: amw-tailwind-4
description: Tailwind CSS v4 reference — utilities, variants, @theme blocks, @utility/@custom-variant directives, PostCSS/CLI/Vite tooling changes, and v3 to v4 migration. Triggers on "tailwind v4", "tailwind 4", "tailwind config", "tailwind migration", "upgrade tailwind", "@theme", "@utility", "@apply", "@source", "@reference", "tailwind variants", "tailwind prefix", "arbitrary value", "tailwind breakpoint". Does NOT trigger on generic "style my page", "CSS help", or framework-agnostic layout questions — the orchestrator routes those elsewhere.
version: 0.1.0
---

# Tailwind CSS v4 Reference

> **Orchestrated by:** `../amw-design-principles/SKILL.md`. This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when the implementation target uses Tailwind CSS v4, or pulled in by `shadcn-ui` for Tailwind-specific questions. Also callable directly when the user names Tailwind v4 syntax, migration, or directive questions.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

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

## Dependencies

- `runtime_binaries`: `python3`, `git`, network access (all three are required only for the first-use docs sync; after sync, this skill works fully offline).
- The full Tailwind v4 docs snapshot (~194 MDX files) is NOT bundled with this skill. The upstream repo `tailwindlabs/tailwindcss.com` is source-available but not open-source, so the user must sync the snapshot locally and accept the upstream license.

## Setup (first use)

Before the first use of this skill, sync the Tailwind v4 docs snapshot into `references/docs/`:

```bash
# From the plugin root:
python3 skills/amw-tailwind-4/scripts/sync_tailwind_docs.py --accept-docs-license
```

This clones `tailwindlabs/tailwindcss.com` (shallow), copies `src/docs/` into `references/docs/`, copies the docs sidebar index into `references/docs-index.tsx`, and writes commit metadata into `references/docs-source.txt`.

Optional flags:

- `--local-repo /path/to/tailwindcss.com` — reuse an existing local clone instead of cloning a temp copy.
- `--ref main` — pin to a different git ref.
- `--accept-docs-license` is **required**; the script refuses to run without it.

**License note:** the Tailwind docs are source-available, not open-source. Review `https://github.com/tailwindlabs/tailwindcss.com#license` before syncing and keep the snapshot local (never redistribute).

**Refresh cadence:** re-run the sync when the snapshot in `references/docs-source.txt` is more than a week old or when you need a recent Tailwind release's docs. Pass `--local-repo` to speed up repeat syncs.

## Structure

- `references/gotchas.md` — v3 to v4 migration pitfalls, quick-scan list. Small and always available (does not need the sync).
- `references/engineering-playbook.md` — implementation / refactor / review guide covering the abstraction ladder, tokens, custom utilities, component classes, `@apply` discipline, responsive strategy, and review checklist. Always available (does not need the sync).
- `references/docs-source.txt` — sync metadata (upstream repo, commit SHA, commit date, snapshot date). Ships with a pre-populated sentinel commit; gets overwritten by the sync script on each run.
- `references/docs/` — synced Tailwind v4 MDX snapshot. **Not present until the user runs the sync script.**
- `references/docs-index.tsx` — synced sidebar index mapping categories to doc slugs. **Not present until the user runs the sync script.**
- `scripts/sync_tailwind_docs.py` — the sync script itself.

## Reading strategy

When invoked:

1. Parse the user's question to classify it: migration, utility lookup, config/directive, variant, compatibility, review, or refactor.
2. Check whether `references/docs/` exists. If it does not, stop and ask the user to run the sync command from the Setup section — do not attempt to answer v4-specific docs questions from memory.
3. For migration questions: read `references/gotchas.md` first (fast), then `references/docs/upgrade-guide.mdx` and `references/docs/compatibility.mdx` from the synced snapshot.
4. For implementation, refactor, or review: read `references/engineering-playbook.md` first, then pull the specific utility/directive doc only if needed.
5. For a specific utility or variant: open the matching MDX file in `references/docs/` (for example `references/docs/hover-focus-and-other-states.mdx`, `references/docs/theme.mdx`, `references/docs/functions-and-directives.mdx`).
6. Treat MDX exports (`export const title`, `export const description`) as metadata. Treat JSX callouts (`<TipInfo>`, `<TipBad>`) as guidance text.
7. Extract the specific answer; do not reload the whole snapshot.

## Graceful degradation (when docs snapshot is absent or stale)

If the user is offline or cannot run the sync:

- `references/gotchas.md` alone covers the most common v3 to v4 breakage points (directive move, PostCSS plugin rename, prefix syntax, important modifier placement, arbitrary CSS variable syntax, stacked variant order, transform reset utility names, `space-*`/`divide-*` selector change, `@theme` placement rules).
- `references/engineering-playbook.md` alone covers the abstraction ladder, when to create tokens vs utilities vs component classes, `@apply` discipline, and the review checklist.
- For anything that requires authoritative doc text (exact utility flag names, exact variant syntax, full upgrade-guide steps), stop and ask the user to sync the docs rather than guessing.

## Cross-references

- `../amw-shadcn-ui/SKILL.md` — shadcn/ui ships Tailwind-based components; migration and `@theme` token design should stay aligned.
- `../amw-design-principles/color-system.md` — the oklch token approach in design-principles can be expressed as `@theme` variables (`--color-*`) that Tailwind v4 auto-promotes into utilities.
- `../amw-design-principles/spacing-rhythm.md` — Tailwind's spacing scale (`--spacing-*`) aligns with the 8pt grid used by design-principles.
- `../amw-design-principles/typography-system.md` — Tailwind's type scale (`--text-*`, `--font-*`) maps to the typography tokens documented there.

## Non-negotiables

- Does NOT own broad design intent. The orchestrator (`../amw-design-principles/SKILL.md`) decides whether Tailwind is the right execution surface; this skill only answers Tailwind-specific questions.
- Docs under `references/docs/` are reference-only: never edit the synced MDX files. If they look wrong, re-sync — do not patch.
- Never paraphrase utility names, directive names, or breaking-change lists from memory. Either the synced docs confirm it or the skill asks for a re-sync.
- The sync command is the single source of truth for docs freshness. When a Tailwind v4 release changes behavior, the fix is to re-run sync, not to edit this SKILL.md.
- English-only content across the skill. No third-language characters in any file.

## Failure modes

- **Sync fails (network/git error):** report the exact command and error to the user; fall back to `references/gotchas.md` + `references/engineering-playbook.md` for non-doc-lookup questions.
- **Upstream repo structure changes (docs moved out of `src/docs/`):** the sync script raises a clear error; update `scripts/sync_tailwind_docs.py` and re-test. Do not silently adapt to stale paths.
- **User asks a v3-specific question:** answer from `references/gotchas.md` (v3→v4 deltas) and note that v3 docs are outside this skill's scope.
- **Offline environment, docs not synced:** acknowledge the constraint, answer what `gotchas.md` + `engineering-playbook.md` cover, and defer authoritative utility lookups until the user can sync.
- **User asks about a post-snapshot Tailwind release:** re-run the sync and retry. If the release is so recent that upstream docs lag, say so instead of guessing.
