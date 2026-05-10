---
name: TECH-character-card-grid
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/style-details.md
---
## Table of Contents

- [What it does](#what-it-does)
- [CSS](#css)
- [HTML](#html)
- [The tight-grid signature](#the-tight-grid-signature)
- [Stat bar sizing](#stat-bar-sizing)
- [When to use](#when-to-use)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Character / NFT card grid — tight 5-column

## What it does

5-column grid of small cards, each with a pixel-art / character
portrait at top, name label, and 2-4 colored horizontal stat bars
beneath. Standard for game-overview and ecosystem pieces.

## CSS

```css
/* source: image-generation/create-infographics/resources/style-details.md */
.char-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 2px;
}

.char-card {
  background: var(--bg3);
  border: 1px solid var(--border);
  overflow: hidden;
}

.char-portrait {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  display: block;
}

.char-name {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 5px 8px 4px;
  color: #fff;
}

.char-stats {
  padding: 0 8px 8px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.char-stat-row {
  display: flex;
  align-items: center;
  gap: 5px;
}

.char-stat-label {
  font-size: 7px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: var(--text-muted);
  width: 28px;
  flex-shrink: 0;
}

.char-stat-bar {
  flex: 1;
  height: 4px;
  background: rgba(255,255,255,0.08);
  border-radius: 2px;
  overflow: hidden;
}

.char-stat-fill {
  height: 100%;
  border-radius: 2px;
}
```

## HTML

```html
<div class="char-grid">
  <div class="char-card">
    <img class="char-portrait" src="char1.png" alt="">
    <div class="char-name">KIRA</div>
    <div class="char-stats">
      <div class="char-stat-row">
        <span class="char-stat-label">ATK</span>
        <div class="char-stat-bar"><div class="char-stat-fill" style="width: 85%; background: var(--primary);"></div></div>
      </div>
      <div class="char-stat-row">
        <span class="char-stat-label">DEF</span>
        <div class="char-stat-bar"><div class="char-stat-fill" style="width: 72%; background: var(--primary);"></div></div>
      </div>
      <div class="char-stat-row">
        <span class="char-stat-label">SPD</span>
        <div class="char-stat-bar"><div class="char-stat-fill" style="width: 91%; background: var(--primary);"></div></div>
      </div>
    </div>
  </div>
  <!-- ... 4 more cards for a 5-card row -->
</div>
```

## The tight-grid signature

```
gap: 2px    /* NOT 8px or 12px — cards pack near-edge-to-edge */
```

2px gap is the signature — frontend designers reach for 8-16px, but
that looks like a product grid, not a game roster.

## Stat bar sizing

- Height: 4px (not 8px+)
- Label width: 28px (fixed, so bars align)
- Label font: 7px (tiny but readable)
- Fill: uses `var(--primary)` — all bars same color unless denoting
  element / element type

## When to use

- Game character rosters (games with distinct playable characters)
- NFT collection previews (showing 5-15 NFTs at once)
- Ecosystem partner grids (logos + brand names)
- Any context where "fit many items on one canvas" matters

## Gotchas

- Square aspect ratio on portraits is mandatory — `aspect-ratio: 1`.
  Rectangular portraits break the grid rhythm.
- Cards shouldn't have internal padding — 5px 8px is the max. More
  padding eats the dense feel.
- For rarity tiers, color stat bars per tier (Gold/Silver/Bronze),
  not per stat type.

## Cross-references

- [TECH-game-overview-playbook](TECH-game-overview-playbook.md) — where this pattern is central.
  > What it does · When to use · Color system · Typography — two sub-variants · Standard game · Pixel / retro game · Standard component prevalence (across 25 pieces) · Visual properties · Signature layout pattern · Character card grid (signature pattern) · Light-mode sub-variant · CSS variables (standard) · CSS variables (pixel) · Reference template · Gotchas · Cross-references
- [TECH-tier-comparison-component](TECH-tier-comparison-component.md) — for non-visual tier data.
  > What it does · When to use · CSS — the base table · CSS — the tier badges · HTML · Custom tier names and colors · Gotchas · Cross-references
- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — why gaps are 2px, not 12px.
  > What it does · The success state · The failure mode · The Anti-Frontend Checklist (run before delivery) · Density targets by canvas · Spacing rules (THE signature) · Content format hierarchy (top = prefer) · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
