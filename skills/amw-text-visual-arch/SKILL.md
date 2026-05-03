---
name: amw-text-visual-arch
description: Produces layered ASCII architecture diagrams — context, container, or component level — for terminals, PRs, and ADRs. Triggers on narrow intents — "ascii architecture diagram", "text-only system diagram", "layered services in ASCII", "terminal-safe architecture sketch", "ADR-embeddable diagram", "PR-paste architecture overview". Does NOT trigger on generic "architecture", "system diagram", "draw the system" — those belong to design-principles / diagram-architecture / ascii-to-svg. Output is ASCII only; every diagram passes bin/amw-validate-ascii.py before delivery. Use when creating a terminal-safe layered ASCII architecture diagram for a PR, ADR, or README. Trigger with explicit "ascii architecture diagram" or "terminal-safe architecture sketch" phrasing.
version: 0.1.0
---

# Text-Visual Architecture — ASCII system diagrams

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Produces layered ASCII architecture diagrams at context, container, or component zoom level for paste-compatible use in terminal output, GitHub PRs, markdown ADRs, and code comments. Uses standard `+---+` box glyphs with labeled protocol arrows. Every diagram passes `bin/amw-validate-ascii.py` before delivery. For the same structure rendered as SVG, route to `amw-diagram-architecture` after ASCII approval.

## Examples

See the `## Diagram framing` section below for minimal examples of context, container, and component diagrams.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A (as a low-fi ASCII medium for architecture sketches) or Phase B (when the approved design requires a validated ASCII architecture artifact). The orchestrator may apply any zoom-level, context/container/component, and export technique from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Renders system, service, and data architectures as ASCII diagrams paste-compatible with terminal output, GitHub PRs, markdown ADRs, and code comments. Maintains multiple zoom levels (context, container, component) in monospaced text.

This skill is for **architectural structure** — components, services, contracts, deployment topology. It is not for flowcharts (`../amw-text-visual-workflows/`), state machines (`../amw-text-visual-state/`), CLI panels (`../amw-text-visual-cheatsheets/`), or retrospectives (`../amw-text-visual-retro/`). If the user wants the same architecture rendered as SVG or a prettier graphic, route them to `../amw-diagram-architecture/` or `../amw-ascii-to-svg/` after the ASCII is approved.

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

### 1. Context diagram

Outer boundary = "the system"; everything outside is users or external systems.

```
+-----------------+       +-----------------+
|     User        |------>|  The System     |
| (web, mobile)   |       |                 |
+-----------------+       +--------+--------+
                                   |
                                   v
                         +-----------------+
                         |  Payment API    |
                         |  (3rd party)    |
                         +-----------------+
```

### 2. Container diagram

Inside "the system", break out services and data stores.

```
+-------------------+     HTTP      +-------------------+
|  Web Frontend     | ============> |  API Gateway      |
|  [React, CDN]     |               |  [AWS ALB]        |
+-------------------+               +---------+---------+
                                              |
                         +--------------------+--------------------+
                         |                    |                    |
                         v                    v                    v
                +-----------------+  +-----------------+  +-----------------+
                |  Auth Service   |  |  Orders Service |  |  Billing Service|
                |  [Node, k8s]    |  |  [Go, k8s]      |  |  [Python, k8s] |
                +--------+--------+  +--------+--------+  +--------+--------+
                         |                    |                    |
                         v                    v                    v
                +-----------------+  +-----------------+  +-----------------+
                |  Users DB       |  |  Orders DB      |  |  Stripe API     |
                |  [Postgres]     |  |  [Postgres]     |  |  (external)     |
                +-----------------+  +-----------------+  +-----------------+
```

### 3. Component diagram

Inside one service, break out modules / packages / classes.

```
+-------------------------- Orders Service -----------------------+
|                                                                 |
|  +---------------+   +---------------+   +----------------+     |
|  |  HTTP Handler | ->|  Order Domain | ->|  Repository    |     |
|  |  [REST]       |   |  [pure Go]    |   |  [Postgres]    |     |
|  +---------------+   +---------------+   +--------+-------+     |
|                              |                    |             |
|                              v                    v             |
|                      +---------------+   +----------------+     |
|                      |  Event Bus    |   |  Read Model    |     |
|                      |  [Kafka out]  |   |  [Redis cache] |     |
|                      +---------------+   +----------------+     |
+-----------------------------------------------------------------+
```

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

Architecture diagrams often need to show more than just "A calls B" — request/response pairs, handshakes, compile-time dependencies, plain associations. Use this vocabulary when the short `->` / `=>` / `~>` set is not expressive enough. Pick one style per diagram; do not mix styles within a single figure. Source: adapted from the diagram-skill-main ASCII-STYLES reference (subsumed into the current skill).

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Synchronous call (A calls B, waits for response). |
| emphasized | `==>` | Primary / high-volume sync path; single accented arrow per diagram. |
| async | `~~>` | Async event, fire-and-forget message. |
| optional | `..>` | Dotted optional / non-deterministic / conditional transition. |
| return | `<--` | Response leg of a sync call (A calls B, B returns to A). |
| bidirectional | `<-->` | Handshake — protocol exchange where both sides send. |
| dependency | `---▷` | Compile/build dependency (hollow triangle head, UML-style). |
| association | `───` | Plain association, no direction (topology link, deployment relation). |

