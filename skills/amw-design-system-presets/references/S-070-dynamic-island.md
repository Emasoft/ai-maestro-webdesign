---
id: S-070
name: Dynamic Island UI
aesthetic_position: component-defined-pill-notification
source_attribution: >
  blocked-B.md #87 viernes-ui-starter-master component "dynamic-island" (MIT, Next.js starter);
  blocked-B.md Category 11 "Component-Defined Micro-Aesthetics #33 — Dynamic Island UI"
  (pill that expands; applicable beyond mobile).
license: MIT (viernes-ui-starter-master)
---

# S-070 — Dynamic Island UI

**Filename:** `skills/amw-design-system-presets/references/S-070-dynamic-island.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Dynamic Island UI is a component-defined micro-aesthetic centred on a single notification/status element styled after iOS's Dynamic Island: a black pill anchored to the top of the viewport (or the top of a region) that expands fluidly to reveal contextual content — incoming call, build status, playback controls, AI agent activity — then contracts back to a minimal pill. The aesthetic of the surrounding page can be anything; what matters is that the island is the *organising attention surface* of the UI. The fingerprint is the matte-black pill body, white type, generous internal padding, fluid morph between collapsed and expanded states using shared-layout/FLIP animation, and a single accent reserved for status indicators inside the island. Applicable beyond mobile — web dashboards, desktop apps, AI co-pilots, build/deploy consoles. Intended audience: agent UIs, live-collab tools, audio/video apps, CI/CD dashboards, anywhere a persistent ambient status surface needs to live without dominating layout.

## Token block

```css
/* S-070 Dynamic Island UI — CSS custom properties */
:root {
  /* Colors — island canvas + page (page tokens are neutral so island stands out) */
  --color-bg:          #F4F4F6;   /* page background — light by default */
  --color-surface:     #FFFFFF;
  --color-text:        #15151A;
  --color-text-muted:  #6A6A75;
  --color-primary:     #15151A;
  --color-accent:      #2563EB;   /* status-blue inside the island */
  --color-border:      #E2E2E6;

  /* Island-specific tokens */
  --island-bg:           #0A0A0A;   /* matte black pill body */
  --island-text:         #F4F4F6;   /* light type inside the island */
  --island-text-muted:   #8A8A95;
  --island-accent:       #2563EB;
  --island-success:      #22C55E;
  --island-warning:      #F59E0B;
  --island-error:        #EF4444;

  /* Typography */
  --font-display: 'Inter', 'SF Pro Display', 'Helvetica Neue', sans-serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'JetBrains Mono', 'SF Mono', 'Fira Code', 'Courier New', monospace;

  /* Island geometry — three states */
  --island-radius:        24px;     /* fully rounded pill ends */
  --island-min-height:    36px;     /* collapsed state height */
  --island-padding-x:     16px;
  --island-padding-y:     8px;
  --island-top:           12px;     /* distance from top of viewport */
  --island-max-width-collapsed: 220px;
  --island-max-width-expanded:  520px;
  --island-z-index:       9000;

  /* Shadow — island floats above page chrome */
  --island-shadow: 0 8px 24px rgba(0, 0, 0, 0.22),
                   0 2px 6px rgba(0, 0, 0, 0.12);

  /* Geometry (page) */
  --spacing:      8px;
  --radius:       8px;
  --border-width: 1px;
  --shadow:       0 1px 2px rgba(0, 0, 0, 0.06);

  /* Motion — fluid morph between states */
  --island-morph-duration: 380ms;
  --island-morph-easing:   cubic-bezier(0.34, 1.36, 0.64, 1);  /* gentle overshoot */
  --motion-duration:       180ms;
  --motion-easing:         cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reference island pattern (consumer copies; expanded state toggles `data-state="expanded"`) */
.dyn-island {
  position: fixed;
  top: var(--island-top);
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: var(--spacing);
  min-height: var(--island-min-height);
  max-width: var(--island-max-width-collapsed);
  padding: var(--island-padding-y) var(--island-padding-x);
  background: var(--island-bg);
  color: var(--island-text);
  border-radius: var(--island-radius);
  box-shadow: var(--island-shadow);
  z-index: var(--island-z-index);
  font-family: var(--font-body);
  font-size: 14px;
  overflow: hidden;
  transition: max-width    var(--island-morph-duration) var(--island-morph-easing),
              min-height   var(--island-morph-duration) var(--island-morph-easing),
              border-radius var(--island-morph-duration) var(--island-morph-easing);
  will-change: max-width, min-height;
}

.dyn-island[data-state="expanded"] {
  max-width:  var(--island-max-width-expanded);
  min-height: 80px;
  border-radius: 28px;
}

.dyn-island[data-status="success"] { --island-accent: var(--island-success); }
.dyn-island[data-status="warning"] { --island-accent: var(--island-warning); }
.dyn-island[data-status="error"]   { --island-accent: var(--island-error); }

.dyn-island__dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--island-accent);
  flex-shrink: 0;
}

