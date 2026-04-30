---
name: amw-ascii-sketch
description: Runs the ASCII plan-phase iteration loop. Triggers when design-principles has decided that a webpage design's plan phase is best explored in ASCII before committing to HTML. Specific triggers — "sketch this in ASCII", "give me layout variants", "propose 3 wireframes in ASCII", "iterate on the layout in ASCII", "ASCII mockup", "box-drawing wireframe". Does NOT self-trigger on broad "design", "make a page", "UI", "landing page", "mockup", "prototype" — those belong to design-principles, which then routes here as its default plan-phase executor.
version: 0.1.0
---

# ASCII Sketch — plan-phase loop

> **Orchestrated by:** `../amw-design-principles/SKILL.md` — this skill is the **default** plan-phase executor for webpage design in this plugin. It is not a fast-path alternative; it is the first thing that should run after design-principles has captured context.

## Activation

Callable via the `/amw-sketch` command (user shortcut — fast entry with explicit parameters), or invoked automatically by the `design-principles` orchestrator as the default Phase A medium after context is gathered in Main-agent mode. In Main-agent mode the orchestrator may apply iteration techniques from this skill beyond what the `/amw-sketch` command parameters expose.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**PLAN (Phase A).** This skill owns the Phase A portion of any webpage design in Main-agent mode. It runs a bounded iteration loop in ASCII until the user explicitly approves a direction, then hands off the approved sketch to `../amw-ascii-to-html/` for HTML conversion in Phase B. It does not emit HTML itself; it does not write files on intermediate loop turns; it lives entirely in chat output.

## Why ASCII, not HTML

- **Token cost.** ASCII costs roughly one percent of the tokens that iterating on real HTML does. A user can push ten or more revisions without hitting context decay or summarization.
- **Synchronous feedback.** ASCII is rendered instantly in chat — no file write, no browser round trip, no `dev-browser` screenshot, no `amw-preview` step.
- **Easy to describe edits against.** Layout changes map naturally to ASCII ("move the CTA to the right of the hero", "make the feature row 2×2 instead of 3×1", "swap the sidebar to the right edge"). Describing the same edit against rendered HTML is always slower and more error-prone.
- **Commits to nothing.** Typography, color, radius, shadow, and other token choices do not exist in ASCII — so they cannot over-constrain layout decisions. The user picks a skeleton first, tokens after.

## The loop (this is the shape of the skill, not a one-shot)

```
               ┌───────────────────────────────┐
               │  User invokes (via orchestr.  │
               │  or directly via /amw-sketch)  │
               └──────────────┬────────────────┘
                              ▼
               ┌───────────────────────────────┐
       ┌──────▶│  Step 1 — Orchestrator check  │
       │       │   (run once per new loop)     │
       │       └──────────────┬────────────────┘
       │                      ▼
       │       ┌───────────────────────────────┐
       │       │  Step 2 — Emit 3 ASCII vars   │
       │       │   A = Baseline                │
       │       │   B = Advanced                │
       │       │   C = Experimental            │
       │       └──────────────┬────────────────┘
       │                      ▼
       │       ┌───────────────────────────────┐
       │       │  Step 3 — Ask for feedback    │
       │       │   "Which direction? Any       │
       │       │    edits before I go further? │
       │       │    When happy, say so so I    │
       │       │    can convert to HTML."      │
       │       └──────────────┬────────────────┘
       │                      ▼
       │                User feedback
       │                      │
       │  ┌───────────────────┼────────────────────┐
       │  ▼                   ▼                    ▼
       │ Ambiguous        Picks one /         Rejects all
       │ acknowledge      mixes / tweaks      three variants
       │  │                   │                    │
       │  ▼                   ▼                    ▼
       │ Probe:           ┌──────────┐       ┌──────────────┐
       │ "Convert         │ Emit a   │       │ Rewind to    │
       │  now, or         │ revised  │       └──┬ Step 1 with─┘
       │  more            │ single   │          │ new probing
       │  changes?"       │ ASCII;   │          │ questions;
       │  │               │ GOTO 3   │          │ then GOTO 2
       │  └───────────────┴──────────┘          └─────┬──────┘
       │                      │                       │
       └──────────────────────┴───────────────────────┘
                              ▲
                              │ (loop continues until
                              │  EXPLICIT satisfaction)
                              │
                              ▼
               ┌───────────────────────────────┐
               │  Step 4 — Hand off            │
               │   Save /tmp/amw-sketch-        │
               │   <slug>-final.txt →          │
               │   route to ../amw-ascii-to-html/  │
               └───────────────────────────────┘
```

The loop has no fixed iteration count. It terminates **only** when the user produces an **explicit** satisfaction token. Ambiguous acknowledgement is NOT approval — see Step 3 below.

