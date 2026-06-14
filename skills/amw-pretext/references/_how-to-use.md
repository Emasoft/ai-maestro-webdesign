---
name: _how-to-use
category: pretext
source: skills/amw-pretext/SKILL.md
---

# Pretext — step-by-step usage workflow

The authoritative decide → pick → follow → build → resize → validate workflow for `amw-pretext`. The SKILL.md `## Technique selection` tree picks the matching TECH file; this doc is the runnable procedure once a technique is chosen.

## Table of Contents

> Instructions · How to use this skill

## Instructions

1. Walk the `## Technique selection` decision tree below to identify the matching technique category (API function, measurement prerequisite, layout pattern, obstacle routing, kinetic typography, virtualized tables, 3D/motion, integration, workflow assembly).
2. Open ONLY the relevant `references/TECH-NN-<slug>.md` file — do not load the whole catalog. The full per-tech index lives in [_index](_index.md).
> [_index.md] API functions (TECH-01 — TECH-13) · Measurement prerequisites (TECH-14 — TECH-18) · Layout patterns / obstacle routing (TECH-19 — TECH-31) · Typography techniques (TECH-32 — TECH-44) · Motion / interactive demos (TECH-45 — TECH-55) · Tables (TECH-56 — TECH-58) · Integration patterns (TECH-59 — TECH-66) · Workflow assemblies (TECH-67 — TECH-71) · Consult / decision-routing (TECH-72 — TECH-78) · Cross-references
3. Follow the TECH file's "How it works" section; call `prepare()` (or the appropriate pretext API function) exactly once before calling any layout function.
4. Reuse the project's existing typography tokens — do not introduce new fonts or motion systems; pretext exposes per-line metrics but does not own typographic decisions.
5. Handle the resize path explicitly: call `clearCache()` on font-change or after every `ResizeObserver` tick when measurement validity has changed.
6. Validate the font-string parity constraint (same CSS font string in both pretext and the renderer) before shipping; see `TECH-18-font-string-parity.md`.

## How to use this skill

1. **Decide first:** read [TECH-72-use-pretext-decision-guide](TECH-72-use-pretext-decision-guide.md) — if CSS solves it (`line-clamp`, `text-overflow`, `text-wrap: balance`) there's no reason to add pretext.
> [TECH-72-use-pretext-decision-guide.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
2. **Pick the technique** from the decision tree above — one TECH file, not a monolithic dump. Use [_index](_index.md) for a flat lookup if you already know the slug.
> [_index.md] API functions (TECH-01 — TECH-13) · Measurement prerequisites (TECH-14 — TECH-18) · Layout patterns / obstacle routing (TECH-19 — TECH-31) · Typography techniques (TECH-32 — TECH-44) · Motion / interactive demos (TECH-45 — TECH-55) · Tables (TECH-56 — TECH-58) · Integration patterns (TECH-59 — TECH-66) · Workflow assemblies (TECH-67 — TECH-71) · Consult / decision-routing (TECH-72 — TECH-78) · Cross-references
3. **Follow the exact API path** documented in that TECH file. Do NOT improvise — pretext has sharp gotchas (lineHeight-in-px, font-string-parity, `system-ui` drift).
4. **Build the wrapper module first** ([TECH-64](TECH-64-wrapper-module.md)) — this catches the #1 integration bug (lineHeight multiplier vs pixels).
> [TECH-64-wrapper-module.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
5. **Handle resize** ([TECH-66](TECH-66-resize-observer-pattern.md)) — re-layout never re-prepare.
> [TECH-66-resize-observer-pattern.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
6. **Validate against the font strategy** ([TECH-77](TECH-77-font-strategy.md)) — named fonts, `document.fonts.ready`, no `system-ui`.
> [TECH-77-font-strategy.md] What it does · When to use · How it works · Minimal example · Suggested font pairings by mood (source: pretext-frontend-motion-main/references/font-strategy.md) · Gotchas · Cross-references
