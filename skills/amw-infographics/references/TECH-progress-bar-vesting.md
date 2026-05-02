---
name: TECH-progress-bar-vesting
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [HTML](#html)
- [CSS](#css)
- [The milestone marker trick](#the-milestone-marker-trick)
- [Labels row — above and below](#labels-row-above-and-below)
- [Gradient fill](#gradient-fill)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Progress bar — vesting timeline with milestones

## What it does

A horizontal progress bar with milestone markers above/below for
vesting schedules. Shows current unlock % + schedule at a glance.

## When to use

- Token vesting schedules (TGE + monthly unlocks).
- Unlock progress on staking pools.
- Any single-metric progress over a timeline.

## HTML

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<div class="vesting-bar">
  <div class="vesting-label-row">
    <span>TGE — 10% UNLOCKED</span>
    <span>MONTH 12 — 100%</span>
  </div>
  <div class="progress-track">
    <div class="progress-fill" style="width: 35%;"></div>
    <div class="progress-marker" style="left: 10%;" title="TGE"></div>
    <div class="progress-marker" style="left: 25%;" title="3M"></div>
    <div class="progress-marker" style="left: 50%;" title="6M"></div>
    <div class="progress-marker" style="left: 75%;" title="9M"></div>
  </div>
  <div class="vesting-milestones">
    <span>TGE</span><span>3M</span><span>6M</span><span>9M</span><span>12M</span>
  </div>
</div>
```

## CSS

```css
.vesting-label-row {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-caption);
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 8px;
}

.progress-track {
  position: relative;
  height: 10px;
  background: rgba(255,255,255,0.07);
  border-radius: 5px;
  overflow: visible;   /* NOT hidden — markers project above */
}

.progress-fill {
  height: 100%;
  border-radius: 5px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  box-shadow: 0 0 10px rgba(var(--primary-rgb), 0.4);
}

.progress-marker {
  position: absolute;
  top: -3px;
  width: 2px;
  height: 16px;
  background: rgba(255,255,255,0.2);
  transform: translateX(-50%);
}

.vesting-milestones {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 6px;
}
```

## The milestone marker trick

`.progress-marker` is a 2×16px tick positioned absolutely at
percentage offsets. Because `.progress-track` has
`overflow: visible`, the ticks project 3px above the track — making
them visible as milestone markers.

## Labels row — above and below

- **Above row** (`.vesting-label-row`) — left shows current status
  ("TGE — 10% UNLOCKED"), right shows goal ("MONTH 12 — 100%").
- **Below row** (`.vesting-milestones`) — evenly-spaced milestone
  labels (TGE, 3M, 6M, 9M, 12M).

## Gradient fill

```css
background: linear-gradient(90deg, var(--primary), var(--secondary));
```

Primary on the left (start), secondary on the right (end) — the bar
visually "fills toward" the goal.

## Gotchas

- Progress marker positions (`left: 10%`) must align with the
  milestone labels below — easy to drift if you don't match the
  percentages.
- `overflow: visible` on the track is essential — without it,
  markers get clipped at the track edge.
- Don't mix this with the simpler CSS horizontal bar chart — this
  one has distinct semantics (timeline + milestones).

## Cross-references

- [TECH-bar-chart-css](TECH-bar-chart-css.md) — simpler horizontal bars.
- [TECH-airdrop-guide-playbook](TECH-airdrop-guide-playbook.md) — 24% of airdrop guides use this.
- [TECH-token-economics-playbook](TECH-token-economics-playbook.md) — 50% of token-economics use this.
- [`../SKILL.md`](../SKILL.md) — parent skill

