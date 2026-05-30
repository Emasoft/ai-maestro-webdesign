---
name: amw-ascii-sketch
description: Runs the ASCII plan-phase iteration loop. Triggers on "sketch this in ASCII", "give me layout variants", "propose 3 wireframes in ASCII", "iterate on the layout in ASCII", "ASCII mockup", "box-drawing wireframe". Does NOT self-trigger on broad "design", "UI", "landing page" — those route to design-principles, which dispatches here as default plan-phase executor. Use when iterating on webpage layout in ASCII before committing to HTML. Trigger with /amw-sketch.
version: 0.1.0
---

# ASCII Sketch — plan-phase loop

> Orchestrated by [SKILL](../amw-design-principles/SKILL.md) — default Phase A executor for webpage design (not a fast-path alternative).

## Overview

ASCII plan-phase iteration loop — three layout variants per turn in pure ASCII, iterates on feedback, hands off to `amw-ascii-to-html` only after explicit approval. **PLAN (Phase A)** — does NOT emit HTML or write intermediate files; lives entirely in chat. Callable via `/amw-sketch`, or invoked by `../amw-design-principles/`. Autonomous and self-contained — any agent can use it by reading this SKILL.md and references.

## Mode A vs Mode B

**Mode A** (JSON-IR-driven via `bin/amw-ascii-render.py`) is the DEFAULT for structured diagrams — flowcharts (`--mode diagram`), sequence diagrams (`--mode sequence`), tables (`--mode table`), layered architectures (`--mode layers`). The renderer computes widths / corners / separators from the spec, eliminating 30-50% of validator-FAIL retries.

**Mode B** (LLM hand-author + validator loop) is the fallback for freeform wireframes (full-page web layouts, hero+nav+footer, dashboard sketches): generate → write to `/tmp/` → validate → on FAIL apply FIX hints → re-validate. The right path for unstructured shapes, not a worse one.

Worked Mode A example (login flowchart, JSON → render → validate) at [loop-diagram-and-worked-examples](./references/loop-diagram-and-worked-examples.md).

## Why ASCII, not HTML

ASCII iteration is ~1% the token cost of HTML iteration (10+ revisions without context decay), renders instantly in chat (no file write / browser round trip / screenshot step), maps naturally to layout-edit language ("move CTA right of hero"), and commits to nothing — typography / color / radius / shadow tokens do not exist in ASCII, so they cannot over-constrain layout decisions. Skeleton first, tokens after.

## Instructions

1. Step 1 — Orchestrator check (gather design system, brand tokens, references; ask if absent).
2. Step 2 — Emit three ASCII variants (Baseline A, Advanced B, Experimental C) — each validated via `bin/amw-validate-ascii.py` BEFORE presentation.
3. Step 3 — Ask for explicit feedback (direction, edits, satisfaction).
4. On ambiguous acknowledgement, probe; on picks/tweaks, emit a revised single ASCII and loop to step 3.
5. Iterate until explicit satisfaction (`yes` / `ship it` / `convert it` / `that's the one` / `perfect` / `done`).
6. On approval, save to `/tmp/amw-sketch-<slug>-final.txt` and hand off to `../amw-ascii-to-html/`.

The full ASCII loop diagram lives at [loop-diagram-and-worked-examples](./references/loop-diagram-and-worked-examples.md). The loop has no fixed iteration count — terminates ONLY on explicit satisfaction.

## Step 1 — Orchestrator check (run once at the start of a new loop)

Before emitting the first variant set, confirm in ≤ 4 sentences: (1) **Context** — design system / brand tokens / reference site? If absent, say *"No design context yet — variants are layout-only; tokens come later via `/amw-extract-style` or a UI kit"*; (2) **Canvas target** — desktop 1440 / mobile 375 / slide 1920x1080; (3) **Surface** — where the sketch is pasted while iterating; default 80 cols if unspecified (GitHub PR → 100, slide preview → 80-120); (4) **Required elements** — logo / primary CTA / named blocks (hard constraints in every variant).

**Lane-labeled variants.** For dashboards / consoles with named regions, use the `lanes` field in `bin/amw-ascii-render.py` input — see [SKILL](../amw-ascii-validator/SKILL.md) for JSON shape. Fall back to freeform boxes for organic structures.

Do NOT re-run this check on iteration turns of the same loop. If the user has not supplied enough context to answer 1-4, pull from [question-templates](../amw-design-principles/question-templates.md) and wait.

## Validation gate (MANDATORY, between variant generation and presentation)

Every variant MUST pass `../../bin/amw-validate-ascii.py` before being shown to the user. LLMs cannot count characters reliably — the validator is how the plugin compensates.

- **Mode A flow:** author JSON → `python3 ../../bin/amw-ascii-render.py < /tmp/spec.json > /tmp/amw-sketch-<slug>-<variant>.txt` → `python3 ../../bin/amw-validate-ascii.py /tmp/amw-sketch-<slug>-<variant>.txt`. PASS on first attempt in nearly all cases. On rare FAIL: fix the JSON spec and re-render; do NOT hand-edit the rendered output.
- **Mode B flow:** hand-author → write to `/tmp/amw-sketch-<slug>-<variant>.txt` → validate → on FAIL apply every `FIX:` hint, re-validate; loop until PASS. Never present an un-validated variant.

See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema (Mode A) and validation output contract. Before generation, substitute banned chars (variable-width triangles, long/double arrows, emoji) with safe equivalents — the validator flags them as forbidden.

## Step 2 — Produce the three variants

Three fenced ASCII blocks, ≈ 60-80 columns wide, each preceded by a one-line caption naming the design decision + trade-off. Each variant on a safe→risky scale, internally consistent (do not mix scales inside one variant):

