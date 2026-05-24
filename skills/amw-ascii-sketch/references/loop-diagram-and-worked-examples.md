# ASCII Sketch loop diagram and worked examples

Companion reference for [SKILL](../SKILL.md). The main SKILL.md describes the workflow in prose; this file provides the visual loop diagram and a worked Mode A example so the orchestrator can stay under the SKILL.md size cap.

## The loop diagram

```
               +-------------------------------+
               |  User invokes (via orchestr.  |
               |  or directly via /amw-sketch) |
               +---------------+---------------+
                               |
                               v
               +-------------------------------+
       +------>|  Step 1 - Orchestrator check  |
       |       |   (run once per new loop)     |
       |       +---------------+---------------+
       |                       |
       |                       v
       |       +-------------------------------+
       |       |  Step 2 - Emit 3 ASCII vars   |
       |       |   A = Baseline                |
       |       |   B = Advanced                |
       |       |   C = Experimental            |
       |       +---------------+---------------+
       |                       |
       |                       v
       |       +-------------------------------+
       |       |  Step 3 - Ask for feedback    |
       |       |   "Which direction? Any       |
       |       |    edits before I go further? |
       |       |    When happy, say so so I    |
       |       |    can convert to HTML."      |
       |       +---------------+---------------+
       |                       |
       |                 User feedback
       |                       |
       |  +--------------------+---------------------+
       |  v                    v                     v
       | Ambiguous         Picks one /          Rejects all
       | acknowledge       mixes / tweaks       three variants
       |  |                    |                     |
       |  v                    v                     v
       | Probe:           +----------+        +-----------------+
       | "Convert         | Emit a   |        | Rewind to       |
       |  now, or         | revised  |        +-+ Step 1 with   |
       |  more            | single   |          | new probing   |
       |  changes?"       | ASCII;   |          | questions;    |
       |  |               | GOTO 3   |          | then GOTO 2   |
       |  +---------------+----------+          +------+--------+
       |                       |                       |
       +-----------------------+-----------------------+
                               ^
                               | (loop continues until
                               |  EXPLICIT satisfaction)
                               |
                               v
               +-------------------------------+
               |  Step 4 - Hand off            |
               |   Save /tmp/amw-sketch-       |
               |   <slug>-final.txt to         |
               |   route to ../amw-ascii-to-html/ |
               +-------------------------------+
```

The loop has no fixed iteration count. It terminates **only** when the user produces an **explicit** satisfaction token (`yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`). Ambiguous acknowledgement is NOT approval — see Step 3 in the parent SKILL.md.

## Mode A worked example (Mode A is preferred)

Given user intent: *"flowchart of a user login sequence with 3 decision points"*

**Step 1 — Author the JSON spec:**

```json
{
  "mode": "diagram",
  "title": "User Login Flow",
  "nodes": [
    { "id": "start",    "label": "Start" },
    { "id": "input",    "label": "Enter credentials" },
    { "id": "valid",    "label": "Credentials valid?" },
    { "id": "mfa",      "label": "MFA required?" },
    { "id": "mfaok",    "label": "MFA code valid?" },
    { "id": "home",     "label": "Go to Home" },
    { "id": "fail",     "label": "Show error" }
  ],
  "edges": [
    { "from": "start",  "to": "input" },
    { "from": "input",  "to": "valid" },
    { "from": "valid",  "to": "mfa",   "label": "yes" },
    { "from": "valid",  "to": "fail",  "label": "no" },
    { "from": "mfa",    "to": "mfaok", "label": "yes" },
    { "from": "mfa",    "to": "home",  "label": "no" },
    { "from": "mfaok",  "to": "home",  "label": "ok" },
    { "from": "mfaok",  "to": "fail",  "label": "fail" }
  ]
}
```

**Step 2 — Render:**

```bash
python3 ../../bin/amw-ascii-render.py --mode diagram --in /tmp/login-flow.json --out /tmp/login-flow.txt
```

**Step 3 — Validate (should be PASS on first run):**

```bash
python3 ../../bin/amw-validate-ascii.py /tmp/login-flow.txt
```

The rendered `/tmp/login-flow.txt` is the variant. No LLM hand-authoring, no alignment guessing, no retry loop needed for a clean structured input.

## Example variant set (Step 2 output shape)

This is the shape Step 2 must produce on the first turn of a new loop — three captioned blocks, A / B / C, in a single chat reply, each fenced with a one-line design-decision caption + trade-off line.

```
### A - Baseline (safe, follows convention)
Design decision: Hero -> 3-col features -> CTA -> footer. Z-pattern reading flow.
Trade-off: Familiar; low memorability.

+--------------------------------------------------+
|  LOGO                                 [sign in]  |
+--------------------------------------------------+
|                                                  |
|        HEADLINE SPANS TWO LINES                  |
|        Subcopy one sentence                      |
|                              [ Primary CTA ]     |
|                                                  |
+--------------+--------------+--------------------+
|  Feature 1   |  Feature 2   |  Feature 3         |
|  one line    |  one line    |  one line          |
+--------------+--------------+--------------------+
|              [ Start for free ]                  |
+--------------------------------------------------+
|  (c) Year - Docs - Privacy                       |
+--------------------------------------------------+

### B - Advanced (typographic hero, editorial)
Design decision: Oversized typographic hero, no screenshot, editorial split.
Trade-off: Requires confident copy; loses screenshot-driven trust signal.

... (second ASCII block here) ...

### C - Experimental (vertical narrative, no hero)
Design decision: Opens on a single-line claim; scroll-driven narrative replaces hero.
Trade-off: Unfamiliar pattern; risky if the brand tone is conservative.

... (third ASCII block here) ...
```

Do NOT produce fewer than three variants on the first turn of a new loop. Do NOT produce more than three — a fourth variant overloads the decision and muddies feedback.

## Cross-references

- [SKILL](../SKILL.md) — the parent skill.
- [SKILL](../../amw-ascii-validator/SKILL.md) — mandatory validation gate.
- [SKILL](../../amw-ascii-to-html/SKILL.md) — terminal handoff after explicit satisfaction.
- [SKILL](../../amw-design-principles/SKILL.md) — orchestrator that routes here by default for webpage design plan-phase.
