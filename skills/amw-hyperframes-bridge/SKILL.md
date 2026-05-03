---
name: amw-hyperframes-bridge
description: HTML composition to MP4 video rendering via the external Hyperframes monorepo. Triggers on "render HTML as video", "HTML to MP4", "website to video", "create video from HTML", "rasterize composition to mp4". Does NOT trigger on generic "animation" or "video" requests — those route to pretext, starter-components/animations.html, or the user's own pipeline. Use when rendering an HTML composition to an MP4 video file via the Hyperframes backend. Trigger with explicit "render HTML as video" or "HTML to MP4" phrasing.
version: 0.1.0
---

# Hyperframes Bridge

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **External dependency wrapper.** The actual Hyperframes monorepo lives at `../../external/hyperframes/` (cloned by `/amw-init` step 6 if the user opts in, OR by this skill on first render as a fallback). This skill documents the shell-out pattern; it does NOT vendor the monorepo.

## Overview

Renders HTML compositions to MP4 video by shelling out to the Hyperframes monorepo (`external/hyperframes/`). Accepts a single HTML scene file or a full Hyperframes project directory. Runs the mandatory pre-render gate (`lint → validate → inspect → render`) before calling `npx hyperframes render --output <mp4>`. Returns the MP4 path and a job-completion report. No re-implementation of the Hyperframes pipeline inside the plugin — shell-out only.

## Instructions

1. Verify the external repo with two checks: `external/hyperframes/package.json` must exist, and `npx hyperframes render --help` must respond; fail fast if either check fails.
2. Resolve the project directory: use `project_dir` if provided, or scaffold a temp project from `html_scene_path`; fail immediately if neither is supplied.
3. Run the pre-render gate sequence in order: `lint → validate → inspect → render` (abort if any step returns non-zero).
4. Execute `cd "$HF_PROJ_DIR" && npx hyperframes render --output <mp4>`; collect the output path.
5. Confirm the MP4 file exists and is non-empty; report the output path and any `inspect` warnings.
6. See the `## Invocation pattern` section below for the authoritative execution steps.

See the `## Invocation pattern` section below for the authoritative execution steps.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator as the final Phase B step in Main-agent mode when the approved design requires MP4 video output. The orchestrator may apply the full Hyperframes shell-out pipeline and composition techniques from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT (Phase B — terminal). HTML to MP4 video rendering pipeline. Triggered only when the user explicitly wants an HTML composition rasterized to a video file. Runs last, after composition authoring is complete.

## Trigger conditions

Invoke this skill ONLY when the request matches one of:

- "render this HTML as a video" / "render to MP4"
- "HTML to MP4" / "website to video" / "page to video"
- "create a video from this HTML composition"
- "rasterize the composition to video"
- Explicit mention of Hyperframes / `hyperframes render` / `.hf.html`

Do NOT invoke on generic mentions of "animation", "motion", "video playback", or "animated component" — those belong to:
- `../amw-design-principles/starter-components/animations.html` (in-browser Stage + Sprite timeline)
- `../amw-pretext/` (typographic motion — `pretext-art/` is a deprecated redirect)
- The user's own pipeline

## Prerequisites

