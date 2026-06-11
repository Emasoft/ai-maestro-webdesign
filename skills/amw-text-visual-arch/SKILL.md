---
name: amw-text-visual-arch
description: Layered ASCII architecture diagrams (context, container, component level) for terminals, PRs, ADRs. Triggers on "ascii architecture diagram", "text-only system diagram", "terminal-safe architecture sketch", "ADR-embeddable diagram". Does NOT trigger on "architecture" / "system diagram" alone — routes to design-principles / diagram-architecture. ASCII only; passes amw-validate-ascii.py. Use when creating a terminal-safe ASCII architecture diagram. Trigger with "ascii architecture diagram".
version: 0.1.0
---

# Text-Visual Architecture — ASCII system diagrams

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Produces layered ASCII architecture diagrams at context, container, or component zoom level for paste-compatible use in terminal output, GitHub PRs, markdown ADRs, and code comments. Uses standard `+---+` box glyphs with labeled protocol arrows. Every diagram passes `bin/amw-validate-ascii.py` before delivery. For the same structure rendered as SVG, route to `amw-diagram-architecture` after ASCII approval.

## Examples

See [examples](./references/examples.md) for full rendered ASCII at context, container, and component zoom levels.

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during Phase A (low-fi sketch) or Phase B (validated artifact). Skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Renders system, service, and data architectures as ASCII diagrams paste-compatible with terminals, GitHub PRs, markdown ADRs, and code comments. Multiple zoom levels (context, container, component).

This skill is for **architectural structure**. It is NOT for flowcharts ([workflows](../amw-text-visual-workflows/SKILL.md)), state machines ([state](../amw-text-visual-state/SKILL.md)), CLI panels ([cheatsheets](../amw-text-visual-cheatsheets/SKILL.md)), or retrospectives ([retro](../amw-text-visual-retro/SKILL.md)). For SVG/PNG output route to [diagram-architecture](../amw-diagram-architecture/SKILL.md) after ASCII approval.

## Trigger conditions

- "ascii architecture diagram of the payment service"
- "terminal-safe layered diagram"
- "system diagram I can paste in an ADR"
- "container diagram in ASCII"
- "component diagram for this PR"
- "C4-ish text diagram"

Do NOT activate on broad design vocabulary. If the user says "architecture diagram" without the ASCII / text / terminal / PR / ADR framing, `design-principles` is the entry point; it may route here or to `diagram-architecture` depending on desired fidelity.

## Inputs expected

1. **Component list** — services, databases, queues, external APIs, clients.
2. **Interaction types** — sync (HTTP / gRPC), async (queue, event bus), data streams, blockchain events.
3. **Deployment / runtime context** — regions, environments (dev/staging/prod), device types (`[iOS]`, `[Windows agent]`), on-prem vs cloud.
4. **Zoom level** — context (users ↔ system), container (services, DBs, queues), or component (modules, classes, contracts). Default to container when the user does not specify.

If any is missing, ask one bundled question — do not guess. A diagram that invents services or mis-labels a protocol is worse than no diagram.

## Diagram framing (pick one zoom level per diagram)

1. **Context diagram** — outer boundary = the system; everything outside is users or external systems. (3-7 boxes.)
2. **Container diagram** — inside the system, break out services and data stores.
3. **Component diagram** — inside one service, break out modules / packages / classes.

See [examples](./references/examples.md) for the full rendered ASCII of each level.
> [examples.md] Context diagram · Container diagram · Component diagram

## Glyph and layout standards

- **Node box:** `+---+` corners, `|` verticals, `-` horizontals.
- **Arrows:** `->` sync call, `=>` emphasized / primary, `~>` async event, `-->` long sync, `==>` long emphasized, `~~>` long async. Pick one set per diagram — do not mix short and long forms.
- **Layer separation:** exactly 2 blank columns between side-by-side boxes; exactly 1 blank line between rows.
- **Node label format:** line 1 = name, line 2 = `[runtime, platform]` in square brackets, optional line 3 = `(region, owner)`.
- **Edge label format:** place it above or below the arrow, aligned with the arrowhead. `HTTP`, `gRPC`, `S3 put`, `Stripe charge`, `L1 tx`.
- **External systems:** mark explicitly `(external)` or `(3rd party)` on the box — reviewers need to know what is inside vs outside the trust boundary.
- **Width ceiling:** 78 columns for terminal / code-comment; 100 for GitHub / ADR. Never exceed 100.
- **No tabs. No decorative emoji. No variable-width glyphs** (`▼ ▲ ▶ ◀ ⟶ ⇒`).

## Extended connection types

Architecture diagrams sometimes need richer arrow vocab than `->` / `=>` / `~>`. Pick one style per diagram; do not mix.

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Synchronous call. |
| emphasized | `==>` | Primary / high-volume sync. |
| async | `~~>` | Async event, fire-and-forget. |
| optional | `..>` | Optional / conditional. |
| return | `<--` | Response leg of a sync call. |
| bidirectional | `<-->` | Handshake — both sides send. |
| dependency | `---▷` | Compile/build dependency (UML hollow triangle). |
| association | `───` | Plain association, no direction. |

`return` arrows matter when the diagram doubles as an informal sequence — without the return leg the reader can't see where data comes back.

## Multi-zoom presentation

When the user asks for "the architecture" without a zoom level, produce two diagrams stacked: a context diagram first (3-7 nodes), then a container diagram (the inside of the system). Label each block `### Context` / `### Container`. Do not produce all three zoom levels in one response unless the user asks — it overwhelms the reviewer and the third level (component) is usually one-per-service.

