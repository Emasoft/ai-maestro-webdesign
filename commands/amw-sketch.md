---
name: amw-sketch
description: "Shortcut for users who want to enter the Phase A ASCII iteration loop directly — proposes wireframe variants, iterates on layout and components until satisfied, then hands off to /amw-ascii-to-html. An agent in Main-agent mode uses skills/amw-ascii-sketch/ via the orchestrator automatically as the default Phase A medium, and may apply additional techniques from that skill beyond what this command's parameters cover."
---

# /amw-sketch — ASCII plan-phase loop

This command is **the entire plan phase** for designing a webpage. The user explicitly wants to iterate on positions, sizes, alignments, and components in ASCII — not in HTML — because ASCII costs a tiny fraction of the tokens and renders instantly. HTML is only written after the user approves the final ASCII.

## The loop (this is the shape of the command, not a one-shot)

```
    ┌────────────────────────────────────────┐
    │  1. Orchestrator check (context etc.)  │
    └──────────────────┬─────────────────────┘
                       ▼
    ┌────────────────────────────────────────┐
    │  2. Emit 3 ASCII variants              │
    │     (baseline / advanced / experim.)   │
    └──────────────────┬─────────────────────┘
                       ▼
    ┌────────────────────────────────────────┐
    │  3. Ask: "Which direction? Any edits?" │
    └──────────────────┬─────────────────────┘
                       ▼
              User feedback
                       │
         ┌─────────────┼──────────────┐
         ▼             ▼              ▼
      "happy"    "tweak X in B"    "none of them"
         │             │              │
         │             ▼              ▼
         │     ┌───────────────┐  ┌─────────────────────┐
         │     │ Emit revised  │  │ Rewind to step 1    │
         │     │ ASCII; GOTO 3 │  │ with new assumptions│
         │     └───────────────┘  └─────────────────────┘
         ▼
    ┌────────────────────────────────────────┐
    │  4. Hand off to /amw-ascii-to-html      │
    │     with the approved ASCII            │
    └────────────────────────────────────────┘
```

The loop has no fixed iteration count. It terminates **only** when the user uses one of the canonical satisfaction tokens: `yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`. Ambiguous responses (`looks fine`, `I guess`, `ok`, `ok I guess`, `sure`) are NOT satisfaction — ask a clarifying question before proceeding. "ok" by itself is explicitly NOT approval (too ambiguous in English).

## Step 1 — Orchestrator check (run once, at the start of a new loop)

Before emitting the first variant set, confirm with the user:

1. **Context:** is there an existing design system, brand tokens, or reference site? If yes, note which constraints bound the variants. If no, say: "No design context yet — these variants are layout-only; tokens come later via `/amw-extract-style` or a user-provided UI kit."
2. **Canvas target:** desktop 1440-wide, mobile 375-wide, or slide 1920×1080? The ASCII must match proportions.
3. **Required elements:** logo, primary CTA, specific content blocks. These go into every variant.

Keep this preamble ≤ 3 sentences. Do not re-run it on subsequent iterations of the same loop — the context is already established.

## Step 2 — Produce the variants

Use Unicode box-drawing characters — `┌─┐│└┘├┤┬┴┼→↓←↑` — at roughly 60 to 80 columns wide. Each variant carries a short caption that names its design decision and the trade-off.

Layout as three fenced code blocks in order, each preceded by a caption line:

```
### A — Baseline (safe, follows convention)
Design decision: Hero → 3-col features → CTA → footer. Z-pattern.
Trade-off: Familiar; low memorability.

┌──────────────────────────────────────────────────┐
│  LOGO                                 [sign in] │
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

...
```

Three variants must sit on a clear scale:

- **A — Baseline:** The most common pattern for this intent. Safe, Jakob's-Law-compliant, zero experimentation.
- **B — Advanced:** Keeps the convention's skeleton but shifts one dimension hard — typography-led hero, asymmetric grid, unexpected CTA placement.
- **C — Experimental:** Breaks the template. New metaphor, novel layout, unusual density. Flag risks explicitly in the caption.

Do not mix them — each should be internally consistent.

## Step 3 — Solicit feedback and iterate

After presenting the variants, ask directly: *"Which direction? Any edits to position, size, alignment, or components before I go further? When you're happy, say so explicitly and I'll convert to HTML."*

Handle the response:

- **User picks one variant, wants changes.** Emit a **revised ASCII** (just the chosen variant, with the requested changes applied). Same caption structure. Ask again for feedback. Loop.
- **User mixes A and B, or A and C.** Emit one consolidated ASCII that combines the requested features. Ask again for feedback. Loop.
- **User rejects all three.** Rewind to step 1, probe for what was wrong (too generic? wrong canvas target? missed a required element?), and emit three new variants. Do not loop back into step 2 blind.
- **Ambiguous response** (`looks good`, `interesting`, `ok`, `ok I guess`, `sure`, `fine`). Do NOT treat as satisfaction. Ask: *"To confirm — should I generate the HTML now, or do you want more changes first?"*
- **Explicit satisfaction** — one of the canonical tokens: `yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`. Proceed to step 4.

Each iteration is one revised ASCII block + one question. No prose essays between iterations. Stay token-cheap.

## Step 4 — Hand off

Once the user confirms: save the final ASCII to `/tmp/amw-sketch-<slug>-final.txt` and suggest: *"ASCII approved. Running `/amw-ascii-to-html` now against this sketch — it will produce the real HTML using design-principles tokens."*

If the user has not yet run `/amw-extract-style <url>` and wants tokens from a reference site, offer that as the step before conversion.

## AI-slop checks on the sketches themselves

Even at ASCII fidelity, check each emitted variant against [ai-slop-avoid](skills/amw-design-principles/ai-slop-avoid.md):

- No "hero → 3-col icons → testimonials → CTA → footer" stamped three times in a row (item 10).
- No fake "Sarah J. CEO of TechCorp" testimonials (item 15).
- No "10x growth" fabricated stats (item 16).
- Every element should earn its place (§ VII of ai-slop-avoid).

If a variant slides toward any of these, rework it before showing.

## Do NOT

- Write any `.html` file at any point in this command. HTML is `/amw-ascii-to-html`'s job.
- Skip the orchestrator check at the start of a new loop.
- Produce fewer than three variants on the first turn.
- Treat ambiguous user acknowledgement as explicit satisfaction.
- Dump prose paragraphs explaining the variants — captions stay to 1–2 lines each.

## When to use

- User has stated a design intent ("dashboard for a devtools team", "landing page for a crypto protocol", "poster for an event") but has not given a concrete layout.
- Design-principles Rule 2 (≥ 3 variants) applies; ASCII is the cheapest medium for satisfying it.
- User has not yet supplied or confirmed a design system. If they have, still run this step — picking ASCII direction first keeps token/component choices from over-constraining layout.

