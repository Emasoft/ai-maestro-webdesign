# Runtime conventions for HTML output

## Table of Contents

- [Tweaks live-tuning mode (recommended)](#tweaks-live-tuning-mode-recommended)
- [Dimensional hard limits (no discussion)](#dimensional-hard-limits-no-discussion)
- [Animation stack order](#animation-stack-order)
- [Decision tree — which file to load when](#decision-tree-which-file-to-load-when)
- [File-management rules](#file-management-rules)
- [Workflow rhythm](#workflow-rhythm)

Authoritative conventions every HTML/SVG emitter under this orchestrator MUST follow. Each rule is a hard invariant; downstream sub-skills MUST NOT override.

## Tweaks live-tuning mode (recommended)

Embed a JSON config block in HTML output with the marker below. This lets a subsequent edit precisely replace the config, and lets the user hand-edit and refresh:

```html
<script>
const TWEAKS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#D97757",
  "fontSize": 16,
  "radius": 8,
  "dark": false
}/*EDITMODE-END*/;
</script>
```

Full template: `../starter-components/tweaks-block.html`.

### Tweaks protocol — three non-negotiable rules

1. **Register the `message` listener BEFORE posting `__edit_mode_available`.** Otherwise the host's activate message races ahead of the listener and the toggle silently fails.
2. **`__edit_mode_set_keys` must carry partial updates** — only the changed keys, never the full config object on each change.
3. **The `EDITMODE-BEGIN/END` block must be valid JSON** — double-quoted keys, double-quoted string values. The host parses this and writes it back to disk; any syntax slip bricks persistence.

## Dimensional hard limits (no discussion)

| Medium | Min font | Min hit target |
|---|---|---|
| 1920×1080 slides | 24 px | — |
| Print documents | 12 pt | — |
| Mobile mockups | 14 px | 44 × 44 px |
| Desktop body copy | 16 px | — |

- Slides must carry `data-screen-label` (1-indexed, format `"01 Title"`). When the user says "page 5" they mean label `"05"`, not `array[4]`.
- Any content with a **playback position** (slides, video timeline) must persist the current position to `localStorage`. Users reload constantly during dev — not persisting position breaks their flow.

## Animation stack order

When animation is needed:

1. **First choice:** `../starter-components/animations.html` (Stage + Sprite + timeline + Easing — ~50 LOC core, covers 90% of use cases).
2. **Fallback:** Popmotion (`https://unpkg.com/popmotion@11.0.5/dist/popmotion.min.js`) for physics, spring, drag.
3. **Banned:** Framer Motion, GSAP. Too heavy; the scaffolds above are sufficient.

## Decision tree — which file to load when

```
Task received
    │
    ▼
ALWAYS start here — SKILL.md and its three hard rules
    │
    ▼
 ┌────────────────────────────────────────────────────────┐
 │ Task type → load this companion or route to sub-skill │
 ├────────────────────────────────────────────────────────┤
 │ About to emit any HTML  → ../ai-slop-avoid.md          │
 │ Need to ask the user    → ../question-templates.md     │
 │ Picking fonts/sizes     → ../typography-system.md      │
 │ Picking colors          → ../color-system.md           │
 │ Picking spacing/radius  → ../spacing-rhythm.md         │
 │ PC webpage chrome       → ../starter-components/browser-window.html │
 │ Mobile app chrome       → ../starter-components/ios-frame.html      │
 │                            /android-frame.html         │
 │ Slide deck              → ../starter-components/deck-stage.html     │
 │ Multi-variant canvas    → ../starter-components/design-canvas.html  │
 │ Animation               → ../starter-components/animations.html     │
 │ Live-editable params    → ../starter-components/tweaks-block.html   │
 │ Something feels off,    → ../design-heuristics.md      │
 │   can't name what         (Gestalt / Fitts / Hick / etc.)        │
 └────────────────────────────────────────────────────────┘
```

## File-management rules

- **Descriptive English filenames** for generated artifacts: `Landing Page.html`, `Dashboard Variants.html`, `iPhone App Prototype.html`. Never `design.html` / `test.html` / `output.html`.
- **Do NOT stack `v2` / `v3` files by default.** New variants become Tweaks in the existing main file. Only duplicate when the user explicitly requests a side-by-side comparison.
- **Split any file > ~1000 lines.** For React, split JSX components into sub-files and have the main file compose.

## Workflow rhythm

- **Show your reasoning and assumptions early — in chat, not on disk.** State the assumptions you're working from in your dialog with the user during Phase A. Write them out in plain text inside the chat so the user can correct them before any artifact is committed. Once approved in Phase B, write the HTML to disk with assumption notes alongside (in code comments or a sibling `.notes.md` file).
- **Accumulate, don't restart.** After writing React components into the HTML, show once more, followed by a "next steps" list.
- **One main file + Tweaks > multiple files.** When the user wants a new version, append as a Tweak to the existing main file. Do not stack v2 / v3 / v4 files.
- **Only duplicate when the user asks for side-by-side comparison** (`My Design.html` → `My Design v2.html`).