## Step 1 — Orchestrator check (run once at the start of a new loop)

Before emitting the first variant set, confirm with the user in ≤ 4 sentences:

1. **Context.** Is there an existing design system, brand tokens, or reference site? If yes, note which constraints bound the variants. If no, say out loud: *"No design context yet — these variants are layout-only; tokens will come later via `/amw-extract-style` or a user-supplied UI kit."* This preserves Rule 1 from `../amw-design-principles/SKILL.md` — context before designing.
2. **Canvas target.** Desktop 1440-wide, mobile 375-wide, or slide 1920×1080? The ASCII column count and aspect ratio must match the canvas. A desktop sketch and a mobile sketch are not the same shape and must not be drawn as if they were.
3. **Surface.** Where does the sketch get pasted while iterating? This determines the ASCII width ceiling — not the eventual HTML canvas. Source: `cc-plugin-text-visualizations-main` — every text-visual skill asks "what surface?" first because column width is the single biggest determinant of ASCII layout and cannot be fixed retroactively.

   | Surface | ASCII width ceiling |
   |---|---|
   | GitHub PR / issue / README | 100 cols |
   | Terminal, `--help` panel, code comment | 78-80 cols |
   | Slack / Discord / Notion message | 80 cols |
   | Generic desktop chat (before HTML conversion) | 80-100 cols |
   | Slide deck preview (pre-1920×1080 render) | 80-120 cols |

   **Rule:** if the user has not specified, default to 80 cols on the iteration turns and tell them — "drawing at 80 cols so it pastes cleanly in chat; the eventual HTML canvas will be `<canvas target>`." If the user is on GitHub specifically, bump to 100 so PR reviewers see the whole sketch without wrapping.

4. **Required elements.** Logo, primary CTA, specific content blocks the user has already named. These must appear in every one of the three variants — they are the user's hard constraints.

**Lane-labeled variants.** When the sketch's subject is a dashboard, console, or multi-panel layout with named regions ("sidebar + main content", "header + body + footer"), represent those regions as `lanes` in `bin/amw-ascii-render.py` input rather than as freeform boxes. Each lane gets a left-margin label (`Nav`, `Content`, `Actions`, etc.) and the renderer aligns the rows automatically. See `../amw-ascii-validator/SKILL.md` § Lane-labeled subsection for the JSON shape. Use this when the user's brief mentions explicit named panels; fall back to freeform boxes when the structure is more organic.

Do NOT re-run this check on subsequent iteration turns of the same loop. The context is already established; re-running wastes turns. A fresh loop (new sketch subject, user abandoned the previous direction and started over) does re-run it.

If the user has not supplied enough context to answer any of the four questions, pull from `../amw-design-principles/question-templates.md` — ask the minimum questions needed to answer 1, 2, 3, and 4, and wait for the user.

## Validation gate (MANDATORY, runs between variant generation and presentation)

Every variant this skill emits MUST pass `../../bin/amw-validate-ascii.pl` before being shown to the user. LLMs cannot count characters reliably — this validator is how the plugin compensates.

The flow:

1. Generate a variant.
2. Write it to `/tmp/amw-sketch-<slug>-<variant>.txt`.
3. Run `perl ../../bin/amw-validate-ascii.pl /tmp/amw-sketch-<slug>-<variant>.txt`.
4. If PASS → include in the presented set.
5. If FAIL → apply every `FIX:` hint in the validator output, re-run. Loop until PASS.
6. Never present an un-validated variant.

For strongly-structured diagrams (flowcharts, tables, sequences, layered architecture) use `../../bin/amw-ascii-render.py` to GENERATE the ASCII from structured JSON — it guarantees alignment by construction. See `../amw-ascii-validator/SKILL.md` for the JSON schema and the validation contract.

Before generation, substitute every BANNED character (`▼ ▲ ▶ ◀ ⟶ ⇒`) with a safe equivalent (`v ^ > <` or `->` / `=>` / `→`), and replace emoji state-markers with ASCII (`[!]`, `(*)`, `[x]`, `[ ]`) — the validator flags these as forbidden because they render at variable width in common monospaced fonts.

## Step 2 — Produce the three variants

Use Unicode box-drawing characters: `┌─┐│└┘├┤┬┴┼→↓←↑`. Width ≈ 60–80 columns. Three fenced code blocks in order, each preceded by a one-line caption that names the design decision and the trade-off.

Each variant sits on a clear scale — from safe to risky — and each is internally consistent (do not mix the scales inside one variant):

