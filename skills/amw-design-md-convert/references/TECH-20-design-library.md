---
name: TECH-20-design-library
category: workflow
source: agents/amw-design-md-author-agent.md, agents/amw-design-md-extractor-agent.md, references/brand-catalog.md
also-in: TECH-07-url-extraction.md, TECH-15-design-md-as-input.md, TECH-19-design-md-apply.md
status: stable
---

# TECH: Cross-project DESIGN.md library (`amw-design-library`)

## Table of Contents

- [What it does](#what-it-does)
- [Why a cross-project library](#why-a-cross-project-library)
- [Library layout on disk](#library-layout-on-disk)
- [Proposed CLI surface](#proposed-cli-surface)
  - [`amw-design-library list`](#amw-design-library-list)
  - [`amw-design-library use <name>`](#amw-design-library-use-name)
  - [`amw-design-library show <name>`](#amw-design-library-show-name)
  - [`amw-design-library remove <name>`](#amw-design-library-remove-name)
  - [`amw-design-library diff <name-a> <name-b>`](#amw-design-library-diff-name-a-name-b)
  - [`amw-design-library preview <name>`](#amw-design-library-preview-name)
  - [`amw-design-library add <name>`](#amw-design-library-add-name)
- [Naming convention](#naming-convention)
- [Workflow — "build this in the Linear style"](#workflow-build-this-in-the-linear-style)
- [Integration with existing skills](#integration-with-existing-skills)
- [Security and privacy](#security-and-privacy)
- [Limitations](#limitations)
- [Cross-references](#cross-references)

## What it does

Documents the **cross-project DESIGN.md library** — a global, user-owned directory of named DESIGN.md files that can be reused across multiple plugin invocations. A user maintains DESIGN.md files for the brands / systems they regularly work with (their own product, a client's site, a public reference like Linear or Stripe) and selects one by name when starting a new design task.

The library is purely user-local. No cloud sync, no centralized registry, no telemetry. It is the long-form complement to the existing pre-paywall snapshot shipped as `references/brand-*.md` (read-only; indexed by `references/brand-catalog.md`).

NOTE: The bin script `amw-design-library` is **proposed** — the CLI surface below is the contract. The actual implementation arrives in a later batch.

## Why a cross-project library

Real-world design work is rarely one-off. A studio working with multiple clients has 5-20 active design systems, each represented by a DESIGN.md. A solo product designer has 1-2 systems (their own product + the design system they're inspired by). A consultant rebuilding sites for clients needs to switch between client A's tokens and client B's tokens within a single day.

Without a library, every session must re-author or re-import the DESIGN.md from scratch — burning tokens, risking drift between sessions ("did I save the latest hex?"), and forcing the user to remember the file path. With a library, the user types `"build this in the Linear style"` and the agent loads `~/.config/ai-maestro/design-library/linear/DESIGN.md` deterministically.

## Library layout on disk

```
~/.config/ai-maestro/design-library/
├── <name>/                        e.g. linear, stripe, my-saas, acme-corp
│   ├── DESIGN.md                  the canonical Variant 1 file
│   ├── tokens.css                 (optional) emitted companion
│   ├── tokens.json                (optional) emitted companion
│   ├── tokens.dtcg.json           (optional) DTCG strict export
│   ├── component-inventory.md     (optional) emitted companion
│   ├── usage-prompt.md            (optional) emitted companion
│   ├── source/                    (optional) original input that produced this DESIGN.md
│   │   ├── tokens.json            (e.g. the original Tokens Studio export, see TECH-18)
│   │   ├── tailwind.config.ts     (e.g. the original Tailwind config, see TECH-10)
│   │   └── url.txt                (e.g. the URL that was extracted, see TECH-07)
│   └── meta.yaml                  (optional) provenance, last-updated, notes
└── _config.yaml                   (optional) library-wide settings
```

Layout invariants:

- The library root is `~/.config/ai-maestro/design-library/` (overridable via `$AMW_DESIGN_LIBRARY_ROOT`).
- Each subdirectory is a single design system, named in kebab-case.
- `DESIGN.md` is mandatory; every other file is optional and re-derivable from the DESIGN.md via existing emit-companions / dtcg-export / showcase scripts.
- `source/` is a snapshot of the artifact the DESIGN.md was built from. Optional but recommended for round-trip integrity.
- The library is gitignorable by the user — most users will NOT commit it because it may contain client-confidential token surfaces.

## Proposed CLI surface

The script lives at `<plugin-root>/bin/amw-design-library` (no extension; portable shell shim that dispatches to Python). All verbs are read-only by default; the only mutating verbs are `add` and `remove`.

### `amw-design-library list`

Lists every named DESIGN.md in the library with one-line summaries.

```
$ amw-design-library list
NAME         VERSION   COLORS   FONTS                 UPDATED
acme-corp    1.2       7        Inter / Manrope       2026-04-02
linear       2.0       12       Inter Tight           2026-03-18
my-saas      0.4       5        Geist / Geist Mono    2026-05-14
stripe       1.0       9        Sohne / Sohne Mono    2026-02-09
```

Summary fields are read from each DESIGN.md's frontmatter; missing fields are blank.

### `amw-design-library use <name>`

Prints the absolute path to the named DESIGN.md. Used by the agent or by `bin/` scripts that accept a DESIGN.md path.

```
$ amw-design-library use linear
~/.config/ai-maestro/design-library/linear/DESIGN.md
```

Exit code 1 if the name does not exist. No side effects.

### `amw-design-library show <name>`

Prints the named DESIGN.md to stdout. Equivalent to running `cat` on the path that `amw-design-library use <name>` resolves, but as a single command.

### `amw-design-library remove <name>`

Moves the named DESIGN.md (and its companion subdirectory) to a `.trashcan/` folder per the project rules (see `~/.claude/rules/use-safe-delete.md`). Never deletes outright.

```
$ amw-design-library remove old-client
safe-deleted: ~/.config/ai-maestro/design-library/old-client/
```

### `amw-design-library diff <name-a> <name-b>`

Wraps `bin/amw-design-md-diff.sh` against the two named systems' DESIGN.md files.

```
$ amw-design-library diff linear stripe
~ colors.primary       #5E6AD2  →  #635BFF
~ typography.body-md.fontFamily   "Inter Tight"  →  "Sohne"
+ components.button-primary.shadow   (added in stripe)
```

### `amw-design-library preview <name>`

Wraps `bin/amw-design-md-showcase.py` against the named DESIGN.md and opens the emitted HTML in the user's default browser via `open` (macOS) / `xdg-open` (Linux) / `start` (Windows).

```
$ amw-design-library preview my-saas
Showcase: /tmp/amw-design-md-showcase/my-saas-20260527-1430.html
Opening in browser ...
```

### `amw-design-library add <name>`

Adds a new entry to the library. Three input modes:

```bash
# Mode A — copy an existing DESIGN.md
amw-design-library add linear --from /path/to/linear.DESIGN.md

# Mode B — import from a Tokens Studio JSON
amw-design-library add stripe --from-figma-tokens /path/to/stripe.tokens.json

# Mode C — extract from a live URL
amw-design-library add acme --from-url https://acme.example.com
```

Mode B dispatches to `bin/amw-figma-tokens-import.py` (see [TECH-18-figma-input-path](../../amw-design-md-extract/references/TECH-18-figma-input-path.md)). Mode C dispatches to `bin/amw-design-md-from-url.sh` (see [TECH-07-url-extraction](../../amw-design-md/references/TECH-07-url-extraction.md)). All modes run the standard validation chain after import; failures abort the add.

After a successful add, the script optionally emits companions (`tokens.css`, `tokens.json`, `tokens.dtcg.json`, `component-inventory.md`, `usage-prompt.md`) when `--with-companions` is passed.

## Naming convention

Library names follow these rules:

- Kebab-case ASCII only — `[a-z0-9][a-z0-9-]*`. The agent enforces this on `add`.
- Brand-style names preferred — `linear`, `stripe`, `acme-corp`, `my-saas`. Avoid version suffixes (`my-saas-v2`); use the `version:` field in the DESIGN.md frontmatter for versioning.
- Reserved name `_default` — when the user types `"use the default style"` without specifying a name, the library resolves to `_default/DESIGN.md` if present, else to the ships-with-plugin reference systems indexed by `references/brand-catalog.md`.
- Reserved prefix `_` — for special entries (`_default`, `_demo`, `_template`). User-added entries MUST NOT start with `_`.

## Workflow — "build this in the Linear style"

The high-level user intent → agent action chain:

```
User: "Build a landing page for my product, in the Linear style."

Main-agent:
  1. Parse "Linear style" → library lookup
  2. amw-design-library use linear
     → /path/to/design-library/linear/DESIGN.md
  3. Read DESIGN.md → resolve brand_tokens (see TECH-15)
  4. Phase A: ASCII sketch + 3 variants
  5. User approves variant
  6. Phase B: amw-wireframe-builder-agent renders HTML
  7. Apply pass (see TECH-19) enforces Linear's tokens + WCAG + Do's/Don'ts
  8. Deliver
```

The agent never re-extracts from the live Linear site. The DESIGN.md is the single source of truth. If the user wants to refresh the Linear tokens, they re-run `amw-design-library add linear --from-url https://linear.app --force`.

## Integration with existing skills

| Skill / agent | How it uses the library |
|---|---|
| `amw-design-md-author-agent` | After authoring a DESIGN.md, prompts the user *"add this to the library as `<name>`?"* — runs `amw-design-library add <name> --from <path>`. |
| `amw-design-md-extractor-agent` | After extraction, same prompt. |
| `amw-wireframe-builder-agent` | When the user says *"in the <name> style"*, resolves via `amw-design-library use <name>`. |
| `amw-brand-researcher-agent` | When the brief mentions a brand name that matches a library entry, prefers the library entry over re-extraction. |
| Main-agent (Phase A) | When the user types a style reference (*"like Stripe"*, *"in the Linear style"*), checks the library first; falls back to live extraction only if no match. |

## Security and privacy

- The library lives under `~/.config/ai-maestro/` — outside any project tree by default. It is never committed by accident.
- The library MAY contain client-confidential token surfaces. Treat the library root as PRIVATE data — do not include its contents in agent reports unless the user explicitly asks.
- The optional `source/` subdirectory may contain Figma tokens, Tailwind configs, or URLs that reveal client identity. The library file structure is designed so that `meta.yaml` does NOT reference `source/` paths externally — the link is implicit (same parent directory).
- No part of the library is uploaded anywhere. No telemetry. The plugin makes zero network calls when reading the library.

## Limitations

- The library is single-user. Sharing a library between collaborators requires manual `rsync` or a user-side git repo at `~/.config/ai-maestro/design-library/`.
- The library is single-machine. Syncing across machines is the user's responsibility (e.g. via Mackup, chezmoi, or a dotfiles repo).
- Library entries are flat — no namespacing for multi-client / multi-product setups. A studio with 50 clients should organize by name prefix (`client-a-product-1`, `client-a-product-2`).
- Version history is NOT tracked by the library itself — use a git repo at the library root for history. Per-entry `meta.yaml` records `updated:` and `version:` but not full revision history.
- The proposed `amw-design-library` bin script does NOT exist yet — this TECH documents the contract; the script lands in a later batch (the recorded plan ledger).

## Cross-references

- [TECH-07-url-extraction](../../amw-design-md/references/TECH-07-url-extraction.md) — Mode C source for `amw-design-library add --from-url`
- [TECH-15-design-md-as-input](./TECH-15-design-md-as-input.md) — how the library's DESIGN.md is consumed downstream by wireframe-builder
- [TECH-18-figma-input-path](../../amw-design-md-extract/references/TECH-18-figma-input-path.md) — Mode B source for `amw-design-library add --from-figma-tokens`
- [TECH-19-design-md-apply](./TECH-19-design-md-apply.md) — apply pass enforces the library DESIGN.md's tokens at code-gen time
- [TECH-11-validation-and-lint](../../amw-design-md/references/TECH-11-validation-and-lint.md) — every `add` runs this chain before accepting the entry
- [TECH-12-companion-files](../../amw-design-md/references/TECH-12-companion-files.md) — `--with-companions` emits these alongside the library DESIGN.md
- [TECH-17-dtcg-export](./TECH-17-dtcg-export.md) — optional tokens.dtcg.json in the library entry
- `brand-catalog.md` + `brand-*.md` — ships-with-plugin reference systems (read-only, distinct from the user-local library at ~/.config/ai-maestro/design-library/)
- ~/.claude/rules/use-safe-delete.md — the `remove` verb uses safe-delete, not `rm`
