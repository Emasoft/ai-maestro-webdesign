## Table of Contents

- [1. Architecture](#1-architecture)
- [2. Flowchart](#2-flowchart)
- [3. Sequence](#3-sequence)
- [4. State machine](#4-state-machine)
- [5. ER / data model](#5-er-data-model)
- [6. Timeline](#6-timeline)
- [7. Swimlane](#7-swimlane)
- [8. Quadrant](#8-quadrant)
- [9. Nested](#9-nested)
- [10. Tree](#10-tree)
- [11. Layer stack](#11-layer-stack)
- [12. Venn](#12-venn)
- [13. Pyramid / funnel](#13-pyramid-funnel)
- [Primitives (cross-type)](#primitives-cross-type)
  - [Annotation callout — italic Instrument Serif + dashed Bézier leader](#annotation-callout-italic-instrument-serif-dashed-bézier-leader)
  - [Sketchy filter — hand-drawn variant](#sketchy-filter-hand-drawn-variant)

# Type Rules — all 13 canonical editorial diagram types

Load this file only when the chosen type needs its specific scaffold. The compact SKILL.md carries the selection table; this file carries the per-type canonical layout, anchor coordinates, and working HTML+SVG scaffolds.

Every scaffold below assumes the six semantic tokens from SKILL.md are defined on `:root`:

```css
:root {
  --paper:    #F8F5F0;  /* background */
  --ink:      #1A1A1A;  /* primary text, borders */
  --muted:    #6B6560;  /* secondary labels, grid lines */
  --paper-2:  #EEEAE4;  /* card fills, lane backgrounds */
  --accent:   #B5523A;  /* focal nodes, 1–2 per diagram */
  --accent-fg:#FFFFFF;  /* text on accent nodes */
}
```

Override via brand onboarding (writes to [style-guide](style-guide.md) alongside this file).
> [style-guide.md] Semantic color tokens (oklch) · Font stack · Grid + line rules · Brand onboarding flow

All coordinates snap to the 4px grid. All borders are 1px hairline. No shadows. Max `rx="10"`. Accent limited to 1–2 focal nodes per diagram.

---

## 1. Architecture

**Use when:** components + connections (services, APIs, infra).

**Canonical layout.** Focal node (usually the ingress — gateway, router, front door) centred at the top. Peers on a second row, spaced evenly. Storage / persistence on a third row. Dashed connections for async / event paths; solid for synchronous. 1 accent node — the focal ingress or the system bottleneck.

**Scaffold.**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    :root {
      --paper: #F8F5F0; --ink: #1A1A1A; --muted: #6B6560;
      --paper-2: #EEEAE4; --accent: #B5523A; --accent-fg: #FFFFFF;
    }
    body { background: var(--paper); margin: 0; padding: 40px; }
    svg  { display: block; }
  </style>
</head>
<body>
<svg width="640" height="400" viewBox="0 0 640 400"
     xmlns="http://www.w3.org/2000/svg"
     font-family="Geist, system-ui, sans-serif">

  <rect width="640" height="400" fill="var(--paper)"/>

  <text x="32" y="40" font-size="15" font-weight="600" fill="var(--ink)">
    Application Architecture
  </text>

  <!-- Focal node (accent): API Gateway -->
  <rect x="240" y="80" width="160" height="48" rx="6" fill="var(--accent)"/>
  <text x="320" y="100" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--accent-fg)">API Gateway</text>
  <text x="320" y="116" text-anchor="middle" font-size="10"
        fill="var(--accent-fg)" opacity="0.8">:443</text>

  <!-- Standard: Frontend -->
  <rect x="60" y="196" width="160" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="140" y="216" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Frontend</text>
  <text x="140" y="232" text-anchor="middle" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">Next.js</text>

  <!-- Standard: Auth Service -->
  <rect x="420" y="196" width="160" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="500" y="216" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Auth Service</text>
  <text x="500" y="232" text-anchor="middle" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">JWT / OAuth</text>

  <!-- Storage: Postgres -->
  <rect x="240" y="312" width="160" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="320" y="332" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Postgres</text>
  <text x="320" y="348" text-anchor="middle" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">:5432</text>

  <!-- Connections: 1px hairline; dashed = async persistence -->
  <line x1="320" y1="128" x2="140" y2="196"
        stroke="var(--muted)" stroke-width="1"/>
  <line x1="320" y1="128" x2="500" y2="196"
        stroke="var(--muted)" stroke-width="1"/>
  <line x1="320" y1="128" x2="320" y2="312"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>

  <defs>
    <marker id="arrow" markerWidth="6" markerHeight="6"
            refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--muted)"/>
    </marker>
  </defs>
</svg>
</body>
</html>
```

---

## 2. Flowchart

**Use when:** decision logic, yes/no branches.

**Canonical layout.** Start node at top. Diamond for each decision (`rx="0"` is allowed only on diamonds — rotate a square 45°; do not draw pointy rectangles). Solid arrow down the happy path; the "no" branch always exits sideways (right or left, consistent). Terminal node at the bottom with a rounded rectangle. 1 accent on the start node OR the terminal success node — not both.

**Minimum.** Each decision diamond carries a one-word question ("paid?", "valid?"). Yes/no labels ride on the edge, 12px from the arrowhead tail.

---

## 3. Sequence

**Use when:** messages over time between actors (OAuth, API calls, webhooks).

**Canonical layout.** Actor boxes in a row across the top (height `36`, rx `6`). Lifelines dashed `4 3` drop straight down from each actor's centre. Messages are horizontal arrows between lifelines, 32px vertical spacing between messages. Solid arrow = request, dashed arrow = response. 1 accent on the initiator (the user-facing actor).

**Scaffold.**

```html
<svg width="600" height="360" viewBox="0 0 600 360"
     xmlns="http://www.w3.org/2000/svg"
     font-family="Geist, system-ui, sans-serif">

  <rect width="600" height="360" fill="var(--paper)"/>

  <!-- Actors -->
  <rect x="40"  y="40" width="100" height="36" rx="6" fill="var(--accent)"/>
  <text x="90"  y="63" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--accent-fg)">Browser</text>

  <rect x="248" y="40" width="100" height="36" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="298" y="63" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Auth Server</text>

  <rect x="456" y="40" width="100" height="36" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="506" y="63" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">API</text>

  <!-- Lifelines -->
  <line x1="90"  y1="76" x2="90"  y2="340"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="298" y1="76" x2="298" y2="340"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="506" y1="76" x2="506" y2="340"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>

  <defs>
    <marker id="seq-arrow" markerWidth="6" markerHeight="6"
            refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--ink)"/>
    </marker>
  </defs>

  <!-- Messages (solid = request, dashed = response) -->
  <line x1="90" y1="120" x2="292" y2="120"
        stroke="var(--ink)" stroke-width="1"
        marker-end="url(#seq-arrow)"/>
  <text x="194" y="114" text-anchor="middle" font-size="10"
        fill="var(--muted)">GET /authorize</text>

  <line x1="298" y1="152" x2="96" y2="152"
        stroke="var(--ink)" stroke-width="1" stroke-dasharray="4 3"
        marker-end="url(#seq-arrow)"/>
  <text x="194" y="146" text-anchor="middle" font-size="10"
        fill="var(--muted)">302 → login page</text>

  <line x1="90" y1="188" x2="292" y2="188"
        stroke="var(--ink)" stroke-width="1"
        marker-end="url(#seq-arrow)"/>
  <text x="194" y="182" text-anchor="middle" font-size="10"
        fill="var(--muted)">POST credentials</text>

  <line x1="298" y1="220" x2="96" y2="220"
        stroke="var(--ink)" stroke-width="1" stroke-dasharray="4 3"
        marker-end="url(#seq-arrow)"/>
  <text x="194" y="214" text-anchor="middle" font-size="10"
        fill="var(--muted)">302 + code</text>

  <line x1="90" y1="260" x2="500" y2="260"
        stroke="var(--ink)" stroke-width="1"
        marker-end="url(#seq-arrow)"/>
  <text x="295" y="254" text-anchor="middle" font-size="10"
        fill="var(--muted)">GET /resource + Bearer token</text>

  <line x1="506" y1="292" x2="96" y2="292"
        stroke="var(--ink)" stroke-width="1" stroke-dasharray="4 3"
        marker-end="url(#seq-arrow)"/>
  <text x="295" y="286" text-anchor="middle" font-size="10"
        fill="var(--muted)">200 OK + data</text>
</svg>
```

---

## 4. State machine

**Use when:** lifecycle with discrete states and transitions (order status, auth state, connection state).

**Canonical layout.** States as rounded rectangles laid out left-to-right in the order of progression. Transitions as labelled arrows between them. Terminal states double-bordered (render as two stacked `<rect>`s with a 2px offset — do not use `stroke-width="3"`). 1 accent on the initial state OR the terminal success state.

**Labels.** Each transition arrow carries the triggering event (`paid`, `shipped`, `refund issued`). No arrows without labels.

---

## 5. ER / data model

**Use when:** entities + fields + relationships.

**Canonical layout.** Each entity is a rectangle split into a title row (entity name, bold Geist Sans) and a field list (each field line 16px high, field name in Geist Sans, type in Geist Mono). Relationships are lines between entities with cardinality at each end (`1`, `N`, `1..*`). No shadows; hairline borders. 1 accent on the entity the reader should focus on (e.g. the PR's new table).

**Width.** Entities are `200` wide by default; expand in multiples of 20 if a field name overflows.

---

## 6. Timeline

**Use when:** events on an axis.

**Canonical layout.** One horizontal or vertical axis (1px hairline, `var(--ink)`). Events as dots (`r="4"`, `fill="var(--ink)"`) on the axis with a label offset 12px above/below. For 2+ parallel tracks (e.g. "product" vs "marketing"), stack two axes 80px apart and colour the event dots by track. 1 accent on the pivotal event.

**Rule.** If the events fit into a table, use a table. A timeline earns its place only when the *gap between events* carries meaning (long pause, clustered rush).

---

## 7. Swimlane

**Use when:** cross-functional flow — who does what, when.

**Canonical layout.** Horizontal lanes, one per role (Design / Eng / PM / QA / Ops). Lane background `var(--paper-2)`, separator `1px var(--muted)`. Steps flow left-to-right within a lane; hand-offs cross lanes with vertical arrows. Role label on the left edge, vertically centred, Geist Sans 11px uppercase letter-spacing `0.05em`. 1 accent on the step that represents the current blocker or the step the post is about.

**Lane height.** 96px minimum (fits a 48px step + 24px padding on each side).

---

## 8. Quadrant

**Use when:** two-axis positioning (impact vs effort, risk vs value).

**Canonical layout.** 520×520 square. Axes 1px `var(--ink)`, quadrant dividers 1px `var(--muted)` dashed `4 3`. Axis labels at 20px / 488px (top/bottom), rotated -90° on the left. Quadrant labels (`QUICK WINS`, `MAJOR PROJECTS`, `FILL-INS`, `THANKLESS TASKS`) at each corner, uppercase Geist Sans 10px letter-spacing `0.05em`, colour `var(--muted)`. Items are circles (`r="22"`–`28"`). 1 accent on the top-priority item in "Quick Wins".

**Scaffold.**

```html
<svg width="520" height="520" viewBox="0 0 520 520"
     xmlns="http://www.w3.org/2000/svg"
     font-family="Geist, system-ui, sans-serif">

  <rect width="520" height="520" fill="var(--paper)"/>

  <!-- Axes -->
  <line x1="64" y1="456" x2="456" y2="456" stroke="var(--ink)" stroke-width="1"/>
  <line x1="64" y1="64"  x2="64"  y2="456" stroke="var(--ink)" stroke-width="1"/>

  <!-- Quadrant dividers -->
  <line x1="260" y1="64" x2="260" y2="456"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="64" y1="260" x2="456" y2="260"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>

  <!-- Axis labels -->
  <text x="260" y="488" text-anchor="middle" font-size="11"
        fill="var(--muted)">← Low Effort · High Effort →</text>
  <text x="20" y="260" text-anchor="middle" font-size="11"
        fill="var(--muted)" transform="rotate(-90, 20, 260)">
    ← Low Impact · High Impact →
  </text>

  <!-- Quadrant labels -->
  <text x="162" y="88"  text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--muted)" letter-spacing="0.05em">QUICK WINS</text>
  <text x="358" y="88"  text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--muted)" letter-spacing="0.05em">MAJOR PROJECTS</text>
  <text x="162" y="448" text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--muted)" letter-spacing="0.05em">FILL-INS</text>
  <text x="358" y="448" text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--muted)" letter-spacing="0.05em">THANKLESS TASKS</text>

  <!-- Focal item -->
  <circle cx="148" cy="148" r="28" fill="var(--accent)" opacity="0.9"/>
  <text x="148" y="144" text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--accent-fg)">Auth</text>
  <text x="148" y="158" text-anchor="middle" font-size="9"
        fill="var(--accent-fg)" opacity="0.85">redesign</text>

  <!-- Standard items -->
  <circle cx="200" cy="200" r="22" fill="var(--paper-2)"
          stroke="var(--ink)" stroke-width="1"/>
  <text x="200" y="196" text-anchor="middle" font-size="9"
        fill="var(--ink)">Dark</text>
  <text x="200" y="208" text-anchor="middle" font-size="9"
        fill="var(--ink)">mode</text>

  <circle cx="340" cy="160" r="26" fill="var(--paper-2)"
          stroke="var(--ink)" stroke-width="1"/>
  <text x="340" y="156" text-anchor="middle" font-size="9"
        fill="var(--ink)">API v2</text>
  <text x="340" y="168" text-anchor="middle" font-size="9"
        fill="var(--ink)">migration</text>
</svg>
```

---

## 9. Nested

**Use when:** hierarchy by containment (layers inside layers — a request passing through middleware, a package inside a module inside a system).

**Canonical layout.** Concentric rounded rectangles with 16px padding between each level. Outermost level is the broadest scope; innermost is the thing the reader cares about. Level labels along the top inside-edge, Geist Sans 11px uppercase letter-spacing `0.05em` colour `var(--muted)`. 1 accent on the innermost (focal) container.

---

## 10. Tree

**Use when:** parent → children (org chart, file tree, decision tree).

**Canonical layout.** Root centred at top. Each level drops 80px. Children spread evenly on their level with 32px minimum horizontal gap. Edges are 1px `var(--muted)` orthogonal polylines (L-shaped — vertical from parent, horizontal at the child's y-band, vertical back down to child) — not diagonals. 1 accent on the root OR on the focal leaf — not both.

**Depth limit.** Beyond 4 levels, switch to nested or layer stack — the tree becomes unreadable.

---

## 11. Layer stack

**Use when:** stacked abstractions (OSI model, tech stack, request lifecycle).

**Canonical layout.** Full-width horizontal rectangles stacked vertically. Each layer 56px tall with 4px gap between. Label on the left inside-edge, Geist Sans 13px bold `var(--ink)`. Sublabel on the right inside-edge, Geist Mono 10px `var(--muted)`. Bottom layer = foundational (silicon, kernel, transport). Top layer = user-facing (presentation, UI). 1 accent on the layer the post is about.

---

## 12. Venn

**Use when:** set overlap, 2 or 3 circles only.

**Canonical layout.** Two circles: `r="120"`, centres 140px apart horizontally. Three circles: `r="120"`, centres on an equilateral triangle 140px apart. Circle fills `var(--paper-2)` at `opacity="0.7"` so overlaps darken naturally. Set labels outside each circle, Geist Sans 12px bold. Region labels inside the overlap zones, Geist Sans 10px `var(--muted)`. 1 accent on the focal set's circle (use `var(--accent)` at `opacity="0.6"` so overlaps still read).

**Four-circle Venn is never editorial.** If the user asks for 4, propose nested or a 2×2 quadrant instead.

---

## 13. Pyramid / funnel

**Use when:** ranked hierarchy (priority tiers) or conversion drop-off.

**Canonical layout.** Pyramid: 5 trapezoidal slices top-to-bottom, each 48px tall, widening by 80px per level. Labels centred inside each slice, Geist Sans 13px bold. Funnel: same shape, conversion rate on the right edge of each slice in Geist Mono 11px `var(--muted)`. 1 accent on the bottleneck slice (the one with the worst drop-off).

**Slices limit.** More than 6 levels pushes the bottom slice too wide and the top slice too thin. Split into two diagrams or switch to a bar chart.

---

## Primitives (cross-type)

These apply to any of the 13 types.

### Annotation callout — italic Instrument Serif + dashed Bézier leader

Use for editorial asides that don't fit in the diagram body — a one-line note about runtime behaviour, cold-start caveats, or the single nuance that justifies writing the post.

```html
<defs>
  <style>
    .callout-text {
      font-family: 'Instrument Serif', Georgia, serif;
      font-style: italic;
      font-size: 12px;
      fill: var(--muted);
    }
  </style>
</defs>

<path d="M 180,200 C 200,180 220,160 260,148"
      stroke="var(--muted)" stroke-width="1"
      stroke-dasharray="3 3" fill="none"/>

<text x="80" y="204" class="callout-text">only runs on cold start</text>
```

### Sketchy filter — hand-drawn variant

Use sparingly for essays and informal posts — not for technical docs, and never inside the same diagram as non-sketchy elements.

```html
<defs>
  <filter id="sketchy" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.04"
                  numOctaves="3" seed="2" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise"
                       scale="2.5" xChannelSelector="R"
                       yChannelSelector="G"/>
  </filter>
</defs>

<rect x="100" y="100" width="160" height="48" rx="6"
      fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1.5"
      filter="url(#sketchy)"/>
```

Even under the sketchy filter, coordinates must still snap to 4 — the filter adds jitter on render, not on layout.
