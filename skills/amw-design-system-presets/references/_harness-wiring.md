# Render-test harness wiring (T-004 / Wave 1 Track H0)

Each per-style file at `references/S-NNN-<slug>.md` references its
canonical render-test. This document describes HOW that test is composed
from `_test-skeleton.html` + the style's tokens, and HOW the resulting
PNG is parity-checked against the upstream source render via the Wave 0
verification harness.

## The pipeline (per style)

**Step 1 — Token injection.**
Read the S-NNN file's `## Token block` section. Parse each CSS custom
property (lines matching `--<token>: <value>;`). Substitute into
`_test-skeleton.html` in place of the `{{TOKEN}}` markers (e.g.
`{{PRIMARY}}` becomes the style's primary hex), producing:

```
/tmp/amw-style-parity-<S-NNN>-mine.html
```

Also substitute `{{STYLE_NAME}}` with the human-readable style name
(e.g. "Swiss / International").

**Step 2 — Render mine.**
Capture a desktop screenshot of the produced HTML via:

```bash
bash bin/amw-dev-browser-wrapper.sh shot \
  "file:///tmp/amw-style-parity-<S-NNN>-mine.html" \
  "/tmp/amw-style-parity-<S-NNN>-mine.png"
```

Fixed viewport: **1440x900** (no full-page scroll — fcvvdp requires
identical dimensions across both screenshots).

**Step 3 — Render source.**
Each S-NNN file's `## Canonical render-test pointer` names the upstream
reference: a demo URL or a local HTML under
`reports_dev/batch9/extracted/<repo>/...`.

Render via dev-browser at the same 1440x900 viewport:

```bash
bash bin/amw-dev-browser-wrapper.sh shot \
  "<upstream-url-or-file-uri>" \
  "/tmp/amw-style-parity-<S-NNN>-source.png"
```

**Step 4 — Parity check.**
Run the Wave 0 fcvvdp parity orchestrator:

```bash
bash bin/amw-verify-parity.sh \
  /tmp/amw-style-parity-<S-NNN>-source.png \
  /tmp/amw-style-parity-<S-NNN>-mine.png \
  --threshold 9.5
```

The threshold of **9.5 JOD** is the user's locked decision for
token-identical style tests.

**Step 5 — Record verdict.**
PASS (JOD >= 9.5): record the JOD score in the S-NNN file's
`## Render-test verdict` section:

```
JOD: 9.7 (PASS) -- 2026-05-26
```

Also log the per-run report path under:
`reports/batch9-verification/<YYYYMMDD_HHMMSS+HHMM>/<S-NNN>/`.

FAIL (JOD < 9.5): iterate on the token block in the S-NNN file until
the threshold is met, OR record an A-class justification in
`## Render-test verdict` explaining why the upstream demo cannot be
parity-tested (see "A-class exemptions" below).

## Light + dark variants

If the style defines both light and dark token bundles, repeat the full
pipeline (steps 1-4) for each variant, substituting the dark tokens:

```
/tmp/amw-style-parity-<S-NNN>-mine-dark.png
/tmp/amw-style-parity-<S-NNN>-source-dark.png
```

Both light AND dark variants must independently meet the JOD >= 9.5
threshold. A style that passes light but fails dark is considered FAIL.

## Mobile variant

The `_test-skeleton.html` is fully responsive. When a style ships
mobile-specific tokens (different radius, font-size, spacing) or
mobile-specific invariants, also render at **375x812**:

```bash
bash bin/amw-dev-browser-wrapper.sh shot \
  "file:///tmp/amw-style-parity-<S-NNN>-mine.html" \
  "/tmp/amw-style-parity-<S-NNN>-mine-mobile.png" \
  --width 375 --height 812
```

fcvvdp parity at both desktop AND mobile is required for such styles.

## Acceptance thresholds

| Test type | JOD threshold |
|---|---|
| Token-identical style test (skeleton vs upstream demo) | >= 9.5 |
| Technique reimplementation (downstream from style application) | >= 9.0 |

Per-style files cite which threshold applies in `## Render-test verdict`.

## A-class exemptions

Some upstream demos cannot be rendered for fcvvdp comparison:

- **Build-required demo**: the upstream demo requires a host-side build
  (e.g. Vite, Next.js SSR). Use the static-export or Storybook variant
  if available; otherwise mark `A-class: build-required` in the verdict
  and provide a prose-level token verification instead.
- **Proprietary assets**: the demo uses fonts, images, or icons the
  plugin cannot redistribute. Document the specific asset and mark
  `A-class: proprietary-assets`.
- **Prose-only source**: the upstream source is a specification article,
  not a rendered demo. Mark `A-class: prose-only` and add a manual
  token audit table in the S-NNN file.
- **Third-party CDN dependency**: the demo makes cross-origin requests
  that fail in the local render environment. Mark `A-class: cdn-dep`.

An A-class exemption is NOT a pass — it is a documented skip with a
reason. The field format:

```
JOD: A-class (build-required) -- 2026-05-26
Reason: upstream demo requires Next.js SSR; static export not available.
Manual audit: token values verified against source CSS dump on 2026-05-26.
```

## Report locations

Per-run parity reports are written to:

```
reports/batch9-verification/<YYYYMMDD_HHMMSS+HHMM>/<S-NNN>/
  mine.png
  source.png
  parity-report.json   (fcvvdp raw output)
  verdict.txt          (PASS/FAIL + JOD + threshold)
```

Resolve the main-repo root via the Wave 0 harness prologue:

```bash
MAIN_ROOT="$(git worktree list | head -n1 | awk '{print $1}')"
REPORT_DIR="$MAIN_ROOT/reports/batch9-verification/$(date +%Y%m%d_%H%M%S%z)/$S_NNN"
mkdir -p "$REPORT_DIR"
```

## What this is NOT

- NOT a substitute for the broader Wave 1 verification. Technique and
  brand-library tests run separately via their own harness invocations.
- NOT a license to render upstream demos that require host-side builds.
  A-class exemptions are documented skips, not passes.
- NOT a replacement for the slop-verifier gate. The slop check
  (`bin/amw-ai-slop-check.py`) runs on final delivered HTML, not on
  the skeleton render.
- NOT exhaustive — the skeleton covers 8 UI primitives. Styles with
  specialized components (data charts, maps, code editors) require
  additional per-component test files authored in Track H-verify.

## Cross-references

- [SKILL](../SKILL.md) — preset skill orchestration
- [catalogue](./catalogue.md) — style routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test HTML scaffold
- `../../../bin/amw-verify-parity.sh` — Wave 0 parity orchestrator
- `../../../bin/amw-screenshot-compare.sh` -- fcvvdp JOD wrapper
- `../../../bin/amw-dev-browser-wrapper.sh` -- browser screenshot primitive
