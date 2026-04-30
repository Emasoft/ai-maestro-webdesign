---
name: amw-infographics
description: Dense editorial infographics as HTML + PNG + PDF from a structured data brief — tokenomics, whitepaper summaries, ecosystem maps, roadmaps, airdrop guides, staking breakdowns, stat posters, NFT showcases. Triggers on narrow data-infographic intents like "infographic", "tokenomics graphic", "ecosystem map", "turn these stats into a graphic". NOT for generic design (see design-principles), editorial diagrams (see diagram-editorial), or freeform SVG (see svg-creator). Full template-to-intent selector in the Template selection section.
version: 0.2.0
author: ai-maestro-webdesign
source: Distilled from the public `create-infographics` skill (175-design DNA analysis). The template library, component CSS patterns, and type playbooks are preserved. Compressed into this plugin's house style — scripts are shared through `bin/`, resources stay as on-demand references.
---

# Infographics

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> This skill is an executor. Its triggers are data-infographic-specific only — `design-principles` routes here when the user has real data or a structured brief and wants a shareable, dense editorial graphic.

## Activation

Callable directly via the `/amw-create-or-modify-html-diagram` command with `--style infographic` (user shortcut — fast path for infographic creation). Also invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode when the user needs a dense editorial graphic. In Main-agent mode the orchestrator may apply the full 24-template library, 175-design DNA, and multi-format export techniques from this skill beyond what the command's parameters expose.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT (Phase B).** Emits self-contained HTML + retina PNG + print-ready PDF from a 24-template library and 175-design DNA set. Each file is dense editorial reference material — closer to a crypto research poster or game cheat sheet than a website. Not a substitute for `../amw-diagram-editorial/` (editorial diagrams), `../amw-svg-creator/` (freeform vector), or `../amw-ascii-to-html/` (general webpage rendering).

## What this skill produces

- **HTML** — self-contained, CDN fonts (Bebas Neue, Montserrat, Teko, Orbitron via Google Fonts) + Phosphor Icons + optional Chart.js.
- **PNG** — retina (2x) via `../../bin/amw-html-export.py` (Playwright + Chromium).
- **PDF** — print-ready via the same script.
- **Canvas sizes** (7): portrait-medium 1080×1440 (default), Twitter/X 1200×675, Instagram 1080×1080, Instagram portrait 1080×1350, LinkedIn 1200×627, Pinterest 1000×1500, website 1100×auto. Full table in `resources/platform-sizes.md`.

## Design DNA (the non-negotiable set)

Derived from 175 real designs. The #1 failure mode is producing something that looks like a dark-mode SaaS landing page. Avoid that by holding these rules:

