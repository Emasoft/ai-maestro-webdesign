---
name: amw-stitch-mcp-integration
description: Integrate with the Stitch MCP server for design-system extraction, component-library bridging, and design-flow handoff. Triggers on "stitch", "stitch design", "stitch flow", "stitch component library", "import from stitch", "export to stitch". Does NOT trigger on generic "design" or "component" — those route to amw-design-principles. Activates only when the Stitch MCP server is reachable; otherwise emits a clean fallback message and routes to amw-design-extract or amw-design-md-extractor-agent.
---

# Stitch MCP Integration

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is a GATED Tier-3 executor. It activates only when the Stitch MCP server is detected; absent that server, it routes to its documented fallbacks.

## Overview

Bridges the ai-maestro-webdesign plugin to the Stitch design-language MCP server. When the MCP is reachable, this skill exposes Stitch's design-token, component, layout, and flow surfaces to the rest of the plugin — letting `amw-design-md-author-agent`, `amw-wireframe-builder-agent`, and `amw-design-extract` import Stitch artifacts (tokens, flows, component manifests) and emit changes back to Stitch via the MCP tool surface.

When the MCP is absent (the most common case at the time of this scaffold) the skill emits one clean line and yields to the documented fallback chain. It never blocks, never retries silently, never fails hard.

## Activation

Activates on the narrow triggers listed above. The triggers do NOT include "design" or "component" alone — those belong to the orchestrator. The skill body checks for the Stitch MCP server immediately and chooses one of two paths:

