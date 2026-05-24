---
name: INDEX
category: hyperframes-bridge
source: skills/amw-hyperframes-bridge/SKILL.md
---

# Reference index — amw-hyperframes-bridge

Every technique in this skill is documented as a single reference file. Each file has its own Table of Contents; load only the file you need.

## Capture pipeline (7 steps — produces an editable Hyperframes project from a live website)

- [TECH-hyperframes-capture-overview](./TECH-hyperframes-capture-overview.md) — pipeline overview, video-type reference, format presets
- [TECH-hyperframes-capture-step-1-capture](./TECH-hyperframes-capture-step-1-capture.md) — Step 1 — Capture & Understand
- [TECH-hyperframes-capture-step-2-design](./TECH-hyperframes-capture-step-2-design.md) — Step 2 — Write DESIGN.md (colors, typography, motion, visual language)
- [TECH-hyperframes-capture-step-3-script](./TECH-hyperframes-capture-step-3-script.md) — Step 3 — Write SCRIPT.md
- [TECH-hyperframes-capture-step-4-storyboard](./TECH-hyperframes-capture-step-4-storyboard.md) — Step 4 — Write STORYBOARD.md
- [TECH-hyperframes-capture-step-5-vo](./TECH-hyperframes-capture-step-5-vo.md) — Step 5 — Generate VO + map timing to beats
- [TECH-hyperframes-capture-step-6-build](./TECH-hyperframes-capture-step-6-build.md) — Step 6 — Build Compositions
- [TECH-hyperframes-capture-step-7-validate](./TECH-hyperframes-capture-step-7-validate.md) — Step 7 — Validate & Deliver

## CLI commands (`npx hyperframes <cmd>`)

- [TECH-hyperframes-cli-doctor](./TECH-hyperframes-cli-doctor.md) — `doctor` + environment utilities
- [TECH-hyperframes-cli-init](./TECH-hyperframes-cli-init.md) — `init` — scaffold a project
- [TECH-hyperframes-cli-lint](./TECH-hyperframes-cli-lint.md) — `lint` — static validation
- [TECH-hyperframes-cli-preview](./TECH-hyperframes-cli-preview.md) — `preview` — live studio preview
- [TECH-hyperframes-cli-render](./TECH-hyperframes-cli-render.md) — `render` — capture composition to MP4 / WebM
- [TECH-hyperframes-cli-transcribe](./TECH-hyperframes-cli-transcribe.md) — `transcribe` — audio → word-level timestamps
- [TECH-hyperframes-cli-tts](./TECH-hyperframes-cli-tts.md) — `tts` — text-to-speech via Kokoro-82M
- [TECH-hyperframes-cli-validate](./TECH-hyperframes-cli-validate.md) — `validate` — WCAG contrast audit
- [TECH-hyperframes-cli-inspect](./TECH-hyperframes-cli-inspect.md) — `inspect` — visual layout audit
- [TECH-hyperframes-cli-browser](./TECH-hyperframes-cli-browser.md) — `browser` — manage Chrome Headless Shell (Puppeteer-based)
- [TECH-hyperframes-cli-snapshot](./TECH-hyperframes-cli-snapshot.md) — `snapshot` — capture key frames as PNG
- [TECH-hyperframes-cli-capture](./TECH-hyperframes-cli-capture.md) — `capture` — capture a website as editable Hyperframes components

## Composition authoring (HTML rules, data attributes, hard gates)

- [TECH-hyperframes-composition-core](./TECH-hyperframes-composition-core.md) — core authoring model + single-file skeleton
- [TECH-hyperframes-data-attributes](./TECH-hyperframes-data-attributes.md) — clip + composition schema; relative timing; sub-composition variable injection
- [TECH-hyperframes-identity-gate](./TECH-hyperframes-identity-gate.md) — Visual Identity Gate (HARD-GATE before writing HTML)
- [TECH-hyperframes-layout-before-animation](./TECH-hyperframes-layout-before-animation.md) — Layout Before Animation
- [TECH-hyperframes-non-negotiables](./TECH-hyperframes-non-negotiables.md) — twelve non-negotiable composition rules
- [TECH-hyperframes-scene-transitions](./TECH-hyperframes-scene-transitions.md) — scene transition rules (entrance/exit policy)
- [TECH-hyperframes-timeline-contract](./TECH-hyperframes-timeline-contract.md) — GSAP integration contract; allowed properties

## Registry (reusable blocks + components)

- [TECH-hyperframes-registry-add](./TECH-hyperframes-registry-add.md) — `add` — install registry blocks + components
- [TECH-hyperframes-registry-blocks](./TECH-hyperframes-registry-blocks.md) — wiring registry blocks into host compositions
- [TECH-hyperframes-registry-components](./TECH-hyperframes-registry-components.md) — wiring registry components into host compositions
- [TECH-hyperframes-visual-styles-library](./TECH-hyperframes-visual-styles-library.md) — `visual-styles.md` — 8 named visual-style presets
