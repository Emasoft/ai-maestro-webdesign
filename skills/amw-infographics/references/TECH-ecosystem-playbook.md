---
name: TECH-ecosystem-playbook
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in:
---

# Ecosystem playbook — 13% (22/175)

## What it does

The playbook for ecosystem / partner-directory infographics —
protocol integrations, partner networks, chain ecosystems. Teal
primary, densest type of all (partner logos packed tight).

## When to use

Content involves: partner directories, protocol integrations, chain
ecosystems, multi-chain support lists, collaboration maps.

## Color system

- **Primary:** teal/green `#00E88A` (most common), `#2ED5D7` (teal-
  blue), or red `#D94A4B`
- **Secondary:** purple `#B98AFF` / `#8B45D9` or complementary accent
- **Background:** solid (50%), gradient (18%), image-overlay (18%)
- **Temperature:** mixed (82%)
- **Saturation:** vibrant (82%)

## Typography

- **Display:** Bebas Neue (55%), Teko (14%), Orbitron (9%)
- **Body:** Montserrat (77%) — heaviest Montserrat concentration of
  any type

## Standard component prevalence (across 22 pieces)

| Component | Prevalence | Notes |
|-----------|------------|-------|
| **Badges / tags** | **100%** | Category pills on every partner entry |
| Footer | 77% | Highest — always attribution |
| Callout box | 50% | |
| Feature cards (outlined 59%) | 59% | |
| Comparison / partner table | 36% | |

## Visual properties

- **Glow:** heavy (73%) — neon border glow on section headers
- **Gradient overlays:** 68%
- **Geometric shapes:** 82%
- **Border radius:** rounded (55%), slight (41%)
- **Density:** compact (82%) — densest type of all

## Signature layout pattern

```
BRANDED HEADER STRIP (logo left, chain/platform right)
  ↓
TITLE + HERO STAT STRIP (Partners | Chains | TVL | Users)
  ↓
SECTION HEADER PILL ("INTEGRATIONS" / "DEPLOYMENTS" / "DEFI")
  ↓
CATEGORY SECTIONS (repeat per category):
  3-col partner grid:
    [logo] [PARTNER NAME] [category pill]
    12px padding, 11px font
  ↓
FEATURED INTEGRATIONS TABLE (dense_table)
  ↓
MORE SECTIONS (Products, Governance, etc.)
  ↓
FOOTER
```

## The partner grid pattern (signature)

```css
.partner-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.partner-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: 1px solid rgba(var(--primary-rgb), 0.25);
  border-radius: 6px;
}
.partner-logo { width: 28px; height: 28px; flex-shrink: 0; }
.partner-name {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text);
}
.partner-category-pill {
  font-size: 9px;
  padding: 2px 6px;
  border-radius: 3px;
  background: rgba(var(--primary-rgb), 0.15);
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
```

## Section header pill badge

```css
/* source: image-generation/create-infographics/resources/style-details.md */
.section-pill {
  display: inline-flex;
  align-items: center;
  background: rgba(var(--primary-rgb),0.1);
  border: 1px solid rgba(var(--primary-rgb),0.35);
  box-shadow: 0 0 8px rgba(var(--primary-rgb),0.25);
  color: var(--primary);
  font-family: 'Bebas Neue', sans-serif;
  font-size: 13px;
  letter-spacing: 2px;
  padding: 4px 16px;
  border-radius: 4px;
  margin-bottom: 14px;
}
```

The section pill with neon glow is THE ecosystem signature.

## CSS variables

```css
--bg: #080808;
--primary: #00E88A;
--secondary: #B98AFF;
--glow: rgba(0,232,138,0.2);
--text: #FFFFFF;
--muted: #8B8B8B;
```

## Reference template

`templates/ecosystem.html`

## Target density

12+ content blocks on portrait-tall. This is the densest type — pack
partners into 3-col grids, don't leave whitespace between logos.

## Gotchas

- Ecosystem pieces are directory-style — dense logo rosters are the
  CORE content. Don't spread them out.
- Section header pills need the neon glow — that's the "ecosystem"
  visual signature.
- Every partner entry gets a category pill — no exceptions.

## Cross-references

- `TECH-per-type-signature-palettes.md` — the color system.
- `TECH-hub-spoke-archetype.md` — alternative for platform-centric layouts.
- `TECH-section-header-pill.md` — the section pill component.
- `TECH-glow-system.md` — the neon glow patterns.
- [`../SKILL.md`](../SKILL.md) — parent skill

