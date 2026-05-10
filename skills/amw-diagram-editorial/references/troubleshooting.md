## Table of Contents

- [Symptom-to-fix table](#symptom-to-fix-table)
  - [Diagrams look generic / AI-generated](#diagrams-look-generic-ai-generated)
  - [Colours don't match the user's site](#colours-dont-match-the-users-site)
  - [Fonts fall back to Times / Arial](#fonts-fall-back-to-times-arial)
  - [WCAG contrast fails on brand colour](#wcag-contrast-fails-on-brand-colour)
  - [Diagram is too dense / cluttered](#diagram-is-too-dense-cluttered)
  - [Wrong type chosen](#wrong-type-chosen)
  - [`bin/amw-svg-render.py` render check fails](#binamw-svg-renderpy-render-check-fails)
  - [Brand onboarding fetched the wrong palette](#brand-onboarding-fetched-the-wrong-palette)
  - [Diagram output opens blank](#diagram-output-opens-blank)
- [When NOT to use this skill](#when-not-to-use-this-skill)

# Troubleshooting — editorial diagrams

Symptom-to-fix table for the most common failure modes, plus the "when NOT to use this skill" routing table.

---

## Symptom-to-fix table

### Diagrams look generic / AI-generated

Most common tell. Usually one of three causes:

- **Coordinates off the 4px grid.** Check every `x`, `y`, `width`, `height`, `cx`, `cy`, `r`, and edge endpoint. Misaligned grids are the single strongest AI-generated tell — even 1px off on a single rectangle reads as sloppy.
- **Too many accent nodes.** If three or more nodes use `var(--accent)`, the reader has no idea what to look at. Reduce to 1–2.
- **Too many nodes overall.** Density above 6/10 makes every diagram look like the same generic AI output. Delete until it hurts, then delete one more.

Fix:

```
1. Re-snap every coordinate to a multiple of 4. Search for any x=/y=/width=/height=
   with a non-4-divisible value.
2. Count accent-coloured nodes. If > 2, move the extras to var(--paper-2) + var(--ink).
3. Count total nodes. If > 8 for non-nested/tree/layer types, split or switch type.
```

### Colours don't match the user's site

Brand onboarding never ran, or the user's palette has drifted from what's in [style-guide](style-guide.md).

Fix:

1. Re-run brand onboarding via `/amw-extract-style <url>` — it routes through `../amw-dev-browser/` (never raw WebFetch) and writes new tokens to [style-guide](style-guide.md) alongside this folder.
  > Semantic color tokens (oklch) · Font stack · Grid + line rules · Brand onboarding flow
2. Or have the user paste hex values directly into [style-guide](style-guide.md):
  > Semantic color tokens (oklch) · Font stack · Grid + line rules · Brand onboarding flow

```markdown
| Token      | Value     | Role                          |
|------------|-----------|-------------------------------|
| paper      | #F8F5F0   | diagram background            |
| ink        | #1A1A1A   | primary text, borders         |
| muted      | #6B6560   | secondary labels, grid lines  |
| paper-2    | #EEEAE4   | card fills, lane backgrounds  |
| accent     | #B5523A   | focal nodes, 1–2 per diagram  |
| accent-fg  | #FFFFFF   | text on accent-colored nodes  |
```

Never invent a palette without the user's input. The default stone + rust is only for first-run pending onboarding.

### Fonts fall back to Times / Arial

Geist and Instrument Serif load only if the host has them. For exact editorial rendering, add to the output HTML's `<head>`:

```html
<link rel="preconnect" href="https://fonts.bunny.net">
<link href="https://fonts.bunny.net/css?family=instrument-serif:400,400i|geist:400,600|geist-mono:400&display=swap"
      rel="stylesheet">
```

System-font fallbacks are tolerated — the diagram still works — but they lose the editorial tone. Bunny Fonts is preferred over Google Fonts for privacy (GDPR-compliant, no tracking).

### WCAG contrast fails on brand colour

Brand onboarding's contrast check flagged `ink`-vs-`paper` or `accent-fg`-vs-`accent` below 4.5:1 at 12px.

Fix:

- Darken `ink` until ratio ≥ 4.5:1. Never ship a failing pair silently.
- Or lighten `paper` if the palette has a dark background.
- For `accent-fg` failure, switch `accent-fg` between `#FFFFFF` and `#1A1A1A` — whichever clears 4.5:1.

Onboarding auto-proposes the adjustment; the user confirms before write. Never silently override the user's colour — surface the problem.

### Diagram is too dense / cluttered

Density above 6/10. Delete nodes until it hurts, then delete one more.

Escape hatches:

- Split into two diagrams: overview + detail.
- Switch to a `nested` or `layer stack` type — both tolerate higher logical density by using containment instead of lines.
- If the user insists on showing every node, it's probably not an editorial diagram. Route to `../amw-diagram-architecture/` for a graph-style output.

### Wrong type chosen

The user's intent mapped better to a different type.

Fix:

- Ask the user to override explicitly: *"Make this a swimlane, not a flowchart — rows for Design / Eng / PM."*
- Do not silently switch types — the user may have reasons.
- Show the 13-type table from SKILL.md if the user doesn't know which type fits.

### `bin/amw-svg-render.py` render check fails

Optional render-verify-finish loop. Usually means:

- CairoSVG isn't installed → run `/amw-init` to install Python packages.
- The SVG references a CSS variable outside the inline `<style>` — CairoSVG can't resolve it. Move the `:root { --* }` block inline to the SVG itself, or set the variables as attributes on the SVG root.

### Brand onboarding fetched the wrong palette

Common when the user's site uses utility CSS (Tailwind) with hundreds of accent-adjacent shades, or when the homepage is mostly hero imagery.

Fix:

- Ask the user to point at an interior page with text-heavy content (a blog post, docs page) — the palette there is usually what they actually use day-to-day.
- Or have the user paste the 6 tokens directly into [style-guide](style-guide.md) and skip onboarding.
  > Semantic color tokens (oklch) · Font stack · Grid + line rules · Brand onboarding flow

### Diagram output opens blank

HTML file opened via `file://` on macOS sometimes blocks inline SVGs with CSS variables.

Fix:

- Use `/amw-preview` — it serves the file over `http://` via `bin/amw-preview-server.py` and bypasses the file-URL quirks.
- Or open in `../amw-dev-browser/` — the plugin's sandboxed Chromium profile handles `file://` correctly.

---

## When NOT to use this skill

The selection rule is *"would a reader learn more from this than from a well-written paragraph?"* If no, don't draw. If yes but the output isn't HTML+SVG, route elsewhere:

| Intent | Use this skill? | Route to |
|---|---|---|
| Quick terminal / tweet diagram | No | `../amw-ascii-sketch/` or a wiretext tool |
| Before/after comparison | No | A table — better than any diagram |
| One-item "diagram" (single box, single label) | No | Write the sentence |
| Simple list of steps with no branching | No | A numbered list |
| SVG icon, vector logo, animated SVG | No | `../amw-svg-creator/` (gated scope) |
| Freeform system sketch, natural-language → SVG | No | `../amw-diagram-svg/` |
| Architecture graph JSON / Mermaid / multi-format export | No | `../amw-diagram-architecture/` |
| Infographic with charts, stats, dense data | No | `../amw-infographics/` |
| HTML → PNG for social share | No | `../amw-infographics/` or `../../bin/amw-html-export.py` |
| ASCII wireframe → HTML | No | `../amw-ascii-to-html/` |
| ASCII box-art → SVG diagram | No | `../amw-ascii-to-svg/` |
| PRD → wireframes + Mermaid | No | `../amw-ux-flows/` |
| Editorial diagram for a blog post or docs page, one of 13 types | **Yes** | This skill |

When in doubt, route back to `../amw-design-principles/SKILL.md` and let the orchestrator decide.
