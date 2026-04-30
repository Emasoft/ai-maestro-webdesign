---
name: amw-ux-flows
description: PRD (or feature list) → use cases → Mermaid diagrams (flowchart + state + sequence) → mobile-first clickable HTML wireframes with inter-screen navigation → consolidated handoff document. Narrow triggers — "user flows from the PRD", "wireframe this feature", "generate a screen map", "document use cases", "clickable prototype for <feature>", "flow diagram for <screen>", "state diagram for <screen>", "sequence diagram for <API>". Do NOT trigger on generic "design a page", "style the UI", "make it look nice" — those stay with design-principles.
version: 0.1.0
author: ai-maestro-webdesign
source: Adapted from the public ux-flow-designer skill by Thomas Praun (MIT). Rewritten for this plugin's orchestrated flow; Chrome-DevTools-MCP dependency replaced with `../amw-dev-browser/`; Figma Dev Mode MCP path preserved.
---

# UX Flows

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> This skill is an executor. Triggers are PRD-to-wireframe-specific only — generic design vocabulary stays with the orchestrator.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A (when a PRD is present and wireframe flows need to be validated before Phase B) or as part of Phase B when clickable wireframes are an implementation deliverable. The orchestrator may apply the full PRD-to-wireframe pipeline from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

PROCESS (Phase A/B bridge). Bridges Product (PRD) and Visual Design. Consumes a PRD or a feature list, emits four artifact classes — use cases, Mermaid diagrams, clickable HTML wireframes, and a master handoff document. Outputs feed downstream into:

- `../amw-ascii-sketch/` — if the user wants to iterate on the generated wireframes in plan-phase ASCII before committing to real HTML.
- `../amw-ascii-to-html/` — if the user hands the wireframe layouts over for responsive-HTML lift.
- `../amw-infographics/` or `../amw-diagram-editorial/` — if the Mermaid diagrams graduate into editorial artifacts.

The wireframes produced here are **prototype-grade** (mobile-first, 375px, dashed-border wireframe aesthetic) — not production HTML. They exist to validate flow, not to ship.

## Trigger conditions

Fires on these specific phrasings:

- "design the user flows from the PRD"
- "wireframe the <feature> feature"
- "generate a screen map for <app>"
- "document the use cases from the PRD"
- "create the clickable prototype for <feature>"
- "flow diagram for the <screen> screen"
- "state diagram for <screen>"
- "sequence diagram for <API endpoint>"
- "map the navigation for <app>"
- "build the user journey for <feature>"

Do NOT fire on: "design a landing page", "make a nice dashboard", "build the UI" — those are design-principles' vocabulary. Do NOT fire on bare "flowchart" either — route that to `../amw-diagram-architecture/` when it is a system diagram, or to `../amw-diagram-svg/` for a freeform diagram.

## Dependencies

- **runtime_binaries (system):** none — Mermaid is text-only and Claude renders the blocks; HTML wireframes are self-contained.
- **runtime_binaries (bundled):** `../../bin/amw-dev-browser-wrapper.sh` — the plugin-standard browser wrapper; used for optional wireframe preview in Phase 3.
- **runtime_binaries (via /amw-init):** `dev-browser` CLI — required only when the user wants an in-browser preview of the clickable prototype.
- **mcp_servers (optional, on explicit request):** Figma Dev Mode MCP Server — for the Code-to-Canvas export path documented in `references/figma-integration.md`. Never activated silently.

## Usage

Designing app flows runs through four mandatory phases in order. Do not skip, summarize, or defer any phase once the skill is invoked.

### Phase 1 — Use Case Extraction

Read `docs/product/prd.md` if it exists. If no PRD is available, ask the user for the feature list or use case descriptions — do not synthesize use cases from nothing.

For each use case, document:

| Field | Description |
|-------|-------------|
| ID | `UC-001`, `UC-002`, ... |
| Name | Short descriptive name |
| Actors | Who participates (User, System, Admin, ...) |
| Preconditions | What must be true before the flow starts |
| Main Flow | Numbered step-by-step sequence |
| Alternative Flows | Branches, error paths, edge cases |
| Postconditions | What is true after the flow completes |

Save to `docs/ux-flows/use-cases.md`. Present the list to the user for approval. **Do not advance to Phase 2 without explicit confirmation.**

