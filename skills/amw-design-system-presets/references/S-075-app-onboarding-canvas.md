---
id: S-075
name: App Onboarding Canvas
aesthetic_position: micro-aesthetic spatial-layout multi-screen-narrative
source_attribution: clean-room summary of `claude-design-aesthetic-workflow-skill-main/references/gallery-cases.md` case #8 "App Onboarding" (license not stated) — generic multi-screen canvas idiom, no proprietary code copied
license: clean-room derivation (no verbatim copy)
---

# S-075 — App Onboarding Canvas

## Identity

App Onboarding Canvas is a layout meta-pattern rather than a chromatic vocabulary: instead of presenting product value through one hero composition, the page lays multiple device mockups across a spatial canvas — three to seven phone-sized screens arrayed horizontally, diagonally, or in a staggered cascade. Each screen is information-sparse on purpose (one heading + one illustration + one interaction zone), and the cumulative density comes from the *quantity* of screens rather than from any single one. The visitor reads the canvas left-to-right as a narrative — "here is the first feature, here is the second, here is the third" — and screen-to-screen transitions on scroll explain product progression. Colours come from the host product's design system (typically 2–3 brand hues on white or near-white grounds); typography is platform-appropriate (SF Pro on iOS demos, Google Sans on Android, system-sans on Web). Intended audience: mobile-app marketing landing pages, SaaS feature tours, AI product walkthroughs, education-app showcases, anywhere the brief is "explain the journey, not the destination".

## Token block

