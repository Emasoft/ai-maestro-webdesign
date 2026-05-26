---
id: S-034
name: Liquid Glass
aesthetic_position: glass-soft-skeuomorphic spatial-ui visionos
source_attribution: https://github.com/dashersw/liquid-glass-js (MIT) + Apple visionOS HIG
license: MIT (liquid-glass-js); Apple visionOS HIG tokens adapted as original summary
---

# S-034 — Liquid Glass

## Identity

Liquid Glass replicates Apple's visionOS material language: translucent panels floating in a luminous 3D scene, where surfaces refract and tint the content behind them via WebGL (liquid-glass-js) or CSS `backdrop-filter` as a fallback. Cards have no hard box-shadows — spatial depth is communicated entirely through translucency, blur, and tint opacity. Typography is system-UI only. Intended for immersive app interfaces, premium SaaS hero sections, and AR/spatial UI mockups on the web.

## Token block

```css
:root {
  /* Colors — no opaque background; the scene IS the background */
  --color-bg:         transparent;
  --color-bg-scene:   linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 70%, #533483 100%);
  --color-surface:    rgba(255, 255, 255, 0.15);
  --color-text:       #FFFFFF;
  --color-text-muted: rgba(255, 255, 255, 0.65);
  --color-primary:    rgba(255, 255, 255, 0.85);
  --color-accent:     rgba(255, 255, 255, 0.25);
  --color-border:     rgba(255, 255, 255, 0.20);

  /* Typography — system-UI stack only */
  --font-display: -apple-system, 'SF Pro Display', 'Helvetica Neue', system-ui, sans-serif;
  --font-body:    -apple-system, 'SF Pro Text',    'Helvetica Neue', system-ui, sans-serif;
  --font-mono:    'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace;

  /* Spacing */
  --spacing: 8px;

  /* Shape — spatial rounded corners */
  --radius: 32px;

  /* Shadow — none; depth is spatial not shadow-based */
  --shadow: none;

  /* Motion — smooth spatial interpolation */
  --motion-duration: 300ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);

  /* Glass-specific tokens */
  --glass-blur:         20px;
  --glass-tint:         rgba(255, 255, 255, 0.15);
  --glass-tint-dark:    rgba(0, 0, 0, 0.10);
  --glass-border-color: rgba(255, 255, 255, 0.20);
  --glass-border-width: 1px;
  --glass-border-radius: 32px;

  /* WebGL refraction parameters (liquid-glass-js config) */
  --glass-webgl-type:        rounded;
  --glass-webgl-tint-opacity: 0.18;
  --glass-webgl-refraction:  0.12;
}

/* Fallback glass panel when WebGL is unavailable */
.glass-panel {
  background: var(--glass-tint);
  backdrop-filter: blur(var(--glass-blur)) saturate(180%);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(180%);
  border: var(--glass-border-width) solid var(--glass-border-color);
  border-radius: var(--glass-border-radius);
}
```

```ts
// tailwind.config.ts — theme extension
export default {
  theme: {
    extend: {
      colors: {
        surface: 'rgba(255,255,255,0.15)',
        text:    '#FFFFFF',
        muted:   'rgba(255,255,255,0.65)',
        primary: 'rgba(255,255,255,0.85)',
        accent:  'rgba(255,255,255,0.25)',
        border:  'rgba(255,255,255,0.20)',
      },
      fontFamily: {
        display: ['-apple-system', '"SF Pro Display"', '"Helvetica Neue"', 'system-ui', 'sans-serif'],
        body:    ['-apple-system', '"SF Pro Text"',    '"Helvetica Neue"', 'system-ui', 'sans-serif'],
        mono:    ['"SF Mono"', 'Menlo', 'Monaco', '"Courier New"', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '32px',
        pill:    '9999px',
        circle:  '50%',
      },
      backdropBlur: {
        glass: '20px',
      },
      transitionDuration: { DEFAULT: '300ms' },
      transitionTimingFunction: {
        DEFAULT: 'cubic-bezier(0.4,0,0.2,1)',
        spatial: 'cubic-bezier(0.4,0,0.2,1)',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if any hard box-shadow is applied to a glass panel — depth must be spatial (translucency + blur), never shadow-based
- breaks if `border-radius` drops below 24px on any primary panel — soft rounded silhouettes are the defining shape language
- breaks if an opaque solid background replaces the scene-gradient — the scene IS the background; glass panels must transmit it
- breaks if a non-system-UI font is substituted for display or body — Apple HIG specifies SF Pro/system-ui exclusively
- breaks if `backdrop-filter: blur` is removed and no WebGL refraction replaces it — the glass material requires blur transmission
- breaks if `--glass-tint` opacity rises above 0.35 — panels become opaque and lose their spatial quality
- breaks if hard edges (0px radius) appear on interactive elements — every interactive surface must be rounded
- breaks if a second chromatic accent colour is introduced — the palette is white-on-scene with a single tint wash

## Canonical render-test pointer

Render-test file: `references/render-tests/S-034-liquid-glass-test.html` (generated from `references/_test-skeleton.html` + this file's `{{TOKEN}}` block; WebGL layer via liquid-glass-js CDN with CSS backdrop-filter fallback).
Upstream source: https://github.com/dashersw/liquid-glass-js (MIT) + Apple visionOS HIG.

## Render-test verdict

JOD: pending

## Cross-references

- S-004 Glassmorphism — flat glassmorphism without WebGL refraction, no spatial scene requirement
- S-005 Neumorphism — soft-shadow embossed surfaces, no translucency
- S-007 Claymorphism — clay-inflated soft shapes, opaque fills
- Source: liquid-glass-js (MIT) — https://github.com/dashersw/liquid-glass-js
- Source: Apple visionOS Human Interface Guidelines — https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos
