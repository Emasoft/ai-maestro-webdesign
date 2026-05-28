---
id: S-004
name: Glassmorphism
aesthetic_position: glass-soft-skeuomorphic
source_attribution: "styles-A §Glassmorphism (Bexa MIT); styles-B §Glassmorphism (DSIAYN); blocked-A #10 (claude-skill-ui-ux-pro-max). MIT per source repos."
license: MIT
---

# S-004 — Glassmorphism

## Identity

Glassmorphism descends from iOS 7's blurred translucent sheets: frosted panels with 5-15% white fill floating over a mandatory gradient or photographic scene background. The background is not decoration — it is the visual contract. Remove the gradient scene and the glass becomes invisible. Reach for it when the brief demands a tech-premium, immersive, or spatial feel — AI dashboards, app landing pages, fintech onboarding.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary: #667eea;              /* the brand-defining color — gradient start anchor */
  --accent: #764ba2;               /* secondary accent — gradient end anchor */
  --bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* page background — gradient scene MANDATORY */
  --surface: rgba(255, 255, 255, 0.10); /* card/elevated surface — frosted glass fill */
  --text: #ffffff;                 /* primary text — white on dark gradient */
  --text-muted: rgba(255, 255, 255, 0.65); /* secondary/muted text */
  --border: rgba(255, 255, 255, 0.25); /* border color — translucent white glass border */
  --font-display: 'Inter', 'SF Pro Display', system-ui, sans-serif; /* display font family with fallbacks */
  --font-body: 'Inter', system-ui, sans-serif;    /* body font family with fallbacks */
  --font-mono: 'Fira Code', 'Courier New', monospace; /* mono */
  --radius: 16px;                  /* corner radius — glass panels always rounded */
  --shadow: 0 8px 32px rgba(31, 38, 135, 0.37); /* soft spread shadow — no hard shadows */
  --spacing: 24px;                 /* base spacing unit */
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#667eea',
        accent: '#764ba2',
        bg: '#667eea',
        surface: 'rgba(255,255,255,0.10)',
        text: '#ffffff',
        'text-muted': 'rgba(255,255,255,0.65)',
        border: 'rgba(255,255,255,0.25)',
      },
      fontFamily: {
        display: ['Inter', '"SF Pro Display"', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: { DEFAULT: '16px' },
      boxShadow: { DEFAULT: '0 8px 32px rgba(31,38,135,0.37)' },
      backdropBlur: { glass: '12px' },
    }
  }
}
```

## "Breaks if" invariants

- Breaks if the page background is a solid colour — a gradient or photographic scene is mandatory (glass is invisible on solid bg).
- Breaks if `backdrop-filter: blur()` is removed — that filter IS the glass effect.
- Breaks if the glass panel fill opacity exceeds 50% (turns opaque, killing the translucency).
- Breaks if `border-radius` drops to 0px — hard corners destroy the floating-panel aesthetic.
- Breaks if a hard box-shadow with no blur replaces the soft spread shadow.
- Breaks if text contrast inside frosted panels falls below WCAG AA 4.5:1 — glass surfaces create contrast risk.
- Breaks if glass is applied to a dark surface on a dark background with no luminance difference.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — tokens direct-ported from `design-system-is-all-you-need-main/glassmorphism.md`, `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md`, `blocked-A #10`
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 550930 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-A.md` §Glassmorphism (Bexa); `reports/batch9-harvest/styles-B.md` §Glassmorphism; `reports/batch9-harvest/blocked-A.md` §10

## Attribution

Token values direct-ported from styles-A.md §Glassmorphism (Bexa, MIT), styles-B.md §Glassmorphism (design-system-is-all-you-need), and blocked-A.md #10 (claude-skill-ui-ux-pro-max). All source repos carry MIT license. Original distillation by the batch9 harvest team.