## Validation gate (MANDATORY)

Every emitted diagram MUST pass `../../bin/amw-validate-ascii.py` before delivery. Flow: draft → write to `/tmp/amw-tva-<slug>.txt` → run validator → PASS = present in fenced block; FAIL = apply every `FIX:` hint and re-run until PASS. Never present un-validated output. For uniform-row layouts, use `../../bin/amw-ascii-render.py layers` (alignment guaranteed by construction). See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema.

## Instructions

1. Confirm the four inputs (components, interactions, context, zoom level). One bundled question for missing pieces.
2. Pick the zoom level. Announce the choice in one sentence.
3. Draft the diagram using the standard glyphs.
4. Run the validation gate. Loop until PASS.
5. Present inside a fenced code block (no language tag).
6. Offer to save a canonical copy to `docs/architecture/<name>.txt` in the project repo. Do not write until user approves.

## Technique selection / References

Each TECH file under `./references/` follows the standard TOC: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references. Open only the file whose label matches the current need.

- [TECH-c4-zoom-levels](./references/TECH-c4-zoom-levels.md) — context / container / component framing
> [TECH-c4-zoom-levels.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-consistent-layer-spacing](./references/TECH-consistent-layer-spacing.md) — fixed grid + 2-space layer separator
> [TECH-consistent-layer-spacing.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-footnote-tags-deployment](./references/TECH-footnote-tags-deployment.md) — post-diagram SLAs / owners / repos
> [TECH-footnote-tags-deployment.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-platform-component-tags](./references/TECH-platform-component-tags.md) — `[iOS]` `[Windows]` `[prod]` prefixes
> [TECH-platform-component-tags.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-protocol-label-arrows](./references/TECH-protocol-label-arrows.md) — `HTTP`, `gRPC`, `L1 tx` on edges
> [TECH-protocol-label-arrows.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [examples](./references/examples.md) — three rendered ASCII zoom-level diagrams
> [examples.md] Context diagram · Container diagram · Component diagram

<!-- end of references -->

## Completion checklist

Verify all items before reporting complete. FAIL on any item triggers a remediation loop.

- Inputs captured verbatim from the user — no silent paraphrasing.
- At least one `TECH-*.md` consulted and cited in the report.
- Output passes Non-negotiables (below).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- Output rendered/validated by the matching tool (`bin/amw-validate-ascii.py` here).
- Cross-skill hand-offs documented in the report.
- User-facing filename is descriptive English.

## Output

Two outputs per invocation:

1. **Artifact(s)** — monospaced ASCII layered architecture diagrams pasted into PRs / ADRs / terminals. Output path is determined by project inference per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (user-supplied path → framework convention → existing `./design/` → `./design/diagrams/` → `/tmp/amw-text-visual-arch-<slug>/`).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references

2. **Job-completion report** — `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<slug>_<8-char-hash>.md` containing: Inputs · Method · Artifacts (path + 1-line · How to use · Next steps) · Checklist (PASS/FAIL/N/A per item) · Deviations. Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. **Every artifact MUST be linked from the report.**

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8`
- **python_packages:** none
- **npm_packages:** none
- **mcp_servers:** none
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py layers` (optional)

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (Rule 1: without real services, the diagram is fabrication).
- [SKILL](../amw-ascii-validator/SKILL.md) — validation contract.
- Siblings: [workflows](../amw-text-visual-workflows/SKILL.md), [state](../amw-text-visual-state/SKILL.md), [cheatsheets](../amw-text-visual-cheatsheets/SKILL.md), [retro](../amw-text-visual-retro/SKILL.md).
- [SKILL](../amw-diagram-architecture/SKILL.md) — route here after ASCII approval for SVG/PNG.
- [SKILL](../amw-ascii-to-svg/SKILL.md) + `/amw-ascii-to-svg` — convert ASCII to SVG.

## How to invoke

No dedicated slash command. Triggered by phrases like "ascii architecture diagram of <X>". Also: `/amw-sketch` for plan-phase architecture overviews; `/amw-ascii-to-svg` to convert the approved ASCII.

## Non-negotiables

- Every diagram passes `../../bin/amw-validate-ascii.py` before delivery. No exceptions.
- 78-column terminal ceiling / 100-column GitHub ceiling. Never exceed 100.
- No tab characters.
- One zoom level per diagram; multi-zoom requests stack two diagrams, not merge them.
- Every node has `[runtime, platform]` or `(external)` annotation. No bare boxes.
- Every edge has a protocol label (`HTTP`, `gRPC`, `async event`, …). No unlabeled arrows.
- No fabricated services. If the user has not named a component, ask rather than invent.
- Does NOT emit HTML or SVG. ASCII only.

## Error Handling

| Failure mode | Recovery |
|---|---|
| Diagram has more than 10 services and cannot fit 100 cols | Drop to two stacked diagrams: group by domain (e.g. `Auth`, `Orders`, `Billing`) and emit one container diagram per group. |
| User asks for the component layer without naming modules | Ask for the module list; do not guess. An invented `UserRepository` is worse than no diagram. |
| Mixed sync and async with unclear protocols | Add a legend block above the diagram: `-> sync HTTP, ~> async event, => primary call`. |
| External system count dominates the internal system | Use a two-column layout: left column internal, right column external, with clear trust-boundary separator `\| \| \| \| \|` between them. |
| User wants C4 style but explicitly ASCII | This is exactly the skill's sweet spot — use context + container as the two stacked diagrams. |
| User wants the same picture as SVG | Emit the ASCII first, then route to `../amw-ascii-to-svg/` after approval. Do not try to emit SVG from this skill. |