- **A — Baseline.** The safest, most conventional pattern for this intent. Jakob's-Law compliant, zero experimentation. If the user has a design system, this one follows it strictly.
- **B — Advanced.** Keeps the conventional skeleton but shifts exactly one dimension hard — typography-led hero, asymmetric grid, unexpected CTA placement, or similar. One dimension, not three.
- **C — Experimental.** Allowed to break the template. New metaphor, novel layout, unusual density. Flag the risks explicitly in the caption ("requires very confident copy", "loses screenshot-driven trust signal", "depends on custom illustration").

The three variants must differ on a **real design dimension** — layout shape, information hierarchy, hero strategy, CTA placement. They must not be three trivial visual re-skins of the same wireframe.

Example of the shape of the output (desktop canvas):

```
### A — Baseline (safe, follows convention)
Design decision: Hero → 3-col features → CTA → footer. Z-pattern reading flow.
Trade-off: Familiar; low memorability.

┌──────────────────────────────────────────────────┐
│  LOGO                                 [sign in]  │
├──────────────────────────────────────────────────┤
│                                                  │
│        HEADLINE SPANS TWO LINES                  │
│        Subcopy one sentence                      │
│                              [ Primary CTA ]     │
│                                                  │
├──────────────┬──────────────┬───────────────────┤
│  Feature 1   │  Feature 2   │  Feature 3        │
│  one line    │  one line    │  one line         │
├──────────────┴──────────────┴───────────────────┤
│              [ Start for free ]                  │
├──────────────────────────────────────────────────┤
│  © Year · Docs · Privacy                         │
└──────────────────────────────────────────────────┘

### B — Advanced (typographic hero, editorial)
Design decision: Oversized typographic hero, no screenshot, editorial split.
Trade-off: Requires confident copy; loses screenshot-driven trust signal.

... (second ASCII block here) ...

### C — Experimental (vertical narrative, no hero)
Design decision: Opens on a single-line claim; scroll-driven narrative replaces hero.
Trade-off: Unfamiliar pattern; risky if the brand tone is conservative.

... (third ASCII block here) ...
```

Do NOT produce fewer than three variants on the first turn of a new loop. Do NOT produce more than three — a fourth variant overloads the decision and muddies feedback.

## Step 3 — Solicit feedback and iterate

After presenting the three variants, ask directly (one question, no paragraphs of prose):

> *"Which direction? Any edits to position, size, alignment, or components before I go further? When you're happy, say so explicitly and I'll convert to HTML."*

Then handle the response using this decision table:

| User response | What the skill does |
|---|---|
| Picks one variant + wants specific edits ("B but move the CTA right of the hero") | Emit a **revised ASCII** — just the chosen variant with edits applied. Same caption structure. Ask again. Loop. |
| Mixes two variants ("A's hero with B's footer") | Emit **one consolidated ASCII** that combines the requested pieces. Ask again. Loop. |
| Rejects all three ("none of these work") | Rewind to Step 1. Probe for what was wrong: too generic, wrong canvas, missed a required element, wrong vibe. Emit three **new** variants afterwards. Do not loop back into Step 2 blind. |
| Ambiguous acknowledgement ("looks fine", "ok I guess", "sure", "interesting", "not bad") | **This is NOT approval.** Probe: *"To confirm — should I generate the HTML now, or do you want more changes first?"* Loop. |
| Explicit satisfaction — canonical set: "yes", "ship it", "convert it", "that's the one", "perfect", "done" | Proceed to Step 4. |

Each iteration turn is exactly one revised ASCII block plus one question. No prose essays between iterations. No meta-commentary on what was changed. Stay token-cheap — that is the entire reason ASCII-first exists.

## Step 4 — Hand off to `ascii-to-html`

Once the user has produced an explicit satisfaction token:

1. Derive a short kebab-case slug from the sketch subject (e.g. `devtools-dashboard`, `crypto-landing`, `event-poster`).
2. Save the final approved ASCII to `/tmp/amw-sketch-<slug>-final.txt`. This file is the single source of truth for the downstream HTML conversion — do not re-describe the layout in prose.
3. Tell the user: *"ASCII approved. Running `/amw-ascii-to-html` against this sketch now — it will produce the real HTML using design-principles tokens and the selected starter-component chrome."*
4. Hand off control to `../amw-ascii-to-html/SKILL.md`.

Before handing off, if the user has not yet extracted tokens from a reference site and has not supplied a brand kit, offer that step: *"If you have a reference site, `/amw-extract-style <url>` will pull its color, type, and spacing tokens first — that will make the HTML match the brand instead of using generic defaults."* This is an offer, not a gate — the user can decline and let the conversion run on design-principles' fallback tokens.

## AI-slop checks applied to every ASCII variant

Even at ASCII fidelity — before ever emitting a variant to the user — scan each one against `../amw-design-principles/ai-slop-avoid.md`. The skeleton is the first place AI slop leaks in. Highlights to check:

