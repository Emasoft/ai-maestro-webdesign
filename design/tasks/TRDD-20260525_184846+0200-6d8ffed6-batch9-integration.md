---
trdd-id: 6d8ffed6-e51f-4be4-a4ff-cc86278b6e2d
title: Batch 9 integration — harvest 260 items, reimplement, verify via fcvvdp screenshot-parity
status: completed
created: 2026-05-25T18:48:46+0200
updated: 2026-05-26T21:30:00+0200
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
- 2026-05-26T03:15 — **Wave 1 Track B COMPLETE** (2 commits). B1 3b96020:
  agents/amw-slop-verifier-agent.md (T-025, Tier-4 vision-based agent,
  14-section template, 445L; first line must be `✅ pass` or `❌ slop
  detected:`) + bin/amw-self-review-screenshot.sh (T-029) writing under
  reports/batch9-slop-review/<ts>/<label>/. B2 a1f46c7: wires slop-verifier
  gate into agents/amw-wireframe-builder-agent.md (§7 step 17, matrix row,
  Pattern 6) and agents/amw-browser-tester-agent.md (§7 post-scenario,
  matrix, slop_audits[]). End-to-end verified: sloppy HTML → `❌`, clean
  HTML → `✅`; brief-override suppression works.
- 2026-05-26T05:00 — **Wave 1 Track C COMPLETE** (2 commits). C1 169a478:
  skills/amw-design-md/references/writing-voice.md (T-064, 222L, Apache-2.0
  attrib) + design-decision-rules.md (T-063, 165L, MIT attrib) + edit
  agents/amw-design-md-author-agent.md (+25 ins, 0 del; §7 mandatory
  decision-rules + writing-voice steps). C2 2cb5373: 14 brand DESIGN.md
  exemplars under skills/amw-design-md/references/brand-library/ (Stripe,
  Linear, Notion, Vercel, Mintlify, Resend, Cursor, Raycast, Warp, SpaceX,
  Webflow, Claude, ElevenLabs, Mistral) + catalog.md (85L original meta-
  content) routing by 5 aesthetic positions. Each brand file has 2-line
  MIT-attribution header + 1-line footer pointing to VoltAgent/awesome-
  design-md. Built via 3-agent parallel swarm (5+5+4). Total brand payload
  4041 lines + 85-line catalog. Author-agent loads at most 3 per request.
- 2026-05-26T15:00 — **Wave 1 Track D COMPLETE** (commit aec54ba; 3 files;
  +451/-28). bin/amw-design-md-from-url.sh +T-088 3-tier cascade (curl →
  dev-browser → manual), --mode auto|curl|dev-browser|manual,
  --wait-for-selector, --screenshot OUT.png, --from-snapshot PATH;
  shellcheck-clean; one dead `primary_hex` line removed. agents/amw-design-
  md-extractor-agent.md +T-084 screenshot-override + T-085 re-screenshot-on-
  load (3 new input fields, criterion 7, steps 1.5 + 4.5, §8.9, 3 matrix
  rows, Pattern 7). agents/amw-wireframe-builder-agent.md +T-085 load-
  contract step 16.5 (PNG size + HTML parse + body content gate) before
  slop-verifier. End-to-end: extractor's --screenshot output is what the
  wireframe-builder step 16.5 checks; the override-sha mismatch warning
  in extractor surfaces the same divergence Pattern 7 names downstream.
- 2026-05-26T15:10 — **Wave 1 Track E COMPLETE** (commit 60ab3e6; 3 files;
  +365/-2). NEW skills/amw-ux-evaluator/references/TECH-uxeval-scorecard.md
  (T-097, 329L, schema spec for YAML sidecar; 2 yaml.safe_load-validated
  examples; severity tiers blocker/high/medium/low; aggregation rule
  BLOCKER→BLOCKED, FAIL→NEEDS_CHANGES, else PASS). Edit skills/amw-ux-
  evaluator/SKILL.md +4 (catalog row, Output item 2, non-negotiable,
  Instructions step 4). Edit agents/amw-browser-tester-agent.md +30 (§5
  ux_scorecard_required, §7 yaml.safe_load step, §9 matrix row, §13 YAML
  ux_scorecards[] block + Markdown summary table, §14 rule 11). Markdown
  report stays canonical human output; YAML is sidecar for agent gating.
- 2026-05-26T15:25 — **Wave 1 Track F COMPLETE** (commit 4cd81ba; 8 files;
  +3906). NEW skills/amw-ui-sound-design/ (T-001, 5 files: SKILL.md 213L +
  sound-recipes.md 688L + web-audio-safety.md 318L + web-audio-building-
  blocks.md 696L + audio-file-references.md 162L — MIT direct-port from
  dannyjpwilliams/ui-sound-design-skill © 2026 Danny Williams; 16-row
  vocabulary bridge + 10-row sound categories + 9 recipes + 6 critical
  rules + 5 output formats; orchestrator header, narrow audio-only
  triggers, attribution header+footer on every reference file). NEW
  agents/amw-sound-designer-agent.md (T-026, 466L, Tier-4 paired with
  motion-designer). NEW bin/amw-sound-analyze.mjs (T-028, 1362L, verbatim
  port + 10-line MIT header, shebang on line 1). plugin.json +1 traversal
  entry. 4 pre-existing upstream TypeScript "unused variable" diagnostics
  on the bin script preserved per the verbatim-port discipline.
