---
name: TECH-paper-texture-filter
category: svg-noise
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The filter](#the-filter)
- [Parameter walkthrough](#parameter-walkthrough)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Usage](#usage)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Paper texture filter

## What it does

A subtle fractal-noise filter that shifts RGB channels toward a
neutral warm-gray — simulates natural paper for editorial /
newsletter aesthetics. Uses `feComponentTransfer` to bias the noise
into the mid-gray range before blending.

## The filter

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<filter id="paper" color-interpolation-filters="linearRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" result="noise"/>
  <feColorMatrix in="noise" type="saturate" values="0" result="gray"/>
  <feComponentTransfer in="gray" result="subtle">
    <feFuncR type="linear" slope="0.12" intercept="0.44"/>
    <feFuncG type="linear" slope="0.12" intercept="0.44"/>
    <feFuncB type="linear" slope="0.12" intercept="0.44"/>
  </feComponentTransfer>
  <feBlend in="SourceGraphic" in2="subtle" mode="multiply"/>
</filter>
```

## Parameter walkthrough

- `baseFrequency="0.9"` — very fine grain (paper fiber scale)
- `numOctaves="4"` — richer texture than the standard 3
- `feFuncR/G/B slope="0.12" intercept="0.44"` — compresses the noise
  range to `[0.44, 0.56]`, a narrow band around mid-gray
- `mode="multiply"` — the multiplied result darkens highs and lows
  equally, mimicking paper absorption

## When to use

- Editorial/Clean infographics — feels trustworthy and printed.
- Premium/Luxury pieces — adds warmth that pure digital can't convey.
- Corporate reports, whitepapers, investor decks.

## When NOT to use

- Bold/Cyber aesthetic — clashes with glow effects and digital neons.
- Data-dense dashboards — grain obscures small text.
- Anywhere colored-shadow or salt-pepper grain is already doing the
  work.

## Usage

```xml
<rect width="800" height="1200" fill="url(#content)" filter="url(#paper)"/>
```

## Gotchas

- Browsers render `feTurbulence` differently — paper texture will
  look slightly different in Firefox vs Chrome. Not a bug.
- The `slope` and `intercept` values are tuned — changing them
  aggressively (slope > 0.3) pushes into "rough paper" territory,
  which reads as distressed, not editorial.

## Cross-references

- [TECH-fe-turbulence-noise](TECH-fe-turbulence-noise.md) — the base noise primitive.
- [TECH-salt-pepper-texture](TECH-salt-pepper-texture.md) — stronger cousin for illustrations.
- [TECH-fe-component-transfer-color-grading](TECH-fe-component-transfer-color-grading.md) — the color-grading
  primitive this filter uses.
- [`../SKILL.md`](../SKILL.md) — parent skill

