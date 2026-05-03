---
name: TECH-step-process-component
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [CSS](#css)
- [HTML](#html)
- [The connector line trick](#the-connector-line-trick)
- [Horizontal variant](#horizontal-variant)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `step_process` — numbered steps with connector line

## What it does

Numbered steps (1, 2, 3, 4...) with a vertical connector line
joining them. Each step has a circular number badge + title +
description. Used for how-to-claim, how-to-play, onboarding flows.

## When to use

- Sequential instructions where order matters.
- Airdrop claim flows (Connect → Check → Claim → Stake).
- Game onboarding, wallet setup, protocol activation.

## CSS

```css
/* source: image-generation/create-infographics/SKILL.md */
.step-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  position: relative;
}
.step-list::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 30px;
  bottom: 16px;
  width: 2px;
  background: rgba(var(--primary-rgb), 0.25);
}
.step-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 0 0 14px 0;
  position: relative;
}
.step-num {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--primary);
  color: #000;
  font-size: 12px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}
.step-content .title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 3px;
}
.step-content .desc {
  font-size: 11px;
  color: var(--muted);
  line-height: 1.45;
}
```

## HTML

```html
<div class="step-list">
  <div class="step-item">
    <div class="step-num">1</div>
    <div class="step-content">
      <div class="title">Connect Wallet</div>
      <div class="desc">Link your Ethereum wallet at the claim portal.</div>
    </div>
  </div>
  <div class="step-item">
    <div class="step-num">2</div>
    <div class="step-content">
      <div class="title">Check Eligibility</div>
      <div class="desc">Verify you held $TKN at the March 31 snapshot.</div>
    </div>
  </div>
  <div class="step-item">
    <div class="step-num">3</div>
    <div class="step-content">
      <div class="title">Claim Tokens</div>
      <div class="desc">Sign the claim transaction. Gas fee: ~$5.</div>
    </div>
  </div>
  <div class="step-item">
    <div class="step-num">4</div>
    <div class="step-content">
      <div class="title">Stake for Rewards</div>
      <div class="desc">Stake within 7 days for +20% bonus.</div>
    </div>
  </div>
</div>
```

## The connector line trick

The `::before` pseudo-element on `.step-list` creates a vertical
line behind all the number badges. It starts at `top: 30px` (after
the first number), ends at `bottom: 16px` (before the last), so it
visually links the numbers without running through them.

The `z-index: 1` on `.step-num` ensures the number badge sits in
front of the line.

## Horizontal variant

For landscape canvases, flip to horizontal:

```css
.step-list-horizontal {
  display: flex;
  gap: 0;
  align-items: flex-start;
}
.step-list-horizontal::before {
  left: 0; right: 0;
  top: 15px; bottom: auto;
  width: auto; height: 2px;
}
```

## Gotchas

- 4-6 steps optimal; 7+ gets long (vertical) or cramped (horizontal).
- Title stays SHORT — 2-4 words. Description is 1 sentence.
- Step number badge should be `background: var(--primary)` with
  `color: #000` — high contrast on the brand color.

## Cross-references

- [TECH-flow-with-arrows-component](TECH-flow-with-arrows-component.md) — when steps aren't numbered.
  > What it does · When to use · Horizontal flow — CSS · Vertical connector — CSS · HTML · Arrow icons — Phosphor only · Label rule — mandatory · Gotchas · Cross-references
- [TECH-airdrop-guide-playbook](TECH-airdrop-guide-playbook.md) — the playbook that uses this heavily.
  > What it does · When to use · Color system · Typography · Standard component prevalence (across 17 pieces) · Visual properties · Signature layout pattern · The amber+blue value split (signature) · The claim-steps horizontal flow · CSS variables · Reference template · Archetype preference · Gotchas · Cross-references
- [TECH-arrows-and-connectors](TECH-arrows-and-connectors.md) — horizontal variant uses arrows.
  > What it does · When arrows are MANDATORY · Rule · Horizontal arrow connector · Vertical connector line between sections · Flow diagram row · Phosphor Icons CDN · Labels on arrows (for flow diagrams) · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