- **Density is the defining trait.** Target 8–15 content blocks on portrait-medium (1080×1440). A "content block" is a table, chart, stat callout, bullet list, flow diagram, or callout box. Under 6 content blocks = too sparse.
- **Backgrounds are near-black.** Default range `#060606`–`#090909`. Lighter `#1a1a1a`–`#1d1d1d` is valid for strategy guides. Light mode is reserved for game-event / quest / bounty guides — never just because the piece is called "whitepaper".
- **Palette is warm + cool together** (75% of pieces). Defaults: amber `#E99A00` warm accent + teal `#00E88A` / blue `#29B7FF` cool complement.
- **Display fonts are all-caps condensed.** Bebas Neue (43% of pieces, default) · Teko (13%) · Orbitron (7%, tech/game) · Press Start 2P (5%, pixel only) · Bungee (3%). Body font: Montserrat. Inter as fallback.
- **Stacked Reference is the default composition.** 70%+ of real pieces stack named sections top-to-bottom. Four other archetypes (Flow Poster, Hub & Spoke, Stat Poster, Cheat Sheet) are secondary.
- **Section variety is mandatory.** 4+ sections must use at least 3 different component types. If 3 sections in a row are card grids, redesign one of them.
- **Arrows are load-bearing.** If content describes a process, economy, or flow — arrows are mandatory, always labeled (action, percentage, token name).
- **Visible borders, not ghost borders.** Minimum `rgba(primary, 0.25)`. `rgba(255,255,255,0.08)` is invisible and looks like a frontend component.
- **Tight spacing inside sections.** Card padding 12–16px (NOT 24–32px). Body font 11–13px for dense content (intentional poster/print-scale exception to design-principles' 16px desktop floor — infographics are shareable graphics, not webpages; see `../amw-design-principles/typography-system.md` for the floor rule this skill carves out from). Gap 8–12px between items. Whitespace separates *sections* from each other, not content within a section.
- **Content format hierarchy.** Tables → bullet lists → flow diagrams → stat callouts → badges. Paragraphs are a last resort, reserved for 1–2 sentence hero intros.

Full design DNA with code samples: `resources/style-details.md` (1062 lines) and `resources/layout-patterns.md` (842 lines).

## Non-negotiable rules

1. **Never fabricate data.** Every stat, figure, or fact must come from the user input. No plausible-sounding invented numbers.
2. **No generic display fonts.** Inter, Roboto, Arial, Helvetica, Plus Jakarta Sans, Syne, Outfit, Space Grotesk, and Rajdhani are banned as the display/heading font (Rajdhani is a rounded-geometric grotesk that reads as exactly the SaaS-display font the banned list filters out). Use Bebas Neue, Teko, Orbitron, Bungee, or Press Start 2P.
3. **No emojis as icons.** Phosphor Icons only: `<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>`.
4. **Brand color first.** If the user supplies a hex or logo, derive the palette from it — do not default to generic tech blue/purple.
5. **Dark mode is the default.** Near-black `#060606`–`#090909`. Words like "whitepaper", "report", or "institutional" do NOT override dark mode.
6. **User-supplied real assets only.** No AI-generated images, no invented testimonials, no stock placeholders. If the user references a game / NFT project, expect to incorporate their imagery.
7. **Footer by default.** 60% of real pieces have a small attribution/logo strip at the bottom. Omit only when the user explicitly says no footer.

## 24-template index (`templates/`)

Each template is a fully-built reference piece using the V4 CSS standards (12px dense tables, `▸` bullet panels, arrow connectors, stat strips with 2px top-border accents, Bebas Neue + Montserrat font pairing). Substitute real content for `{{PLACEHOLDER}}` variables.

### Crypto / Web3

| Template | File | Best for |
|---|---|---|
| Token Economics | `token-economics.html` | Allocation pie, vesting schedule, supply breakdown |
| Crypto Explainer | `crypto-explainer.html` | Protocol explainers, how-it-works for DeFi/Web3 concepts |
| Game Overview | `game-overview.html` | GameFi launch posters, character rosters, tokenomics |
| Ecosystem Map | `ecosystem.html` | Partner directories, protocol integrations, chain ecosystems |
| Airdrop Guide | `airdrop-guide.html` | Eligibility criteria, tier tables, claim steps, vesting |
| Token Flywheel | `token-flywheel.html` | Value accrual loops, fee → buyback → burn cycles |
| Staking & Yield | `staking-yield.html` | APY breakdown, staking tiers, yield source flow |
| DeFi Protocol | `defi-protocol.html` | Protocol mechanics, fee structures, risk matrices |
| Roadmap | `roadmap.html` | Phase cards, milestone tables, delivery timelines |
| Stats Poster | `stats-poster.html` | Dominant single-stat hero, period-over-period tables |
| Whitepaper Overview | `whitepaper-overview.html` | Technical summaries, problem/solution, competitor comparisons |
| Game Event | `game-event.html` | Tournament schedules, prize tiers, participation guides |
| Game Cheat Sheet | `game-cheat-sheet.html` | Quick-ref class/resource tables, combat/economy tips |

### Generic

| Template | File | Best for |
|---|---|---|
| NFT Showcase | `nft-showcase.html` | Rarity tiers, trait distribution, collection stats |
| How It Works | `how-it-works.html` | Step-flow explainers, mechanics breakdowns |
| Comparison | `comparison.html` | A vs B head-to-head with winner highlights |
| Listicle | `listicle.html` | Ranked lists, top-N formats, scoring criteria |
| Feature Roster | `feature-roster.html` | Product feature cards, feature matrix, pricing tiers |
| Modern Timeline | `modern-timeline.html` | History/roadmap with done/active/planned track |
| Dark Modern | `dark-modern.html` | General-purpose dark overview with data panels |
| Data Story | `data-story.html` | KPI-dominant with horizontal bar charts, period tables |
| Event Schedule | `event-schedule.html` | Conference/event day columns, speaker grid, session table |
| Branded Minimal | `branded-minimal.html` | Brand-forward with pullquote, gradient accent bar |
| Light Editorial | `light-editorial.html` | Light-mode reports, editorial research, press-ready output |

### Template selection

| User says… | Template |
|---|---|
| "tokenomics", "vesting", "allocation" | `token-economics.html` |
| "how does X protocol work", "explainer" | `crypto-explainer.html` or `how-it-works.html` |
| "game overview", "NFT game" | `game-overview.html` |
| "ecosystem", "partner map", "integrations" | `ecosystem.html` |
| "airdrop", "claim guide", "eligibility" | `airdrop-guide.html` |
| "flywheel", "value loop" | `token-flywheel.html` |
| "staking", "yield", "APR" | `staking-yield.html` |
| "DeFi", "AMM", "liquidity" | `defi-protocol.html` |
| "roadmap", "Q1/Q2" | `roadmap.html` or `modern-timeline.html` |
| "stats poster", "metrics" | `stats-poster.html` or `data-story.html` |
| "whitepaper", "technical overview" | `whitepaper-overview.html` |
| "tournament", "game event" | `game-event.html` |
| "cheat sheet", "quick reference" | `game-cheat-sheet.html` |
| "NFT collection", "rarity" | `nft-showcase.html` |
| "compare X vs Y" | `comparison.html` |
| "top 10", "best", "ranked" | `listicle.html` |
| "product features", "pricing" | `feature-roster.html` |
| "event", "conference", "schedule" | `event-schedule.html` |
| "brand one-pager" | `branded-minimal.html` |
| "light mode report", "editorial" | `light-editorial.html` |

## Execution modes

### A. Interactive Builder — preview each component live

Use when the user says "show me each", "piece by piece", "step by step", "let me iterate", or asks for a single component.

1. **Start preview server** (once per session):
   ```bash
   python3 ../../bin/amw-preview-server.py --file .infographic/.preview.html --port 7883 &
   ```
   Tell the user once: *"Preview running at http://localhost:7883 — it auto-refreshes on every render."*
2. **Plan components** — state the archetype, density target, and component list. Get an explicit go-ahead.
3. **Render one component at a time** to `.infographic/.preview.html` as a full self-contained HTML document. Ask for approval before locking it in.
4. **Approval gate** — only write approved components to the state file `{cwd}/.infographic/{project}.json`. Verbatim HTML, no re-generation.
5. **Assemble** on user command (`assemble`, `finalize`, `done`) — stitch approved components, wrap with header/footer, run Reduction Pass, export via `html-export.py`.

Full builder protocol (state file schema, approval vocabulary, assembly rules): `resources/layout-patterns.md` and the `create-infographics` upstream SKILL.md.

### B. One-Shot — generate the full infographic in one pass

Use when the user provides a complete data brief or says "create an infographic about X", "generate", "build this".

1. **Design Brief (3 questions)** — brand (color/logo), platform (default portrait-medium 1080×1440), key insight. Skip any already answered.
2. **Classify + Archetype + Layout Intent** — state in one sentence: content type (playbook or generic), composition archetype (Stacked Reference default), dominant component, density target. Example: *"Token-Economics playbook, Stacked Reference, dominated by allocation pie + vesting timeline, targeting 10 content blocks on portrait-medium."*
3. **Build** — single self-contained HTML, required `<head>` includes Google Fonts + Phosphor Icons + optional Chart.js. Apply playbook colors/fonts. All CSS inline, CSS custom properties at `:root`, no lorem ipsum.
4. **Anti-Frontend Checklist + Reduction Pass** — see Quality Gate below.
5. **Export** — `python3 ../../bin/amw-html-export.py -i {file}.html -o {name} -f all --width {W} --scale 2`.

### C. Guided Creative — two composition options before building

Use when the user says "help me figure out the design", "give me options", "show me two approaches", or is uncertain about style.

1. **Design Brief** — as in Mode B.
2. **Classify + Layout Intent** — understand the content and key insight.
3. **Present two composition options** — no code yet. Each option gets a short name, its archetype (two *different* archetypes from the five), a one-sentence description, and why it fits this data.
4. **User picks a direction.**
5. **One-shot build** using the chosen archetype. Follow Mode B Steps 2–5.

## Quality gate (before delivery)

Run both passes:

**Anti-Frontend Checklist** (must all be ✓):
- [ ] No uniform card grids — at least 3 different component types used.
- [ ] No paragraph descriptions — body text is bullet points.
- [ ] Card padding 12–16px, body font 11–13px, gap 8–12px.
- [ ] Borders visible — minimum `rgba(primary, 0.25)`.
- [ ] Arrows/connectors present if content describes a process/flow.
- [ ] At least one table if data has comparisons/specs/rates.
- [ ] Content block count meets density target.

**Reduction Pass** — remove gridlines that aren't needed for reading values, axis tick marks where direct labels exist, decorative icons, borders/glows on elements already separated by whitespace, text that repeats what the visual shows. Strictness scales to aesthetic (see `resources/style-details.md` reduction table). Do NOT reduce information density.

**Final quality check** — no fabricated data, display font is not banned, Phosphor CDN included, canvas width matches platform, background mode matches request, footer present (unless user said no), all labels directly on charts (annotation-first), logo present (95% of real pieces), type-specific playbook applied if one fits.

## Dependencies

- **runtime_binaries (system):** `python3 ≥ 3.8`.
- **runtime_binaries (installed via `/amw-init`):** Playwright + Chromium (`python3 -m playwright install chromium --with-deps`), optional Inkscape or pdf2svg for SVG export.
- **python_packages:** `playwright ≥ 1.40.0`.
- **npm_packages:** none required.
- **mcp_servers:** none.
- **CDN assets (run-time):** Google Fonts (Bebas Neue, Teko, Orbitron, Montserrat), Phosphor Icons, optional Chart.js. Offline environments need the CDN resolvable — `html-export.py` spins up a local HTTP server so Playwright resolves them cleanly.
- **Shared scripts:** `../../bin/amw-html-export.py` (PNG / PDF / SVG export), `../../bin/amw-preview-server.py` (Mode A live preview).

## Cross-references

- `../amw-design-principles/SKILL.md` — upstream orchestrator; route here only when the user has structured data and wants a dense editorial graphic.
- `../amw-design-principles/ai-slop-avoid.md` — final AI-slop scan every HTML output must pass.
- `../amw-design-principles/color-system.md` — brand-color / WCAG AA validation when a custom color is supplied.
- `../amw-design-principles/typography-system.md` — type-scale rules that compose with this skill's display-font hierarchy.
- `../../bin/amw-html-export.py` — PNG / PDF / SVG export pipeline; shared with `hyperframes-bridge` and `ascii-to-html`.
- `../../bin/amw-preview-server.py` — Mode A live preview server, port 7883.
- `resources/design-brief.md` — 5-question intake framework + aesthetic decision table.
- `resources/style-details.md` — full 1062-line design system with component CSS patterns, type playbooks, reduction-pass rules.
- `resources/layout-patterns.md` — full 842-line layout and archetype scaffold library with CSS grid implementations per archetype.
- `resources/charts.md` — chart rules (bar / line / pie / radar / stat callouts) with annotation-first placement.
- `resources/color-palettes.md` — full palette library by type (token-economics amber, crypto-explainer purple, ecosystem teal, airdrop amber+blue, etc.).
- `resources/font-pairings.md` — display-font prevalence table and body-font pairings per type.
- `resources/platform-sizes.md` — 7 canvas sizes with per-platform layout/font adjustments and safe zones.
- `resources/copy-guide.md` — headline, callout, and label writing rules.
- `templates/` — 24 reference templates (see index above).
- `examples/` — 15 rendered PNG reference outputs for each template family.
- `evals/evals.json` — 5 scenario test prompts + expected outcomes.

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Output looks like a SaaS landing page | Uniform card grids, generous whitespace, paragraph descriptions, no tables/arrows | Replace card grids with `bullet_panel` + `dense_table`. Add directional arrow connectors between sections. |
| Output looks like a dashboard | Data-sparse, too much empty space, body font 14–16px | Tighten to 11–13px body, 12–16px padding. Add content blocks until 8+ on portrait-medium. |
| Output looks like a slide deck | Each section is one idea surrounded by whitespace | Merge sparse sections, increase density, use mixed layouts per section. |
| "Component demo" repetition | Same component type repeated 3+ times in a row | Apply Section Variety Rule — at least 3 different component types across 4+ sections. |
| Floating-islands sections | No arrows/connectors showing how sections relate | Add labeled arrows between related sections. Use consistent color coding to signal linked concepts. |
| Playwright missing at export | `/amw-init` not run or `playwright install chromium` skipped | Install: `python3 -m pip install --user --break-system-packages playwright && python3 -m playwright install chromium --with-deps`. |
| CDN fonts fall back to Times/Arial | Offline environment, or Google Fonts blocked | `html-export.py` defaults to spinning up a local HTTP server; confirm the host can reach `fonts.googleapis.com`. Fallback: use system-font stack and accept degraded editorial feel. |
| Fabricated stats in output | Skill guessed numbers not in the brief | Reject; regenerate using only the user's supplied data. Every non-user number is a Rule 1 violation. |
| Wrong template chosen | User intent mapped to a generic template when a playbook fits | Re-read the Template Selection table; if the content type is one of the 5 playbooks (token-economics, crypto-explainer, game-overview, ecosystem, airdrop-guide), override and use the playbook template. |
| Output is light mode when user wanted dark | Wording like "whitepaper" or "report" was misread as a light-mode signal | Dark is the default. Light mode requires an explicit user request ("light background", "white background", "print-ready report"). |

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `infographics` is the user asking about?
  - **section** (3 techniques)
    - [TECH-section-band](./references/TECH-section-band.md) — Full-width section separator bands
    - [TECH-section-header-pill](./references/TECH-section-header-pill.md) — Section header pill badge (ecosystem signature)
    - [TECH-section-variety-rule](./references/TECH-section-variety-rule.md) — Section Variety Rule — MANDATORY across 4+ sections
  - **copy** (2 techniques)
    - [TECH-copy-guide-bullets](./references/TECH-copy-guide-bullets.md) — Bullet points rule — over paragraphs, always
    - [TECH-copy-guide-numbers](./references/TECH-copy-guide-numbers.md) — Number formatting rules
  - **dense** (2 techniques)
    - [TECH-dense-editorial-dna](./references/TECH-dense-editorial-dna.md) — Dense editorial DNA — the defining aesthetic
    - [TECH-dense-table-component](./references/TECH-dense-table-component.md) — `dense_table` — the designer's primary data format
  - **flow** (2 techniques)
    - [TECH-flow-poster-archetype](./references/TECH-flow-poster-archetype.md) — Archetype 2: Flow Poster
    - [TECH-flow-with-arrows-component](./references/TECH-flow-with-arrows-component.md) — `flow_with_arrows` — horizontal flow nodes with arrow connectors
  - **preview** (2 techniques)
    - [TECH-preview-animations](./references/TECH-preview-animations.md) — Preview entrance animations — browser only
    - [TECH-preview-server](./references/TECH-preview-server.md) — Preview server — live reload during builder sessions
  - **stat** (2 techniques)
    - [TECH-stat-poster-archetype](./references/TECH-stat-poster-archetype.md) — Archetype 4: Stat Poster
    - [TECH-stat-strip-component](./references/TECH-stat-strip-component.md) — `stat_strip` — full-width KPI row with colored top borders
  - **airdrop** (1 techniques)
    - [TECH-airdrop-guide-playbook](./references/TECH-airdrop-guide-playbook.md) — Airdrop-Guide playbook — 10% (17/175)
  - **annotated** (1 techniques)
    - [TECH-annotated-bar-chart](./references/TECH-annotated-bar-chart.md) — Annotated bar chart — SVG with callout + benchmark
  - **annotation** (1 techniques)
    - [TECH-annotation-first](./references/TECH-annotation-first.md) — Annotation-first — labels on charts, not in legends
  - **anti** (1 techniques)
    - [TECH-anti-frontend-checklist](./references/TECH-anti-frontend-checklist.md) — Anti-Frontend Checklist — pre-delivery gate
  - **arrows** (1 techniques)
    - [TECH-arrows-and-connectors](./references/TECH-arrows-and-connectors.md) — Arrows & connectors — 71% of pieces
  - **background** (1 techniques)
    - [TECH-background-depth](./references/TECH-background-depth.md) — Background depth — radial gradient orbs, scanlines, paper texture
  - **bar** (1 techniques)
    - [TECH-bar-chart-css](./references/TECH-bar-chart-css.md) — CSS horizontal bar chart — vesting / allocation strips
  - **bordered** (1 techniques)
    - [TECH-bordered-section-component](./references/TECH-bordered-section-component.md) — `bordered_section` — visible-border content panel
  - **bullet** (1 techniques)
    - [TECH-bullet-panel-component](./references/TECH-bullet-panel-component.md) — `bullet_panel` component — DEFAULT for text content
  - **chain** (1 techniques)
    - [TECH-chain-color-coding](./references/TECH-chain-color-coding.md) — Blockchain chain color-coding
  - **character** (1 techniques)
    - [TECH-character-card-grid](./references/TECH-character-card-grid.md) — Character / NFT card grid — tight 5-column
  - **chart** (1 techniques)
    - [TECH-chart-selection-guide](./references/TECH-chart-selection-guide.md) — Chart selection — decision tree for chart type
  - **cheat** (1 techniques)
    - [TECH-cheat-sheet-archetype](./references/TECH-cheat-sheet-archetype.md) — Archetype 5: Cheat Sheet
  - **color** (1 techniques)
    - [TECH-color-palette-recipes](./references/TECH-color-palette-recipes.md) — 13 named palette recipes
  - **crypto** (1 techniques)
    - [TECH-crypto-explainer-playbook](./references/TECH-crypto-explainer-playbook.md) — Crypto-Explainer playbook — 17% (29/175)
  - **design** (1 techniques)
    - [TECH-design-brief](./references/TECH-design-brief.md) — Design Brief — 3 (or 5) intake questions
  - **dot** (1 techniques)
    - [TECH-dot-plot](./references/TECH-dot-plot.md) — Dot plot — distribution + individual points
  - **ecosystem** (1 techniques)
    - [TECH-ecosystem-playbook](./references/TECH-ecosystem-playbook.md) — Ecosystem playbook — 13% (22/175)
  - **export** (1 techniques)
    - [TECH-export-pipeline](./references/TECH-export-pipeline.md) — Export pipeline — HTML → PNG + PDF + SVG
  - **flywheel** (1 techniques)
    - [TECH-flywheel-loop-component](./references/TECH-flywheel-loop-component.md) — `flywheel_loop` — rectangular nodes → circular back to start
  - **font** (1 techniques)
    - [TECH-font-system](./references/TECH-font-system.md) — Font system — the 5-font display hierarchy
  - **game** (1 techniques)
    - [TECH-game-overview-playbook](./references/TECH-game-overview-playbook.md) — Game-Overview playbook — 14% (25/175)
  - **glow** (1 techniques)
    - [TECH-glow-system](./references/TECH-glow-system.md) — Glow system — neon box-shadow + text-shadow
  - **guided** (1 techniques)
    - [TECH-guided-creative-mode](./references/TECH-guided-creative-mode.md) — Guided Creative (Mode C) — show two directions before building
  - **hub** (1 techniques)
    - [TECH-hub-spoke-archetype](./references/TECH-hub-spoke-archetype.md) — Archetype 3: Hub & Spoke
  - **inline** (1 techniques)
    - [TECH-inline-token-coloring](./references/TECH-inline-token-coloring.md) — Inline token coloring — `$TOKEN` names always colored
  - **interactive** (1 techniques)
    - [TECH-interactive-builder-mode](./references/TECH-interactive-builder-mode.md) — Interactive Builder (Mode A) — component-by-component iteration
  - **line** (1 techniques)
    - [TECH-line-chart](./references/TECH-line-chart.md) — Line chart — Chart.js with designer theming
  - **one** (1 techniques)
    - [TECH-one-shot-mode](./references/TECH-one-shot-mode.md) — One-Shot mode (Mode B) — generate the full infographic in one pass
  - **outer** (1 techniques)
    - [TECH-outer-canvas-border](./references/TECH-outer-canvas-border.md) — Outer canvas border — thin accent-colored frame
  - **per** (1 techniques)
    - [TECH-per-type-signature-palettes](./references/TECH-per-type-signature-palettes.md) — Per-content-type signature palettes
  - **platform** (1 techniques)
    - [TECH-platform-sizing](./references/TECH-platform-sizing.md) — Platform sizing — Twitter, Instagram, LinkedIn, Pinterest
  - **progress** (1 techniques)
    - [TECH-progress-bar-vesting](./references/TECH-progress-bar-vesting.md) — Progress bar — vesting timeline with milestones
  - **proportional** (1 techniques)
    - [TECH-proportional-circles](./references/TECH-proportional-circles.md) — Proportional circles — area = value
  - **radar** (1 techniques)
    - [TECH-radar-chart](./references/TECH-radar-chart.md) — Radar chart — Chart.js for game stats + multi-axis comparison
  - **reduction** (1 techniques)
    - [TECH-reduction-pass](./references/TECH-reduction-pass.md) — Reduction Pass — strip everything that doesn't encode data
  - **signature** (1 techniques)
    - [TECH-signature-palette](./references/TECH-signature-palette.md) — Signature palette — near-black + amber + teal/blue complement
  - **slope** (1 techniques)
    - [TECH-slope-chart](./references/TECH-slope-chart.md) — Slope chart — before/after comparison
  - **stacked** (1 techniques)
    - [TECH-stacked-reference-archetype](./references/TECH-stacked-reference-archetype.md) — Archetype 1: Stacked Reference (DEFAULT, 70%+ of work)
  - **step** (1 techniques)
    - [TECH-step-process-component](./references/TECH-step-process-component.md) — `step_process` — numbered steps with connector line
  - **svg** (1 techniques)
    - [TECH-svg-pie-chart](./references/TECH-svg-pie-chart.md) — SVG pie chart — token allocation (the #1 chart)
  - **swim** (1 techniques)
    - [TECH-swim-lane-architecture](./references/TECH-swim-lane-architecture.md) — Swim-lane architecture diagram
  - **template** (1 techniques)
    - [TECH-template-registry](./references/TECH-template-registry.md) — Template registry — 24 reference templates
  - **tier** (1 techniques)
    - [TECH-tier-comparison-component](./references/TECH-tier-comparison-component.md) — `tier_comparison` — tier badge table
  - **token** (1 techniques)
    - [TECH-token-economics-playbook](./references/TECH-token-economics-playbook.md) — Token-Economics playbook — 35% of body of work (62/175)
  - **typography** (1 techniques)
    - [TECH-typography-scale](./references/TECH-typography-scale.md) — Typography scale — minor third (1.25 ratio)
  - **waffle** (1 techniques)
    - [TECH-waffle-chart](./references/TECH-waffle-chart.md) — Waffle chart — 10×10 grid for % of total

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-airdrop-guide-playbook.md](./references/TECH-airdrop-guide-playbook.md)**
  - Description: Airdrop-Guide playbook — 10% (17/175)
  - TOC:
    - What it does
    - When to use
    - Color system
    - Typography
    - Standard component prevalence (across 17 pieces)
    - Visual properties
    - Signature layout pattern
    - The amber+blue value split (signature)
    - The claim-steps horizontal flow
    - CSS variables
    - Reference template
    - Archetype preference
    - Gotchas
    - Cross-references
- **[./references/TECH-annotated-bar-chart.md](./references/TECH-annotated-bar-chart.md)**
  - Description: Annotated bar chart — SVG with callout + benchmark
  - TOC:
    - What it does
    - When to use
    - HTML (excerpt — see source for full)
    - CSS
    - The hero bar signature
    - Gotchas
    - Cross-references
- **[./references/TECH-annotation-first.md](./references/TECH-annotation-first.md)**
  - Description: Annotation-first — labels on charts, not in legends
  - TOC:
    - What it does
    - The per-chart-type rule
    - Legend exception
    - Callout line technique — highlight outliers
    - Insight callout box (for major insights)
    - Threshold / benchmark line
    - The rule
    - Gotchas
    - Cross-references
- **[./references/TECH-anti-frontend-checklist.md](./references/TECH-anti-frontend-checklist.md)**
  - Description: Anti-Frontend Checklist — pre-delivery gate
  - TOC:
    - What it does
    - The checklist
    - Common failure modes
    - After checklist → run Reduction Pass
    - Gotchas
    - Cross-references
- **[./references/TECH-arrows-and-connectors.md](./references/TECH-arrows-and-connectors.md)**
  - Description: Arrows & connectors — 71% of pieces
  - TOC:
    - What it does
    - When arrows are MANDATORY
    - Rule
    - Horizontal arrow connector
    - Vertical connector line between sections
    - Flow diagram row
    - Phosphor Icons CDN
    - Labels on arrows (for flow diagrams)
    - Gotchas
    - Cross-references
- **[./references/TECH-background-depth.md](./references/TECH-background-depth.md)**
  - Description: Background depth — radial gradient orbs, scanlines, paper texture
  - TOC:
    - What it does
    - Gradient mesh background
    - SVG noise grain
    - Scanline overlay (Cyber aesthetic)
    - Paper texture (Editorial aesthetic)
    - Glassmorphism accent panels
    - Background decoration hierarchy
    - Gotchas
    - Cross-references
- **[./references/TECH-bar-chart-css.md](./references/TECH-bar-chart-css.md)**
  - Description: CSS horizontal bar chart — vesting / allocation strips
  - TOC:
    - What it does
    - HTML
    - CSS
    - The 3-column grid layout
    - Animation — CSS transition
    - Progress bars — single metric variant
    - Gotchas
    - Cross-references
- **[./references/TECH-bordered-section-component.md](./references/TECH-bordered-section-component.md)**
  - Description: `bordered_section` — visible-border content panel
  - TOC:
    - What it does
    - When to use
    - Left-accent variant (most common)
    - Full-border variant
    - Header styles
    - HTML
    - Minimum border opacity
    - Gotchas
    - Cross-references
- **[./references/TECH-bullet-panel-component.md](./references/TECH-bullet-panel-component.md)**
  - Description: `bullet_panel` component — DEFAULT for text content
  - TOC:
    - What it does
    - When to use
    - CSS
    - HTML
    - The ▸ bullet convention
    - 2-col grid pattern
    - One fact per bullet (mandatory)
    - Gotchas
    - Cross-references
- **[./references/TECH-chain-color-coding.md](./references/TECH-chain-color-coding.md)**
  - Description: Blockchain chain color-coding
  - TOC:
    - What it does
    - The color table
    - CSS tokens
    - Chain badge component
    - Table row left-border per chain
    - When to use
    - Gotchas
    - Cross-references
- **[./references/TECH-character-card-grid.md](./references/TECH-character-card-grid.md)**
  - Description: Character / NFT card grid — tight 5-column
  - TOC:
    - What it does
    - CSS
    - HTML
    - The tight-grid signature
    - Stat bar sizing
    - When to use
    - Gotchas
    - Cross-references
- **[./references/TECH-chart-selection-guide.md](./references/TECH-chart-selection-guide.md)**
  - Description: Chart selection — decision tree for chart type
  - TOC:
    - What it does
    - The decision table
    - The rule
    - Chart.js when yes
    - Chart.js loading
    - The canvas size trick
    - Gotchas
    - Cross-references
- **[./references/TECH-cheat-sheet-archetype.md](./references/TECH-cheat-sheet-archetype.md)**
  - Description: Archetype 5: Cheat Sheet
  - TOC:
    - What it does
    - When to use
    - The shape
    - CSS implementation
    - The mixed-layout rule
    - Flow connector between sections
    - Gotchas
    - Cross-references
- **[./references/TECH-color-palette-recipes.md](./references/TECH-color-palette-recipes.md)**
  - Description: 13 named palette recipes
  - TOC:
    - What it does
    - Dark palettes (99% of work)
    - Standout palettes
    - Light mode palettes (rare, <1%)
    - Gotchas
    - Cross-references
- **[./references/TECH-copy-guide-bullets.md](./references/TECH-copy-guide-bullets.md)**
  - Description: Bullet points rule — over paragraphs, always
  - TOC:
    - What it does
    - Why
    - Rule 1 — Bullets, not paragraphs
    - Rule 2 — One fact per bullet
    - Rule 3 — Sentence fragments, not full sentences
    - Rule 4 — Inline token coloring
    - Rule 5 — Color-coded keyword highlighting (beyond tokens)
    - Badge / tag rules
    - Disclaimer (always include in footer)
    - Gotchas
    - Cross-references
- **[./references/TECH-copy-guide-numbers.md](./references/TECH-copy-guide-numbers.md)**
  - Description: Number formatting rules
  - TOC:
    - What it does
    - The number format table
    - Labeling rules
    - Currency
    - Headline formulas (ALL CAPS + verb-first OR noun phrase)
    - Subtitle rules
    - Per-component word budgets
    - Common mistakes to avoid
    - Gotchas
    - Cross-references
- **[./references/TECH-crypto-explainer-playbook.md](./references/TECH-crypto-explainer-playbook.md)**
  - Description: Crypto-Explainer playbook — 17% (29/175)
  - TOC:
    - What it does
    - When to use
    - Color system
    - Typography
    - Standard component prevalence (across 29 pieces)
    - Visual properties
    - Signature layout pattern
    - CSS variables (purple variant)
    - CSS variables (pink variant)
    - Font pair
    - Reference template
    - Archetype preference
    - Gotchas
    - Cross-references
- **[./references/TECH-dense-editorial-dna.md](./references/TECH-dense-editorial-dna.md)**
  - Description: Dense editorial DNA — the defining aesthetic
  - TOC:
    - What it does
    - The success state
    - The failure mode
    - The Anti-Frontend Checklist (run before delivery)
    - Density targets by canvas
    - Spacing rules (THE signature)
    - Content format hierarchy (top = prefer)
    - Gotchas
    - Cross-references
- **[./references/TECH-dense-table-component.md](./references/TECH-dense-table-component.md)**
  - Description: `dense_table` — the designer's primary data format
  - TOC:
    - What it does
    - When to use
    - CSS
    - The signature rules
    - HTML
    - Usage rules
    - Gotchas
    - Cross-references
- **[./references/TECH-design-brief.md](./references/TECH-design-brief.md)**
  - Description: Design Brief — 3 (or 5) intake questions
  - TOC:
    - What it does
    - The 3 minimum questions
    - The 5 full-brief questions
    - Aesthetic direction mapping (Question 2)
    - Rules
    - Skip-brief defaults
    - Thesis extraction (from data)
    - Tone → palette mapping
    - Audience sophistication → density
    - Gotchas
    - Cross-references
- **[./references/TECH-dot-plot.md](./references/TECH-dot-plot.md)**
  - Description: Dot plot — distribution + individual points
  - TOC:
    - What it does
    - When to use
    - HTML
    - CSS
    - Y-jitter convention
    - Annotations — median line, ranges
    - Gotchas
    - Cross-references
- **[./references/TECH-ecosystem-playbook.md](./references/TECH-ecosystem-playbook.md)**
  - Description: Ecosystem playbook — 13% (22/175)
  - TOC:
    - What it does
    - When to use
    - Color system
    - Typography
    - Standard component prevalence (across 22 pieces)
    - Visual properties
    - Signature layout pattern
    - The partner grid pattern (signature)
    - Section header pill badge
    - CSS variables
    - Reference template
    - Target density
    - Gotchas
    - Cross-references
- **[./references/TECH-export-pipeline.md](./references/TECH-export-pipeline.md)**
  - Description: Export pipeline — HTML → PNG + PDF + SVG
  - TOC:
    - What it does
    - When to use
    - Install
    - Basic invocation
    - With local server (recommended)
    - Width and scale
    - Per-platform widths
    - Wait-for-render helper
    - SVG export
    - Gotchas
    - Cross-references
- **[./references/TECH-flow-poster-archetype.md](./references/TECH-flow-poster-archetype.md)**
  - Description: Archetype 2: Flow Poster
  - TOC:
    - What it does
    - When to use
    - The shape
    - CSS implementation
    - Label rule
    - Gotchas
    - Cross-references
- **[./references/TECH-flow-with-arrows-component.md](./references/TECH-flow-with-arrows-component.md)**
  - Description: `flow_with_arrows` — horizontal flow nodes with arrow connectors
  - TOC:
    - What it does
    - When to use
    - Horizontal flow — CSS
    - Vertical connector — CSS
    - HTML
    - Arrow icons — Phosphor only
    - Label rule — mandatory
    - Gotchas
    - Cross-references
- **[./references/TECH-flywheel-loop-component.md](./references/TECH-flywheel-loop-component.md)**
  - Description: `flywheel_loop` — rectangular nodes → circular back to start
  - TOC:
    - What it does
    - When to use
    - CSS
    - HTML
    - Arrow labels (mandatory)
    - When to use a horizontal flow instead
    - Gotchas
    - Cross-references
- **[./references/TECH-font-system.md](./references/TECH-font-system.md)**
  - Description: Font system — the 5-font display hierarchy
  - TOC:
    - What it does
    - The 5 display fonts (authoritative hierarchy)
    - Banned display fonts
    - The body font hierarchy
    - Rules (non-negotiable)
    - Tested font pairings (top 5)
    - Typography constants
    - Gotchas
    - Cross-references
- **[./references/TECH-game-overview-playbook.md](./references/TECH-game-overview-playbook.md)**
  - Description: Game-Overview playbook — 14% (25/175)
  - TOC:
    - What it does
    - When to use
    - Color system
    - Typography — two sub-variants
    - Standard component prevalence (across 25 pieces)
    - Visual properties
    - Signature layout pattern
    - Character card grid (signature pattern)
    - Light-mode sub-variant
    - CSS variables (standard)
    - CSS variables (pixel)
    - Reference template
    - Gotchas
    - Cross-references
- **[./references/TECH-glow-system.md](./references/TECH-glow-system.md)**
  - Description: Glow system — neon box-shadow + text-shadow
  - TOC:
    - What it does
    - The glow system
    - Double-layer glow pattern
    - Top confirmed glow colors
    - When to use each
    - Light-mode override
    - Gotchas
    - Cross-references
- **[./references/TECH-guided-creative-mode.md](./references/TECH-guided-creative-mode.md)**
  - Description: Guided Creative (Mode C) — show two directions before building
  - TOC:
    - What it does
    - When to use
    - The flow
    - The two-option presentation
    - Example presentation
    - User selection handling
    - Step 5 — one-shot build
    - Step 6 — Live Editor Block
    - Gotchas
    - Cross-references
- **[./references/TECH-hub-spoke-archetype.md](./references/TECH-hub-spoke-archetype.md)**
  - Description: Archetype 3: Hub & Spoke
  - TOC:
    - What it does
    - When to use
    - The shape
    - CSS implementation
    - Connection lines — SVG overlay
    - Gotchas
    - Cross-references
- **[./references/TECH-inline-token-coloring.md](./references/TECH-inline-token-coloring.md)**
  - Description: Inline token coloring — `$TOKEN` names always colored
  - TOC:
    - What it does
    - The two patterns
    - HTML
    - What gets colored
    - The 2-per-bullet cap
    - The `highlight` class vs `.accent`
    - The token-pill variant (standalone)
    - Gotchas
    - Cross-references
- **[./references/TECH-interactive-builder-mode.md](./references/TECH-interactive-builder-mode.md)**
  - Description: Interactive Builder (Mode A) — component-by-component iteration
  - TOC:
    - What it does
    - When to use
    - The flow
    - State file — `.infographic/{project}.json`
    - Preview server
    - The approval gate (A4)
    - State schema per component
    - Why verbatim HTML
    - Session resume
    - Gotchas
    - Cross-references
- **[./references/TECH-line-chart.md](./references/TECH-line-chart.md)**
  - Description: Line chart — Chart.js with designer theming
  - TOC:
    - What it does
    - When to use
    - HTML
    - The signature options
    - The container-height trick
    - Gotchas
    - Cross-references
- **[./references/TECH-one-shot-mode.md](./references/TECH-one-shot-mode.md)**
  - Description: One-Shot mode (Mode B) — generate the full infographic in one pass
  - TOC:
    - What it does
    - When to use
    - The 5 steps
    - Classification — identify the type
    - Composition archetype — pick one
    - Build rules
    - Head elements (required)
    - Step 5 — export command
    - Gotchas
    - Cross-references
- **[./references/TECH-outer-canvas-border.md](./references/TECH-outer-canvas-border.md)**
  - Description: Outer canvas border — thin accent-colored frame
  - TOC:
    - What it does
    - Implementation 1 — body outline
    - Implementation 2 — wrapping container border
    - Implementation 3 — pseudo-element overlay
    - When to use
    - When NOT to use
    - Color choice
    - Gotchas
    - Cross-references
- **[./references/TECH-per-type-signature-palettes.md](./references/TECH-per-type-signature-palettes.md)**
  - Description: Per-content-type signature palettes
  - TOC:
    - What it does
    - The 5 major-type palettes
    - Why these
    - The full selection order
    - CSS variables per type
    - Gotchas
    - Cross-references
- **[./references/TECH-platform-sizing.md](./references/TECH-platform-sizing.md)**
  - Description: Platform sizing — Twitter, Instagram, LinkedIn, Pinterest
  - TOC:
    - What it does
    - The size table
    - Safe zones per platform
    - CSS — fixed-aspect platforms
    - Font size scaling by platform
    - Density by format
    - Watermark / attribution per platform
    - Export commands
    - Gotchas
    - Cross-references
- **[./references/TECH-preview-animations.md](./references/TECH-preview-animations.md)**
  - Description: Preview entrance animations — browser only
  - TOC:
    - What it does
    - When to use
    - Per-component animation table
    - Stat counter — JS
    - Bar chart — CSS transition
    - Feature card stagger — CSS
    - SVG line draw
    - The export capture
    - Gotchas
    - Cross-references
- **[./references/TECH-preview-server.md](./references/TECH-preview-server.md)**
  - Description: Preview server — live reload during builder sessions
  - TOC:
    - What it does
    - When to use
    - Start the server
    - User instruction
    - How auto-refresh works
    - Workflow during iteration
    - Preview file structure
    - Full design fidelity in preview
    - Gotchas
    - Cross-references
- **[./references/TECH-progress-bar-vesting.md](./references/TECH-progress-bar-vesting.md)**
  - Description: Progress bar — vesting timeline with milestones
  - TOC:
    - What it does
    - When to use
    - HTML
    - CSS
    - The milestone marker trick
    - Labels row — above and below
    - Gradient fill
    - Gotchas
    - Cross-references
- **[./references/TECH-proportional-circles.md](./references/TECH-proportional-circles.md)**
  - Description: Proportional circles — area = value
  - TOC:
    - What it does
    - When to use
    - The math
    - HTML
    - CSS — primary shade coloring
    - Positioning
    - Gotchas
    - Cross-references
- **[./references/TECH-radar-chart.md](./references/TECH-radar-chart.md)**
  - Description: Radar chart — Chart.js for game stats + multi-axis comparison
  - TOC:
    - What it does
    - When to use
    - HTML
    - The signature options
    - Multi-character comparison — overlay datasets
    - Gotchas
    - Cross-references
- **[./references/TECH-reduction-pass.md](./references/TECH-reduction-pass.md)**
  - Description: Reduction Pass — strip everything that doesn't encode data
  - TOC:
    - What it does
    - The checklist
    - Per-aesthetic strictness
    - The rule
    - Before / after — gridline removal
    - Before / after — legend to direct labels
    - Before / after — decoration removal
    - Decision rule
    - Gotchas
    - Cross-references
- **[./references/TECH-section-band.md](./references/TECH-section-band.md)**
  - Description: Full-width section separator bands
  - TOC:
    - What it does
    - The CSS
    - HTML
    - Numbered section headers with icon prefix
    - When to use
    - The color choice
    - Gotchas
    - Cross-references
- **[./references/TECH-section-header-pill.md](./references/TECH-section-header-pill.md)**
  - Description: Section header pill badge (ecosystem signature)
  - TOC:
    - What it does
    - CSS
    - HTML
    - The four visual layers
    - When to use
    - Variants
    - Gotchas
    - Cross-references
- **[./references/TECH-section-variety-rule.md](./references/TECH-section-variety-rule.md)**
  - Description: Section Variety Rule — MANDATORY across 4+ sections
  - TOC:
    - What it does
    - Acceptable section variety
    - Anti-patterns (reject and redesign)
    - The enforcement routine
    - The available component types (pick 3+)
    - Rule of thumb
    - Gotchas
    - Cross-references
- **[./references/TECH-signature-palette.md](./references/TECH-signature-palette.md)**
  - Description: Signature palette — near-black + amber + teal/blue complement
  - TOC:
    - What it does
    - Background rules
    - The default accent hierarchy
    - Palette temperature
    - Other most-used accents (in order)
    - Named palette recipes (top 3)
    - Rule — brand first, signature second
    - Gotchas
    - Cross-references
- **[./references/TECH-slope-chart.md](./references/TECH-slope-chart.md)**
  - Description: Slope chart — before/after comparison
  - TOC:
    - What it does
    - When to use
    - Coordinate system
    - HTML
    - CSS
    - Gotchas
    - Cross-references
- **[./references/TECH-stacked-reference-archetype.md](./references/TECH-stacked-reference-archetype.md)**
  - Description: Archetype 1: Stacked Reference (DEFAULT, 70%+ of work)
  - TOC:
    - What it does
    - When to use
    - The shape
    - CSS implementation
    - The section-variety rule still applies
    - Gotchas
    - Cross-references
- **[./references/TECH-stat-poster-archetype.md](./references/TECH-stat-poster-archetype.md)**
  - Description: Archetype 4: Stat Poster
  - TOC:
    - What it does
    - When to use
    - The shape
    - CSS implementation
    - The number-first rule
    - Tabular numerics mandatory
    - Gotchas
    - Cross-references
- **[./references/TECH-stat-strip-component.md](./references/TECH-stat-strip-component.md)**
  - Description: `stat_strip` — full-width KPI row with colored top borders
  - TOC:
    - What it does
    - When to use
    - CSS
    - HTML
    - The signature — colored top border
    - Number formatting rules
    - Common stat fields
    - Gotchas
    - Cross-references
- **[./references/TECH-step-process-component.md](./references/TECH-step-process-component.md)**
  - Description: `step_process` — numbered steps with connector line
  - TOC:
    - What it does
    - When to use
    - CSS
    - HTML
    - The connector line trick
    - Horizontal variant
    - Gotchas
    - Cross-references
- **[./references/TECH-svg-pie-chart.md](./references/TECH-svg-pie-chart.md)**
  - Description: SVG pie chart — token allocation (the #1 chart)
  - TOC:
    - What it does
    - The color rule
    - SVG arc math
    - Segment calculator
    - Template — 4 segments
    - Legend — side-by-side
    - Gotchas
    - Cross-references
- **[./references/TECH-swim-lane-architecture.md](./references/TECH-swim-lane-architecture.md)**
  - Description: Swim-lane architecture diagram
  - TOC:
    - What it does
    - When to use
    - CSS
    - HTML
    - The vertical label trick
    - When NOT to use
    - Gotchas
    - Cross-references
- **[./references/TECH-template-registry.md](./references/TECH-template-registry.md)**
  - Description: Template registry — 24 reference templates
  - TOC:
    - What it does
    - The shared V4 standards
    - Crypto / Web3 templates (13)
    - Generic templates (11)
    - Template selection by user intent
    - Usage
    - Gotchas
    - Cross-references
- **[./references/TECH-tier-comparison-component.md](./references/TECH-tier-comparison-component.md)**
  - Description: `tier_comparison` — tier badge table
  - TOC:
    - What it does
    - When to use
    - CSS — the base table
    - CSS — the tier badges
    - HTML
    - Custom tier names and colors
    - Gotchas
    - Cross-references
- **[./references/TECH-token-economics-playbook.md](./references/TECH-token-economics-playbook.md)**
  - Description: Token-Economics playbook — 35% of body of work (62/175)
  - TOC:
    - What it does
    - When to use
    - Color system
    - Typography
    - Standard component prevalence (across 62 pieces)
    - Visual properties
    - Signature layout pattern (portrait-tall, 10+ content blocks)
    - CSS variables
    - Font pair
    - Reference template
    - Density rule
    - Gotchas
    - Cross-references
- **[./references/TECH-typography-scale.md](./references/TECH-typography-scale.md)**
  - Description: Typography scale — minor third (1.25 ratio)
  - TOC:
    - What it does
    - The scale
    - Weight-based hierarchy
    - Letter-spacing rules
    - Tabular numerics (mandatory for numbers)
    - Summary rules
    - Body font size rules (the density signature)
    - Gotchas
    - Cross-references
- **[./references/TECH-waffle-chart.md](./references/TECH-waffle-chart.md)**
  - Description: Waffle chart — 10×10 grid for % of total
  - TOC:
    - What it does
    - When to use
    - HTML
    - CSS
    - JS — add `.filled` + stagger
    - Legend styling
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-infographics/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.pl`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. self-contained HTML + retina PNG + print-ready PDF infographic posters). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/infographics/` created fresh)
   - Last-resort scratch: `/tmp/amw-infographics-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- [path/to/artifact.ext](./path/to/artifact.ext) — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.
