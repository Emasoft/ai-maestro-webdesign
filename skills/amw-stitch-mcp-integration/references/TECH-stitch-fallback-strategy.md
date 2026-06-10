# TECH-stitch-fallback-strategy

## Table of Contents

- [What it documents](#what-it-documents)
- [When this file applies](#when-this-file-applies)
- [Decision tree](#decision-tree)
- [Choosing between Nodes A and B when both apply](#choosing-between-nodes-a-and-b-when-both-apply)
- [Worked example — MCP absent, user has a URL](#worked-example-mcp-absent-user-has-a-url)
- [Worked example — MCP absent, codebase only](#worked-example-mcp-absent-codebase-only)
- [Worked example — MCP absent, no source at all](#worked-example-mcp-absent-no-source-at-all)
- [Non-negotiables for the fallback path](#non-negotiables-for-the-fallback-path)
- [Cross-references](#cross-references)

## What it documents

The deterministic fallback decision tree the Stitch integration skill follows when the Stitch MCP server is unavailable. The fallback is selected by the caller (typically `amw-design-md-extractor-agent` or `amw-design-md-author-agent`) after the parent SKILL emits its fallback line. The decision tree below picks the next source in order of fidelity; the first source that can satisfy the user's intent wins.

## When this file applies

This file applies on EVERY invocation where the Stitch MCP probe in [SKILL](../SKILL.md) fails. The probe failure modes covered: server unreachable, tool surface absent, no workspace bound, malformed payload, single-tool returns an explicit "not implemented" error.

This file does NOT apply when the MCP probe succeeds — in that case the parent SKILL proceeds with the documented Stitch tool surface and this file plays no role.

## Decision tree

Walk the tree top-down. The first node whose preconditions match the user's intent wins. Each node has a documented recipe and a documented bailout — when a node fails, the next node is tried.

```
START
  |
  v
[Does the user have a target URL?]
  yes -> Node A: amw-design-extract
  no  -> [Does the user have a codebase to scan?]
           yes -> Node B: amw-design-md-from-codebase.py
           no  -> [Does the user have a brief or a reference description?]
                    yes -> Node C: amw-ui-ux-reasoning
                    no  -> Node D: Ask the user for one of the three above. STOP.
```

### Node A — `amw-design-extract`

**Preconditions:** the user named a URL or pasted one in the conversation.

**Recipe:**

1. Call `bin/amw-designlang-wrapper.sh tokens <url>`.
2. The wrapper writes the 8-file token dump to `$TMPDIR/ai-maestro-webdesign-tokens/<slug>/`.
3. If the caller was `amw-design-md-author-agent`, also call `bin/amw-design-md-from-url.sh <url>` to emit a full DESIGN.md draft.
4. Hand off the artifacts to the original caller. Record in the report that the Stitch path was unavailable and `amw-design-extract` was substituted.

**Fidelity vs Stitch:** ~80% — URL extraction captures tokens, types, spacing, and rough component inventory but not the variant matrix, slot definitions, or user-flow graph. The caller is responsible for synthesising the missing layers (typically via `amw-design-md-author-agent`'s 5-question interview).

**Bailout:** if `bin/amw-designlang-wrapper.sh` fails (URL unreachable, auth wall, 4xx), surface the error to the user and move to Node B. Do NOT silently retry.

### Node B — `amw-design-md-from-codebase.py`

**Preconditions:** the user has a codebase the skill can scan (a path to a local directory, a GitHub URL, or a checked-out repo) AND that codebase uses one of the supported design-system flavors (Tailwind, shadcn, Chakra, vanilla CSS, styled-components).

**Recipe:**

1. Call `bin/amw-design-md-from-codebase.py <path>`.
2. The script auto-detects the design-system flavor and emits a DESIGN.md draft plus a tokens.css companion.
3. If a `tailwind.config.{ts,js,mjs}` is present, additionally call `bin/amw-design-md-from-tailwind.ts` for higher-fidelity token extraction.
4. Hand off the DESIGN.md draft to the original caller.

**Fidelity vs Stitch:** ~70% — codebase extraction captures the implemented token set and the component tree but not the design intent (why a token exists, what variants are planned but not yet shipped, what flows the components serve). The caller may need to interview the user to fill the intent layer.

**Bailout:** if the codebase has no detectable design system, emit a clear "no supported design system detected" line and move to Node C.

### Node C — `amw-ui-ux-reasoning`

**Preconditions:** the user has a brief, a reference description, or a verbal account of what they want — but no live URL and no scannable codebase.

**Recipe:**

1. Invoke `amw-ui-ux-reasoning` with the user's brief as context.
2. The skill applies design heuristics (Gestalt, Fitts, Hick, Miller, Jakob, visual hierarchy, F/Z pattern, peak-end) to propose a tokens skeleton, a component shortlist, and a flow outline.
3. Surface the proposal to the user for confirmation before any artifact is written. This is the "last resort" path and the orchestrator's [CLAUDE.md](../../../CLAUDE.md) explicitly warns against treating it as a default.

**Fidelity vs Stitch:** ~40% — heuristic reasoning produces a plausible starting point but cannot match real extracted tokens. The output is a proposal, not a spec.

**Bailout:** if the user does not have even a brief, move to Node D.

### Node D — Ask the user

**Preconditions:** the previous nodes' preconditions all failed (no URL, no codebase, no brief).

**Recipe:**

1. Surface a short question: "I cannot reach the Stitch MCP server. To continue I need one of: (a) a URL to extract tokens from, (b) a path to a codebase I can scan, or (c) a written brief describing the design intent. Which can you provide?"
2. STOP. Do not proceed without an answer.

**Fidelity vs Stitch:** N/A — this node is a graceful halt, not a substitute.

## Choosing between Nodes A and B when both apply

When the user has BOTH a URL and a codebase (typical for projects under active development), prefer Node A (`amw-design-extract`) when the user said "the design should look like <url>" and prefer Node B (`amw-design-md-from-codebase.py`) when the user said "extract from the current project". When the intent is ambiguous, ask once.

## Worked example — MCP absent, user has a URL

Scenario: `amw-design-md-author-agent` ran the Stitch integration skill. The probe returned "tool not found". The user originally said "pull from stitch workspace acme-marketing" but also mentioned "the design should look like https://stripe.com" earlier in the conversation.

1. The caller reads the fallback line emitted by [SKILL](../SKILL.md).
2. The caller consults this file. URL is present in the conversation history → Node A wins.
3. The caller invokes `bin/amw-designlang-wrapper.sh tokens https://stripe.com`. The wrapper writes the token dump.
4. The caller also invokes `bin/amw-design-md-from-url.sh https://stripe.com` because the original intent was DESIGN.md authoring (not just tokens).
5. The caller hands the artifacts to `amw-design-md-author-agent`, which proceeds with its normal interview to add the intent layer.
6. The final report records: "Stitch MCP probe failed (tool not found). Fell back to Node A (amw-design-extract) per TECH-stitch-fallback-strategy.md. Artifacts: <paths>. Fidelity: ~80% vs Stitch direct extraction."

## Worked example — MCP absent, codebase only

Scenario: a user runs `amw-design-md-author-agent` on a checked-out repo and mentions "import from stitch if you can". No URL, no brief.

1. Probe fails. Fallback chain starts.
2. URL absent → skip Node A.
3. Codebase present → Node B wins.
4. The caller invokes `bin/amw-design-md-from-codebase.py <repo>`. The script detects Tailwind and emits the DESIGN.md draft.
5. Caller proceeds with `amw-design-md-author-agent`'s normal flow.

## Worked example — MCP absent, no source at all

Scenario: a user says "design a landing page for a new startup, ideally importing from stitch".

1. Probe fails. Fallback chain starts.
2. No URL, no codebase, no brief → only a one-sentence concept → Node C wins.
3. `amw-ui-ux-reasoning` proposes a tokens skeleton based on heuristics.
4. Caller surfaces the proposal to the user, who confirms or amends.
5. Once the user has confirmed the heuristic proposal, `amw-design-md-author-agent` proceeds with its normal flow using that proposal as a starting point.

## Non-negotiables for the fallback path

- **One node, one attempt.** The caller does not loop through every node trying each; it picks the first whose preconditions match. If that node bails out, the caller moves to the next node — once.
- **Record the fallback in the report.** Every fallback run records which node was selected, why, and what fidelity the user should expect. The user must know they did not get the Stitch path.
- **Never silently downgrade.** If Node A wins, the user must know that Node A was selected because the Stitch MCP was unavailable. Do not hide the choice.
- **Stop at Node D.** When all preceding nodes' preconditions fail, ask the user. Do not invent a brief on the user's behalf.

## Cross-references

- [SKILL](../SKILL.md) — Parent skill that emits the fallback line and yields to this chain.
- [TECH-stitch-design-language](./TECH-stitch-design-language.md) — The Stitch surface this fallback replaces.
- [SKILL](../../amw-design-extract/SKILL.md) — Node A executor.
- `bin/amw-design-md-from-codebase.py` — Node B executor.
- `bin/amw-design-md-from-tailwind.mjs` — Node B higher-fidelity helper.
- [SKILL](../../amw-ui-ux-reasoning/SKILL.md) — Node C executor.
- [SKILL](../../amw-design-md/SKILL.md) — Common downstream consumer regardless of which node won.
