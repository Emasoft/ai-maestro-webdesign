---
name: TECH-flow-with-arrows-component
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Horizontal flow — CSS](#horizontal-flow-css)
- [Vertical connector — CSS](#vertical-connector-css)
- [HTML](#html)
- [Arrow icons — Phosphor only](#arrow-icons-phosphor-only)
- [Label rule — mandatory](#label-rule-mandatory)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `flow_with_arrows` — horizontal flow nodes with arrow connectors

## What it does

Boxes connected by directional arrows, horizontal or vertical.
**Mandatory when content describes a process** — token flows, fee
flows, process steps, economy loops, how-it-works.

## When to use

- ANY process, flow, economy, or loop in the content.
- If 3+ related sections exist, at least one arrow connector must
  show the relationship.
- Replaces isolated "feature cards" that describe steps.

## Horizontal flow — CSS

```css
/* source: image-generation/create-infographics/SKILL.md */
.flow-row {
  display: flex;
  align-items: center;
  gap: 0;
}
.flow-node {
  flex: 1;
  padding: 10px 14px;
  border: 1.5px solid rgba(var(--primary-rgb), 0.4);
  border-radius: 8px;
  background: rgba(var(--primary-rgb), 0.06);
  text-align: center;
}
.flow-node .label {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.flow-node .sub {
  font-size: 10.5px;
  color: var(--muted);
  margin-top: 3px;
}
.flow-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  flex-shrink: 0;
  color: var(--primary);
  font-size: 16px;
}
```

## Vertical connector — CSS

```css
.connector-down {
  width: 2px;
  height: 28px;
  margin: 0 auto;
  background: var(--primary);
  position: relative;
}
.connector-down::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: -3px;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 6px solid var(--primary);
}
```

## HTML

```html
<div class="flow-row">
  <div class="flow-node">
    <div class="label">STAKE</div>
    <div class="sub">Deposit $TKN</div>
  </div>
  <div class="flow-arrow"><i class="ph-bold ph-arrow-right"></i></div>
  <div class="flow-node">
    <div class="label">EARN</div>
    <div class="sub">8% APY</div>
  </div>
  <div class="flow-arrow"><i class="ph-bold ph-arrow-right"></i></div>
  <div class="flow-node">
    <div class="label">REINVEST</div>
    <div class="sub">Compound</div>
  </div>
  <div class="flow-arrow"><i class="ph-bold ph-arrow-right"></i></div>
  <div class="flow-node">
    <div class="label">STAKE</div>
    <div class="sub">Loop</div>
  </div>
</div>
```

## Arrow icons — Phosphor only

```html
<!-- Use Phosphor: -->
<i class="ph-bold ph-arrow-right"></i>
<i class="ph-bold ph-arrow-down"></i>
<i class="ph-bold ph-arrow-u-down-right"></i>  <!-- for branches -->
```

**No emoji arrows.** No text arrows like `→` except in pure ASCII
contexts. Phosphor Icons CDN is mandatory.

## Label rule — mandatory

Arrows in a flow diagram MUST carry text labels — action names,
percentages, token names. Never unlabeled arrows. If the label won't
fit, use a smaller font or a shorter label.

## Gotchas

- Ghost borders (opacity 0.1) make flow nodes invisible — use 0.3+
  opacity for borders.
- 5+ nodes in one row wrap awkwardly — break into 2 rows with a
  connector.
- Don't mix horizontal and vertical arrows randomly — pick one
  orientation per diagram unless you have a branch.

## Cross-references

- [TECH-arrows-and-connectors](TECH-arrows-and-connectors.md) — broader arrow patterns.
- [TECH-flywheel-loop-component](TECH-flywheel-loop-component.md) — circular variant.
- [TECH-step-process-component](TECH-step-process-component.md) — numbered-steps variant.
- [`../SKILL.md`](../SKILL.md) — parent skill