- **runtime_binaries (system prerequisites):** Node.js >= 22, git
- **runtime_binaries (installed by `/amw-init`):** Bun (Hyperframes's package manager), FFmpeg. Chrome is managed by Hyperframes itself via `hyperframes browser ensure` (uses Puppeteer + `@puppeteer/browsers` internally — NOT Playwright).
- **external source:** `../../external/hyperframes/` — the Hyperframes monorepo cloned from `https://github.com/heygen-com/hyperframes`. Pin to v0.4.30 or later for `inspect`, `--hdr`, and `data-variable-values` support. If the folder does not exist, `/amw-init` or this skill MUST clone it before proceeding:

  ```bash
  git clone --branch v0.4.30 --depth 1 https://github.com/heygen-com/hyperframes.git external/hyperframes
  cd external/hyperframes && bun install
  ```

## Input contract

The bridge accepts two mutually exclusive inputs. Provide exactly one:

| Field | Type | Description |
|---|---|---|
| `html_scene_path` | string (optional) | Absolute path to a single HTML file. The bridge scaffolds a temporary hyperframes project directory via `mktemp -d -t hf-XXXXXX` (POSIX-portable), writes the HTML as `index.html`, renders, then cleans up after the report is written. |
| `project_dir` | string (optional) | Absolute path to a pre-existing hyperframes project directory (contains `index.html` and optionally `compositions/`, `assets/`). The bridge `cd`s directly into it — no scaffolding. Supports sub-compositions, audio, and external assets. |

If both are provided, `project_dir` wins. If neither is provided, fail immediately.

## Invocation pattern

1. **Verify external repo — two checks required:**
   ```bash
   # Check 1 — package.json present (monorepo cloned)
   test -f "external/hyperframes/package.json" || exit-fail "monorepo not found"
   # Check 2 — CLI responds (install is functional)
   # @hyperframes/cli is NOT published to npm — must run from inside the monorepo workspace
   (cd external/hyperframes && npx hyperframes render --help) >/dev/null 2>&1 || exit-fail "hyperframes CLI not functional — run bun install inside external/hyperframes/"
   ```
   If either check fails, fail fast. Do not proceed.

2. **Resolve the project directory.**
   - If `project_dir` is provided: use it directly. Set `HF_PROJ_DIR="$project_dir"`.
   - If `html_scene_path` is provided: scaffold a temp project:
     ```bash
     HF_PROJ_DIR="$(mktemp -d -t hf-XXXXXX)"
     cp "$html_scene_path" "$HF_PROJ_DIR/index.html"
     ```
   - Otherwise: fail immediately.

3. **Run the pre-render gate sequence: `lint → validate → inspect → render`.**
   ```bash
   cd "$HF_PROJ_DIR"
   npx hyperframes lint
   npx hyperframes validate
   npx hyperframes inspect --json  # abort if any errors (non-zero exit with --strict)
   ```
   See [TECH-hyperframes-cli-lint](./references/TECH-hyperframes-cli-lint.md), [TECH-hyperframes-cli-validate](./references/TECH-hyperframes-cli-validate.md), [TECH-hyperframes-cli-inspect](./references/TECH-hyperframes-cli-inspect.md).
   > [TECH-hyperframes-cli-inspect.md] What it does · When to use · How it works · Flags · Output (JSON mode) · Minimal example · Opt-out attributes · Gotchas · Cross-references

   > **Gate-sequence note:** The bridge's sequence (`lint → validate → inspect → render`) intentionally extends upstream's (`lint → inspect → preview → render`, see `external/hyperframes/skills/hyperframes-cli/SKILL.md:14-17`) by adding `validate` for unattended Phase B pipelines and dropping `preview` (a developer-loop primitive).

4. **Render.** From inside the resolved project directory:
   ```bash
   cd "$HF_PROJ_DIR"
   npx hyperframes render --output <abs-mp4-path>
   ```
   Additional flags as needed (`--fps`, `--quality`, `--format`, `--hdr`, etc.) — see [TECH-hyperframes-cli-render](./references/TECH-hyperframes-cli-render.md).
   > [TECH-hyperframes-cli-render.md] What it does · When to use · How it works · Flags · Quality guidance · Transparent video · Minimal example · Workers tuning · Gotchas · Cross-references

5. **Return the MP4 path** to the caller. If the project dir was a temp scaffold (`html_scene_path` path), remove it after the report is written.

## HTML composition rules (Hyperframes-specific)

Compositions use plain HTML with `data-*` timeline attributes on a `#stage` root and its children (tracks / clips / overlays). This is the same Stage + Sprite mental model as `../amw-design-principles/starter-components/animations.html` — Hyperframes extends it with multi-track audio/video mixing and offscreen deterministic render.

Key attributes (authoritative schema lives in `external/hyperframes/packages/core/` once cloned):

- `data-composition-id` — stage-level identifier
- `data-start`, `data-duration` — seconds, per clip
- `data-track-index` — layer ordering (video / overlay / audio tracks)
- `data-width`, `data-height` — stage-level canvas dimensions

Do NOT introduce Framer Motion, GSAP-as-dependency, or any third-party animation runtime into the bridge. Hyperframes has its own Frame Adapter pattern; if the user wants GSAP inside a composition, that is Hyperframes's concern, not the bridge's.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `hyperframes-bridge` is the user asking about?
  - **hyperframes** (27 techniques)
    - [TECH-hyperframes-capture-overview](./references/TECH-hyperframes-capture-overview.md) — Website-to-Hyperframes capture — pipeline overview
      > What it does · When to use · How it works · Video type reference · Format presets · Minimal example · Gotchas · Cross-references
    - [TECH-hyperframes-capture-step-1-capture](./references/TECH-hyperframes-capture-step-1-capture.md) — Step 1 — Capture & Understand
    - [TECH-hyperframes-capture-step-2-design](./references/TECH-hyperframes-capture-step-2-design.md) — Step 2 — Write DESIGN.md
    - [TECH-hyperframes-capture-step-3-script](./references/TECH-hyperframes-capture-step-3-script.md) — Step 3 — Write SCRIPT.md
      > What it does · When to use · How it works · Narration style rules · Format · Gate · Minimal example · Gotchas · Cross-references
    - [TECH-hyperframes-capture-step-4-storyboard](./references/TECH-hyperframes-capture-step-4-storyboard.md) — Step 4 — Write STORYBOARD.md
    - [TECH-hyperframes-capture-step-5-vo](./references/TECH-hyperframes-capture-step-5-vo.md) — Step 5 — Generate VO + map timing to beats
    - (see `## References` for the remaining 21 in this group)

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-hyperframes-capture-overview.md](./references/TECH-hyperframes-capture-overview.md)**
  > What it does · When to use · How it works · Video type reference · Format presets · Minimal example · Gotchas · Cross-references
  - Description: Website-to-Hyperframes capture — pipeline overview
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-capture-step-1-capture.md](./references/TECH-hyperframes-capture-step-1-capture.md)**
  - Description: Step 1 — Capture & Understand
  - TOC:
    - What it does
    - When to use
    - How it works
    - Gate
    - Minimal example
    - SITE.md — acme.com
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-capture-step-2-design.md](./references/TECH-hyperframes-capture-step-2-design.md)**
  - Description: Step 2 — Write DESIGN.md
  - TOC:
    - What it does
    - When to use
    - How it works
    - Gate
    - Minimal example
    - Style Prompt
    - Colors
    - Typography
    - Motion / Easing
    - Visual Language
    - What NOT to Do
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-capture-step-3-script.md](./references/TECH-hyperframes-capture-step-3-script.md)**
  - Description: Step 3 — Write SCRIPT.md
  - TOC:
    - What it does
    - When to use
    - How it works
    - Gate
    - Minimal example
    - Beat 1 (hook)
    - Beat 2 (problem)
    - Beat 3 (solution)
    - Beat 4 (proof)
    - Beat 5 (CTA)
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-capture-step-4-storyboard.md](./references/TECH-hyperframes-capture-step-4-storyboard.md)**
  - Description: Step 4 — Write STORYBOARD.md
  - TOC:
    - What it does
    - When to use
    - How it works
    - Gate
    - Minimal example
    - Beat 1 (hook, 0-2.5 s) — "Address verification, in under 120 milliseconds."
    - Beat 2 (problem, 2.5-7.5 s) — ...
    - ...
    - Asset Audit
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-capture-step-5-vo.md](./references/TECH-hyperframes-capture-step-5-vo.md)**
  - Description: Step 5 — Generate VO + map timing to beats
  - TOC:
    - What it does
    - When to use
    - How it works
    - Gate
    - Minimal example
    - Beat 1 (hook, 0.0-2.47 s) — "Address verification, in under 120 milliseconds."
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-capture-step-6-build.md](./references/TECH-hyperframes-capture-step-6-build.md)**
  > What it does · When to use · How it works · Per-composition workflow · Gate · Minimal example · Gotchas · Cross-references
  - Description: Step 6 — Build Compositions
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-capture-step-7-validate.md](./references/TECH-hyperframes-capture-step-7-validate.md)**
  > What it does · When to use · How it works · Validate sequence · Gate · Minimal example · Gotchas · Cross-references
  - Description: Step 7 — Validate & Deliver
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Intent
    - Video type / format
    - State
    - Known issues
    - Next session
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-doctor.md](./references/TECH-hyperframes-cli-doctor.md)**
  > What it does · When to use · How it works · What `doctor` checks · Minimal example · Common failure modes surfaced by `doctor` · Gotchas · Cross-references
  - Description: `hyperframes doctor` + environment utilities
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-init.md](./references/TECH-hyperframes-cli-init.md)**
  > What it does · When to use · How it works · Registry templates (`--example`) · Side effects · Minimal example · Gotchas · Cross-references
  - Description: `hyperframes init` — scaffold a project
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-lint.md](./references/TECH-hyperframes-cli-lint.md)**
  - Description: `hyperframes lint` — static validation
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-preview.md](./references/TECH-hyperframes-cli-preview.md)**
  - Description: `hyperframes preview` — live studio preview
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-render.md](./references/TECH-hyperframes-cli-render.md)**
  > What it does · When to use · How it works · Flags · Quality guidance · Transparent video · Minimal example · Workers tuning · Gotchas · Cross-references
  - Description: `hyperframes render` — capture composition to MP4 / WebM
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-transcribe.md](./references/TECH-hyperframes-cli-transcribe.md)**
  > What it does · When to use · How it works · Models · Output schema · Minimal example · Gotchas · Cross-references
  - Description: `hyperframes transcribe` — audio → word-level timestamps
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-tts.md](./references/TECH-hyperframes-cli-tts.md)**
  > What it does · When to use · How it works · Flags · Voice naming scheme · Speed tuning · Minimal example · Gotchas · Cross-references
  - Description: `hyperframes tts` — text-to-speech via Kokoro-82M
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-validate.md](./references/TECH-hyperframes-cli-validate.md)**
  > What it does · When to use · How it works · Output · When warnings appear · Minimal example · Gotchas · Cross-references
  - Description: `hyperframes validate` — WCAG contrast audit
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-inspect.md](./references/TECH-hyperframes-cli-inspect.md)**
  > What it does · When to use · How it works · Flags · Output (JSON mode) · Minimal example · Opt-out attributes · Gotchas · Cross-references
  - Description: `hyperframes inspect` — visual layout audit
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Opt-out attributes
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-browser.md](./references/TECH-hyperframes-cli-browser.md)**
  - Description: `hyperframes browser` — manage Chrome Headless Shell (Puppeteer-based, NOT Playwright)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-snapshot.md](./references/TECH-hyperframes-cli-snapshot.md)**
  > What it does · When to use · How it works · Flags · Output · Minimal example · Gotchas · Cross-references
  - Description: `hyperframes snapshot` — capture key frames as PNG for visual verification
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-cli-capture.md](./references/TECH-hyperframes-cli-capture.md)**
  > What it does · When to use · How it works · Flags · Minimal example · Gotchas · Out of scope for the bridge · Cross-references
  - Description: `hyperframes capture` — capture a website as editable Hyperframes components
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-composition-core.md](./references/TECH-hyperframes-composition-core.md)**
  > What it does · When to use · How it works · Approach (narrative order) · Single-file skeleton · Visual Identity Gate (MUST — before writing HTML) · Gotchas · Cross-references
  - Description: Composition authoring — core model
  - TOC:
    - What it does
    - When to use
    - How it works
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-data-attributes.md](./references/TECH-hyperframes-data-attributes.md)**
  > What it does · When to use · How it works · Clip attributes (all clips) · Composition-level attributes (on the root `data-composition-id`) · Relative timing · Banned / deprecated attributes · Minimal example · Sub-composition wrapping · Per-instance variable injection via `data-variable-values` · Gotchas · Cross-references
  - Description: Data attributes — clip + composition schema
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-identity-gate.md](./references/TECH-hyperframes-identity-gate.md)**
  > What it does · When to use · How it works · DESIGN.md exists in the project? · visual-style.md exists? · User named a style (e.g. "Swiss Pulse", "dark and techy", "luxury brand")? · None of the above? · Minimal example · Gotchas · Cross-references
  - Description: Visual Identity Gate (HARD-GATE)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Style Prompt
    - Colors
    - Typography
    - What NOT to Do
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-layout-before-animation.md](./references/TECH-hyperframes-layout-before-animation.md)**
  > What it does · When to use · How it works · Why this matters · Minimal example · Wrong pattern (hardcoded dimensions + absolute positioning) · Layered + temporal intent · Gotchas · Cross-references
  - Description: Layout Before Animation
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-non-negotiables.md](./references/TECH-hyperframes-non-negotiables.md)**
  > What it does · When to use · How it works · The twelve rules · Determinism clause · Animation scope clause · Animation conflict clause · Minimal example · Gotchas · Cross-references
  - Description: Non-negotiable composition rules
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-registry-add.md](./references/TECH-hyperframes-registry-add.md)**
  > What it does · When to use · How it works · Blocks vs components · Paths (configurable in `hyperframes.json`) · Minimal example · Gotchas · Cross-references
  - Description: `hyperframes add` — install registry blocks + components
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-registry-blocks.md](./references/TECH-hyperframes-registry-blocks.md)**
  > What it does · When to use · How it works · Include pattern · Required attributes on the include · Verification · Minimal example · Gotchas · Cross-references
  - Description: Wiring registry blocks into host compositions
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-registry-components.md](./references/TECH-hyperframes-registry-components.md)**
  > What it does · When to use · How it works · Wiring process · Example component file · Merging into host · Minimal example · Gotchas · Cross-references
  - Description: Wiring registry components into host compositions
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-scene-transitions.md](./references/TECH-hyperframes-scene-transitions.md)**
  > What it does · When to use · How it works · Rule 1 — ALWAYS use transitions between scenes · Rule 2 — ALWAYS use entrance animations on every scene · Rule 3 — NEVER use exit animations except on the final scene · Rule 4 — Final scene only may fade elements out · Wrong pattern · Right pattern · Minimal example · Gotchas · Cross-references
  - Description: Scene transitions (non-negotiable rules)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-timeline-contract.md](./references/TECH-hyperframes-timeline-contract.md)**
  > What it does · When to use · How it works · Required pattern · Banned patterns · Allowed GSAP properties · Minimal example · Use `tl.set()` for later-scene clips · Gotchas · Cross-references
  - Description: Timeline contract — GSAP integration
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-hyperframes-visual-styles-library.md](./references/TECH-hyperframes-visual-styles-library.md)**
  - Description: `visual-styles.md` — 8 named visual-style presets
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Examples

