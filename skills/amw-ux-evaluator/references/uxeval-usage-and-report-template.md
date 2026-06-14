# UX Evaluator — usage workflow and report template

The four-step evaluation workflow and the canonical Markdown report template.
This is the detail behind the SKILL.md `## Usage` summary; the SKILL.md keeps
only the pointer, the full procedure lives here.

## Usage

Invoked by `/amw-eval [file.html | url]` or directly on an evaluation trigger.

**Step 1 — Gather context.** Identify the component, the reason for evaluation, and the input source. Classify the component's role (primary CTA, secondary action, utility control, navigation, form field).

**Step 2 — Score the 3 dimensions.** For every inspected component:

| Dimension | What to analyze | Key questions |
|---|---|---|
| **Position** | Location relative to other elements, reading flow, adjacency | Does position follow conventions (primary right, utility far right)? Discoverable? |
| **Visual Weight** | Fill vs ghost vs icon-only, color, shadow, size, font weight | Does it compete with the primary action? Is the hierarchy legible at a glance? |
| **Spacing** | Gaps from adjacent elements, touch target, rhythm | Adequate separation (≥ 8 px intra-group, ≥ 24 px between groups)? Touch targets ≥ 44 × 44 px mobile? |

Each dimension gets one of: **Pass** (matches convention), **Warn** (acceptable but suboptimal — improvement attached), **Fail** (breaks convention or accessibility floor — recommendation mandatory).

**Step 3 — Report.** Markdown output, every Fail / Warn citing concrete evidence (selector, computed-style value, DOM attribute, measured pixel distance). Prose-only verdicts are rejected.

```markdown
## [Component Name] Evaluation

### Current State
- **Position:** [selector + coordinates]
- **Visual Weight:** [selector + computed-style evidence]
- **Spacing:** [measured gaps + selector pairs]

### Analysis
| Dimension | Verdict | Evidence | Rationale |
|---|---|---|---|
| Position | Pass / Warn / Fail | `selector` + value | Why + cited convention |
| Visual Weight | Pass / Warn / Fail | `selector` + computed-style | Why + cited convention |
| Spacing | Pass / Warn / Fail | measured gap + selectors | Why + cited convention |

### Verdict: PASS / NEEDS CHANGES

### Recommendations
| Priority | Change | Evidence | Cited principle |
|---|---|---|---|
| P1 | [Specific change] | [selector / value] | [e.g. Balsamiq #4 — primary on right] |
| P2 | [Specific change] | [selector / value] | [e.g. Nielsen #4 — consistency] |
```

**Priority rubric:** **P1** breaks UX (wrong button order, inaccessible touch target, buried primary, contrast below AA). **P2** suboptimal but usable (tight spacing, non-standard utility placement, weak label). **P3** polish only (token drift, micro-alignment, aesthetic).

**Step 4 — Hand off.** All Pass → emit report and stop. Warnings only → report; user decides. Fails present → recommendations return to `design-principles`, which decides patch-in-place vs re-enter `../amw-ascii-sketch/`.
