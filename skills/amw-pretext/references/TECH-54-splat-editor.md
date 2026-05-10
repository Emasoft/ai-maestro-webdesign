---
name: TECH-54-splat-editor
category: 3d
source: pretext-skills/amw-pretext-skill-main/patterns.md (Creative Demo Patterns — 3D)
also-in: 
---

# Splat editor — text wrapping around Gaussian splats in real time

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** 3d
**Status:** demo-only

## What it does

The "splat editor" community demo renders a Gaussian-splat 3D scene and wraps body text around the projected 2D silhouette of the splats. Same technique as TECH-53 but the silhouette is derived from depth/alpha of rendered splats instead of a solid mesh.

## When to use

- Cutting-edge demos
- 3D-to-2D text flow experiments
- Research / showcase pieces

## How it works

Concept mirror of TECH-53 (silhouette → per-line widths → `layoutNextLine`) — the distinctive piece is the splat-rendering path on a web GPU backend (not documented in the pretext sources; see community showcase https://pretextwall.xyz/).

## Minimal example

Not in the source material. See SKILL-11 `references/opentype-integration.md` and the community showcase.

## Gotchas

- Requires WebGL / WebGPU support.
- Alpha-based silhouettes need threshold tuning.

## Cross-references

- Related: TECH-53-threejs-text-wrapping
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