```css
:root {
  /* Ground — light or off-white canvas surrounding the device mockups */
  --color-bg:           #FAFAFA;
  --color-surface:      #FFFFFF;
  --color-text:         #1A1A1A;
  --color-text-muted:   #6B6B6B;

  /* Brand palette — inherit from host design system; placeholder defaults shown */
  --color-primary:      #5B5BD6;   /* swap for host primary */
  --color-accent:       #14B8A6;   /* swap for host secondary */
  --color-tertiary:     #F59E0B;   /* optional third — keep ≤3 brand hues total */

  /* Device mockup geometry — phone-sized canonical */
  --canvas-screen-width:        375px;          /* iPhone logical width — also Android equiv */
  --canvas-screen-height:       812px;          /* portrait ratio canonical */
  --canvas-screen-radius:       48px;           /* iOS HIG corner radius; 36px on Android variant */
  --canvas-screen-bezel:        12px;           /* device frame thickness */
  --canvas-screen-bezel-color:  #1A1A1A;        /* near-black device frame */
  --canvas-screen-shadow:       0 32px 64px -16px rgba(20, 20, 30, 0.20);   /* native platform elevation feel */

  /* Layout — spatial canvas containing N screens */
  --canvas-screen-count:        4;                                  /* 3–7 screens; ≥8 is too many */
  --canvas-layout:              horizontal;                         /* horizontal | diagonal | staggered-cascade */
  --canvas-gap:                 96px;                               /* generous breathing room between screens */
  --canvas-stagger-y:           48px;                               /* vertical offset between adjacent screens in staggered layout */
  --canvas-tilt:                -6deg;                              /* optional screen rotation for parallax feel; 0deg = flat */
  --canvas-padding-block:       clamp(96px, 12vw, 160px);
  --canvas-padding-inline:      clamp(48px, 6vw, 96px);

  /* Per-screen content density rule — exactly one of each */
  --canvas-screen-heading-size: 24px;          /* ONE heading per screen */
  --canvas-screen-illustration: contain;        /* ONE illustration / mockup region per screen */
  --canvas-screen-cta-size:     56px;           /* ONE action / interaction zone per screen */

  /* Annotation lines — connect screens to their explanatory copy */
  --canvas-annotation-color:    rgba(91, 91, 214, 0.30);   /* dashed connector using primary alpha */
  --canvas-annotation-stroke:   1.5px;
  --canvas-annotation-dash:     6 4;

  /* Motion — scroll-driven progression */
  --canvas-transition-duration: 800ms;
  --canvas-transition-easing:   cubic-bezier(0.4, 0, 0.2, 1);
  --canvas-scroll-stagger:      120ms;          /* delay between adjacent screens entering viewport */
  --canvas-scroll-distance:     40px;            /* translateY distance on scroll-in */
}

/* The canvas — spatial container holding N device mockups */
.onboarding-canvas {
  display: flex;
  flex-direction: row;
  gap: var(--canvas-gap);
  padding: var(--canvas-padding-block) var(--canvas-padding-inline);
  background: var(--color-bg);
  overflow-x: visible;           /* canvas may extend beyond viewport — page expands per no-nested-scrollbars rule */
  align-items: center;
}

/* Diagonal variant — adjacent screens drift down-right */
.onboarding-canvas[data-layout="diagonal"] .device-mockup:nth-child(n) {
  transform: translateY(calc(var(--canvas-stagger-y) * var(--n, 0))) rotate(var(--canvas-tilt));
}

/* Staggered cascade — alternating up-down offsets */
.onboarding-canvas[data-layout="staggered-cascade"] .device-mockup:nth-child(odd)  { transform: translateY(calc(-1 * var(--canvas-stagger-y))); }
.onboarding-canvas[data-layout="staggered-cascade"] .device-mockup:nth-child(even) { transform: translateY(var(--canvas-stagger-y)); }

/* Each device mockup — phone-sized container with native platform chrome */
.device-mockup {
  position: relative;
  flex: 0 0 var(--canvas-screen-width);
  width: var(--canvas-screen-width);
  height: var(--canvas-screen-height);
  background: var(--color-surface);
  border: var(--canvas-screen-bezel) solid var(--canvas-screen-bezel-color);
  border-radius: var(--canvas-screen-radius);
  box-shadow: var(--canvas-screen-shadow);
  opacity: 0;
  transform: translateY(var(--canvas-scroll-distance));
  transition:
    opacity   var(--canvas-transition-duration) var(--canvas-transition-easing),
    transform var(--canvas-transition-duration) var(--canvas-transition-easing);
}

.device-mockup.in-view {
  opacity: 1;
  transform: translateY(0);
}

.device-mockup:nth-child(1).in-view { transition-delay: calc(var(--canvas-scroll-stagger) * 0); }
.device-mockup:nth-child(2).in-view { transition-delay: calc(var(--canvas-scroll-stagger) * 1); }
.device-mockup:nth-child(3).in-view { transition-delay: calc(var(--canvas-scroll-stagger) * 2); }
.device-mockup:nth-child(4).in-view { transition-delay: calc(var(--canvas-scroll-stagger) * 3); }
.device-mockup:nth-child(5).in-view { transition-delay: calc(var(--canvas-scroll-stagger) * 4); }
.device-mockup:nth-child(6).in-view { transition-delay: calc(var(--canvas-scroll-stagger) * 5); }
.device-mockup:nth-child(7).in-view { transition-delay: calc(var(--canvas-scroll-stagger) * 6); }

/* Reduced motion — screens appear instantly, no translateY */
@media (prefers-reduced-motion: reduce) {
  .device-mockup {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

```js
// onboarding-canvas.js — skeleton; IntersectionObserver fires `.in-view` per
// device as it enters the viewport
const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      observer.unobserve(entry.target);
    }
  }
}, { threshold: 0.35, rootMargin: '0px 0px -10% 0px' });