@media (prefers-reduced-motion: reduce) {
  .dyn-island { transition: none; }
}
```

```ts
// S-070 Dynamic Island UI — Tailwind theme extension
const dynamicIsland = {
  colors: {
    bg:               '#F4F4F6',
    surface:          '#FFFFFF',
    text:             '#15151A',
    'text-muted':     '#6A6A75',
    primary:          '#15151A',
    accent:           '#2563EB',
    border:           '#E2E2E6',
    'island-bg':      '#0A0A0A',
    'island-text':    '#F4F4F6',
    'island-muted':   '#8A8A95',
    'island-accent':  '#2563EB',
    'island-success': '#22C55E',
    'island-warning': '#F59E0B',
    'island-error':   '#EF4444',
  },
  fontFamily: {
    display: ['Inter', '"SF Pro Display"', '"Helvetica Neue"', 'sans-serif'],
    body:    ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"SF Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
  },
  borderRadius: { DEFAULT: '8px', island: '24px' },
  boxShadow: {
    DEFAULT: '0 1px 2px rgba(0,0,0,0.06)',
    island:  '0 8px 24px rgba(0,0,0,0.22), 0 2px 6px rgba(0,0,0,0.12)',
  },
  transitionDuration: { DEFAULT: '180ms', island: '380ms' },
  transitionTimingFunction: {
    DEFAULT: 'cubic-bezier(0.4,0,0.2,1)',
    island:  'cubic-bezier(0.34,1.36,0.64,1)',
  },
} as const;
```

**Dark page variant (the island itself stays the same matte-black):**
```css
[data-theme="dark"] {
  --color-bg:         #0F0F12;
  --color-surface:    #18181D;
  --color-text:       #F4F4F6;
  --color-text-muted: #8A8A95;
  --color-border:     #2A2A30;
  /* island tokens unchanged — the island is always matte black */
}
```

## "Breaks if" invariants

- breaks if the island body is not matte black (`#0A0A0A` to `#14141A` range) — the iOS Dynamic Island reading depends on the deep-black pill silhouette against the page
- breaks if border-radius drops below 20px on the collapsed pill — sharp corners destroy the "pill" affordance
- breaks if the morph transition is omitted or shorter than 200ms — the morph IS the aesthetic; instant state-swap reads as a different component
- breaks if `prefers-reduced-motion: reduce` does not flatten the morph — accessibility regression
- breaks if more than ONE island is rendered per viewport — multiple islands compete for the attention surface they are supposed to centralise
- breaks if the island carries advertising or non-status content — it is reserved for system/agent/live status only
- breaks if the expanded width exceeds 640px or the collapsed width exceeds 280px — outside these bounds it stops reading as a pill and becomes a panel
- breaks if the island sits below the fold (top > 80px) — the island MUST anchor near the top of its host region
- breaks if z-index is below the page's modal layer (typically 5000+) — the island must remain visible above page chrome
- breaks if more than ONE chromatic status colour is shown simultaneously inside the island — single-status rule
- breaks if the island background uses a gradient — flat matte black is structural to the iOS reference
- breaks if the island is positioned `static` rather than `fixed` — it must hover above scroll content

## Canonical render-test pointer

Render test: inject this file's PAGE-LEVEL tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#F4F4F6`, `{{SURFACE}}` = `#FFFFFF`, `{{TEXT}}` = `#15151A`, `{{TEXT_MUTED}}` = `#6A6A75`, `{{PRIMARY}}` = `#15151A`, `{{ACCENT}}` = `#2563EB`, `{{BORDER}}` = `#E2E2E6`, `{{FONT_DISPLAY}}` = `'Inter', sans-serif`, `{{FONT_BODY}}` = `'Inter', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `8px`, `{{SHADOW}}` = `0 1px 2px rgba(0,0,0,0.06)`, `{{SPACING}}` = `8px`). The island itself must be added as the `.dyn-island` pattern documented above; the skeleton verifies the host-page palette only.

Upstream parity source: viernes-ui-starter-master `dynamic-island` component (MIT) + blocked-B.md Category 11 #33.

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling styles:** S-004 Glassmorphism (transparent floating surface, but full-page chrome not single-component), S-008 Material-3 (component-system, includes notifications but not the pill-island morph), S-067 Card Constellation (component-defined motion, but 3D arrangement vs single-element morph)
- **Differentiators:** S-070 is a single *attention-pill* atop ANY host palette; consumers pair S-070 with another preset (typically S-008, S-001, S-038, or S-066) to set the page chrome — S-070 only specifies the island contract
- **Source:** viernes-ui-starter-master `dynamic-island` (MIT) + blocked-B.md Category 11 #33
