---
name: TECH-type-selection-rule
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-type-selection-rule

## What it does

Picks the right editorial diagram type for the user's intent, and —
critically — refuses to draw when a sentence or a table would do the job
better. The selection rule is not a cute heuristic; it is the anti-slop
guard at the front door.

## When to use

- **Every user request**, before any HTML is emitted.
- **Whenever the user's wording is generic** ("make a diagram", "visualize
  this"). Ask a clarifying question rather than guessing.
- **Whenever two types could fit**, pick the more specific one (state
  machine over flowchart if lifecycles are involved; swimlane over
  flowchart if cross-actor handoffs are involved).

## How it works

**Step 1 — Gate question:** "Would a reader learn more from this than
from a well-written paragraph?" If **no** → don't draw. Write the
sentence. If **yes** → continue.

**Step 2 — Map intent to canonical type:**

| Reader needs to see | Type |
|---|---|
| Components + connections (services, APIs, infra) | architecture |
| Decision logic, yes/no branches | flowchart |
| Messages over time between actors | sequence |
| States + transitions of a single entity | state machine |
| Entities + fields + relationships | ER / data model |
| Events on a time axis | timeline |
| Cross-functional flow (who does what, when) | swimlane |
| Two-axis positioning | quadrant |
| Hierarchy by containment | nested |
| Parent → children | tree |
| Stacked abstractions | layer stack |
| Set overlap (2–3 circles) | Venn |
| Ranked hierarchy / conversion funnel | pyramid |

**Step 3 — Exit conditions.** If none of the types cleanly fits:
- Before-after comparison → use a **table**, not a diagram.
- Simple list → use **bullets**.
- Single-shape "diagram" (one box, one label) → **write the sentence**.
- Quick ASCII for a terminal or tweet → route to `../../amw-ascii-sketch/`
  or a wiretext tool; editorial HTML+SVG is overkill.

**Step 4 — User override.** If the user explicitly asked for a type ("make
this a swimlane, not a flowchart"), honour that — don't silently switch.

## Minimal example

Ambiguous intent:

```
User: "Visualize the checkout flow"
Agent: Ambiguous — could be flowchart (decision logic), swimlane
       (cross-functional handoffs), or sequence (client-API messages).
       Ask one question:
         "Is the focus on decision branches (flowchart), on who does
          what between design/eng/support (swimlane), or on the HTTP
          messages between client and services (sequence)?"
```

Clear intent:

```
User: "Draw the OAuth 2.0 handshake"
Agent: This is sequence — OAuth is fundamentally time-ordered messages
       between Browser, Auth Server, Resource Server.
       → Load references/TECH-type-sequence.md.
```

Correct refusal:

```
User: "Diagram our login button"
Agent: A single-shape diagram is a sentence. Instead:
       "Users click the 'Log in' button in the top-right nav to start
        the OAuth handshake."
```

## Gotchas

- **The gate question is non-negotiable.** Defaulting to "draw it anyway"
  produces AI-slop visualizations. Always ask whether the diagram adds
  reader value over prose.
- **Type specificity wins.** State machine over flowchart; swimlane over
  flowchart; ER over architecture. The more specific primitive carries
  more meaning per pixel.
- **Never silently substitute.** If the user said "flowchart" and you
  think "state machine" is actually right, surface the observation:
  *"This looks like state transitions — would state-machine fit better?
  Your call."*
- **Overview + detail beats one huge diagram.** If none of the 13 types
  fits at the intended density, split the subject into two diagrams
  rather than inventing a hybrid.

## Cross-references

- [SKILL](../SKILL.md) — the orchestrator; this rule runs at the top of every
  request
- Each of the 13 `<TECH-type-*.md>` files in this same directory carries its own "when to use"
  stricture that narrows further
- [TECH-density-4-of-10](TECH-density-4-of-10.md) — density rule; a subject that needs 15+
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  nodes should split, not pick a denser type
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — Default-to-deletion is
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
  codified there
