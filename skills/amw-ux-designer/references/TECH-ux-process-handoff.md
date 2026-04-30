---
name: TECH-ux-process-handoff
category: ux-process
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
also-in:
---

# TECH: UX process — Handoff & Iterate (Phase 5)

## What it does

The fifth phase. MEDIUM priority. Phase 5 converts validated mockups into a complete spec that engineering can implement without ambiguity, then verifies the implementation matches the spec post-release.

## When to use

After Phase 4 (Prototype & Test) confirms the design works. The Phase 5 spec is the contract between design and engineering.

## How it works

Three deliverables:

- **Detailed design spec** — every state (default / hover / focus / active / disabled / error / loading / empty / success), every responsive breakpoint (375 / 768 / 1024 / 1440), every interaction (micro-animation durations, easing, triggers).
- **Edge-case documentation** — explicit list of edge cases and their handling: empty state, error state, slow-network state, zero-result state, overflow state.
- **Post-release review** — once engineering ships, re-audit the implementation against the spec. Diff findings become the next iteration's backlog.

## Minimal example

Spec for Sarah's "basics rail" button:

```markdown
### Reorder All Button

**Position:** top-right of basics rail, 16 px from edge
**Size:** 44 × 44 px (mobile touch target)
**States:**
- default: filled bg #0066CC, white icon
- hover (desktop only): bg darkens to #0052A3, 200 ms ease-out
- focus: 2 px outline #0066CC, 2 px offset (keyboard)
- active: scale 0.96, 100 ms ease-in
- disabled (cart empty): opacity 0.4, cursor not-allowed, aria-disabled="true"
- loading: spinner replaces icon, aria-busy="true"
**Aria label:** "Reorder all items in your basics rail"
**Breakpoints:** identical across 375/768/1024/1440 (fixed size)
**Edge cases:**
- Empty cart → disabled state
- Network failure → toast "Couldn't reorder. Try again." + retry CTA
- All items out of stock → swap label to "See alternatives"
```

*Attributed to the ux-designer skill — `SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md`.*

## Gotchas

- Missing states = engineering guesses = inconsistent implementation. Every interactive element needs all 9 states enumerated.
- "Hover" states must be explicitly noted as desktop-only — on touch, hover either doesn't exist or is a tap-to-activate quirk.
- Post-release review is often skipped. It is the feedback loop that keeps the next iteration from recreating the same gap.
- Specs that link to Figma without written documentation strand anyone without Figma access. Embed screenshots + written states.

## Cross-references

- `TECH-ux-process-prototype.md` — upstream (Phase 4)
- `../SKILL.md`