### Phase 2 — Mermaid Diagrams

Read `references/mermaid-patterns.md` for syntax patterns before generating any diagram.

1. **Master screen map** — one `graph TD` flowchart at `docs/ux-flows/diagrams/screen-map.md` showing every screen + general navigation paths of the entire app.
2. **Per-use-case diagrams** — for each approved use case, generate three diagrams under `docs/ux-flows/diagrams/{use-case-id}/`:
   - `flow.md` — `graph TD` flowchart with screen-to-screen navigation + decision nodes.
   - `states.md` — `stateDiagram-v2` with app states (loading, error, success, idle, ...).
   - `sequence.md` — `sequenceDiagram` with frontend-backend interaction + HTTP methods.
3. **Index** — `docs/ux-flows/diagrams/INDEX.md` listing all diagrams with cross-links.

Constraints:
- Max 15-20 nodes per diagram. Split complex flows into sub-diagrams linked via `[[Sub-flow]]` nodes.
- Use `classDef` for consistent node styling across diagrams (patterns in `references/mermaid-patterns.md`).

### Phase 3 — HTML Wireframes (Clickable Prototype)

> **MANDATORY.** Every invocation that reaches Phase 2 MUST continue to Phase 3. Do not ask the user whether to proceed — just do it.

1. **Generate HTML files.** For each unique screen identified in the flowcharts, copy `assets/wireframe-template.html` and fill it in. Requirements:
   - Self-contained — inline CSS only, no external dependencies, no JS.
   - Mobile-first — 375px viewport width.
   - Wireframe aesthetic — greys (`#f5f5f5` background, dashed `#ccc` borders, `#666` placeholder text). Wireframes are low-fidelity prototype HTML and are intentionally exempt from the plugin's oklch discipline; the raw greyscale hex is load-bearing to signal "prototype grade, not production". Production output (handed off to `../amw-ascii-to-html/` or direct design-principles work) must tokenize.
   - Use the template classes: `.wf-header`, `.wf-input`, `.wf-button`, `.wf-card`, `.wf-nav`, `.wf-list-item`, `.wf-tab-bar`, `.wf-icon-placeholder`, `.wf-link`, `.wf-back`.
   - Footer metadata carries screen name + related use-case ID.
2. **Add inter-screen navigation.** Every wireframe links to other screens via `<a href="target.html" class="wf-link">`. Rules:
   - Buttons that navigate: wrap in `<a href="target.html" class="wf-link"><div class="wf-button">Label</div></a>`.
   - Tab bars: each tab is an `<a class="wf-link">` pointing to its screen; consistent across shared screens.
   - Back buttons: `<a href="previous.html" class="wf-link wf-back">&larr; Back</a>` in the `.wf-nav` bar.
   - Tappable list items / cards: wrap the whole element in `<a class="wf-link">`.
   - **No dead ends** — every screen has at least one outgoing link (back button, tab bar, or action).
   - **No JavaScript** — pure HTML `<a>` navigation only. No onclick, no form submits.
3. **Save and index.** Save wireframes to `docs/ux-flows/wireframes/`. Generate `docs/ux-flows/wireframes/INDEX.md` with screen name, file link, related use cases, key elements, outgoing links.
4. **Offer browser preview.** After generation, proactively propose opening the entry screen via `bin/amw-dev-browser-wrapper.sh mobile file://$(pwd)/docs/ux-flows/wireframes/<entry>.html` (375px mobile viewport matches the wireframe target). Do not wait to be asked.

### Phase 4 — Consolidation and Handoff

Generate `docs/ux-flows/UX-FLOWS.md` with:

- Master screen map (link to `screen-map.md`).
- Screen inventory table (screen, purpose, wireframe, use cases).
- Use case diagrams (per UC: flow, states, sequence links).
- Clickable prototype links (from-screen, element, to-screen).
- Navigation patterns (tab bar, back navigation, modal flows, drawer menus, ...).
- Open questions for the visual-design phase.

After the handoff document is written, inform the user:
- The wireframes can be exported to Figma via the official Code-to-Canvas integration.
- Only requires Figma desktop app with Dev Mode MCP Server enabled (2-step setup in `references/figma-integration.md`).
- If interested, the user says "export to figma" and the setup steps are presented.