- **A — Baseline.** Safest, Jakob's-Law-compliant, zero experimentation; follows the user's design system if present.
- **B — Advanced.** Conventional skeleton + ONE dimension shifted hard (typography-led hero, asymmetric grid, unexpected CTA placement). One dimension, not three.
- **C — Experimental.** Allowed to break the template. New metaphor, novel layout, unusual density. Flag risks explicitly in the caption.

Variants must differ on a real design dimension (layout shape, information hierarchy, hero strategy, CTA placement), NOT three trivial visual re-skins. Output shape example: [loop-diagram-and-worked-examples](./references/loop-diagram-and-worked-examples.md#example-variant-set-step-2-output-shape). Do NOT produce fewer or more than three on the first turn — a fourth muddies the decision.

## Step 3 — Solicit feedback and iterate

After presenting variants, ask one question (no prose paragraphs): *"Which direction? Any edits to position, size, alignment, or components before I go further? When you're happy, say so explicitly and I'll convert to HTML."*

| User response | Skill action |
|---|---|
| Picks one + wants edits | Emit revised ASCII (chosen variant with edits applied), same caption shape, ask again. Loop. |
| Mixes two variants ("A's hero with B's footer") | Emit one consolidated ASCII combining the pieces. Loop. |
| Rejects all three | Rewind to Step 1; probe for the failure mode (too generic, wrong canvas, missed element, wrong vibe); emit three NEW variants. |
| Ambiguous acknowledgement ("looks fine", "ok I guess", "sure") | NOT approval. Probe: *"To confirm — generate HTML now, or more changes?"* Loop. |
| Explicit satisfaction ("yes" / "ship it" / "convert it" / "perfect" / "done" / "that's the one") | Proceed to Step 4. |

Each iteration turn is one revised ASCII block + one question. No prose essays, no meta-commentary on what changed — stay token-cheap.

## Step 4 — Hand off to `ascii-to-html`

After an explicit satisfaction token: (1) derive a kebab-case slug from the subject; (2) save final ASCII to `/tmp/amw-sketch-<slug>-final.txt` — the single source of truth for HTML conversion, do NOT re-describe in prose; (3) tell the user *"ASCII approved. Running `/amw-ascii-to-html` against this sketch now — it will produce the real HTML using design-principles tokens and the selected starter-component chrome."*; (4) hand off control to [SKILL](../amw-ascii-to-html/SKILL.md).

Before handoff, if the user has not extracted tokens or supplied a brand kit, OFFER (not gate): *"If you have a reference site, `/amw-extract-style <url>` will pull color / type / spacing tokens first — making the HTML match the brand instead of using generic defaults."*

## AI-slop checks per variant

Before emitting any variant, scan each one against [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md). The skeleton is the first place slop leaks in. Highlights: no "hero → 3-col icons → testimonials → CTA → footer" stamped across all three variants (item 10); no fake testimonials (item 15); no fabricated statistics (item 16); every block must earn its place (§ VII). Rework before showing the user — do NOT ship slop and rely on the user to catch it.

## Output

Three ASCII layout variants per iteration, each labelled A / B / C, presented in chat only (no file writes). After approval, the selected variant is passed to `amw-ascii-to-html` for HTML conversion.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Prerequisites

- runtime / python / npm / mcp: none
- scripts: `../../bin/amw-ascii-render.py` (JSON → ASCII, 4 modes), `../../bin/amw-validate-ascii.py` (PASS/FAIL gate + FIX hints)
- `../../bin/amw-ascii-parse.py` is invoked only by the downstream `ascii-to-html` skill — not from within this loop.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator; three hard rules apply to every variant.
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — applied per variant before emission.
- [question-templates](../amw-design-principles/question-templates.md) — source of Step 1 questions when context is missing.
- [SKILL](../amw-ascii-to-html/SKILL.md) — terminal handoff (`/tmp/amw-sketch-<slug>-final.txt` is the input contract).
- [SKILL](../amw-ascii-to-svg/SKILL.md) — adjacent skill for diagram-shaped sketches (route there for boxes-and-arrows, not wireframes).
- [SKILL](../amw-ux-flows/SKILL.md) — upstream when the user already has a PRD (PRD → flow diagrams → then this skill).
- `../../bin/amw-preview-server.py` — optional multi-variant HTML comparison server, used after handoff.
- `/amw-sketch` — user-facing slash command.

## Non-negotiables

- Does NOT write any `.html` file at any point. Output stays in chat as ASCII; HTML is the next skill's job.
- Does NOT skip Step 1 on a NEW loop (must skip on iteration turns of the SAME loop).
- Does NOT produce fewer or more than three variants on the first turn.
- Does NOT treat ambiguous acknowledgement as approval — probe first.
- Variants must differ on a real design dimension, not be trivial visual re-skins.
- No prose essays between iterations — one ASCII block + one question per turn.
- Does NOT auto-trigger on broad design vocabulary; those route via `../amw-design-principles/`.

## Error Handling

| Situation | Recovery |
|---|---|
| User says "great" / "looks good" / "nice" with no commit | Probe — do NOT proceed to Step 4 |
| User pastes their own ASCII for variants | Treat as Variant A; emit B and C as departures |
| User rejects 3 variant sets in a row | Escalate — likely a Rule 1 context failure; re-open the context conversation, consider `../amw-ui-ux-reasoning/` |
| User asks "which is best?" | Briefly name each variant's strength and ask again; the skill offers options, doesn't decide |
| Brief shifts mid-loop ("make it a dashboard instead") | New loop — drop state, re-run Step 1, then Step 2 |
| User pastes a screenshot for ASCII variants | Describe its structure in Step 1 as the baseline constraint; emit variants that preserve the essential shape but shift one dimension |
