---
name: TECH-heatmap-intensity-markers
category: text-visual-retro
source: cc-plugin-text-visualizations-main/skills/tools-visual-retro/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-heatmap-intensity-markers — `[++] [+] [~] [!]` density cells

## What it does

Renders an ASCII heatmap where each cell is a 4-char intensity marker:
`[++]` (very high), `[+]` (high), `[~]` (moderate), `[!]` (warning /
anomaly). Used for incident-per-day, exposure-per-segment, or
error-rate-per-endpoint density readouts.

## When to use

- Daily incident counts for a sprint readout
- Experiment exposure per user segment
- Error-rate heatmaps (endpoint × hour-of-day)
- Capacity readouts (service × region)
- Any 2-axis density readout where the reader needs "worse where?" at
  a glance

## How it works

Each cell is a fixed-width marker (4 chars including brackets) so
columns stay aligned:

| Marker | Meaning |
|---|---|
| `[++]` | Very high / hot (red) |
| `[+]` | High (orange) |
| `[~]` | Moderate (yellow) |
| `[.]` | Low (green) |
| `[ ]` | None / idle |
| `[!]` | Warning / anomaly, requires attention |

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-retro/SKILL.md line 27 + adapted
Service    Mon   Tue   Wed   Thu   Fri
---------  ----  ----  ----  ----  ----
API GW     [+]   [~]   [+]   [++]  [!]
Payments   [.]   [.]   [~]   [+]   [+]
Auth       [.]   [.]   [.]   [.]   [!]
Search     [ ]   [ ]   [.]   [.]   [.]
```

## Gotchas

- All markers MUST be the same character width to keep columns aligned.
- Color intuition doesn't transfer through ASCII — a legend explaining
  `[++] = very high` is part of the deliverable.
- Don't mix marker sets in one heatmap (e.g. `[+]` with `*` and `!`) —
  pick one vocabulary and stick to it.

## Cross-references

- `./TECH-grid-side-by-side.md`
- `./TECH-milestone-timeline.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

