# Drift detection procedure — amw-skill-drift-audit

## Table of Contents

- [Phase 0 — Resolve plugin root and inventory skills](#phase-0-resolve-plugin-root-and-inventory-skills)
- [Phase 1 — Source-map resolution](#phase-1-source-map-resolution)
- [Phase 2 — Per-upstream HEAD lookup](#phase-2-per-upstream-head-lookup)
- [Phase 3 — Diff per pin](#phase-3-diff-per-pin)
- [Phase 4 — Classification](#phase-4-classification)
- [Phase 5 — Diff summary for STALE skills](#phase-5-diff-summary-for-stale-skills)
- [Phase 6 — Emit the plan](#phase-6-emit-the-plan)
- [Phase 7 — Self-test (optional, on demand)](#phase-7-self-test-optional-on-demand)
- [Anti-patterns (don't do)](#anti-patterns-dont-do)

Detailed algorithm. Read top-to-bottom; each phase depends on the previous. The audit is purely read-only — no git writes, no skill edits.

## Phase 0 — Resolve plugin root and inventory skills

1. Find the plugin root — the directory containing `.claude-plugin/plugin.json`. If invoked from a subdirectory, walk parents until found. Refuse if no plugin manifest exists (`amw-skill-drift-audit` operates only on Claude Code plugins, not arbitrary repos).
2. Glob `skills/*/SKILL.md` from the plugin root. For each match, parse YAML frontmatter into `(name, source, source_version)` — `source` is a list of upstream paths, `source_version` is a commit SHA string.
3. **UNPINNED detection** — a skill missing EITHER `source:` OR `source_version:` from frontmatter cannot be audited. Add to the UNPINNED list and skip downstream phases for it.
4. Build a reverse map: `upstream_repo → list[(skill_name, source_paths, pin)]`. This is the audit's working set.

## Phase 1 — Source-map resolution

For each upstream repo referenced by any skill's `source:`, find its location on disk:

1. **`_meta/source-map.yaml`** at the plugin root (if present) — explicit `upstream:` mappings override everything else.
2. **CLI argument** — `--source-root <path>` if invoked from a command with that option.
3. **`SKILLS-TO-INTEGRATE/`** at the plugin root — convention used by `ai-maestro-webdesign` for read-only upstream copies.
4. **`$HOME/Documents/github/<repo-name>`** — last-resort default for local development checkouts.

If no upstream location resolves for a given source path → emit a **DEGRADED** warning for that skill: list the pin, state "cannot diff — upstream not found", and skip diff-classification (the skill ends up in neither CLEAN nor STALE — it's "unverified").

Verify each resolved path is actually a git repo (`git -C <path> rev-parse --git-dir` returns 0). If not, treat as DEGRADED.

## Phase 2 — Per-upstream HEAD lookup

For each unique resolved upstream:

```
HEAD=$(git -C <upstream> rev-parse --short HEAD)
```

Compare against every skill's pin for this upstream. There are three possibilities:

1. **All skills agree** — they all pin to the same commit. Common case. Single diff suffices.
2. **Skills disagree** — different skills pin to different commits in the same upstream. This is acceptable (skills can be re-distilled at different times) but emit an INFO note for visibility. Run one diff per distinct pin.
3. **Pin is not a valid commit** — `git rev-parse <pin>` fails. Mark this skill as **DEGRADED** (bad pin). Common cause: the upstream was force-pushed and old commits are now unreachable.

## Phase 3 — Diff per pin

For each `(upstream, pin)` pair:

```
git -C <upstream> diff --name-only <pin> HEAD -- <space-separated source paths>
```

Restricting the diff to source paths (`-- <paths>`) keeps the changed-file set small and relevant. Skills that source from `docs/` ignore changes in `src/`, etc.

Cache the changed-file set per `(upstream, pin)` to avoid re-running diffs when multiple skills share a pin.

## Phase 4 — Classification

For each skill (excluding UNPINNED / DEGRADED):

1. **CLEAN** — `HEAD == source_version` (no diff needed).
2. **PIN-ONLY** — `HEAD != source_version` AND no file in the changed-file set matches ANY of this skill's `source:` paths. (HEAD moved, but not for this skill's content.) Mechanical pin bump suffices.
3. **STALE** — `HEAD != source_version` AND ≥1 file in the changed-file set matches ≥1 of this skill's `source:` paths. The skill's source content has actually moved; human re-distillation is needed.

**Path matching rules:**

- Exact match — `source: docs/conventions.md` matches `docs/conventions.md`.
- Prefix match for directories — `source: components/ui/` matches any `components/ui/**` file.
- Wildcard support — `source: components/ui/*.tsx` matches the obvious pattern (use shell-style globbing).
- Case-sensitive on Linux/CI, case-insensitive on macOS — normalize to lowercase for the comparison to avoid platform-dependent verdicts.

## Phase 5 — Diff summary for STALE skills

For each STALE finding, generate a short human-readable summary:

1. For each changed source file, run `git -C <upstream> diff --stat <pin> HEAD -- <file>`. Capture insertions/deletions.
2. For files with <50 lines changed, also capture `git diff --unified=0 <pin> HEAD -- <file>` and extract added function/component names (regex `^\+\s*(export\s+)?(async\s+)?function\s+(\w+)` and similar).
3. Build a one-line "what changed" string: `"42 added, 18 removed; new exports: X, Y; renamed Z → W"`.
4. Add a "re-check" pointer — a heuristic suggestion about which part of the distilled skill is most likely affected. Pure pattern-based: if the diff touches `*.test.{ts,tsx}`, suggest "test examples in the skill"; if it touches `*.config.{js,ts}`, suggest "configuration snippets"; if it touches markdown docs, suggest "narrative explanations". Don't try to interpret the actual diff — that's the human's job.

## Phase 6 — Emit the plan

Single markdown file at the report path. Default:
`$MAIN_ROOT/reports/skill-drift/<YYYYMMDD_HHMMSS±HHMM>-skill-drift-audit.md`

Always include — even if CLEAN — so the audit is auditable.

### Section order

1. **Header** — plugin name, plugin version (from `.claude-plugin/plugin.json`), audit timestamp, list of upstreams resolved with their HEAD commits.
2. **Summary verdict** — `CLEAN: 38 | PIN-ONLY: 5 | STALE: 2 | UNPINNED: 1 | DEGRADED: 0`.
3. **STALE skills** — one block per skill (the section that costs the most human time):
   ```
   ### amw-shadcn-ui (STALE)
   - Pin: 8edaa0b → upstream HEAD: 9f3c1d2
   - Changed source files:
     - components/ui/button.tsx (42 added, 18 removed)
       — new exports: ButtonGroup; renamed link → text
   - Re-check: button-variants reference + the variant matrix in component-inventory.md
   ```
4. **PIN-ONLY skills** — single table:
   ```
   | Skill | Old pin | New pin |
   |---|---|---|
   | amw-design-extract | 8edaa0b | 9f3c1d2 |
   ```
5. **UNPINNED skills** — flat list with a "needs pin" note and a hint about where the upstream likely is.
6. **DEGRADED skills** — flat list with the reason (upstream-not-found / invalid-commit / not-a-git-repo).
7. **CLEAN skills** — count only by default; expand to a list iff a `--verbose` flag is set or the audit was invoked with `verbose=true`.
8. **Next steps** — explicit ordered directive list:
   1. Author pins for N UNPINNED skill(s).
   2. Re-distill M STALE skill(s) by hand (one bullet per skill).
   3. Bulk-bump K PIN-ONLY skill(s) — a single sed/awk one-liner can update all of them.

## Phase 7 — Self-test (optional, on demand)

If the audit needs to verify its own correctness:

1. Pick a skill with a known-good pin.
2. Re-run the audit against that pin alone. Result must be CLEAN.
3. Manually bump the pin in the skill to a known-stale value (without changing content).
4. Re-run. Result must be PIN-ONLY or STALE depending on whether the new pin's commit range touched the skill's source paths.

This is for development / debugging the audit itself — not part of the user-facing flow.

## Anti-patterns (don't do)

- **Don't infer the upstream from the skill name.** Always read frontmatter `source:`. The skill name and upstream path frequently don't match (e.g. `amw-shadcn-ui` sources from `SKILLS-TO-INTEGRATE/web-design/shadcn-ui-skills-main/` — there's a 1-to-many possible mapping).
- **Don't auto-fix pins.** Even for PIN-ONLY skills the human reviews the diff first; the plan lists the bumps but applying them is a separate step.
- **Don't fetch / pull / clone.** The audit is read-only against the upstream's CURRENT working tree state. If the upstream is stale on disk, that's the user's responsibility to refresh; flag DEGRADED if HEAD looks suspiciously old (>180 days) but never fetch on their behalf.
- **Don't summarize diff content as an instruction.** The audit says "this file changed; review here". It does NOT say "the skill should now read X" — that's the re-distillation gate.
