---
name: TECH-dashboard-archetypes
category: infographic-template
source: web-content-designer-main/dashboard-structure.md + ux-designer-skill-main/references/18-data-visualization.md (T-145..T-147 synthesis)
also-in:
---

## Table of Contents

- [What this is](#what-this-is)
- [The four archetypes at a glance](#the-four-archetypes-at-a-glance)
- [Archetype 1 — Executive Summary](#archetype-1--executive-summary)
- [Archetype 2 — Operational Real-time](#archetype-2--operational-real-time)
- [Archetype 3 — Analytical Drill-down](#archetype-3--analytical-drill-down)
- [Archetype 4 — Tactical Single-screen](#archetype-4--tactical-single-screen)
- [How to choose an archetype](#how-to-choose-an-archetype)
- [Cross-references](#cross-references)

# Dashboard archetypes — four shapes, four density rules

## What this is

A dashboard is not a single thing. There are four archetypes, each with different density rules, refresh cadence, drill-down behavior, and information hierarchy. Picking the wrong archetype produces a dashboard that looks busy but does not answer the user's actual question.

When the user asks "build me a dashboard", the first decision is *which kind* of dashboard. This file catalogues the four; each links to the appropriate composition templates in `TECH-data-viz-templates.md` and chart variants in `TECH-chart-variants.md`.

## The four archetypes at a glance

| Archetype | Audience | Density | Refresh | Drill-down | Time on page |
|---|---|---|---|---|---|
| **Executive Summary** | C-suite, board | Low (5–9 KPIs) | Daily / weekly | No, flat | < 2 min |
| **Operational Real-time** | Ops staff, on-call | Medium-high | Sub-minute | Limited | All day, glanceable |
| **Analytical Drill-down** | Analysts, PMs | High | On demand | Deep | 15–60 min sessions |
| **Tactical Single-screen** | Field operator | Very high | 1–5 min | None | Continuous focus |

## Archetype 1 — Executive Summary

**The "is everything OK?" dashboard.** Senior leadership opens this on a phone or a meeting display. They want yes/no on the headline KPIs and a one-glance read on direction.

**Density rules:**
- 4–9 top-level KPIs maximum. Beyond 9, the cognitive load passes the executive threshold.
- One headline number per KPI. The trend gets a sparkline; the breakdown does NOT belong here.
- One time series chart (revenue, active users, headline metric) — full-width, last 12 weeks or 12 months.
- One ranked-bar showing the headline breakdown (segment, region, channel — the most important slice).
- One narrative band: "what changed since last week" in plain prose, 2–4 sentences.

**Refresh:** daily or weekly. A real-time-updating executive dashboard signals dysfunction — leadership shouldn't be hitting refresh.

**Drill-down:** none. If an exec wants to drill, they hand off to an analyst with the Analytical Drill-down dashboard.

**Information hierarchy:** numbers first (largest), trend second (next-largest), breakdown third, narrative last. The eye reads top-to-bottom in priority order.

**Composition:** `Template 1` (KPI row) × 1, then `Template 2` (time-series + breakdown), then optionally `Template 6` (risk meters) for an alert-level summary. Never more than 3 panels total.

**Anti-pattern:** an executive dashboard with 20 charts is a vanity project. Cut to 9 or fewer KPIs and one trend.

## Archetype 2 — Operational Real-time

**The "what's happening right now?" dashboard.** Ops, SRE, customer support, on-call. Multiple metrics updating in sub-minute cadence. Designed to be glanceable from across a room (NOC display).

**Density rules:**
- Higher density than Executive (10–30 metrics) but every metric must be diagnostic — if a metric never changes color, cut it.
- Big numbers for current state; small sparkline for trend; no detailed history (this is *now*, not *over time*).
- Status colors are functional, not decorative — use `#6b1220` muted oxblood for critical, `--primary` for normal, `--accent` for warning. Color must mean something.
- Sound or color alerts on threshold breach. If a metric doesn't have a threshold, it doesn't belong here.

**Refresh:** sub-minute. Auto-refresh in the UI; never require the user to click reload.

**Drill-down:** limited. Click a metric → linked detail page (NOT in-place expansion). Operational dashboards should stay single-screen.

**Information hierarchy:** alerts first (color-flagged metrics), then high-traffic-volume metrics (the things most likely to break), then secondary state.

**Composition:** A grid of compact `Template 1`-style cards, sized for glanceability. Mix `Template 6` (risk/progress bars) for capacity-style metrics. NO long-form narrative.

**Anti-pattern:** an operational dashboard with no alert thresholds is just a status board. Without thresholds, the operator has to remember "is 87% bad?" — that fails the room-glance test.

## Archetype 3 — Analytical Drill-down

**The "why did that happen?" dashboard.** Analysts, PMs, growth teams. Sessions are 15–60 minutes; the user is exploring, not glancing. Density is high and drill-down is deep.

**Density rules:**
- Headline section (4–6 KPIs) at top so the user re-grounds before drilling.
- Filter bar (date range, segment, region, channel) immediately below the header — drill-down lives here.
- Main content: 6–15 panels, each answering a specific analytical question. Use `Template 2` (time-series + breakdown), `Template 3` (comparison matrix), `Template 5` (cohort retention), `Template 7` (geographic).
- Cross-filtering encouraged: clicking a segment in one panel filters the others.
- Every chart has a "view raw data" / "export CSV" affordance.

**Refresh:** on demand. The user picks the time range; the dashboard reloads.

**Drill-down:** deep. Click → modal with detailed breakdown → linked underlying-data table. Multi-level.

**Information hierarchy:** filters first (drill-down is the primary verb), KPIs second, exploratory panels third.

**Composition:** Mix freely from all templates in `TECH-data-viz-templates.md`. Layout is usually a 12-column grid with 2-col, 4-col, 6-col, 12-col panels mixed.

**Anti-pattern:** an analytical dashboard with no filters is a static report — the user can't answer "why" because they can't change the slice. Always include date-range, segment, and at least one categorical filter.

## Archetype 4 — Tactical Single-screen

**The "what should I do next?" dashboard.** Field operators, dispatch, trading desk, manufacturing floor. The user lives on this screen for hours; it must support continuous focused work.

**Density rules:**
- Very high — 30+ metrics is normal. The user has trained pattern recognition; they're not glancing, they're scanning.
- NO scrolling. The entire workspace fits one screen. This is the same `NO SCROLLBARS` rule as Layout 3 (one-page-structure) — content that doesn't fit must be cut, never squeezed.
- Information density is rewarded, not penalized — the user has chosen this screen as their workspace.
- Sortable tables, not charts, for the data the operator actually uses. Charts are for context.
- Persistent action affordances (acknowledge, dispatch, route) at fixed positions — muscle memory matters.

**Refresh:** 1–5 minutes (faster causes flicker; slower causes stale decisions).

**Drill-down:** none. Drill-down breaks focus. If a detail is important, surface it inline.

**Information hierarchy:** the actionable queue first (a sortable table of items needing attention), then the supporting context (charts, status of upstream systems), then long-tail metrics.

**Composition:** Mostly tables (`Template 3` style) and dense metric grids. Sparklines inline in tables. Minimal chart real estate — the screen is for the queue.

**Anti-pattern:** building a Tactical screen with the Executive density rules. Field operators will reject it — too sparse, too many clicks, too much wasted screen.

## How to choose an archetype

Ask three diagnostic questions:

1. **Who looks at this, and how long do they spend?**
   - < 2 min, leadership → Executive
   - All day, room-glance → Operational
   - 15–60 min, exploring → Analytical
   - Continuous, focused work → Tactical
2. **What is the primary action after looking?**
   - "OK, carry on" → Executive
   - "Acknowledge alert" → Operational
   - "Slice the data differently" → Analytical
   - "Take the next item in the queue" → Tactical
3. **What is the refresh expectation?**
   - Daily/weekly → Executive
   - Sub-minute → Operational
   - On demand → Analytical
   - 1–5 min → Tactical

If the answers conflict, the dashboard is doing too much — split it into two dashboards. The most common failure mode is one dashboard trying to serve all four audiences; the result serves none.

## Cross-references

- `TECH-data-viz-templates.md` — the panel templates that compose each archetype
- `TECH-chart-variants.md` — chart type selection per data shape
- `TECH-chart-selection-guide.md` — CSS-vs-Chart.js render method per chart type
- `skills/amw-design-principles/starter-components/` — page chrome
- `skills/amw-ux-flows/references/TECH-flow-patterns.md` — drill-down flow patterns for Analytical archetype
