---
name: amw-hyperframes-bridge
description: HTML composition to MP4 video rendering via the external Hyperframes monorepo. Triggers on "render HTML as video", "HTML to MP4", "website to video", "create video from HTML", "rasterize composition to mp4". Does NOT trigger on generic "animation" / "video" — those route to pretext or the user's pipeline. Use when rendering HTML to MP4 via Hyperframes. Trigger with "render HTML as video" or "HTML to MP4".
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
   >
   > **Gate-sequence note:** The bridge's sequence (`lint → validate → inspect → render`) intentionally extends upstream's (`lint → inspect → preview → render` — see the upstream Hyperframes CLI SKILL.md inside the vendored `external/hyperframes/` monorepo) by adding `validate` for unattended Phase B pipelines and dropping `preview` (a developer-loop primitive).

4. **Render.** From inside the resolved project directory:
   ```bash
   cd "$HF_PROJ_DIR"
   npx hyperframes render --output <abs-mp4-path>
   ```
   Additional flags as needed (`--fps`, `--quality`, `--format`, `--hdr`, etc.) — see [TECH-hyperframes-cli-render](./references/TECH-hyperframes-cli-render.md).

5. **Return the MP4 path** to the caller. If the project dir was a temp scaffold (`html_scene_path` path), remove it after the report is written.

## HTML composition rules (Hyperframes-specific)

Compositions use plain HTML with `data-*` timeline attributes on a `#stage` root and its children (tracks / clips / overlays). This is the same Stage + Sprite mental model as `../amw-design-principles/starter-components/animations.html` — Hyperframes extends it with multi-track audio/video mixing and offscreen deterministic render.

Key attributes (authoritative schema lives in `external/hyperframes/packages/core/` once cloned):

- `data-composition-id` — stage-level identifier
- `data-start`, `data-duration` — seconds, per clip
- `data-track-index` — layer ordering (video / overlay / audio tracks)
- `data-width`, `data-height` — stage-level canvas dimensions

Do NOT introduce Framer Motion, GSAP-as-dependency, or any third-party animation runtime into the bridge. Hyperframes has its own Frame Adapter pattern; if the user wants GSAP inside a composition, that is Hyperframes's concern, not the bridge's.

## References

Full reference index: [INDEX.md](./references/INDEX.md) — 32 TECH-*.md files grouped by Capture pipeline (7 steps), CLI commands (12), Composition authoring (7), Registry (4). Each file has its own Table of Contents; load only the one you need.

## Examples

See the worked examples in the per-step reference files under `./references/TECH-hyperframes-capture-step-*.md` (7-step website-to-video pipeline) and the composition authoring guide at [TECH-hyperframes-composition-core](./references/TECH-hyperframes-composition-core.md).

## Output

A rendered **MP4 video file** plus a job-completion report. The MP4 is produced by `npx hyperframes render --output <mp4>` from the resolved project directory; the bridge confirms the file exists and is non-empty before reporting success. Full contract below.

## Output and completion checklist

Full output contract (artifact-path inference rules, job-completion report shape, mandatory checklist) lives in [TECH-output-contract](./references/TECH-output-contract.md). Two outputs are mandatory:

1. **Artifacts** — hyperframes project folder + rendered MP4. Path is inferred from the project (user path → framework convention → `./design/<subtype>/` → fallback `./design/videos/`).
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<ts±tz>-amw-video-producer-<slug>-<8-char-hash>.md` listing every artifact + the per-item checklist verdict.

Before reporting complete: every checklist item in TECH-output-contract MUST be PASS or N/A. Any FAIL triggers a remediation loop.

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

Common failure modes and remediation steps live in [TECH-error-handling](./references/TECH-error-handling.md). Covers: missing external repo, Bun / FFmpeg / Chrome provisioning, HTML attribute parse errors, video encoding failures, stale clones.