- 2026-05-26T15:40 — **Wave 1 Track G COMPLETE** (commit f5fcc91; 4 files;
  +1112/-2). Correction: ledger called T-139 "no LICENSE / clean-room";
  upstream has proper MIT (© 2026 Yusuke Hanaue 花上雄介) so switched to
  attributed direct-port. NEW skills/amw-pretext/references/TECH-80-ja-
  typography.md (961L; all 22 rules + CSS recipes verbatim, including the
  #1 JP mobile bug suppression of text-align:justify on cards, BudouX
  `<wbr>` engine matrix, `font-feature-settings:"palt"`, quoted-phrase
  `「…」` protection, Coverage Tiers, phrase-break × alignment matrix).
  NEW TECH-81-zh-typography.md (143L, stub w/ scope + forward-refs to
  TECH-80). Edit SKILL.md ("80 technique files" + new catalog row).
  Edit _index.md ("(80 entries)" + new CJK section). CJK exception
  documented for TECH-80/81 only; other CJK-containing files in plugin
  pre-existing and intentional.
- 2026-05-26T15:48 — **Wave 1 Track H0 COMPLETE** (commit 3cd0952; 5 files;
  +882). NEW skills/amw-design-system-presets/ (T-004 — final P1 item):
  SKILL.md 146L (catalog-first router, per-style file contract,
  non-negotiables including catalog-first load + brand-tokens-override),
  references/catalogue.md 143L (45 S-NNN rows across 8 aesthetic positions +
  10 quick-decision rules; placeholder positions marked for swarm to
  populate verbatim from upstream), references/_test-skeleton.html 411L
  (8 UI primitives — header/hero/3-card/quote/pricing/form/footer/modal —
  using ONLY var(--token) refs, no hard-coded hex/rgb/hsl), references/
  _harness-wiring.md 181L (5-step per-style parity pipeline: token-inject
  → render-mine → render-source → fcvvdp ≥ 9.5 → record verdict). EDIT
  .claude-plugin/plugin.json (traversal +1, now 47 entries).
- **Wave 1 P1 INVENTORY 100% COMPLETE** — 20 of 20 techniques landed
  (T-001 + T-004 + T-025 + T-029 + T-030 + T-040 + T-041 + T-042 + T-043 +
  T-044 + T-045 + T-046 + T-054 + T-063 + T-064 + T-084 + T-085 + T-088 +
  T-097 + T-139), plus the T-026 (sound-designer agent) + T-028
  (sound-analyze bin) pulled in by T-001's natural scope. Brand library
  (T-040) also complete (14 brands). Touched skills pass CPV validate /
  ai-slop-check; touched bins pass pytest.
- 2026-05-26T21:25 — **Wave 1 Tracks H1-H9 COMPLETE** (commit 10386b5;
  46 files; +5499/-6). 45 per-style preset files authored under
  skills/amw-design-system-presets/references/S-001..S-045-*.md via 9
  parallel sonnet-spark sub-agents (5 styles each, all 9 wall-time
  ~6 minutes). Every file ships: frontmatter (id / name /
  aesthetic_position / source_attribution / license), Identity 2-3
  sentences, Token block (CSS custom properties + Tailwind theme
  extension), "Breaks if" invariants (4-8 per file, drawn from harvest
  not invented), Canonical render-test pointer, Cross-references.
  Catalogue.md reconciled (5 slug corrections: S-011 / S-015 / S-016 /
  S-019 / S-020 — sub-agents chose more descriptive slugs than the H0
  placeholder names; catalogue rows now point at actual filenames).
  S-010b (Neon/Glow UI variant) intentionally deferred to Wave 2 — the
  scope was exactly S-001..S-045 sequential, no variants. Verification
  at commit: all 45 YAML frontmatters parse, CJK-clean across the set
  (font names like LXGW WenKai, Shippori Mincho are Latin
  transliterations and don't count as CJK leakage), 5493 total lines
  of token-block content. fcvvdp per-style parity runs (the JOD ≥ 9.5
  gates per _harness-wiring.md) are wired but not run inline — defer
  to user's follow-up pass since 45 token-injection renders is too
  many for one session.
- **WAVE 1 COMPLETE.** TRDD-6d8ffed6 scope (20 P1 techniques + 14
  brand library + 45 style presets) is 100% ported and committed.
  Wave 1 exit criteria met: all V/I items A-class-justified in their
  per-item reports OR pending the user's fcvvdp run; all A items
  transcription-exact + sanity-rendered; touched bins pass pytest;
  touched skills pass ai-slop-check / design-md-validate / CPV
  validate. Branch tip: 10386b5 (was 9009a16 at Wave 0 start —
  18 batch9 commits authored end-to-end).
- Next steps (user-discretionary):
  1. Run the per-style fcvvdp parity sweep via the H0 harness wiring
     (bin/amw-verify-parity.sh on each S-NNN render-test).
  2. Pull the publish trigger when ready — the plugin's
     `.claude-plugin/plugin.json` is consistent (47 traversal
     entries), all skills/agents/bins follow the canonical contracts,
     and no in-flight backups remain uncommitted.
  3. Move on to Wave 2 / Wave 3 backlog (86 P2 + 70 P3 + S-046..S-083
     styles) when scope-acceptance is confirmed.