See the worked examples in the per-step reference files under `./references/TECH-hyperframes-capture-step-*.md` (7-step website-to-video pipeline) and the composition authoring guide at [TECH-hyperframes-composition-core](./references/TECH-hyperframes-composition-core.md).
> [TECH-hyperframes-composition-core.md] What it does · When to use · How it works · Approach (narrative order) · Single-file skeleton · Visual Identity Gate (MUST — before writing HTML) · Gotchas · Cross-references

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-hyperframes-bridge/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. hyperframes project folders + rendered MP4 videos). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/videos/` created fresh)
   - Last-resort scratch: `/tmp/amw-hyperframes-bridge-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>-amw-video-producer-<slug>-<8-char-hash>.md`

   (The agent name is embedded in the path so multi-agent runs in the same minute don't collide; the 8-char hash disambiguates re-runs of the same agent on the same input. This grammar matches `agents/amw-video-producer-agent.md` §7.10 — both producers MUST emit the same shape.)

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Resources

- `../amw-design-principles/starter-components/animations.html` — the ~50-LOC Stage + Sprite timeline engine used for in-browser previews; Hyperframes shares the same rhythm.
- `../../bin/amw-html-export.py` — **NOT a substitute.** `html-export` renders a single frame to PNG/PDF; Hyperframes renders a multi-frame MP4 using Puppeteer + Chrome (managed by `hyperframes browser ensure`) + FFmpeg.
- `../amw-dev-browser/` — **NOT a substitute.** `dev-browser` is for input/automation; Hyperframes is the output rasterizer.
- `/amw-init` — installs Bun, FFmpeg, and clones `external/hyperframes/` on first use. Chrome for rendering is provisioned by Hyperframes itself via `hyperframes browser ensure`.
- External repo: `https://github.com/heygen-com/hyperframes`

