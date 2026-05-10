---
name: TECH-svg-output-robustness
category: svg-shape
source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-svg-output-robustness

## What it does

Lists the **non-negotiable output constraints** for mechanical SVG
diagrams emitted by this skill. The skill's output must be trustworthy
— a file the caller can write to disk and render without patching.

## When to use

- **Every return** from the skill.
- **Every example** in this skill's references.
- **Before any write** — validate these constraints, not after.

## How it works

The output must:

1. **Be valid SVG.** Every tag closed, every attribute value quoted,
   every `<` properly escaped inside text. A quick sanity check: the
   output parses cleanly in `DOMParser.parseFromString(text,
   "image/svg+xml")` without an error node.
2. **Contain no explanations.** The SVG is the answer. If context is
   needed, the caller's prompt was ambiguous — reply with a
   clarifying question, not prose around an SVG.
3. **Contain no markdown.** No `` ``` ``svg`` fences in the output body;
   return raw `<svg ...>...</svg>` text (or HTML wrapper if requested).
4. **Contain no scripts.** No `<script>`, no `onclick`, no
   `javascript:` URLs. SVGs with scripts are a security hazard and get
   stripped by any trusted renderer anyway.
5. **Contain no external resources.** No `<image href="https://...">`,
   no `<link>`, no external font loads. Everything inline.
6. **Use only SVG primitives.** `<rect>`, `<circle>`, `<ellipse>`,
   `<polygon>`, `<line>`, `<path>`, `<text>`, `<g>`, `<defs>`,
   `<marker>`, `<clipPath>`, `<pattern>`, `<animateMotion>`, `<animate>`.
   Avoid `<foreignObject>` unless the caller explicitly asked for HTML
   embedding.
7. **Have all tags closed.** Even self-closing ones use the `/>` form
   consistently. Mixing `<rect>` and `<rect/>` confuses some XML
   parsers.

## Minimal example

Valid output:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <rect x="400" y="400" width="200" height="80" rx="20"
        fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
  <text x="500" y="450" text-anchor="middle" font-size="24"
        fill="#0f172a">Node</text>
</svg>
```

Invalid outputs (each violates one rule):

````xml
<!-- Rule 2 violation: explanation wraps the SVG -->
Here's your diagram:
```svg
<svg viewBox="0 0 1000 1000">...</svg>
```

<!-- Rule 4 violation: inline script -->
<svg viewBox="0 0 1000 1000">
  <rect onclick="alert('x')" x="0" y="0" width="100" height="100"/>
</svg>

<!-- Rule 5 violation: external image -->
<svg viewBox="0 0 1000 1000">
  <image href="https://example.com/logo.png" x="0" y="0" width="100" height="100"/>
</svg>

<!-- Rule 7 violation: unclosed tag -->
<svg viewBox="0 0 1000 1000">
  <rect x="0" y="0" width="100" height="100">
</svg>
````

## Gotchas

- **Callers write the output to disk directly.** If you include
  markdown fences, the file becomes invalid SVG. The skill's contract
  is "the output IS an SVG file, verbatim".
- **`<foreignObject>` for HTML embedding is OK** when the caller
  explicitly asks for it — but keep the HTML self-contained too (no
  external styles, no scripts). Default is to decline `<foreignObject>`.
- **Text with ampersands must be escaped.** `&` → `&amp;`,
  `<` inside text → `&lt;`. This is the most commonly-missed rule.
- **Return the SVG ONLY.** If the caller's prompt asks for a file, the
  answer is the file path + the SVG contents. No "I created..." prefix.
- **The caller will diff the output against expected.** Inconsistent
  whitespace or attribute ordering makes diffs noisy. Prefer
  deterministic emission — attributes in the order shown in the
  examples.

## Cross-references

- [SKILL](../SKILL.md) — Robustness Rules section
- [TECH-canvas-1000x1000](TECH-canvas-1000x1000.md) — the canvas constraint (complements these
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  rules)
- [TECH-svg-group-structure](TECH-svg-group-structure.md) — the structural convention
  > What it does · When to use · How it works · Why this order · Minimal example · Gotchas · Cross-references
- `../../../bin/amw-svg-render.py` — render-verify-fix loop; treat its output
  as ground truth for "valid SVG that renders"
