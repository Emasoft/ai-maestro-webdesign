---
name: TECH-full-output-enforcement
category: design-principles-workflow
source: reimplemented in this plugin's architecture (on-disk-artifact + structured-return-contract model) from taste-skill's full-output-enforcement skill (Leonxlnx, MIT) — no verbatim copy; the on-disk-vs-inline split and the content-placeholder-vs-code-elision distinction are amw-specific
license: this file = MIT (plugin license)
also-in: "amw-wireframe-builder-agent (artifact completeness gate); amw-infographic-builder-agent (artifact completeness gate); amw-asset-generator-agent + amw-email-designer-agent (same gate when they emit code); amw-design-principles SKILL.md (cross-cutting output discipline)"
---

# FULL-OUTPUT ENFORCEMENT — a partial deliverable is a broken deliverable

## Table of Contents

- [What this is](#what-this-is)
- [Baseline rule](#baseline-rule)
- [Two faces in this plugin's architecture](#two-faces-in-this-plugins-architecture)
- [Banned elision patterns](#banned-elision-patterns)
- [Content placeholder vs code elision — the load-bearing distinction](#content-placeholder-vs-code-elision--the-load-bearing-distinction)
- [Scope-count lock](#scope-count-lock)
- [Clean-split PAUSED protocol (inline output only)](#clean-split-paused-protocol-inline-output-only)
- [Pre-return quick check](#pre-return-quick-check)
- [Cross-references](#cross-references)

## What this is

A standing output-discipline rule that every code-emitting skill and sub-agent in this plugin inherits. It exists because the default LLM behavior under length pressure is to *abbreviate* — emit the first two of five components, stub the middle of a file with `// ... rest follows the same pattern`, or stop with "let me know if you want the rest." For a design plugin whose deliverables are runnable artifacts, an abbreviated deliverable is not a smaller deliverable — it is a broken one. The user cannot ship `// rest of code`.

## Baseline rule

Treat every deliverable as production-critical. **Optimize for completeness, not brevity.** If the brief asks for a full file, emit the full file. If it asks for five components, emit five complete components. If a layout has nine sections, materialize all nine. "You can extend this later" is never an acceptable substitute for finishing the work now.

## Two faces in this plugin's architecture

The taste-skill original assumed code streamed inline into chat. This plugin emits most deliverables as **files on disk** and reports back through the [sub-agent return contract](sub-agent-return-contract.md) (`status: ok | partial | failed`). So the rule has two concrete forms:

| Output channel | What "complete" means | What a length problem looks like → correct handling |
|---|---|---|
| **On-disk artifact** (HTML / SVG / CSS / `.tsx` / MJML written to a file) | The file is fully materialized end to end — no elision comments, no stubbed sections, valid and parseable. | If you genuinely cannot finish the artifact, **never** write a stub file with `<!-- rest of sections -->` and return `status=ok`. Write what you completed, return `status=partial`, and list the unfinished scope in `blocking_issues`. A half-file masquerading as done is the failure mode this rule forbids. |
| **Inline output** (code or prose emitted directly into chat — orchestrator responses, a skill emitting a snippet) | Every requested item is present and finished in the message. | If you approach the token limit, do **not** compress or skip ahead. Write at full quality to a clean breakpoint and use the [PAUSED protocol](#clean-split-paused-protocol-inline-output-only). |

The on-disk form is the dominant one for sub-agents. The `status=partial` + `blocking_issues` path is the architecture's first-class way to say "I ran out of room" — use it instead of shipping an abbreviated file. This composes with the existing "fail fast, return structured partial over silent best-effort" rule the builder agents already carry.

## Banned elision patterns

These are hard failures anywhere a deliverable's *known* structure is being emitted (file or inline). Never produce them:

| Class | Banned |
|---|---|
| **Code-block elision** | `// ...`, `// rest of code`, `// rest of the sections`, `// implement here`, `// (continue pattern)`, `// add more as needed`, `// similar to above`, `/* ... */`, a bare `...` standing in for omitted markup, `<!-- remaining cards follow the same structure -->` |
| **Prose escape hatches** | "for brevity", "the rest follows the same pattern", "similarly for the remaining N", "and so on" (replacing real content), "I'll leave that as an exercise", "let me know if you want me to continue", "I can provide the rest if needed" |
| **Structural shortcuts** | Emitting a skeleton when a full implementation was requested. Showing the first and last section while skipping the middle. Replacing N repeated-but-distinct items with one example + "repeat for the others". Describing what code *should* do instead of writing it. |

The tell is always the same: the agent *knows* what the omitted bytes are and chooses not to write them. That choice is forbidden.

## Content placeholder vs code elision — the load-bearing distinction

This rule looks like it contradicts the plugin's "use a placeholder, do not fabricate" rules in [ai-slop-avoid](../ai-slop-avoid.md) (rules 1 and 15) and [three-hard-rules](three-hard-rules.md). It does not. They govern two different things:

- **Content placeholder — ALLOWED, often required.** When the real *data* is unknown (a testimonial you weren't given, a metric nobody supplied, an image asset that doesn't exist yet), you do NOT invent it. You leave a labeled placeholder — `[customer testimonial TK]`, `[customer TK]`, a gray asset box with descriptive `alt`. The placeholder marks "real data belongs here; ask the user." This is correct behavior.
- **Code / structure elision — NEVER allowed.** When you *know* the markup, the CSS, the next six sections, you emit all of it. You never replace known structure with `// rest follows`.

The clean line: **a complete artifact may contain content-TK placeholders for unknown data, but must never contain structure elision for known-but-omitted markup.** One section reading `<h2>[headline TK]</h2>` is fine. A comment reading `<!-- 5 more sections like the one above -->` is a hard failure. Materialize the structure fully; mark only the genuinely-unknown data with a TK.

## Scope-count lock

1. **Scope** — read the full request and count the distinct deliverables expected (files, components, sections, variants, answers). Lock that number before building.
2. **Build** — produce every deliverable completely. No partial drafts.
3. **Cross-check** — before returning, re-read the original request and compare your delivered count against the locked scope. If anything is missing, add it before responding. For sub-agents, the locked count and the delivered count should also be reflected honestly in the return contract (`status=ok` only when delivered == scope).

For the plugin's structural gates this is mechanical: the ASCII the wireframe-builder consumes declares a binding section/column count (see the builder's "ASCII structure is binding" rule), so the scope count is *already* pinned by the approved Phase A artifact — emitting fewer sections than the ASCII declares is both a scope-lock violation and a structure-binding violation.

## Clean-split PAUSED protocol (inline output only)

When an **inline** response (not an on-disk artifact) genuinely approaches the token limit:

- Do not compress remaining sections to squeeze them in.
- Do not skip ahead to a conclusion.
- Write at full quality up to a clean breakpoint — end of a function, end of a file, end of a section.
- End with exactly:

```
[PAUSED — X of Y complete. Send "continue" to resume from: <next section name>]
```

On "continue", resume exactly where you stopped — no recap, no repetition. (For on-disk artifacts, prefer `status=partial` + `blocking_issues` over a PAUSED marker inside the file.)

## Pre-return quick check

Before finalizing any deliverable, verify:

- No banned elision pattern from the table above appears anywhere in the output.
- Every item the locked scope counted is present and finished.
- Code/markup contains actual runnable content, not a description of what it would contain.
- Nothing was shortened to save space.
- If the deliverable is incomplete, the return contract says `status=partial` (never `ok`) and `blocking_issues` names the unfinished scope.

## Cross-references

- [ai-slop-avoid](../ai-slop-avoid.md) — content-fabrication rules; the *content placeholder* side of the distinction above.
- [three-hard-rules](three-hard-rules.md) — "never fabricate data" rule that pairs with content placeholders.
- [sub-agent-return-contract](sub-agent-return-contract.md) — the `status: ok | partial | failed` contract that carries the on-disk "I ran out of room" signal.
- `agents/amw-wireframe-builder-agent.md` — applies this as an artifact-completeness gate (companion to its fail-fast rule).
- `agents/amw-infographic-builder-agent.md` — applies this as an artifact-completeness gate.