document.querySelectorAll('.device-mockup').forEach(el => observer.observe(el));
```

## "Breaks if" invariants

- breaks if any single screen contains more than ONE heading, ONE illustration / mockup region, and ONE interaction zone — the canvas density rule is "density comes from quantity of screens, never from per-screen complexity"
- breaks if the canvas shows fewer than 3 or more than 7 device mockups — 2 screens read as a before/after, ≥ 8 screens read as a catalogue and lose narrative continuity
- breaks if all screens use the same colour for their interaction state — each screen must use a distinct brand colour or distinct UI state to signal progression
- breaks if the device mockups are not platform-faithful (iOS without SF Pro / Android without rounded radii / Web without system-sans) — the canvas relies on instant platform recognition for legibility
- breaks if the canvas drops the device frame entirely (bezel, screen-radius, shadow) — without a recognisable device chrome the screens read as random panels, not as a product walkthrough
- breaks if a chromatic background replaces the off-white ground — the canvas requires neutral surroundings so each screen's own palette reads cleanly
- breaks if all screens are aligned on a single horizontal baseline without any tilt, stagger, or diagonal offset — the canvas devolves into a slideshow strip
- breaks if `--canvas-tilt` exceeds 12° — screens read as falling rather than as parallax depth
- breaks if `--canvas-gap` falls below 48px — adjacent screens touch and the spatial-canvas reading is lost
- breaks if scroll-driven `in-view` reveals are omitted on a long page — the canvas needs progressive disclosure to read as narrative, not as a static gallery
- breaks if explanatory copy is placed *inside* the device screens — copy belongs in the spatial canvas between/around the screens, not crammed into mockup chrome
- breaks if `prefers-reduced-motion` is not respected — translateY scroll-in triggers vestibular reactions; screens must appear at final position with opacity 1
- breaks if a single brand palette exceeds 3 hues — the canvas relies on screen-to-screen colour difference to mark progression; a riot of brand hues defeats this

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html`, substituting `{{TOKEN}}` markers. Place a `<div class="onboarding-canvas" data-layout="horizontal">` containing four `<div class="device-mockup">…</div>` children with placeholder content (one heading + one coloured fill + one CTA per mockup). Capture the parity screenshot at 1440×900 with the canvas fully visible — all four screens must be in view and `.in-view` class applied (simulate by adding the class statically in the test fixture).
Upstream parity source: `claude-design-aesthetic-workflow-skill-main/references/gallery-cases.md` case #8 "App Onboarding" (license not stated — visual reference only, no code copied) — surveyed in `reports/batch9-harvest/styles-A.md` line 14. The implementation in this preset is a clean-room derivation of the documented layout meta-pattern (multi-screen spatial canvas + scroll-driven reveal + platform-faithful chrome); no source code from the third-party skill is copied.

## Render-test verdict

JOD: A-class (specialized-tokens) — 2026-05-29
Reason: effect / layout / multi-brand token block — defines effect or scene parameters, not the 13-slot landing-page palette (absent slots: border,font-body,font-display,font-mono,radius,shadow,spacing). Canonical render uses the effect element/file named in the pointer, not the bare skeleton. Render OK 1440x900, det-JOD 10.00.

## Cross-references

- **Companion presets:** S-008 Material Design 3 (Android platform vocabulary — App Onboarding Canvas inherits Material chrome on Android variant), S-022 Minimal Pure (neutral host palette — Canvas screens use brand colour over minimal ground), S-045 Warm Minimalism (Notion-style warm off-white canvas ground for productivity-app onboardings)
- **Sibling micro-aesthetics:** S-068 Cinematic Scroll (page-as-film-reel — Cinematic Scroll is the immersive counterpart, App Onboarding Canvas is the explanatory counterpart), S-067 Card Constellation (3D-tilted cards with mouse parallax — Canvas uses scroll parallax + platform chrome instead), S-070 Dynamic Island UI (single-component micro-aesthetic — Canvas frames many such components in spatial sequence)
- **Source attribution:** `claude-design-aesthetic-workflow-skill-main/references/gallery-cases.md` case #8 "App Onboarding" — license not stated, treated as clean-room. The documented behaviour (multi-screen spatial canvas, information-sparse per screen, native platform chrome, scroll-driven progression) is the public-domain layout pattern this preset describes; the token contract here is a fresh composition.
- **Note:** App Onboarding Canvas is a LAYOUT preset, not a chromatic preset. Colour, typography, and visual styling come from the host product's design system — Canvas only owns the spatial arrangement, device chrome, and progression motion. Pair with any chromatic preset (S-001..S-070, S-074) by inheriting that preset's `--color-primary` / `--color-accent` / `--color-text` and overriding only the Canvas-specific tokens above. The maximum is one onboarding canvas per page; placing two canvases on the same page breaks narrative continuity.