1. **MCP reachable** — proceeds with the Stitch tool surface. Reports the tool versions and the workspace ID it bound to.
2. **MCP absent** — emits the fallback line documented in section [Failure mode](#failure-mode) and returns control to the caller.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The trigger description does NOT mention the MCP requirement; the failure surface is inside the skill body so discovery still works when the MCP is offline.

## Position in flow

INPUT and OUTPUT. As an input source it pulls design tokens, component manifests, layout grids, and user-flow graphs from a Stitch workspace and feeds them into [`amw-design-md`](../amw-design-md/SKILL.md), [`amw-design-extract`](../amw-design-extract/SKILL.md), and the wireframe builder. As an output sink it can push amw-* artifacts (a finalized DESIGN.md, a token bundle, a wireframe ASCII pack) back to a Stitch workspace via the MCP write surface.

The full mapping between Stitch's vocabulary and amw-* concepts lives in [TECH-stitch-design-language](./references/TECH-stitch-design-language.md). The complete fallback decision tree (what to do when the MCP is unavailable) lives in [TECH-stitch-fallback-strategy](./references/TECH-stitch-fallback-strategy.md).
> [TECH-stitch-fallback-strategy.md] What it documents · When this file applies · Decision tree · Choosing between Nodes A and B when both apply · Worked example — MCP absent, user has a URL · Worked example — MCP absent, codebase only · Worked example — MCP absent, no source at all · Non-negotiables for the fallback path · Cross-references
> [TECH-stitch-design-language.md] What it documents · Stitch vocabulary · Canonical MCP tool surface · Translation table: Stitch ↔ amw · Worked example — pulling components into a DESIGN.md draft · Cross-references

## Trigger conditions

Fires on these specific phrasings:

- "use stitch"
- "import from stitch"
- "export to stitch"
- "sync with stitch"
- "stitch design tokens"
- "stitch component library"
- "stitch flow"
- "stitch workspace"
- "pull <tokens|components|flow|layout> from stitch"
- "push <tokens|components|flow> to stitch"

Do NOT fire on: "design a landing page", "component library" (without "stitch"), "extract design tokens" (without "stitch" — that routes to `amw-design-extract`), or "design.md" (that routes to `amw-design-md`).

## Prerequisites

This skill has ONE hard prerequisite and a documented fallback chain when the prerequisite is unmet.

### Required runtime

- **`stitch-mcp-server` (an MCP server that exposes the `mcp__stitch__*` tool surface).** This server is NOT bundled with this plugin. The user installs and configures it independently. Refer to the upstream Stitch documentation for installation; the canonical URL is recorded in [TECH-stitch-design-language](./references/TECH-stitch-design-language.md).
> [TECH-stitch-design-language.md] What it documents · Stitch vocabulary · Canonical MCP tool surface · Translation table: Stitch ↔ amw · Worked example — pulling components into a DESIGN.md draft · Cross-references
- **A bound Stitch workspace.** The MCP must be authenticated to at least one Stitch workspace before this skill can pull or push. The skill does NOT prompt for credentials — that lives in the MCP server's own configuration.

### Probe procedure (run first, before any other operation)

Probe whether the Stitch MCP is reachable by attempting one read-only tool call. The canonical probe is `mcp__stitch__ping` (or, if that name is unavailable, `mcp__stitch__list_workspaces` with a small limit). If the probe times out, returns a network error, or returns "tool not found":

1. STOP. Do NOT retry, do NOT fall back to scraping, do NOT silently mock.
2. Emit the one-line fallback message from [Failure mode](#failure-mode).
3. Return control to the caller and let it choose from [TECH-stitch-fallback-strategy](./references/TECH-stitch-fallback-strategy.md).
> [TECH-stitch-fallback-strategy.md] What it documents · When this file applies · Decision tree · Choosing between Nodes A and B when both apply · Worked example — MCP absent, user has a URL · Worked example — MCP absent, codebase only · Worked example — MCP absent, no source at all · Non-negotiables for the fallback path · Cross-references

## Failure mode

When the Stitch MCP server is not detected (probe failed, tool unavailable, no workspace bound), the skill emits exactly this line and exits cleanly:

```
Stitch MCP not detected — install via the upstream Stitch documentation (linked in TECH-stitch-design-language.md), or fall back to amw-design-extract / amw-design-md-extractor-agent per TECH-stitch-fallback-strategy.md.
```

The skill MUST NOT:

- Continue silently with no Stitch data.
- Invent or mock Stitch tool calls.
- Block the orchestrator or the user.
- Re-attempt the probe more than once within a single invocation.

The skill MAY (and is the recommended pattern):

- Hand off to the fallback chain documented in [TECH-stitch-fallback-strategy](./references/TECH-stitch-fallback-strategy.md). The chain is: (a) `amw-design-extract` for token-only extraction from a URL, (b) `amw-design-md-from-url.sh` for a full DESIGN.md extraction, (c) `amw-ui-ux-reasoning` for last-resort design reasoning when no live source is available.
> [TECH-stitch-fallback-strategy.md] What it documents · When this file applies · Decision tree · Choosing between Nodes A and B when both apply · Worked example — MCP absent, user has a URL · Worked example — MCP absent, codebase only · Worked example — MCP absent, no source at all · Non-negotiables for the fallback path · Cross-references

The discovery layer is unaffected — the trigger description does NOT mention "requires Stitch MCP". The trigger fires on phrasing; the failure surface appears only inside the skill body.

## Instructions

1. **Probe.** Attempt the read-only Stitch MCP probe described in [Prerequisites](#prerequisites). Record the outcome.
2. **Branch.**
   - If probe succeeds, continue to step 3.
   - If probe fails, emit the fallback line and stop. The caller chooses a fallback per [TECH-stitch-fallback-strategy](./references/TECH-stitch-fallback-strategy.md).
> [TECH-stitch-fallback-strategy.md] What it documents · When this file applies · Decision tree · Choosing between Nodes A and B when both apply · Worked example — MCP absent, user has a URL · Worked example — MCP absent, codebase only · Worked example — MCP absent, no source at all · Non-negotiables for the fallback path · Cross-references
3. **Identify the user intent.** Map the trigger phrase to one of three operation classes documented in [TECH-stitch-design-language](./references/TECH-stitch-design-language.md): pull-tokens, pull-components, pull-flow, push-tokens, push-components, push-flow.
4. **Invoke the matching Stitch MCP tool call.** The canonical tool names live in [TECH-stitch-design-language](./references/TECH-stitch-design-language.md). The skill does NOT hardcode tool names in this SKILL.md — the reference file is the single source of truth for the MCP surface so the skill stays portable when the upstream tool names evolve.
> [TECH-stitch-design-language.md] What it documents · Stitch vocabulary · Canonical MCP tool surface · Translation table: Stitch ↔ amw · Worked example — pulling components into a DESIGN.md draft · Cross-references
5. **Translate.** Map the returned Stitch payload onto amw-* canonical formats. For tokens that is the W3C token JSON consumed by `amw-design-extract`. For components that is the component-inventory.md format used by `amw-design-md`. For flows that is the Mermaid source consumed by `amw-mermaid-render`.
6. **Hand off.** Write the translated artifact to the project's standard output path (see [project-output-routing](../amw-design-principles/references/project-output-routing.md)) and emit the path so the next skill or sub-agent can pick it up.
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
7. **Report.** Write the job-completion report to the standard reports location with sections: Inputs, Probe outcome, Method, Artifacts, Checklist, Deviations.

## Usage and examples

Invoked indirectly through `amw-design-md-author-agent`, `amw-wireframe-builder-agent`, or `amw-design-extract` when those agents detect a Stitch trigger. No user-facing slash command at this scaffold stage. The direct Phase-B pseudocode invocation, plus two end-to-end worked scenarios (MCP reachable → pull tokens; MCP absent → fallback), live in [TECH-stitch-worked-examples](./references/TECH-stitch-worked-examples.md).
> [TECH-stitch-worked-examples.md] Usage · Examples · Scenario 1 — MCP reachable, pull tokens · Scenario 2 — MCP absent, fallback

## Resources

- [SKILL](../amw-design-extract/SKILL.md) — Primary fallback for URL-based token extraction.
- [SKILL](../amw-design-md/SKILL.md) — Sibling skill for canonical DESIGN.md authoring; consumes Stitch tokens when available.
- [SKILL](../amw-ui-ux-reasoning/SKILL.md) — Last-resort fallback when no live source is reachable.
- [project-output-routing](../amw-design-principles/references/project-output-routing.md) — Where Stitch-imported artifacts land.
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references

The four `TECH-stitch-*` reference files (design-language, fallback-strategy, worked-examples, error-contract) — Stitch vocabulary + MCP tool surface, the fallback decision tree, the worked usage scenarios, and the operating contract + error cases respectively — are listed with their complete tables of contents in the [References](#references) section below.

## Non-negotiables and error handling

The 7-bullet operating contract (probe first / one probe per invocation / clean discovery layer / no mocking / no credentials in the skill / tool-name table in the reference file / deterministic fallback chain) and the 5 enumerated error cases (probe timeout, tool-not-found, workspace-not-bound, malformed payload, multi-workspace) live together in [TECH-stitch-error-contract](./references/TECH-stitch-error-contract.md). Read that file before any push/pull operation.
> [TECH-stitch-error-contract.md] Non-negotiables · Error Handling

## References

Each technique is documented as a single reference file under `./references/`. Read only the file whose TOC matches the current need.

- [TECH-stitch-design-language](./references/TECH-stitch-design-language.md)
> [TECH-stitch-design-language.md] What it documents · Stitch vocabulary · Canonical MCP tool surface · Translation table: Stitch ↔ amw · Worked example — pulling components into a DESIGN.md draft · Cross-references
- [TECH-stitch-fallback-strategy](./references/TECH-stitch-fallback-strategy.md)
> [TECH-stitch-fallback-strategy.md] What it documents · When this file applies · Decision tree · Choosing between Nodes A and B when both apply · Worked example — MCP absent, user has a URL · Worked example — MCP absent, codebase only · Worked example — MCP absent, no source at all · Non-negotiables for the fallback path · Cross-references
- [TECH-stitch-worked-examples](./references/TECH-stitch-worked-examples.md)
> [TECH-stitch-worked-examples.md] Usage · Examples · Scenario 1 — MCP reachable, pull tokens · Scenario 2 — MCP absent, fallback
- [TECH-stitch-error-contract](./references/TECH-stitch-error-contract.md)
> [TECH-stitch-error-contract.md] Non-negotiables · Error Handling

## Completion checklist

Verify every item before reporting complete. FAIL on any item should trigger a remediation loop.

- Probe outcome recorded verbatim in the report (success / failure + reason).
- If MCP absent, the fallback line was emitted verbatim and the caller was informed of the decision tree.
- If MCP reachable, the canonical tool name actually called is recorded in the report (not paraphrased).
- Translated artifact written to the project's standard output path per [project-output-routing](../amw-design-principles/references/project-output-routing.md).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
- No mocking and no silent downgrade — every deviation from the nominal flow is documented in the report.
- Hand-off documented: name the downstream skill or sub-agent that consumes the translated artifact.

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — when the MCP is reachable, the translated payload (W3C tokens JSON, component-inventory.md, Mermaid flow source, etc.). When the MCP is absent, NO artifact — only the fallback line and the deferred decision to the caller.
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` with sections: Inputs, Probe outcome, Method, Artifacts (each `- <path> — <desc>`), Checklist (PASS/FAIL/N/A), Deviations.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. Every artifact MUST be linked from the report.
