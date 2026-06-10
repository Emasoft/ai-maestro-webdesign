<!--
Direct-port + adapt from SKILLS-TO-INTEGRATE/web-design/claude-skill-design-system (MIT,
component-scanning + design-page templates) and claude-design-suite (MIT, brand-
intelligence/extract-design-md + design-systems/component-spec asset patterns). 2026-05-27.
-->

# TECH — Extractor Icon and Raster Asset Export (T-093, T-095)

## Table of Contents

- [When this runs](#when-this-runs)
- [Phase A — Discovery](#phase-a-discovery)
- [Phase B — Role assignment (T-093 + T-095)](#phase-b-role-assignment-t-093-t-095)
- [Phase C — Alt-text inference (T-095, raster only)](#phase-c-alt-text-inference-t-095-raster-only)
- [Phase D — Export](#phase-d-export)
- [License + provenance](#license-provenance)
- [Privacy + robots compliance](#privacy-robots-compliance)
- [What the extractor refuses to do](#what-the-extractor-refuses-to-do)
- [Cross-references](#cross-references)

How the URL extractor (`bin/amw-design-md-from-url.sh`) and the codebase
extractor (`bin/amw-design-md-from-codebase.py`) discover, classify, and
export **inline SVG icons** and **raster brand assets** (logos, hero images,
illustration backgrounds, pattern textures) alongside the DESIGN.md. Activated
by `--extract-icons` (SVG only) and `--extract-assets` (raster); when both
flags are passed the extractor produces one merged manifest.

## When this runs

- Either flag was passed explicitly.
- Or the calling agent (`amw-design-md-extractor-agent`) detected an
  `## 5. Components` block in the DESIGN.md that references icon roles
  (`icon-search`, `icon-close`, `icon-menu`) — the agent then runs icon
  export to populate those references with real SVG content.
- Or the source page has a recognizable header `<svg>` matching brand-logo
  heuristics (see §Logo detection).

When the flag is absent the extractor emits one `# TODO: icon-{role}` line
per referenced icon and one `# TODO: asset-logo` for the brand mark, rather
than fabricating placeholder paths.

## Phase A — Discovery

### Inline SVG discovery (URL)

The URL extractor delegates to `amw-dev-browser` and asks the page to return
every reachable `<svg>` node. For each node it records:

| Field | Source |
|---|---|
| `outer_html` | `node.outerHTML` |
| `bounding_rect` | `node.getBoundingClientRect()` — used for size buckets |
| `parent_tag` | `node.parentElement.tagName` |
| `parent_role` | `node.parentElement.getAttribute("role")` |
| `aria_label` | `node.getAttribute("aria-label")` or `<title>` text |
| `class_list` | `node.getAttribute("class")` |
| `path_count` | number of `<path>` children |
| `viewbox` | `node.getAttribute("viewBox")` |
| `fill` | `getComputedStyle(node).fill` |
| `color` | `getComputedStyle(node).color` (for `fill="currentColor"` SVGs) |

The DOM-traversal evaluation runs ONCE per page (see
[TECH-07-url-extraction](TECH-07-url-extraction.md) for the `dev-browser eval`
contract).

### Inline SVG discovery (codebase)

The codebase scanner reads every `*.svg` file and every JSX/TSX/Vue/Svelte
file that contains an inline `<svg>` literal. For each it records the same
fields as above plus:

| Field | Source |
|---|---|
| `file_path` | absolute path to the file containing the SVG |
| `export_name` | the named export (e.g. `IconSearch`, `MenuIcon`) |
| `import_count` | number of files that import this SVG (computed via cross-file grep) |

### Raster asset discovery (URL)

For every `<img>`, `<picture><source>`, and `background-image: url(...)`
the extractor records:

| Field | Source |
|---|---|
| `src` | resolved absolute URL |
| `width`, `height` | rendered dimensions from `getBoundingClientRect()` |
| `natural_width`, `natural_height` | from `HTMLImageElement` |
| `alt` | `node.getAttribute("alt")` (empty string is recorded as such) |
| `role` | `node.getAttribute("role")` |
| `parent_tag` | `node.parentElement.tagName` |
| `parent_section` | nearest `<section>` / `<header>` / `<footer>` / `<main>` / `<nav>` ancestor |
| `loading` | `lazy` / `eager` / `auto` (`loading=` attribute) |
| `mime_type` | server-reported `Content-Type` (followed via head request) |

### Raster asset discovery (codebase)

The codebase scanner walks `public/`, `static/`, `assets/`, `src/assets/`,
`src/images/` and records every `*.{png,jpg,jpeg,webp,avif,gif,ico}` plus
every `import` of those files from a TS/JS file. The import count and the
referencing file paths become provenance metadata.

## Phase B — Role assignment (T-093 + T-095)

Each candidate is assigned a **role** via this priority cascade. The first
rule that fires wins; later rules append metadata only.

### Role priority for SVGs

1. **`aria-label` / `<title>` provides the role.** If the label is a
   well-known UI verb (`search`, `close`, `menu`, `chevron-down`, `arrow-right`,
   `check`, `plus`, `minus`, `external-link`, `user`, `settings`, `home`,
   `trash`, `edit`, `download`, `upload`, `info`, `warning`, `error`,
   `success`, `play`, `pause`, `volume`, `heart`, `star`, `bookmark`,
   `share`, `more`, `filter`, `sort`), the role becomes
   `icon-<normalized-label>`. Normalization is kebab-case ASCII, no diacritics.

2. **`class_list` provides the role.** Class names matching
   `icon-{name}`, `feather-{name}`, `lucide-{name}`, `tabler-{name}`,
   `heroicon-{name}`, `material-{name}`, `phosphor-{name}` are stripped
   to `{name}` and used as the role suffix. `class="lucide lucide-search"` →
   `icon-search`.

3. **The file/export name provides the role** (codebase only). `IconSearch.tsx`
   → `icon-search`. `SearchIcon.tsx` → `icon-search`. `Search.svg` → `icon-search`.

4. **Size + chrome position infers the role:**
   - Inside `<header>` or `<nav>` AND `path_count >= 3` AND
     `aria-label` matches a brand name → role `logo` (see §Logo detection).
   - Inside a `<button>` or `[role="button"]` with no other text content →
     role `icon-<closest-aria-label-or-class>` ultimately resolved by rules 1-3,
     otherwise `icon-unknown-N` with a confidence note.
   - Bounding rect ≤ 32×32px with `viewBox` ≤ 32×32 → `icon-small`.
   - 32×32 < rect ≤ 64×64 → `icon-medium`.
   - rect > 64×64 → `illustration` (no further role inference).

5. **Identical SVG content collapses to one role.** Two `<svg>` nodes with
   matching `outer_html` (after whitespace normalization) are recorded ONCE
   with `usage_count: 2` instead of duplicated.

If none of rules 1-4 fire, the SVG is recorded as `icon-unknown-N` with
confidence=low. The auditor / wireframe-builder can promote it to a real
role later.

### Role priority for raster assets

1. **`alt` text provides the role.** Non-empty `alt` is normalized to
   kebab-case and prefixed with a category:
   - "Acme logo" → `logo-primary`
   - "John Smith, CEO" → `headshot-john-smith`
   - "Dashboard screenshot" → `screenshot-dashboard`
   - "Hero illustration" → `illustration-hero`

2. **`parent_section` infers the role:**
   - inside `<header>` or first child of `<nav>` → `logo-primary`
   - inside `<section class="hero">` or the first `<section>` of `<main>` →
     `hero-image`
   - inside `<footer>` → `logo-footer` if image is small (≤ 200×100px) or
     `image-footer` otherwise
   - inside `<article>` → `article-image-N`
   - background-image of `<body>` → `background-page`
   - background-image of a `<section>` → `background-section-N`

3. **MIME type filters out non-design assets.** Tracking pixels (1×1 GIF,
   `pixel.gif`, `transparent.png`) are skipped. SVG-as-img is rerouted to
   the inline-SVG pipeline.

### Logo detection (special case)

A candidate is promoted to role `logo-primary` when ALL of the following
hold:

- Located inside `<header>`, `<nav>`, or as direct child of `<body>` in the
  first 200px of vertical position.
- For SVG: `path_count >= 2` (not a simple icon) AND viewbox aspect ratio
  is non-square (typical for wordmarks).
- For raster: width >= 80px AND height >= 24px AND aspect ratio between
  1:1 and 6:1.
- The `alt` / `aria-label` / surrounding text contains the brand name (derived
  from `<title>`, `og:site_name`, or `package.json#name` in codebase mode).

If all conditions hold the entry is recorded with role `logo-primary` and
its provenance is logged in extraction-notes. A second matching candidate
becomes `logo-secondary` (often used for footer / mark-only variant).

## Phase C — Alt-text inference (T-095, raster only)

When a raster asset has an empty `alt` attribute, the extractor infers a
candidate alt-text from these signals, in priority order:

1. **Adjacent `<figcaption>` text.**
2. **`<img title>` attribute.**
3. **The text of the closest `<h*>` heading in the same `<section>`.**
4. **The filename, normalized.** `team-photo-2024-q1.jpg` → "Team photo".
5. **The `alt` of the nearest `<img>` with the same `src` on another page**
   (cross-page mode only, when multipage extraction is active).

Inferred alt-text is written as `# alt-suggested: ...` in DESIGN.md (NOT
as a canonical `alt:` field). The wireframe-builder treats the suggestion
as advisory; the auditor flags assets that still lack canonical alt-text
after extraction.

### When the source is intentionally decorative

If the asset's parent has `role="presentation"`, `aria-hidden="true"`, or
the `alt=""` is explicit (NOT missing), the extractor records
`decorative: true` and skips alt-text inference. This is the only correct
output for purely decorative chrome — see WCAG 2.1 H67.

## Phase D — Export

Output files are written next to the DESIGN.md (or to a directory passed
via `--icon-out` / `--asset-out`):

```
DESIGN.md
DESIGN.assets.json                # manifest of every icon + asset
DESIGN.assets/
├── icons/
│   ├── icon-search.svg
│   ├── icon-close.svg
│   ├── icon-menu.svg
│   └── logo-primary.svg
├── raster/
│   ├── logo-primary.png         # downloaded (URL) or copied (codebase)
│   ├── hero-image.webp
│   └── headshot-john-smith.jpg
└── PROVENANCE.md                # one entry per asset — source URL or file path
```

### `DESIGN.assets.json` schema

```json
{
  "icons": [
    {
      "role": "icon-search",
      "path": "DESIGN.assets/icons/icon-search.svg",
      "size_px": 20,
      "viewbox": "0 0 24 24",
      "fill": "currentColor",
      "color_token": "{colors.foreground}",
      "usage_count": 7,
      "source": "https://example.com/ (header.search-bar > button > svg)",
      "license_hint": "MIT (from lucide-react package.json)",
      "confidence": "high"
    }
  ],
  "raster": [
    {
      "role": "logo-primary",
      "path": "DESIGN.assets/raster/logo-primary.png",
      "width": 120,
      "height": 32,
      "mime": "image/png",
      "alt": "Acme logo",
      "alt_source": "img[alt]",
      "decorative": false,
      "source": "https://example.com/logo.png",
      "natural_size": [240, 64],
      "confidence": "high"
    },
    {
      "role": "illustration-hero",
      "path": "DESIGN.assets/raster/hero-image.webp",
      "width": 1200,
      "height": 600,
      "mime": "image/webp",
      "alt": "",
      "alt_suggested": "Dashboard preview showing the analytics view",
      "alt_source": "h1-in-same-section + filename-normalize",
      "decorative": false,
      "source": "https://example.com/assets/hero@2x.webp",
      "confidence": "medium"
    }
  ],
  "fingerprint_hash": "sha256:<emitted by extractor-fingerprinting>",
  "extracted_at": "2026-05-27T14:30:00+0200"
}
```

### Component-token wiring

When a role is `icon-*` and the icon is referenced by an entry in
`components:` (e.g. `button.icon: {icons.icon-search}`), the extractor
writes the reference into DESIGN.md exactly as listed. The wireframe
builder reads the path from `DESIGN.assets.json` at render time.

For raster assets, `components:` references stay path-based:
`hero.background: "DESIGN.assets/raster/hero-image.webp"`.

## License + provenance

`PROVENANCE.md` contains one entry per asset capturing:

- The source URL or file path where the asset was found.
- A `license_hint` field — the extractor looks for nearby `LICENSE` files,
  npm package.json `license` keys, or `<svg data-license="...">` annotations
  and records what it found, NEVER guessing.
- Empty `license_hint` is recorded as `# UNKNOWN`. The auditor / human is
  expected to confirm license before redistributing.

The extractor never strips license headers from SVG content. Inline SVGs
with embedded `<!-- license: ... -->` comments are preserved verbatim.

## Privacy + robots compliance

The asset downloader respects the SAME `robots.txt` and `X-Robots-Tag`
checks as the parent URL extractor (per §Hard Rule 3 of the extractor agent).
Any asset with `<meta name="robots" content="noindex">` on its containing
page is skipped and recorded as `# SKIPPED: robots-disallow` in
`DESIGN.assets.json`.

Assets behind a login wall fail the parent extraction (status=failed) and
no asset download is attempted.

## What the extractor refuses to do

- Generate alt-text via an LLM. The inference rules in Phase C are
  deterministic; nothing is invented.
- Rasterize an SVG. The wireframe-builder is downstream and may rasterize
  for export; the extractor only records the SVG source.
- Convert color in icons. `fill="currentColor"` is preserved verbatim so
  downstream consumers can theme via CSS.
- Optimize / minify the SVG. Optimization is a separate concern handled
  by the wireframe-builder or a build step.

## Cross-references

- [TECH-extractor-component-detection](TECH-extractor-component-detection.md) —
  component detection runs in the same scan; icon-role assignments link to
  component-spec entries
- [TECH-extractor-fingerprinting](TECH-extractor-fingerprinting.md) — uses
  the asset manifest as one of the canonicalized token blocks fed into the
  SHA-256 fingerprint
- [TECH-07-url-extraction](TECH-07-url-extraction.md) — URL → DESIGN.md
  pipeline (icon discovery is the SVG-traversal pass of the same extraction)
- [TECH-08-codebase-extraction](TECH-08-codebase-extraction.md) — codebase
  scan that discovers assets/, public/, and inline SVGs
- [SKILL](../../amw-dev-browser/SKILL.md) — browser primitive used by URL
  asset discovery
- [SKILL](../../amw-svg-creator/SKILL.md) — downstream consumer for icon
  generation when an icon role is referenced by a component but no source
  was found
