---
name: TECH-annotation-first
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/style-details.md
---
## Table of Contents

- [What it does](#what-it-does)
- [The per-chart-type rule](#the-per-chart-type-rule)
- [Legend exception](#legend-exception)
- [Callout line technique — highlight outliers](#callout-line-technique-highlight-outliers)
- [Insight callout box (for major insights)](#insight-callout-box-for-major-insights)
- [Threshold / benchmark line](#threshold-benchmark-line)
- [The rule](#the-rule)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Annotation-first — labels on charts, not in legends

## What it does

Every label lives DIRECTLY on the chart at the data point. No
separate legend unless the chart has 5+ series. This is the
editorial convention — viewers never look away from the chart to
understand what they're seeing.

## The per-chart-type rule

| Chart type | Label placement |
|------------|----------------|
| Bar chart | Value at the end of each bar |
| Line chart | Series label at rightmost endpoint |
| Pie/donut | % + category inside slice, or callout line outside for small slices |
| Stat cards | Label directly below/above number — never separate caption |
| Flow diagrams | Labels inline on nodes/arrows — no key |
| Progress bars | % at end of fill, label above or inline |

## Legend exception

Only use a legend when:
- 5+ series and direct labeling would overlap

Even then, place it immediately adjacent to the chart. Never in a
footer or sidebar.

## Callout line technique — highlight outliers

Use SVG lines from data point to annotation text:

```html
<svg class="callout-layer" style="position:absolute;inset:0;pointer-events:none;overflow:visible">
  <!-- Dashed line from data point to annotation -->
  <line x1="240" y1="80" x2="320" y2="50"
        stroke="rgba(255,255,255,0.4)" stroke-width="1" stroke-dasharray="3,3"/>
  <circle cx="240" cy="80" r="3" fill="var(--primary)"/>
  <text x="324" y="54" font-size="10" fill="rgba(255,255,255,0.7)">
    Peak: Mar 2024
  </text>
</svg>
```

Style:
- Short declarative text ("Peak adoption", "+180% YoY", "Threshold")
- Secondary callouts: `stroke-dasharray: 4 3` + stroke opacity 0.5
- Primary insight callouts: solid stroke

## Insight callout box (for major insights)

```css
/* source: image-generation/create-infographics/resources/style-details.md */
.insight-callout {
  border-left: 3px solid var(--primary);
  background: rgba(var(--primary-rgb), 0.06);
  padding: 10px 14px;
  border-radius: 0 6px 6px 0;
  font-size: 12px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.8);
}
.insight-callout .insight-label {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 4px;
}
```

```html
<div class="insight-callout">
  <div class="insight-label">Key Insight</div>
  Revenue grew 3× faster in markets where onboarding took under 2 minutes.
</div>
```

## Threshold / benchmark line

For data with a reference value (average, target):

```html
<!-- SVG benchmark line -->
<svg style="position:absolute;inset:0;pointer-events:none;overflow:visible">
  <line x1="0" y1="120" x2="600" y2="120"
        stroke="rgba(255,255,255,0.25)" stroke-width="1" stroke-dasharray="6,4"/>
  <text x="4" y="115" font-size="9" fill="rgba(255,255,255,0.5)"
        text-anchor="start">
    Industry avg: 42%
  </text>
</svg>
```

Label inline at the right edge: `"Avg: 42%"` or `"Target"`. Dashed,
muted color so it recedes behind the data.

## The rule

Every label that explains a data point must live next to that data
point. Viewers should never have to look away from the chart to
understand what they're seeing.

## Gotchas

- Direct labels require space — if the chart is too dense, use
  callout lines instead.
- Don't use both a legend AND direct labels — pick one.
- Callout text should be short (2-4 words max).

## Cross-references

- [TECH-reduction-pass](TECH-reduction-pass.md) — removes redundant labels.
  > What it does · The checklist · Per-aesthetic strictness · The rule · Before / after — gridline removal · Before · After · Before / after — legend to direct labels · Before · After · Before / after — decoration removal · Before (everything shouting) · After (structure creates hierarchy, not decoration) · Decision rule · Gotchas · Cross-references
- [TECH-annotated-bar-chart](TECH-annotated-bar-chart.md) — a direct example of this pattern.
  > What it does · When to use · HTML (excerpt — see source for full) · CSS · The hero bar signature · Gotchas · Cross-references
- [TECH-bordered-section-component](TECH-bordered-section-component.md) — the callout-box pattern.
  > What it does · When to use · Left-accent variant (most common) · Full-border variant · Header styles · HTML · Minimum border opacity · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