`return` arrows are especially important for architecture diagrams that double as informal sequence diagrams — showing just the request without the response leaves the reader guessing where the data comes back. Use `<--` labeled with the return payload.

## Multi-zoom presentation

When the user asks for "the architecture" without a zoom level, produce two diagrams stacked: a context diagram first (3–7 nodes), then a container diagram (the inside of the system from the context box). Label each block:

```
### Context

... context diagram ...

### Container

... container diagram ...
```

Do not produce all three zoom levels in one response unless the user asks — it overwhelms the reviewer and the third level (component) is usually one-per-service.

## Validation gate (MANDATORY)

Every diagram this skill emits MUST pass `../../bin/amw-validate-ascii.py` before being shown to the user.

The flow:

1. Draft the diagram.
2. Write it to `/tmp/amw-tva-<slug>.txt`.
3. Run `perl ../../bin/amw-validate-ascii.py /tmp/amw-tva-<slug>.txt`.
4. If PASS → present in a fenced code block.
5. If FAIL → apply every `FIX:` hint, re-run. Loop until PASS.
6. Never present an un-validated diagram.

For layered architectures with uniform rows, use `../../bin/amw-ascii-render.py` in `layers` mode — the renderer guarantees alignment by construction. See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema.

## Instructions

1. Confirm the four inputs (components, interactions, context, zoom level). One bundled question for missing pieces.
2. Pick the zoom level. Announce the choice in one sentence.
3. Draft the diagram using the standard glyphs.
4. Run the validation gate. Loop until PASS.
5. Present inside a fenced code block (no language tag).
6. Offer to save a canonical copy to `docs/architecture/<name>.txt` in the project repo. Do not write until user approves.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `text-visual-arch` is the user asking about?
  - **c4** (1 techniques)
    - [TECH-c4-zoom-levels](./references/TECH-c4-zoom-levels.md) — context / container / component framing
  - **consistent** (1 techniques)
    - [TECH-consistent-layer-spacing](./references/TECH-consistent-layer-spacing.md) — fixed grid + 2-space layer separator
  - **footnote** (1 techniques)
    - [TECH-footnote-tags-deployment](./references/TECH-footnote-tags-deployment.md) — post-diagram SLAs / owners / repos
  - **platform** (1 techniques)
    - [TECH-platform-component-tags](./references/TECH-platform-component-tags.md) — `[iOS]` `[Windows]` `[prod]` prefixes
  - **protocol** (1 techniques)
    - [TECH-protocol-label-arrows](./references/TECH-protocol-label-arrows.md) — `HTTP`, `gRPC`, `L1 tx` on edges

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-c4-zoom-levels.md](./references/TECH-c4-zoom-levels.md)**
  - Description: context / container / component framing
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-consistent-layer-spacing.md](./references/TECH-consistent-layer-spacing.md)**
  - Description: fixed grid + 2-space layer separator
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-footnote-tags-deployment.md](./references/TECH-footnote-tags-deployment.md)**
  - Description: post-diagram SLAs / owners / repos
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-platform-component-tags.md](./references/TECH-platform-component-tags.md)**
  - Description: `[iOS]` `[Windows]` `[prod]` prefixes
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-protocol-label-arrows.md](./references/TECH-protocol-label-arrows.md)**
  - Description: `HTTP`, `gRPC`, `L1 tx` on edges
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-text-visual-arch/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. monospaced ASCII layered architecture diagrams pasted into PRs / ADRs / terminals). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-text-visual-arch-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Prerequisites

- **runtime_binaries:** `perl >= 5.10`
- **python_packages:** none (optional `python3` for `bin/amw-ascii-render.py`)
- **npm_packages:** none
- **mcp_servers:** none
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py layers` (optional)

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator. Rule 1 (context) matters especially here: without knowing the real services, the diagram is a fabrication.
- [SKILL](../amw-ascii-validator/SKILL.md) — validation contract.
- [SKILL](../amw-text-visual-workflows/SKILL.md) — sibling for flowcharts and timelines.
- [SKILL](../amw-text-visual-state/SKILL.md) — sibling for state machines.
- [SKILL](../amw-text-visual-cheatsheets/SKILL.md) — sibling for CLI panels.
- [SKILL](../amw-text-visual-retro/SKILL.md) — sibling for retrospectives.
- [SKILL](../amw-diagram-architecture/SKILL.md) — if the user wants SVG / PNG instead of ASCII, route here after ASCII is approved.
- [SKILL](../amw-ascii-to-svg/SKILL.md) — convert approved ASCII to SVG.
- `/amw-ascii-to-svg` — slash command for the SVG conversion step.

## How to invoke via existing commands

No dedicated slash command. Invoke via:

- **Direct skill activation** — phrases like "ascii architecture diagram of the orders service" trigger this skill.
- `/amw-sketch` — when used inside the plan phase and the sketch is an architecture overview instead of a UI wireframe.
- `/amw-ascii-to-svg` — after the ASCII architecture is approved, convert to SVG for publication.

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
| External system count dominates the internal system | Use a two-column layout: left column internal, right column external, with clear trust-boundary separator `| | | | |` between them. |
| User wants C4 style but explicitly ASCII | This is exactly the skill's sweet spot — use context + container as the two stacked diagrams. |
| User wants the same picture as SVG | Emit the ASCII first, then route to `../amw-ascii-to-svg/` after approval. Do not try to emit SVG from this skill. |
