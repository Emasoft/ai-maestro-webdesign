---
name: project-output-routing
description: Detection rules for deciding where to write the plugin's produced artifacts based on the current project's conventions. Triggers on "where should the output go", "which folder for artifacts", "default output path".
category: orchestrator-routing
---

# Project output routing

## Table of Contents

- [When to consult this doc](#when-to-consult-this-doc)
- [Detection order](#detection-order)
- [Per-artifact-type default subpath](#per-artifact-type-default-subpath)
- [Reconciliation when multiple candidates match](#reconciliation-when-multiple-candidates-match)
- [Edge cases](#edge-cases)
- [Quick-reference algorithm (pseudo-code)](#quick-reference-algorithm-pseudo-code)
- [Cross-references](#cross-references)

## When to consult this doc

Every webdesign skill that produces an artifact reads this doc before deciding
where to write. Bypass only if the user has explicitly named an output path in
their prompt.

---

## Detection order

Highest priority first; stop at the first match.

### 1. User-supplied path

If the user's prompt names a path (e.g. "write it to `./mocks/`", "save as
`~/Documents/design.html`"), honor it verbatim. No detection needed.

### 2. Project-type detection (inspect project root)

Look for the following marker files; use the matched convention:

| Marker file | Artifact destination |
|---|---|
| `package.json` with `"react"` / `"next"` / `"vite"` / `"solid-js"` dep | Components → `./src/components/`; assets → `./public/` or `./assets/`; build output → `./dist/` or `./build/` or `./.next/` |
| `package.json` with `"@astrojs/"` or `"astro"` dep | Source → `./src/pages/`; static → `./public/` |
| `package.json` with `"@remix-run/"` or `"qwik"` dep | Follow framework convention (`app/routes/` for Remix, `src/routes/` for Qwik) |
| `package.json` with `"eleventy"` or `"@11ty/"` dep | Source → `./src/`; output → `./_site/` |
| `package.json` with `"gatsby"` dep | Source → `./src/pages/`; static → `./static/` |
| `package.json` with `"svelte"` or `"@sveltejs/"` dep | Source → `./src/`; build → `./build/` |
| `package.json` with `"nuxt"` dep | Source → `./pages/`; assets → `./assets/` |
| `Cargo.toml` | Backend/Rust project; design artifacts → `./design/` |
| `pyproject.toml` or `setup.py` | Python project; design artifacts → `./design/` |
| `go.mod` | Go project; design artifacts → `./design/` |
| `pubspec.yaml` | Flutter project; source → `./lib/`; assets → `./assets/` |
| `composer.json` | PHP project; web root → `./public/` or `./src/` |
| `_config.yml` | Jekyll site; includes → `./_includes/`; assets → `./assets/` |
| `pom.xml` or `build.gradle` | Java/JVM project; design artifacts → `./design/` |

When multiple marker files are present, prefer the most specific framework match
(e.g. `next` beats plain `react`).

### 3. Existing design folder

If detection step 2 did not match, inspect the directory tree:

- `./design/` exists → use subfolders under it:
  - wireframes → `./design/wireframes/`
  - mockups / HTML → `./design/mockups/`
  - tokens → `./design/tokens/`
  - diagrams → `./design/diagrams/`
  - illustrations → `./design/illustrations/`
  - infographics → `./design/infographics/`
  - videos → `./design/videos/`
  - references → `./design/references/`
- `./docs/design/` exists → `./docs/design/<subfolder>/` (same subfolders)

### 4. Existing convention from Claude design skills

Look for these marker files that indicate a Claude design-skills workflow is
active:

- `.claude-plugin/plugin.json` with `"ai-maestro-webdesign"` → use the
  skill's recommended subfolder under `./design/`.
- `.claude/skills/` directory present → inspect each skill for a declared
  output dir; use it if unambiguous.
- `DESIGN.md` at project root → project follows the design-principles Rule 1
  workflow; artifacts go to `./design/<type>/`.

### 5. Generic fallback (no project type detected)

| Artifact category | Path |
|---|---|
| Static design artifacts (wireframes, mockups, ASCII sketches) | `./design/<artifact-type>/` |
| Working-copy / intermediate (throwaway JSON, IR dumps) | `./tmp/amw-<skill>/` (user can delete) |
| Final deliverables (HTML, SVG, PDF) | `./dist/` or `./output/` (create the folder) |

### 6. Last resort (nothing matched, no project context at all)

Use `/tmp/amw-<skill>-<slug>/`. Explicitly warn the user:

> "Saving to `/tmp/…` — this folder does not survive a reboot. Move the file
> to your project before closing."

This path is acceptable **only** when all five detection steps above returned
no match.

---

## Per-artifact-type default subpath

Once a project root is resolved via steps 1–5, use this table to choose the
exact subpath within that root:

| Artifact kind | Subpath under project root |
|---|---|
| ASCII wireframes | `design/wireframes/<name>.txt` |
| ASCII diagrams (flowcharts, arch, state, cheatsheets, retro) | `design/diagrams/<name>.txt` |
| HTML mockups | `design/mockups/<name>.html` |
| SVG diagrams (standalone) | `design/diagrams/<name>.svg` |
| Mermaid source (`.mmd`) | `design/diagrams/<name>.mmd` |
| React components | `src/components/<PascalName>.tsx` |
| CSS modules | `src/styles/<name>.module.css` |
| Tailwind config tweaks | `tailwind.config.js` (edit in place) |
| Design tokens JSON | `design/tokens/<name>.json` |
| Infographic HTML + PNG + PDF | `design/infographics/<name>.{html,png,pdf}` |
| Excalidraw PNG | `design/illustrations/<name>.png` |
| Screen-recording MP4 | `design/videos/<name>.mp4` |
| pretext HTML (kinetic typography) | `design/mockups/<name>.html` |
| SEO / UX evaluation report | `reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title>_<hash>.md` (always; per plugin report rule) |
| UI/UX reasoning notes | `design/references/<name>.md` |
| Editorial report (job-completion) | `reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title>_<hash>.md` (always; per plugin report rule) |

---

## Reconciliation when multiple candidates match

When detection yields multiple plausible paths, prefer in this order:

1. User-supplied path (absolute override — always wins)
2. Framework convention (React → `./src/…`, Flutter → `./lib/`, etc.)
3. Existing `./design/<subtype>/` folder if it is already populated
4. Generic fallback (`./design/<subtype>/` created fresh)
5. Last-resort scratch (`/tmp/amw-<skill>-<slug>/`)

---

## Edge cases

| Situation | Action |
|---|---|
| Monorepo root detected (multiple `package.json` at sub-paths) | Ask the user which package the artifact belongs to before writing |
| Read-only working tree (e.g. CI environment) | Warn the user; fall back to `/tmp/` |
| Path would overwrite an existing file | Prompt for confirmation, or append `-v2` / `-v3` suffix |
| Path is outside the current project tree | Require explicit user confirmation before writing |
| No git repo / no project root marker | Use `/tmp/amw-<skill>-<slug>/` and warn |

---

## Quick-reference algorithm (pseudo-code)

```
function resolve_output_path(skill, artifact_kind, user_hint):
  if user_hint:
    return user_hint  # step 1 — honor verbatim

  root = detect_project_root()  # look for package.json, Cargo.toml, etc.

  if framework = detect_framework(root):
    return framework_path(framework, artifact_kind)  # step 2

  if exists(root + "/design/") or exists(root + "/docs/design/"):
    return design_folder_path(root, artifact_kind)   # step 3

  if has_claude_design_markers(root):
    return "./design/" + artifact_subtype(artifact_kind) + "/"  # step 4

  if root:
    return "./design/" + artifact_subtype(artifact_kind) + "/"  # step 5

  warn("Saving to /tmp/ — not persistent")
  return "/tmp/amw-" + skill + "-" + slug + "/"  # step 6
```

---

## Cross-references

- [SKILL](../SKILL.md) — the orchestrator that routes to this doc
- [SKILL](../../amw-ascii-sketch/SKILL.md) — plan-phase artifacts (ASCII)
- [SKILL](../../amw-ascii-to-html/SKILL.md) — final-phase HTML artifacts
- Every skill's `## Output` section — links here instead of hardcoding a path
