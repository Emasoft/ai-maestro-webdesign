---
name: amw-tui-designer
description: Retro/cyberpunk/terminal aesthetic for web — three signature palettes (phosphor green / cyberpunk neon / amber CRT), monospace + box-drawing typography, CSS CRT effects (scanlines, neon glow, barrel distortion, flicker), terse-uppercase copy voice, and Tuimorphic React-library reference. Triggers on "phosphor terminal", "CRT effect", "scanlines + neon glow", "amber CRT", "cyberpunk terminal UI", "Tuimorphic", "retro hacker interface". Does NOT trigger on generic "retro design", "dark theme", or "make it look cool" — those route to amw-design-principles. Use when wiring a deliberate terminal/CRT aesthetic onto a web UI.
version: 0.1.0
---

<!--
ai-maestro-webdesign / skills / amw-tui-designer
Adapted from Chris Korhonen's `tui-designer` skill in https://github.com/ckorhonen/claude-skills
Original work © 2025 Chris Korhonen — MIT License (see SKILLS-TO-INTEGRATE/.../LICENSE).
Adaptation © 2026 Emasoft — MIT License.
-->

# TUI Designer — Retro / CRT / Cyberpunk Aesthetic

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Reference for designing **deliberate terminal/CRT aesthetics** on the web: phosphor-green classic terminals, cyberpunk-neon (cyan + magenta), amber CRTs, scanline overlays, neon glow via `text-shadow`, barrel-distortion CRT curvature, flicker animations, and the [Tuimorphic](https://github.com/douglance/tuimorphic) React component library that supplies 37 pre-styled terminal components.

This skill owns the *aesthetic vocabulary* — palettes, typography, CSS effect recipes, copy voice, performance caveats, accessibility escape hatches. It does **not** own broad design intent (the orchestrator decides whether a terminal aesthetic is the right surface for the user's product), and it does **not** wrap the React/HTML build (that is `amw-wireframe-builder-agent`).

The upstream skill covers React + SwiftUI + CSS in one document; this adaptation keeps the **web track only** (CSS effects, Tuimorphic) and drops SwiftUI / Metal-shader content — out of scope for ai-maestro-webdesign. For React-component patterns to compose with this aesthetic, see [SKILL](../amw-react-colorful/SKILL.md), [SKILL](../amw-react-promptify/SKILL.md), [SKILL](../amw-progressive-blur/SKILL.md), and the shadcn library at [SKILL](../amw-shadcn-ui/SKILL.md).

## Instructions

1. Confirm the user wants a *deliberate* retro/terminal aesthetic — not a generic "dark theme" or "make it cool". If the intent is just dark mode, hand back to the orchestrator.
2. Pick **one** of the three signature palettes (phosphor green, cyberpunk neon, amber CRT) — full hex tables in [palettes](references/TECH-palettes.md). Do NOT mix palettes; the aesthetic depends on a tight 3–5-color range.
> [TECH-palettes.md] Palette 1 — Phosphor Green (classic terminal) · Palette 2 — Cyberpunk Neon (cyan + magenta) · Palette 3 — Amber CRT (warm terminal) · Typography · Copy voice · Tuimorphic (React library)
3. Choose typography: monospace family (GNU Unifont / IBM Plex Mono / JetBrains Mono / SF Mono / Consolas). Use **box-drawing characters** (`╭╮╰╯│─━┃┏┓┗┛═║╔╗╚╝`) for frames; ASCII-fallback (`+-|`) when the target may render on legacy terminals.
4. Apply the CRT effect stack from [crt-effects](references/TECH-crt-effects.md): scanlines (subtle, 10–15 % opacity), neon glow (≤ 4 `text-shadow` layers), optional CRT curvature (`perspective` + `rotateX`), optional flicker (`@keyframes` only, never JS-driven).
> [TECH-crt-effects.md] Scanlines overlay · Neon glow — text and borders · CRT curvature · Flicker animation · WebGL CRT (when CSS is insufficient) · Effect-pattern reference · Performance considerations · Accessibility — non-negotiable · Pitfalls and prevention · When CRT effects backfire
5. Write copy in the terminal voice — UPPERCASE for headers/labels/status, lowercase for command input, sentence-case for body. Use `[SYS]` / `[ERR]` / `[INF]` / `[NET]` prefixes for messages. Avoid "please" / "sorry" / emojis. Full vocabulary in [palettes § copy voice](references/TECH-palettes.md#copy-voice).
6. If a React surface, install Tuimorphic (`npm install tuimorphic`) and wrap with `<div className="theme-dark tint-green">`. Component list and tints in [palettes § Tuimorphic](references/TECH-palettes.md#tuimorphic-react-library).
7. Validate accessibility (a hard gate — see Non-negotiables): WCAG 4.5:1 contrast, full keyboard navigation, `prefers-reduced-motion` removes flicker + scanlines, focus indicators on every interactive element.
8. Run the orchestrator's ai-slop-avoid checklist against the result — the aesthetic does NOT exempt the design from the three hard rules of `amw-design-principles`.

## Trigger conditions

Invoke when the request is specifically:

- "phosphor terminal" / "green-on-black terminal" / "amber CRT" / "cyberpunk neon UI"
- "add scanlines" / "CRT effect" / "barrel distortion" / "screen curvature" on a web surface
- "neon glow text" / "neon border" with deliberate retro intent
- using Tuimorphic React components
- terse-uppercase / hacker / `[SYS]`-prefixed terminal copy voice
- box-drawing characters for frames / borders

Do NOT invoke for:

- generic "dark theme" or "make it look cool" (route to `amw-design-principles`)
- monochrome non-terminal palettes (route to `amw-design-system-presets`)
- ASCII-art images from photos (route to `amw-ascii-pixel-art`)
- ASCII wireframes for layout iteration (route to `amw-ascii-sketch`)
- iOS / SwiftUI / Metal shaders — explicitly out of scope for this plugin
- HTML email aesthetics (terminal styling on email is unreliable — route to `amw-email-designer-agent`)

## Prerequisites

- **Required (web):** a modern browser supporting CSS `text-shadow`, `box-shadow`, `@keyframes`, `repeating-linear-gradient`, `perspective`, `prefers-reduced-motion`. All evergreen browsers.
- **Optional (React):** `react` ≥ 16.8, `react-dom` ≥ 16.8, and `npm install tuimorphic` if using the component library. Without Tuimorphic, the CSS recipes in [crt-effects](references/TECH-crt-effects.md) are framework-agnostic.
> [TECH-crt-effects.md] Scanlines overlay · Neon glow — text and borders · CRT curvature · Flicker animation · WebGL CRT (when CSS is insufficient) · Effect-pattern reference · Performance considerations · Accessibility — non-negotiable · Pitfalls and prevention · When CRT effects backfire
- **Out of scope:** iOS / SwiftUI / Metal shaders. The upstream skill covered them; this adaptation does not.
- **Out of scope:** native terminal apps (TUIs in the Unix sense). This skill is the *web* terminal aesthetic, not a tool for building real terminal applications.

## Position in flow

REFERENCE + EXECUTOR. Invoked by the orchestrator during **Phase B** when an approved design's aesthetic axis is "terminal / CRT / cyberpunk". Provides the palette, typography, CSS effects, and copy voice; the actual HTML/React build is composed by `amw-wireframe-builder-agent` consuming this skill's recipes.

## Output

This skill produces no standalone artifacts — it supplies aesthetic recipes. The downstream artifact (HTML / React / CSS) is produced by `amw-wireframe-builder-agent` or directly by the orchestrator using the recipes in [crt-effects](references/TECH-crt-effects.md).
> [TECH-crt-effects.md] Scanlines overlay · Neon glow — text and borders · CRT curvature · Flicker animation · WebGL CRT (when CSS is insufficient) · Effect-pattern reference · Performance considerations · Accessibility — non-negotiable · Pitfalls and prevention · When CRT effects backfire

## Error Handling

Failure modes and prevention live in [crt-effects § Pitfalls](references/TECH-crt-effects.md#pitfalls-and-prevention). Highlights:

- **Scanlines reduce readability** — keep opacity ≤ 15 %, frequency 2 px max.
- **Glow hides text** — cap at 4 `text-shadow` layers; > 5 layers makes body text illegible.
- **Barrel distortion breaks alignment** — decorative only, never use it for critical layout (forms, tables).
- **Flicker triggers motion sickness / photosensitive epilepsy** — `prefers-reduced-motion: reduce` MUST disable flicker, scanlines, and shimmer. This is a legal/safety requirement, not a preference.
- **JS-driven flicker tanks performance** — never `setInterval` opacity changes; use `@keyframes` (GPU-accelerated).
- **Box-drawing chars on legacy terminals** — VT100/older xterm render `╭╮╰╯` as gibberish. Detect via `TERM` env on terminal targets; on the web, this is not an issue (modern browsers render Unicode reliably).

## Non-negotiables

- Does NOT own broad design intent. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether a terminal aesthetic is the right surface — this skill answers "how" once that decision is made.
- **Accessibility is mandatory.** WCAG AA contrast (4.5:1 minimum on body text), full keyboard navigation, focus indicators, `prefers-reduced-motion: reduce` MUST disable flicker + scanlines + shimmer. A "looks cool but unreadable" output fails the orchestrator's ai-slop check.
- Pick **one** palette and stick to it. Mixing phosphor-green with cyberpunk-neon dilutes the aesthetic and produces visual noise. Three accent colors max.
- Cap `text-shadow` glow at 4 layers. Each layer is a GPU pass; > 5 layers blurs the text core and degrades performance on mobile.
- Flicker is `@keyframes` only — never `setInterval`. Main-thread opacity changes cause stutter and battery drain.
- Out of scope: SwiftUI, Metal shaders, native terminal apps, HTML email. Hand back to the orchestrator if the request lands in those.
- English-only content. No third-language characters in any file.

## Resources

- [palettes](references/TECH-palettes.md) — three signature palettes (phosphor green / cyberpunk neon / amber CRT), typography, copy voice, Tuimorphic component matrix.
> [TECH-palettes.md] Palette 1 — Phosphor Green (classic terminal) · Palette 2 — Cyberpunk Neon (cyan + magenta) · Palette 3 — Amber CRT (warm terminal) · Typography · Copy voice · Tuimorphic (React library)
- [crt-effects](references/TECH-crt-effects.md) — CSS recipes (scanlines, neon glow, CRT curvature, flicker), pitfalls, accessibility escape hatches.
> [TECH-crt-effects.md] Scanlines overlay · Neon glow — text and borders · CRT curvature · Flicker animation · WebGL CRT (when CSS is insufficient) · Effect-pattern reference · Performance considerations · Accessibility — non-negotiable · Pitfalls and prevention · When CRT effects backfire

Cross-skill:

| Resource | Role |
|---|---|
| [SKILL](../amw-design-principles/SKILL.md) | Orchestrator — decides whether a terminal aesthetic fits the user's product |
| [SKILL](../amw-ascii-pixel-art/SKILL.md) | Image-to-animated-ASCII (different artifact — single canvas from a photo) |
| [SKILL](../amw-ascii-creator/SKILL.md) | Perfect single ASCII artifact (text-mode) for headers / banners inside a terminal UI |
| [SKILL](../amw-box-diagram/SKILL.md) | Unicode rounded-corner box diagrams — natural inside a terminal-aesthetic page |
| [SKILL](../amw-design-system-presets/SKILL.md) | Non-terminal aesthetic presets (modern, brutalist, editorial) — alternatives if terminal is the wrong fit |
| [SKILL](../amw-shadcn-ui/SKILL.md) | Component chrome (Card, Dialog, Button, Tabs) compatible with Tuimorphic theming |
| [SKILL](../amw-tailwind-4/SKILL.md) | Utility-class styling for non-Tuimorphic terminal UIs |

Upstream:

- Tuimorphic React library: `https://github.com/douglance/tuimorphic` (MIT) — pinned at the upstream HEAD when this skill was authored.
- CRTFilter.js WebGL backend: nicholashamilton's `crtfilter` (repo no longer public; use only when CSS recipes are insufficient).

<!--
Original sources adapted under MIT License:
- ckorhonen/claude-skills · skills/tui-designer · © 2025 Chris Korhonen
Adapted © 2026 Emasoft. Both upstream and adaptation are MIT-licensed.
Out-of-scope upstream content (SwiftUI + Metal shaders) intentionally dropped.
-->
