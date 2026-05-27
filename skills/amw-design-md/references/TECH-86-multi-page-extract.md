# TECH-86: Multi-page extraction — merging tokens from N URL roles

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Architecture](#architecture)
- [URL-role taxonomy](#url-role-taxonomy)
- [Merge strategies](#merge-strategies)
  - [Strategy 1 — Most-frequent wins (default)](#strategy-1--most-frequent-wins-default)
  - [Strategy 2 — First-wins (home is authoritative)](#strategy-2--first-wins-home-is-authoritative)
  - [Strategy 3 — Merge-by-role (positional weighting)](#strategy-3--merge-by-role-positional-weighting)
- [Per-token merge rules](#per-token-merge-rules)
- [Provenance recording](#provenance-recording)
- [Failure modes](#failure-modes)
- [Cross-references](#cross-references)

## What it does

Documents how `amw-design-md-extractor-agent` produces ONE Variant 1 DESIGN.md when the user supplies several **structurally distinct public URLs from the same site** — typically the home page, an inner content page, a marketing/features page, and the footer-anchored "about" or "pricing" page. Each URL exposes a different surface area of the design system; merging them produces a more faithful DESIGN.md than any single page would.

This is the **conflict-resolution** layer that sits on top of [TECH-07-url-extraction](TECH-07-url-extraction.md) (single URL) and is orthogonal to [TECH-09-multipage-extraction](TECH-09-multipage-extraction.md) (session-aware login + N pages). TECH-09 handles authentication; TECH-86 handles **token disagreement across pages**.

## When to use

- User says: "extract DESIGN.md from this site — here are 4 URLs (home, /pricing, /docs, /blog)"
- User says: "use the homepage AND the product detail page; they have different tones"
- Brand-researcher: "extract from competitor.com — sample home, features, and pricing to capture the full palette"

## When NOT to use

- Single URL only → use [TECH-07-url-extraction](TECH-07-url-extraction.md)
  > What it does · When to use · Architecture · Inputs · What `dev-browser eval` returns · Heuristics for token extraction · Colors · Typography · Spacing · Radius · Components · Output structure · Failure modes and recovery · Validation gate · Cross-references
- Authenticated SaaS app (login required) → use [TECH-09-multipage-extraction](TECH-09-multipage-extraction.md) — that flow handles sessions; this one assumes public pages
  > What it does · When to use · When NOT to use · Architecture · Session handling · Page-list strategy · A. User provides explicit URL list · B. Crawl mode (limited) · Per-page token aggregation · Colors · Typography · Components · Layout · Provenance annotations · Failure modes · Privacy and credential handling · Cross-references
- User wants per-page DESIGN.md files (one per surface) → run TECH-07 once per URL, do not merge

## Architecture

```
        ┌────────────────────────────────────────────┐
        │ Inputs:                                     │
        │  - urls: [home, features, pricing, docs]    │
        │  - merge_strategy: most-frequent | first    │
        │                  | role-weighted            │
        └─────────────────────┬──────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────────┐
        │ Per-URL extraction (TECH-07 in parallel):   │
        │   bin/amw-design-md-from-url.sh <URL_i>     │
        │     → DRAFT_i (Variant 1 frontmatter only)  │
        └─────────────────────┬──────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────────┐
        │ Merge layer (this TECH):                    │
        │   - tag each token with source URL          │
        │   - apply merge strategy per token type     │
        │   - record provenance in prose              │
        └─────────────────────┬──────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────────┐
        │ Unified DESIGN.md with per-section          │
        │ provenance annotations + validation gate    │
        └────────────────────────────────────────────┘
```

Per-URL extraction runs in parallel (one `dev-browser eval` per URL). The merge layer is a deterministic post-processor inside `bin/amw-design-md-from-url.sh` when called with multiple `<URL>` positional arguments OR a `--urls-file <file>` flag.

## URL-role taxonomy

When the user supplies URLs without labels, the extractor classifies each by URL pattern + page content:

| Role | Heuristic | Weight (role-weighted strategy) |
|---|---|---|
| `home` | URL ends in `/`, `/index`, or root; has hero + nav | 3 |
| `features` | URL contains `/features`, `/product`, `/about` | 2 |
| `pricing` | URL contains `/pricing`, `/plans` | 2 |
| `docs` | URL contains `/docs`, `/guide`, `/manual` | 1 |
| `blog` | URL contains `/blog`, `/post`, `/article` | 1 |
| `legal` | URL contains `/terms`, `/privacy`, `/legal` | 0 (skip) |
| `unknown` | Anything else | 1 |

Legal pages typically use the system font + minimal styling — excluding them prevents noise. The user can override with `--include-legal`.

## Merge strategies

The strategy applies token-by-token. The user picks one strategy globally via `--strategy <name>`; individual token types CAN override via `--strategy-colors most-frequent --strategy-typography first`.

### Strategy 1 — Most-frequent wins (default)

For each token slot (`primary`, `surface`, `display`, etc.), the value seen on the **most pages** wins. Ties broken by total usage count across all pages.

**Rationale:** A truly canonical brand color appears everywhere; one-page outliers are accidents or marketing-page experiments.

**Example:**
- Home: `primary = #1A1C1E`
- Features: `primary = #1A1C1E`
- Pricing: `primary = #1A1C1E`
- Docs: `primary = #0F1115` (slightly different — page-specific dark mode default)

Result: `primary = #1A1C1E` (3 of 4 pages). The `#0F1115` is dropped but recorded in prose ("/docs page used #0F1115 as primary; treated as page-local override").

### Strategy 2 — First-wins (home is authoritative)

The first URL in the input list is canonical. Other pages contribute only **NEW** tokens (e.g., a `tertiary` color seen on /features but not /home is added; a different value for `primary` on /features is dropped silently).

**Rationale:** When the user explicitly orders URLs by importance ("home first, then secondary surfaces"), respect that ordering.

**Use when:** the user says "the homepage is the brand reference; the other pages may have drifted".

### Strategy 3 — Merge-by-role (positional weighting)

Each URL gets a role weight (see [URL-role taxonomy](#url-role-taxonomy)). Token values are scored by `sum(weight) × usage_count` across the pages they appear on. Highest score wins.

**Rationale:** Home > features > docs in terms of how authoritative the styling is — the home page is the curated brand surface; docs are often a template the brand team rarely touches.

**Use when:** the URLs span a mix of curated (home) and templated (docs) surfaces.

## Per-token merge rules

The merge layer treats each token slot independently:

| Token type | Merge granularity | Conflict handling |
|---|---|---|
| `colors` (primary, secondary, surface, etc.) | Per-slot | Apply chosen strategy; record losers in prose |
| `typography.fontFamily` (display, body, mono) | Per-slot | Apply chosen strategy; flag if 2+ families compete |
| `typography` sizes / weights | Union, dedupe | If the same level (`body-md`) maps to different `fontSize`, keep the most-frequent |
| `rounded.sm/md/lg/full` | Union, dedupe; sorted by value | Cluster nearby values (within 2px) before merging |
| `spacing.scale` | Union, dedupe; sorted | If multiple base units (4 vs 8) detected, prefer the one that fits more values |
| `components.button-primary`, etc. | Per-component | Apply chosen strategy on each property (background, padding, radius) |

Spacing and rounded scales are UNION-DEDUPED rather than strategy-merged because they are intrinsically multi-value (a system has `sm`, `md`, `lg` simultaneously). Per-slot competition only applies to scalar tokens.

## Provenance recording

The output DESIGN.md prose section names every contributing URL and flags any per-token disagreements:

```markdown
## Colors

Extracted from 4 pages: /, /features, /pricing, /docs.

The palette is consistent across the 3 marketing pages. The /docs page
uses a slightly darker primary (#0F1115 vs the canonical #1A1C1E); we
adopted the marketing value as canonical since /docs appears to be a
templated surface with limited brand styling.

- **Primary (#1A1C1E):** Headlines, CTA primary fill. Seen on /, /features, /pricing.
- **Tertiary (#B8422E):** CTA accent on /features only; the other surveyed pages
  do not use this color. Verify it is brand-canonical, not a launch-page experiment.
```

This transparency lets the user accept or reject suspect tokens before the file becomes canonical.

## Failure modes

| Failure | Cause | Recovery |
|---|---|---|
| One URL fails to extract | 404, JS errors, timeout | Continue with the others; record in `warnings`; if 0 URLs succeed, return `failed` |
| All URLs agree but on a non-WCAG color | The brand legitimately uses low contrast | Emit `partial` with contrast violation in `warnings`; do NOT silently adjust |
| Strategy yields no clear winner (all 4 pages disagree on `primary`) | Site has no single brand color | Pick the most-used overall; flag in prose; suggest user pick manually |
| User-provided URLs span different brands (mistake) | User typo'd a URL pointing to a different domain | Detect domain mismatch; refuse with `failed` and surface the mismatch |
| Crawl-mode loop | (Not applicable — TECH-86 requires explicit URL list) | N/A |

## Cross-references

- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — single-URL extraction (per-URL leg of this flow)
  > What it does · When to use · Architecture · Inputs · What `dev-browser eval` returns · Heuristics for token extraction · Colors · Typography · Spacing · Radius · Components · Output structure · Failure modes and recovery · Validation gate · Cross-references
- [TECH-09-multipage-extraction](./TECH-09-multipage-extraction.md) — session-aware multi-page (login + N internal pages)
  > What it does · When to use · When NOT to use · Architecture · Session handling · Page-list strategy · A. User provides explicit URL list · B. Crawl mode (limited) · Per-page token aggregation · Colors · Typography · Components · Layout · Provenance annotations · Failure modes · Privacy and credential handling · Cross-references
- [TECH-91-shadow-and-elevation-extract](./TECH-91-shadow-and-elevation-extract.md) — shadow/elevation extraction (one token dimension that benefits from multi-page sampling)
- `../../../bin/amw-design-md-from-url.sh` — bin script accepting multiple URLs
- `../../../bin/amw-dev-browser-wrapper.sh` — browser primitive used internally
- [amw-design-md-extractor-agent](../../../agents/amw-design-md-extractor-agent.md) — the agent that owns this flow