## Cross-references

- `../amw-design-principles/SKILL.md` — orchestrator
- `../amw-dev-browser/SKILL.md` — wireframe preview primitive (replaces the upstream skill's Chrome-DevTools-MCP dependency)
- `../../bin/amw-dev-browser-wrapper.sh` — plugin-standard browser wrapper
- `../amw-ascii-sketch/SKILL.md` — downstream option when the user wants to iterate on the generated wireframes in plan-phase ASCII
- `../amw-ascii-to-html/SKILL.md` — downstream lift from wireframe prototype to responsive HTML
- `../amw-ux-designer/SKILL.md` — broader UX methodology the wireframes slot into
- `../amw-ux-evaluator/SKILL.md` — consumes the clickable prototype for heuristic scoring
- `references/mermaid-patterns.md` — Mermaid syntax cookbook (node shapes, subgraphs, sequence patterns, styling)
- `references/figma-integration.md` — Figma Dev Mode MCP workflow (on explicit request only)
- `references/install-commands.md` — auxiliary skill + dev-browser install references
- `assets/wireframe-template.html` — mobile-first 375px wireframe base template

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `ux-flows` is the user asking about?
  - **mermaid** (3 techniques)
    - [TECH-mermaid-flowchart-screen-map](./references/TECH-mermaid-flowchart-screen-map.md) — TECH-mermaid-flowchart-screen-map
    - [TECH-mermaid-sequence-authenticated](./references/TECH-mermaid-sequence-authenticated.md) — TECH-mermaid-sequence-authenticated
    - [TECH-mermaid-state-diagram-screen](./references/TECH-mermaid-state-diagram-screen.md) — TECH-mermaid-state-diagram-screen
  - **wireframe** (2 techniques)
    - [TECH-wireframe-html-mobile-first](./references/TECH-wireframe-html-mobile-first.md) — TECH-wireframe-html-mobile-first
    - [TECH-wireframe-index-inventory](./references/TECH-wireframe-index-inventory.md) — TECH-wireframe-index-inventory
  - **4** (1 techniques)
    - [TECH-4-phase-mandatory-workflow](./references/TECH-4-phase-mandatory-workflow.md) — TECH-4-phase-mandatory-workflow
  - **clickable** (1 techniques)
    - [TECH-clickable-prototype-navigation](./references/TECH-clickable-prototype-navigation.md) — TECH-clickable-prototype-navigation
  - **figma** (1 techniques)
    - [TECH-figma-code-to-canvas-export](./references/TECH-figma-code-to-canvas-export.md) — TECH-figma-code-to-canvas-export
  - **no** (1 techniques)
    - [TECH-no-dead-end-screens](./references/TECH-no-dead-end-screens.md) — TECH-no-dead-end-screens
  - **prd** (1 techniques)
    - [TECH-prd-to-usecases](./references/TECH-prd-to-usecases.md) — TECH-prd-to-usecases
  - **split** (1 techniques)
    - [TECH-split-large-flows-subflow-linking](./references/TECH-split-large-flows-subflow-linking.md) — TECH-split-large-flows-subflow-linking
  - **use** (1 techniques)
    - [TECH-use-case-document-schema](./references/TECH-use-case-document-schema.md) — TECH-use-case-document-schema

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-4-phase-mandatory-workflow.md](./references/TECH-4-phase-mandatory-workflow.md)**
  - Description: TECH-4-phase-mandatory-workflow
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-clickable-prototype-navigation.md](./references/TECH-clickable-prototype-navigation.md)**
  - Description: TECH-clickable-prototype-navigation
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-figma-code-to-canvas-export.md](./references/TECH-figma-code-to-canvas-export.md)**
  - Description: TECH-figma-code-to-canvas-export
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-mermaid-flowchart-screen-map.md](./references/TECH-mermaid-flowchart-screen-map.md)**
  - Description: TECH-mermaid-flowchart-screen-map
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-mermaid-sequence-authenticated.md](./references/TECH-mermaid-sequence-authenticated.md)**
  - Description: TECH-mermaid-sequence-authenticated
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-mermaid-state-diagram-screen.md](./references/TECH-mermaid-state-diagram-screen.md)**
  - Description: TECH-mermaid-state-diagram-screen
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-no-dead-end-screens.md](./references/TECH-no-dead-end-screens.md)**
  - Description: TECH-no-dead-end-screens
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Validation check
    - Gotchas
    - Cross-references
