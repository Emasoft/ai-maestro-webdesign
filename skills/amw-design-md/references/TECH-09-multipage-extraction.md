---
name: TECH-09-multipage-extraction
category: extraction
source: clone-design-main (multi-page session-aware extraction)
also-in: TECH-07-url-extraction.md, TECH-08-codebase-extraction.md
status: stable
---

# TECH: Multi-page extraction with session awareness

## What it does

Documents how to extract a single DESIGN.md from a website that spans multiple pages — typically requiring authenticated browsing (login + N internal pages). Extends [TECH-07-url-extraction](TECH-07-url-extraction.md) to handle session cookies, page-by-page traversal, and per-page token aggregation.

The flow uses `amw-dev-browser` for the session-aware browsing. There is no dedicated bin script; the orchestration runs through `amw-design-md-extractor-agent` directly via `Bash` calls to `bin/amw-dev-browser-wrapper.sh` followed by `bin/amw-design-md-from-url.sh` per page.

## When to use

- User says: "extract DESIGN.md from this app — login + 3 dashboard pages"
- User says: "the design system covers logged-in views only; here's a test account"
- Brand-researcher needs to extract tokens from a SaaS product where the public landing differs from the authenticated product UI

## When NOT to use

- Public-only single-page extraction → use [TECH-07-url-extraction](TECH-07-url-extraction.md)
- Local codebase available → use [TECH-08-codebase-extraction](TECH-08-codebase-extraction.md) (faster, no auth issues)
- Pages behind a paywall the user does not own → out of scope; refuse

## Architecture

```
                    ┌────────────────────────────────────┐
                    │ User input:                         │
                    │  - login URL + credentials          │
                    │  - list of N pages to extract from  │
                    └────────────────┬───────────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────────┐
                    │ amw-design-md-extractor-agent       │
                    └────────────────┬───────────────────┘
                                     │
                                     ▼
                    For each page in [login, page1, ..., pageN]:
                      bin/amw-dev-browser-wrapper.sh
                          ├── --persist-session  (reuse cookies)
                          └── eval extraction script

                                     │
                                     ▼
                    Per-page JSON snapshots aggregated
                                     │
                                     ▼
                    Merge tokens:
                      - colors: union (deduplicated by hex)
                      - typography: union (deduplicated by fontFamily+size+weight)
                      - spacing: union
                      - rounded: union
                      - components: per-page or merged with provenance
                                     │
                                     ▼
                    Final DESIGN.md with per-page provenance notes
```

## Session handling

`amw-dev-browser` supports a `--persist-session` (or equivalent) flag that reuses the browser's cookie jar across invocations. The agent:

1. **Login step**: Invokes `dev-browser` with login URL + credentials. The browser session is persisted to a temp profile dir.
2. **Page traversal**: Subsequent invocations reuse the same profile dir. The session cookies authenticate each request.
3. **Cleanup**: At the end of extraction, the temp profile dir is deleted.

Credentials are NEVER written to a report or logged. They are passed via `dev-browser` env / arguments and discarded after the session ends.

## Page-list strategy

Two modes:

### A. User provides explicit URL list

```yaml
login_url: "https://app.example.com/login"
credentials:
  email: "test@example.com"
  password: "$ENV_VAR"   # passed via env, never in the input doc
pages:
  - "https://app.example.com/dashboard"
  - "https://app.example.com/settings"
  - "https://app.example.com/profile"
  - "https://app.example.com/onboarding/step-1"
```

The agent traverses each URL in order. This is the safest mode.

### B. Crawl mode (limited)

The agent provides a starting URL and a max-pages cap; the extractor follows internal links up to the cap. **Disabled by default** — opt-in via `--crawl --max-pages N`. Crawl mode is more brittle (can get stuck on infinite scroll, can wander outside the design surface). Prefer mode A when possible.

## Per-page token aggregation

After all per-page snapshots are collected:

### Colors
Each page contributes a list of colors. Union all, dedupe by exact hex match. The most-used color across all pages → `primary`. Per-page-only colors (appearing on one page only) are flagged as suspect and noted in the prose ("Found color #xxx only on /settings; verify it is brand-canonical, not a one-off").

### Typography
Same union/dedupe. Font families seen on every page → likely the system fonts. Family seen on one page only → flagged.

### Components
The component extraction now has multiple instances of "the primary button". The agent computes the consensus: if 4 pages have button styles within a tolerance (same color, same radius, ±2px padding), the consensus is the canonical button. If pages diverge significantly, the agent emits a warning and surfaces the inconsistency.

### Layout
Spacing and grid often DO vary across pages (dashboard uses denser grid; landing uses sparser). The agent extracts the most common scale and notes per-page deviations in `## Layout` prose.

## Provenance annotations

The output DESIGN.md prose annotates origin:

```markdown
## Colors

The palette is consistent across the 4 surveyed pages.

- **Primary (#1A1C1E):** Headlines, CTA primary fill. Seen on all 4 pages.
- **Tertiary (#B8422E):** Single CTA accent. Seen on /dashboard and /onboarding only;
  /settings and /profile do not use this color.
- **Surface-elevated (#F7F5F2):** Card backgrounds. Seen on /dashboard
  primarily; other pages use the default surface color.

(Tokens with limited per-page presence may indicate one-off styling rather
than canonical system tokens. Verify before treating as system-wide.)
```

This transparency lets the user accept or reject suspect tokens before the file becomes canonical.

## Failure modes

| Failure | Cause | Recovery |
|---|---|---|
| Login fails | Wrong credentials, captcha, MFA | Return `failed` with `blocking_issues=["Login at <url> failed"]`. Do NOT retry with stored credentials. |
| Session expires mid-traversal | Long traversal, server-side timeout | Re-login automatically. If re-login also fails, return `partial` with snapshots up to the failure point. |
| Page returns 403 / 404 mid-traversal | Permission problem, page deleted | Skip the page; note in `warnings`; continue. |
| Rate-limit (429) | Site detects automation | Slow down (insert delays); fall back to snapshots-so-far if persists. |
| Crawl mode loops | Infinite-scroll or paginated content | Detect via URL similarity; cap at `--max-pages`. |

## Privacy and credential handling

- Credentials passed via env vars, never inline in the input doc, never written to logs or reports.
- The temp browser profile is deleted after extraction; cookies do NOT persist after the agent run.
- The output DESIGN.md does NOT mention credentials. URLs in provenance annotations may be redacted on user request (e.g., for sensitive internal apps).

## Cross-references

- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — single-URL extraction (subset of this flow)
- [TECH-08-codebase-extraction](./TECH-08-codebase-extraction.md) — when local source is available (preferred)
- `../../../bin/amw-dev-browser-wrapper.sh` — browser primitive
- `../../amw-dev-browser/SKILL.md` — dev-browser skill spec
- `../../../agents/amw-design-md-extractor-agent.md` — the agent that owns this flow