- Item 10: No "hero → 3-col icons → testimonials → CTA → footer" stamped across all three variants. If A, B, and C all use that same rhythm, the user has been given one answer dressed three ways.
- Item 15: No fake testimonials ("Sarah J., CEO of TechCorp" with a fabricated quote).
- Item 16: No fabricated statistics ("10x growth", "500% increase") inserted for visual weight.
- § VII: Every block on the page must earn its place. If a section exists only because "landing pages usually have one", cut it.

If a variant slides toward any of these, rework it before showing the user. Do not ship slop and rely on the user to catch it.

## Dependencies

- **runtime_binaries:** none.
- **python_packages:** none.
- **npm_packages:** none.
- **mcp_servers:** none.
- **scripts:** none (this skill is pure chat output).

`../../bin/amw-ascii-parse.py` is referenced only by the downstream `ascii-to-html` skill for parsing the handed-off file; it is not invoked from within this loop.

## Cross-references

- `../amw-design-principles/SKILL.md` — orchestrator. The three hard rules apply to every variant emitted here.
- `../amw-design-principles/ai-slop-avoid.md` — applied per variant as described above.
- `../amw-design-principles/question-templates.md` — source of the questions used in the Step 1 orchestrator check when context is missing.
- `../amw-ascii-to-html/SKILL.md` — the **terminal handoff**. The approved ASCII file at `/tmp/amw-sketch-<slug>-final.txt` is the input contract.
- `../amw-ascii-to-svg/SKILL.md` — the adjacent skill for the subset of ASCII sketches that are actually diagrams (boxes and arrows describing a system), not wireframes. If the user's intent was a diagram, route there instead.
- `../amw-ux-flows/SKILL.md` — when the user already has a PRD, the flow is `ux-flows` first (PRD → flow diagrams → wireframe intent), then `ascii-sketch` for variant exploration on the chosen wireframe. Both routes are valid.
- `../../bin/amw-preview-server.py` — optional multi-variant HTML comparison server, used **after** handoff if the user wants to see the rendered HTML side by side. Not used inside this loop.
- `/amw-sketch` — the user-facing slash command (at `../../commands/amw-sketch.md`) that invokes this skill.

## Non-negotiables

- Does NOT write any `.html` file, at any point, on any turn. Output stays in chat as ASCII. HTML is the next skill's job.
- Does NOT skip the Step 1 orchestrator check on a **new** loop. (Can and must skip it on iteration turns of the **same** loop.)
- Does NOT produce fewer than three variants on the first turn of a new loop.
- Does NOT produce more than three variants on the first turn — a fourth muddies the decision.
- Does NOT treat ambiguous user acknowledgement ("looks fine", "ok", "sure", "interesting") as explicit satisfaction. Probe first.
- Does NOT emit three variants that are trivial visual re-skins of each other. Variants must differ on a real design dimension — layout shape, information hierarchy, hero strategy, CTA placement.
- Does NOT dump prose paragraphs between iterations. Captions stay to one or two lines. Each iteration turn is one ASCII block plus one question.
- Does NOT auto-trigger on the broad design vocabulary (`design`, `UI`, `landing page`, `mockup`, `prototype`, `make a page`). Those belong to `../amw-design-principles/`, which then routes here.

## Failure modes and how to recover

| Failure mode | Recovery |
|---|---|
| User says "great", "looks good", "nice" — no explicit commit to convert. | Do NOT proceed to Step 4. Probe: *"To confirm — convert to HTML now, or more changes first?"* |
| User pastes their own ASCII and asks for variants. | Treat the paste as an existing Variant A. Emit B and C as departures from it. Skip Step 1's canvas check if the paste answers it unambiguously. |
| User rejects all three variants three loops in a row. | Escalate. This is almost always a Rule 1 (context) failure — the orchestrator check missed something critical. Stop emitting variants, re-open the context conversation, and consider falling back to `../amw-ui-ux-reasoning/` for a broader palette of visual directions. |
| User asks "which one is best?" | Do not pick for them. Briefly name each variant's strength ("A is safest, B is most distinctive, C is most memorable but riskiest") and ask again. The skill's job is to offer options, not to decide. |
| User's brief shifts mid-loop ("actually, make it a dashboard, not a landing page"). | This is a new loop. Drop the current state. Re-run Step 1, then Step 2. Do not try to salvage the previous three variants — they were answering a different question. |
| User pastes a rendered screenshot and asks for ASCII variants of it. | Describe the screenshot's structure in Step 1 as the baseline constraint, then emit three variants that each preserve the screenshot's essential shape but shift one dimension. This is the screenshot acting as the user's design reference. |
