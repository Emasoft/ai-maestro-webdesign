---
trdd-id: 6d8ffed6-e51f-4be4-a4ff-cc86278b6e2d
title: Batch 9 integration — harvest 260 items, reimplement, verify via fcvvdp screenshot-parity
status: in-progress
created: 2026-05-25T18:48:46+0200
updated: 2026-05-26T01:20:44+0200
---

# TRDD-6d8ffed6 — Batch 9 integration — harvest 260 items, reimplement, verify via fcvvdp screenshot-parity

**Filename:** `design/tasks/TRDD-20260525_184846+0200-6d8ffed6-batch9-integration.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)
**Approved plan:** `~/.claude/plans/cuddly-churning-narwhal.md` (this TRDD is the durable, git-tracked copy)
**Todo cross-ref:** task #82

## User directive (verbatim intent)

> "examine the skills … in SKILLS-TO-INTEGRATE/webdesign-skills-batch9 and
> extract the best ideas to integrate into our webdesign agent plugin."
> "be careful of malicious code. always scan first with the cpv scanner."
> "full first wave. but remember to not miss any idea, technique or trick …
> Even the most useless has at least a couple of good ideas … graphic styles
> are also good to add to the plugin DESIGN.md catalogue."
> Acceptance test: "use dev-browser to display a sample of the technique of
> the source with its libs, take a screenshot. then do the same with your
> implementation. compare the 2 screenshots. if identical the goal is
> reached. Otherwise fix/edit until they match. interactive elements must
> also be screenshotted before and after the interaction."
> Tool: "use this for image comparison: https://github.com/halidecx/fcvvdp"

## Scope

Integrate the harvested backlog `reports/batch9-analysis/MASTER-LEDGER.md` —
**260 distinct items** = 176 techniques (`T-001…T-176`) + 84 graphic-style
IDs (`S-001…S-083` incl. `S-010b`). Every ported item is proven by the
fcvvdp screenshot-parity acceptance test (or, for non-renderable items, by
transcription + applied-sanity-render).

## Locked decisions

1. **Image comparison = `fcvvdp`** (halidecx/fcvvdp 0.3.0, Apache-2.0) — fast
   C/Zig CVVDP (ColorVideoVDP) perceptual metric. PNG in, `-j` JSON out, JOD
   score. JOD scale: 10.0 identical · 9.0–10.0 barely visible · 8.0–9.0
   slight · 7.0–8.0 noticeable. Built from source via Zig 0.16.x into
   gitignored `libs_dev/fcvvdp/` (verification-only, not shipped).
2. **Acceptance bar = Strict numeric → JOD.** Token-identical style tests
   **JOD ≥ 9.5**; technique reimplementations **JOD ≥ 9.0**; below ⇒ fail +
   iterate. Recalibratable after first runs.
3. **Immediate scope (Wave 1, "full first wave") = P1 + prescriptive styles**
   — all 20 P1 techniques + brand DESIGN.md library + the ~45 named styles
   with token blocks (S-001…S-045). Everything else = Waves 2–3 backlog.

The 20 P1 techniques: T-001, T-004, T-025, T-029, T-030, T-040, T-041,
T-042, T-043, T-044, T-045, T-046, T-054, T-063, T-064, T-084, T-085, T-088,
T-097, T-139 (+ T-026 sound-designer-agent pulled in as T-001's owner).

## Verification classes (from the ledger)

- **V** (visual, 115) — screenshot-parity via fcvvdp; ≥9.5 token-identical / ≥9.0 technique; desktop+mobile, light+dark.
- **I** (interactive, 16) — before+after-interaction screenshots, both pairs ≥9.0; sound also asserts `AudioContext` fired.
- **A** (abstract, 128) — transcription exact + applied-sanity-render + mechanical checker green (no screenshot).
- **Escape hatch:** a V/I item whose source has no runnable/content-matchable demo is verified as A-class, with the reason recorded in its per-item report.

## License handling

- direct-port (MIT/Apache-2.0): transcribe/adapt + attribution.
- clean-room (GPL/none/unknown): reimplement, no verbatim copy. GPL: T-034,
  T-068, T-087, T-089 (GPL-3.0); T-135, T-166 (GPL-2.0). Wave-1 clean-room =
  T-139 only.
- Batch9 **source** demos: render ONLY in the dev-browser sandbox; never run
  source host tooling (npm/bun/node build). `fcvvdp` build is exempt (trusted
  user-requested verification toolchain).

## Architecture (260 items → plugin surfaces)

- §1 NEW SKILLS → `skills/amw-<name>/` (P1: `amw-ui-sound-design`, `amw-design-system-presets`).
- §2 NEW AGENTS → `agents/amw-<name>-agent.md` 14-section template (P1: `amw-slop-verifier-agent`, + `amw-sound-designer-agent`).
- §3 NEW BIN → `bin/amw-*.{py,sh,mjs}` (P1: `amw-self-review-screenshot.sh`, content-slop module in `amw-ai-slop-check.py`; + harness `amw-screenshot-compare.sh`, `amw-verify-parity.sh`).
- §4 AUGMENT → edits + new `references/` in existing skills/agents.
- §6 GRAPHIC STYLES → `skills/amw-design-system-presets/references/S-NNN-*.md` + `catalogue.md`.
- Auto-discovery is total: no plugin.json edits except adding new skill dirs to `cpv.allow_orchestrator_traversal`.

## Plan / phasing

Full phasing in `~/.claude/plans/cuddly-churning-narwhal.md`:
- **Wave 0** — verification harness foundation (fcvvdp build + `amw-screenshot-compare.sh` + `amw-verify-parity.sh` + tests + fixtures + tests/README). Built first; gates everything.
- **Wave 1** — Tracks A–H (anti-slop refs, slop-verifier agent, DESIGN.md reasoning + brand library, extraction fidelity, UX scorecard, UI sound, CJK typography, style catalogue S-001…S-045). ≤5 files/phase; brand-library + style-catalogue are swarmed.
- **Wave 2** — P2 backlog (86). **Wave 3** — P3 backlog (70). Phase-planned when reached.

## Per-phase protocol

re-read → backup-if-editing (`docs_dev/backups/<ts>-batch9/`) → ≤5 files →
verify (fcvvdp JOD for V/I, transcription+sanity for A, pytest for bins, CPV
validate for skills) → fix until green → commit by explicit paths (never
`git add -A`) → tick ledger → next.

## Acceptance criteria (Wave 1 exit)

All 20 P1 items + brand library + S-001…S-045 ported; every V/I item ≥ its
JOD bar (or A-class-justified); every A item transcription-exact +
sanity-rendered; touched bins pass pytest; touched skills pass
ai-slop-check / design-md-validate / CPV validate. Then check in with user
before Wave 2.

## Progress log

- 2026-05-25T18:48 — TRDD created; plan approved; Zig 0.16.0 confirmed
  present; fcvvdp clone+build kicked off into `libs_dev/fcvvdp/`. Wave 0 in
  progress.
- 2026-05-25T18:55 — **Wave 0 COMPLETE** (commit 9009a16). fcvvdp 0.3.0 built
  into `libs_dev/fcvvdp/`. Harness verified end-to-end: `bin/amw-screenshot-
  compare.sh` (fcvvdp JOD gate) + `bin/amw-verify-parity.sh` (dev-browser fixed-
  viewport render → compare). Identical→JOD 10.0 PASS, different→7.6/3.2 FAIL.
  Tests: `test_screenshot_compare.py` (5, fcvvdp-only, self-skip) +
  `test_verify_parity.py` (2, opt-in AMW_VERIFY). fcvvdp `-j` JSON → stderr;
  errors on dim-mismatch (⇒ fixed-viewport renders). Full suite green.
- 2026-05-25T18:58 — **dev-browser wrapper FIXED** (commit 839acc6, task #83).
  Discovered pre-existing bug: installed dev-browser dropped the
  `screenshot --url`/`eval --script` subcommands the wrapper used → shot/mobile/
  dom all broken (also blocked Wave 1 Track D). Rewrote onto the QuickJS script
  API (Playwright pages + saveScreenshot/writeFile). Verified: shot deterministic
  (JOD 10), mobile 375×812 PNG, dom valid JSON. Opt-in regression test added.
  Original backed up to `docs_dev/backups/20260525_185759+0200-batch9/`.
- 2026-05-26T01:20 — **Wave 1 Track A COMPLETE** (3 commits). A1 58c8e42:
  references/component-taste.md (T-041), pre-output-checklist.md (T-045),
  visual-direction-tokens.md (T-046, 8 anchors w/ token blocks + breaks-if).
  A2 ffb2f10 (additive, 154 ins / 0 del): ai-slop-avoid.md §VIII content
  anti-patterns + Preserve (T-042) + §IX anti-AI-cliché checklist (T-044);
  typography-system.md §VIII forbidden fonts (T-043); design-heuristics.md §X
  Refactoring-UI rules (T-054, Wathan/Schoger attrib). A3 35b6740:
  amw-ai-slop-check.py +9 content checks (T-030) on code-masked prose + 5
  real tests. Verified: faithful transcription, zero CJK, Swiss token render
  sane, full suite 92 passed / 6 skipped, ruff clean.
- Next: Wave 1 Track B (slop-verifier agent + self-review screenshot — browser).