## Non-negotiables

- Use the external monorepo via shell-out. Do NOT reimplement its pipeline inside the plugin.
- Do NOT vendor Hyperframes source into `skills/` — 500+ files is wrong scope for a skill.
- Do NOT substitute `dev-browser` for Hyperframes — they solve opposite problems (input vs. output).
- Do NOT substitute `html-export.py` — single-frame PNG is not video.
- The user MUST run `/amw-init` before first use to install Bun + FFmpeg and clone the external repo. Chrome is provisioned by running `(cd external/hyperframes && npx hyperframes browser ensure)` once after cloning.

## Error Handling

- **`external/hyperframes/` missing** — first-use clone step was skipped. Run `/amw-init` or clone manually (see Dependencies).
- **`npx hyperframes render --help` fails** — monorepo cloned but `bun install` not run. `cd external/hyperframes && bun install`.
- **`bun: command not found`** — Bun not installed. `/amw-init` provisions it via `brew install bun` (macOS) or `curl -fsSL https://bun.sh/install | bash`.
- **`ffmpeg: command not found`** — FFmpeg not on PATH. `/amw-init` installs it (macOS: `brew install ffmpeg`; Linux: distro package manager).
- **Chrome not provisioned** — Hyperframes uses Puppeteer + `@puppeteer/browsers` (NOT Playwright) to manage Chrome. Run `(cd external/hyperframes && npx hyperframes browser ensure)` to download Chrome Headless Shell.
- **HTML attribute parse errors** — composition is missing required `data-composition-id`, `data-start`, or `data-duration`. Re-author the HTML per the schema in `external/hyperframes/packages/core/`.
- **Video encoding failure** — check stderr log from the render shell-out; usually an FFmpeg codec mismatch or missing source asset (video/audio file referenced by the composition does not exist).
- **Stale clone** — if render fails with "method not found" errors that suggest an API change, verify the version: `node -e "console.log(require('./external/hyperframes/packages/cli/package.json').version)"`. If below 0.4.30, pull and re-run `bun install`.