- **[./references/TECH-prd-to-usecases.md](./references/TECH-prd-to-usecases.md)**
  - Description: TECH-prd-to-usecases
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-split-large-flows-subflow-linking.md](./references/TECH-split-large-flows-subflow-linking.md)**
  - Description: TECH-split-large-flows-subflow-linking
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-use-case-document-schema.md](./references/TECH-use-case-document-schema.md)**
  - Description: TECH-use-case-document-schema
  - TOC:
    - What it does
    - When to use
    - How it works
    - UC-001: [Short Name]
    - UC-002: [Next Short Name]
    - Minimal example
    - UC-001: User Registration
    - UC-002: User Login
    - Gotchas
    - Cross-references
- **[./references/TECH-wireframe-html-mobile-first.md](./references/TECH-wireframe-html-mobile-first.md)**
  - Description: TECH-wireframe-html-mobile-first
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-wireframe-index-inventory.md](./references/TECH-wireframe-index-inventory.md)**
  - Description: TECH-wireframe-index-inventory
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Validation pass
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-ux-flows/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.pl`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. PRD-derived Mermaid flows + HTML wireframes + use-case `.md` files). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/wireframes/` or `./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-ux-flows-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- [path/to/artifact.ext](./path/to/artifact.ext) — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Non-negotiables

- **`dev-browser` is the only authorized browser-automation primitive.** Any wireframe preview, inter-screen click-through, or live inspection routes through `bin/amw-dev-browser-wrapper.sh`. Chrome DevTools MCP is not used by this plugin — the upstream references in the original skill have been rewritten.
- **Figma Dev Mode MCP stays intact.** It is Figma-specific, opt-in, and only activated when the user explicitly says "export to figma". Never probe for it automatically.
- **Phase 3 is mandatory.** Reaching Phase 2 and then stopping (diagrams only, no clickable prototype) is a failure mode — the whole value of this skill is the wireframe handoff.
- **Pure-HTML prototypes.** Wireframes use `<a href>` navigation only; no JS, no form submits, no onclick. This guarantees the prototype works in any browser, preserves the back button, and makes Figma Code-to-Canvas export deterministic.
- **Wireframes are prototype-grade.** Dashed-border wireframe aesthetic, mobile-first 375px, no brand tokens, no real typography. Production HTML belongs to `../amw-ascii-to-html/` or direct design-principles output — not here.
- **No dead-end screens.** Every screen has at least one outgoing link. Enforced in the Phase 3 INDEX review.
- **Respect design-principles Rule 1.** If no PRD and no feature list, stop and ask — do not synthesize use cases.
- **Never silent on Figma.** Always present prerequisites before touching the Dev Mode MCP — per the upstream skill's original protocol.

## Failure modes

- **No PRD, no feature list.** The skill cannot proceed. Ask the user; optionally route them to `product-manager-toolkit` via `references/install-commands.md`.
- **Phase 2 stops before Phase 3.** The user gets Mermaid diagrams without a clickable prototype — a violation of this skill's contract. The orchestrator should abort and re-enter Phase 3.
- **Mermaid block rendering conflict.** When the output context already has a Mermaid renderer (e.g. this skill's output is embedded in another skill's HTML), use fenced `mermaid` blocks with unique IDs or delegate the render to `../amw-diagram-architecture/` instead.
- **Figma MCP requested but not installed.** Stop. Present the two-step install (preferences toggle + `claude mcp add ...`) from `references/install-commands.md`. Do not try alternate paths.
- **`dev-browser` CLI missing for preview.** Surface `/amw-doctor` and `/amw-init` to the user; the wireframes still open in any browser without the wrapper (Phase 3 always emits standalone HTML), but the plugin-standard mobile-viewport preview needs the CLI.
- **Wireframe aesthetic drift.** Filling the template with real colors, real images, or real typography pulls the output out of prototype territory. Keep the dashed-border greyscale look; anything else belongs to a downstream skill.
- **Inter-screen dead ends.** A screen with no outgoing link breaks the clickable prototype and fails Phase 3 review. Fix before emitting the INDEX.
