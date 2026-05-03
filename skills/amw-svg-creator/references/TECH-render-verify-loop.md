---
name: TECH-render-verify-loop
category: svg-render-loop
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/scripts/svg_loop.py
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [The six steps](#the-six-steps)
- [Why the loop script](#why-the-loop-script)
- [Iteration guidelines](#iteration-guidelines)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# The render-verify-deliver loop (mandatory)

## What it does

Every SVG the skill delivers goes through an explicit 6-step loop:
write → render → view PNG → assess → fix → repeat. The loop script
tracks render invocations and REFUSES to deliver an SVG that was
never rendered.

## When to use

- **Every SVG.** Non-negotiable. Characters need 5–8 iterations,
  simple icons 1–2, scenes 3–5.
- The loop catches coordinate-math bugs the LLM can't verify blind
  (disconnected limbs, clipping, invisible elements).

## The six steps

```
1. WRITE SVG to /home/claude/draft.svg
2. RENDER: python3 scripts/svg_loop.py render /home/claude/draft.svg
   → produces /home/claude/svg_preview.png
3. VIEW the PNG using the `view` tool (MANDATORY — you must actually look)
4. ASSESS:
   - Positions correct?
   - Gaps, overlaps, misalignment?
   - Gradients working?
   - For characters: body parts connected?
5. FIX — edit draft.svg, go back to step 2
6. DELIVER: python3 scripts/svg_loop.py finish /home/claude/draft.svg output.svg
```

## Why the loop script

LLMs can't verify pixel positions from source. The loop forces
visual feedback. The script's `status` / `reset` / `finish` commands
track iteration count and block premature delivery:

```
python3 scripts/svg_loop.py render <file.svg>    # render + view cycle
python3 scripts/svg_loop.py finish <file.svg> [name.svg]
python3 scripts/svg_loop.py status                 # iteration count
python3 scripts/svg_loop.py reset                  # start fresh
```

## Iteration guidelines

| Category | Iterations |
|----------|------------|
| Simple icons, logos, patterns | 1–2 |
| Diagrams, infographics | 2–3 |
| Scenes, illustrations | 3–5 |
| Characters, figures, animals | 5–8 (build incrementally — torso first, limbs one at a time) |

## Minimal example

```bash
# source: image-generation/svg-creator/SKILL.md
# Write the SVG
cat > /home/claude/draft.svg << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">...</svg>
SVGEOF

# Render + view cycle
python3 /path/to/skill/scripts/svg_loop.py render /home/claude/draft.svg

# View the preview PNG with the `view` tool

# When satisfied — deliver
python3 /path/to/skill/scripts/svg_loop.py finish /home/claude/draft.svg output-name.svg
```

## Gotchas

- The `finish` command BLOCKS if no `render` was run — this is the
  whole point. Don't try to skip it.
- `/home/claude/` is the canonical draft location in the sandbox.
  Adapt for your actual temp directory.
- Build characters incrementally (torso → legs → arms → head) — a
  single big SVG has too much coordinate math to fix in one pass.

## Cross-references

- [TECH-five-zone-lighting](TECH-five-zone-lighting.md) — applied during the assess/fix steps.
  > What it does · The five zones · Implementation — radial gradient + overlays · When to use · Gotchas · Cross-references
- [TECH-multi-stop-gradients](TECH-multi-stop-gradients.md) — the visual quality techniques
  > What it does · When to use · Sky gradient — 6 stops · Sphere radial — 5 stops with offset focal · The `color-interpolation="linearRGB"` rule · Gotchas · Cross-references
  applied while building.
- [TECH-character-incremental-construction](TECH-character-incremental-construction.md) — category-specific
  > What it does · The incremental build order · The thick-line trick for static characters · 8-head proportions (standing adult) · For animated characters — React + forward kinematics · Animation timing · When to recommend external tools · Gotchas · Cross-references
  iteration pattern.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

