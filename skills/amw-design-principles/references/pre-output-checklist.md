# Pre-Output Checklist — Phase B Gate

Loaded by `amw-design-principles` (the orchestrator) and consumed during Phase B.

This is the main-agent's mandatory pre-flight gate. Run it before delivering **any** visual
output (HTML, SVG, wireframe, diagram, infographic, email). If any answer is "no", revise
before presenting — senior designers iterate, they do not ship first drafts.

## Table of Contents

- [I. The 7-Point Gate](#i-the-7-point-gate)
- [II. Final Gut Check](#ii-final-gut-check)
- [III. How to use this gate in Phase B](#iii-how-to-use-this-gate-in-phase-b)

---

## I. The 7-Point Gate

### 1. Visual Hierarchy

> Is there one clear focal point? Can you trace the intended reading order from most to least important?

Every screen needs a single visual anchor. If two elements compete at the same weight, one must yield.
Test: trace your eye path across the output. If it bounces randomly, hierarchy is broken.

### 2. Color

> Does every color serve a functional purpose? Is text contrast at minimum 4.5:1? Are three or fewer intentional colors present in this component?

Decorative color is noise. Functional color (status, hierarchy, emphasis, interaction) is signal.
Squint at the output — the colors that pop should be the ones that matter most.

### 3. Spacing

> Are spatial relationships deliberate? Do related items group together? Does internal padding differ from external gaps?

Spacing communicates grouping. Items 8 px apart feel related; items 32 px apart feel separate.
Internal card padding should be less than the gap between cards.

### 4. System Fidelity

> Does this follow the project's existing patterns? Are all values sourced from the design system? Any magic numbers or one-off values?

Extend the existing system — never fight it. If no system exists, default to refined minimalism.
Every spacing, color, font-size, and radius value should be traceable to a token.

### 5. Restraint

> Can anything be removed without losing meaning or function? Did you default to less rather than more?

Borders, shadows, icons, badges, labels — question every element. Fewer elements executed well
always beats many elements competing. If you can remove it and nothing breaks, remove it.

### 6. Interactive States

> Have you considered hover, focus, active, disabled, loading, empty, and error? (You don't need all of them, but you need to have *considered* each one.)

Shipping a component without thinking about states is shipping an incomplete component.
At minimum: hover, focus-visible, disabled, and error states must be intentional or explicitly deferred.

### 7. Responsive

> Will this work at 375 px, 768 px, and 1200 px+? What is the content priority on mobile?

Mobile is not a shrunk desktop. Rethink the information hierarchy for each breakpoint.
Touch targets must be at least 44 × 44 px. Typography must scale, not just shrink.

---

## II. Final Gut Check

> "Would a senior designer ship this, or would they send it back for another pass?"

If there is any hesitation, do another pass. The question is not "is this acceptable?" but "is
this the best version of itself?"

---

## III. How to use this gate in Phase B

The gate is a blocking check, not an advisory. Before any sub-agent (wireframe-builder,
diagram-producer, infographic-builder, email-designer) delivers its output to the user, the
orchestrator runs this checklist against the artifact. The 7 yes/no questions take under a
minute against a rendered artifact; they prevent the most common failure modes of AI-generated UI.

**Gate position in the workflow:**

```
Phase A approval → sub-agent produces artifact → orchestrator runs 7-point gate → delivery
```

If an item fails, the orchestrator instructs the sub-agent to revise that dimension before
returning to the user. The revision is silent (not shown to the user unless the issue is
architectural and requires a re-brief).

---

*Sources: agave / SKILL.md "Senior Designer Filter — Pre-Output Checklist" (MIT) and
claude-design-skills-master / ui-designer (MIT). Merged and adapted.*
