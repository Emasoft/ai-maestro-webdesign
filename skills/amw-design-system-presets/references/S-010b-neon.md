---
id: S-010b
name: Neon / Glow UI
aesthetic_position: dark-cinematic-cyber
source_attribution: "styles-B Neon / Glow UI; `design-system-is-all-you-need/.../neon.md` (parametric glow-intensity system); `frontend-design-main/SKILL.md` Industrial / Retro-Futuristic phosphor variants; `claude-website-design-skills-main/skills/claude-remix/SKILL.md` cyberpunk vocabulary. MIT per source repos."
license: MIT (direct-port)
---

# S-010b — Neon / Glow UI

## Identity

Neon / Glow UI is the sister aesthetic to S-010 Cyberpunk — same near-black canvas, same phosphorescent vocabulary, but stripped of the genre signifiers (glitch, scanline, all-caps Orbitron camp). It is electric without theatre: two carefully chosen neon colours, multi-layer `box-shadow` glow as the SOLE elevation primitive, Space Grotesk or Orbitron for type, 8–12px radius (NOT zero — that distinguishes it from cyberpunk). The parametric DSIAYN system exposes three glow-intensity levels — `dim` (5px), `standard` (20px), `vivid` (40px + bloom) — so the same token set scales from subtle CTA accents to fullscreen hero phosphorescence. No light mode is permitted: the glow IS the colour, and on a light field the glow physics collapse. Reach for it when the brief asks for "neon" or "glow" without the retro genre baggage of synthwave or cyberpunk.

## Token block

```css
:root {
  /* Colors */
  --bg-base:        #0A0A0F;   /* near-black canvas — slightly blue-tinted */
  --bg-surface:     #14141C;   /* elevated card on the base canvas */
  --neon-primary:   #00D9FF;   /* electric cyan — the dominant neon */
  --neon-secondary: #FF006E;   /* hot pink — the accent neon */
  --ink:            #F5F5FA;   /* primary text on dark */
  --ink-muted:      #8A8A95;   /* muted secondary text */
  --border:         rgba(0, 217, 255, 0.6);  /* primary at 60% opacity */

  /* Typography */
  --font-display: 'Space Grotesk', 'Orbitron', system-ui, sans-serif;
  --font-body:    'Space Grotesk', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Geometry — 8–12px (NOT 0; that's cyberpunk territory) */
  --radius:         8px;
  --radius-card:    12px;
  --border-width:   1px;

  /* The glow primitive — multi-layer box-shadow as elevation */
  --neon-glow:        0 0 5px var(--neon-primary), 0 0 20px var(--neon-primary), 0 0 40px var(--neon-primary);
  --neon-glow-soft:   0 0 5px var(--neon-primary);
  --neon-glow-vivid:  0 0 5px var(--neon-primary), 0 0 20px var(--neon-primary), 0 0 40px var(--neon-primary), 0 0 80px var(--neon-primary);

  /* Glow-intensity levels (DSIAYN parametric system) */
  --glow-dim:      0 0 5px;     /* spread only — subtle hint */
  --glow-standard: 0 0 20px;    /* default elevation */
  --glow-vivid:    0 0 40px;    /* fullscreen hero phosphorescence */

  /* Motion — glow-pulse keyframe driver */
  --motion-pulse:    pulse 2400ms ease-in-out infinite;
  --motion-entrance: glow-in 600ms cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes pulse {
  0%, 100% { box-shadow: var(--neon-glow); }
  50%      { box-shadow: var(--neon-glow-vivid); }
}
@keyframes glow-in {
  from { box-shadow: none; opacity: 0; }
  to   { box-shadow: var(--neon-glow); opacity: 1; }
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        'bg-base':        '#0A0A0F',
        'bg-surface':     '#14141C',
        'neon-primary':   '#00D9FF',
        'neon-secondary': '#FF006E',
        ink:              '#F5F5FA',
        'ink-muted':      '#8A8A95',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'Orbitron', 'system-ui', 'sans-serif'],
        body:    ['"Space Grotesk"', 'system-ui', 'sans-serif'],
      },
      borderRadius: { DEFAULT: '8px', card: '12px' },
      boxShadow: {
        'neon':       '0 0 5px #00D9FF, 0 0 20px #00D9FF, 0 0 40px #00D9FF',
        'neon-soft':  '0 0 5px #00D9FF',
        'neon-vivid': '0 0 5px #00D9FF, 0 0 20px #00D9FF, 0 0 40px #00D9FF, 0 0 80px #00D9FF',
      },
    },
  },
}
```

## "Breaks if" invariants

- Breaks if a light-mode variant is shipped — the glow physics require a near-black canvas (`#0A0A0F`–`#14141C` range); on light fields the glow becomes invisible smear.
- Breaks if more than two neon colours appear simultaneously — primary + secondary is the contract; a third hue dilutes the duotone signature.
- Breaks if warm colour accents are introduced (amber, terracotta, gold) — Neon is strictly cool-electric.
- Breaks if serif typography replaces the geometric/technical sans (Space Grotesk / Orbitron / IBM Plex Sans).
- Breaks if elevation is delivered via hard geometric shadows (`8px 8px 0` brutalism shadow) or drop-shadows with offset — only the multi-layer `0 0 Npx` glow is permitted.
- Breaks if `border-radius` drops to 0 — that's S-010 Cyberpunk; Neon keeps 8–12px softness.
- Breaks if flat non-glowing UI elements (buttons, cards, badges) appear in the same view as glowing ones — every interactive element earns its glow.
- Breaks if the `--glow-dim/standard/vivid` parametric ladder is collapsed into a single fixed glow value — the three-tier intensity is structural to the system.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: `design-system-is-all-you-need/.../neon.md` parametric token system (DSIAYN); no live demo URL — token block is the canonical artifact.
Parity threshold: A-class justified (token-only direct-port; no upstream rendered demo to match pixel-for-pixel).

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling styles:** S-010 Cyberpunk / Dark Neo-Noir (0 radius, glitch/scanline, all-caps Orbitron); S-011 Retro-Futuristic / Synthwave (CRT scanlines, deep-space bg, magenta+cyan OR phosphor+amber); S-012 Retro Terminal (mono-only, green-on-black phosphor); S-038 Dark Tech (Space Grotesk + JetBrains Mono on `#0A0A0A`, no glow — Neon's flat cousin).
- **Differentiator vs S-010:** S-010b keeps 8–12px radius, drops the genre signifiers (scanline, glitch, all-caps), keeps the glow as the SOLE elevation. S-010 is theatrical; S-010b is electric-functional.
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-B.md` §Neon / Glow UI

## Attribution

Token values direct-ported from `styles-B.md §Neon / Glow UI`, which itself transcribes the parametric glow-intensity ladder from `design-system-is-all-you-need-main/.../neon.md`, the cyberpunk-vocabulary baseline from `claude-website-design-skills-main/skills/claude-remix/SKILL.md`, and the phosphor-green variant guidance from `frontend-design-main/SKILL.md` Industrial / Retro-Futuristic anchors. All source repos carry MIT license. The three-tier `--glow-dim/standard/vivid` ladder is the DSIAYN signature; preserve it verbatim.
