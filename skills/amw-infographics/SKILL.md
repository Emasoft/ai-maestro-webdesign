---
name: amw-infographics
description: Dense editorial infographics as HTML + PNG + PDF from a structured data brief — tokenomics, whitepaper summaries, ecosystem maps, roadmaps, airdrop guides, staking breakdowns, stat posters. Triggers on "infographic", "tokenomics graphic", "ecosystem map", "turn stats into a graphic". NOT for generic design (design-principles) or editorial diagrams (diagram-editorial). Use when producing a dense infographic from a data brief. Trigger with /amw-create-or-modify-html-diagram.
version: 0.2.0
author: ai-maestro-webdesign
---

# Infographics

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Its triggers are data-infographic-specific only — `design-principles` routes here when the user has real data or a structured brief and wants a shareable, dense editorial graphic.

## Overview

Produces dense editorial infographics as self-contained HTML + retina PNG + print-ready PDF from a 24-template library and 175-design DNA set. Three execution modes: Interactive Builder (component-by-component with live preview), One-Shot (full infographic in one pass from a complete data brief), and Guided Creative (two composition options before building). Near-black backgrounds, warm+cool accent palettes, all-caps condensed display fonts, high content density (8–15 blocks on portrait-medium). Not a generic webpage renderer — closer to a crypto research poster or game cheat sheet.

## Instructions

1. Classify the invocation mode: Interactive Builder (step-by-step with live preview at `localhost:7883`), One-Shot (full pass from a complete data brief), or Guided Creative (two composition options first).
2. For One-Shot and Guided Creative: ask the three Design Brief questions (brand, platform, key insight); classify the content type, archetype, and dominant component.
3. Build the infographic as a single self-contained HTML with required head includes (Google Fonts, Phosphor Icons, optional Chart.js); apply playbook colors/fonts; all CSS inline with `:root` custom properties.
4. Run the Anti-Frontend Checklist and Reduction Pass per the Quality Gate in `## Execution modes`.
5. Export via `bin/amw-html-export.py -i {file}.html -o {name} -f all --width {W} --scale 2`.
6. See the `## Execution modes` section below for the three authoritative mode workflows (Interactive Builder, One-Shot, Guided Creative).

## Activation

Callable directly via the `/amw-create-or-modify-html-diagram` command with `--style infographic` (user shortcut — fast path for infographic creation). Also invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode when the user needs a dense editorial graphic. In Main-agent mode the orchestrator may apply the full 24-template library, 175-design DNA, and multi-format export techniques from this skill beyond what the command's parameters expose.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT (Phase B).** Emits self-contained HTML + retina PNG + print-ready PDF from a 24-template library and 175-design DNA set. Each file is dense editorial reference material — closer to a crypto research poster or game cheat sheet than a website. Not a substitute for `../amw-diagram-editorial/` (editorial diagrams), `../amw-svg-creator/` (freeform vector), or `../amw-ascii-to-html/` (general webpage rendering).

## What this skill produces

- **HTML** — self-contained, CDN fonts (Bebas Neue, Montserrat, Teko, Orbitron via Google Fonts) + Phosphor Icons + optional Chart.js.
- **PNG** — retina (2x) via `../../bin/amw-html-export.py` (Playwright + Chromium).
- **PDF** — print-ready via the same script.
- **Canvas sizes** (7): portrait-medium 1080×1440 (default), Twitter/X 1200×675, Instagram 1080×1080, Instagram portrait 1080×1350, LinkedIn 1200×627, Pinterest 1000×1500, website 1100×auto. Full table in [platform-sizes](resources/platform-sizes.md).
  > Quick Reference · Layout & Font Adjustments Per Platform · Twitter/X (Most Common) · Instagram Post (1:1 Square) · Instagram Story / TikTok (9:16 Vertical) · LinkedIn · Pinterest · Font Size Scaling by Platform · Watermark / Attribution Rule by Platform · export.py Commands by Platform

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
- **Tight spacing inside sections.** Card padding 12–16px (NOT 24–32px). Body font 11–13px for dense content (intentional poster/print-scale exception to design-principles' 16px desktop floor — infographics are shareable graphics, not webpages; see [typography-system](../amw-design-principles/typography-system.md) for the floor rule this skill carves out from). Gap 8–12px between items. Whitespace separates *sections* from each other, not content within a section.
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- **Content format hierarchy.** Tables → bullet lists → flow diagrams → stat callouts → badges. Paragraphs are a last resort, reserved for 1–2 sentence hero intros.

Full design DNA with code samples: [style-details](resources/style-details.md) and [layout-patterns](resources/layout-patterns.md).

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
3. **Render one component at a time** to `<.infographic/.preview.html>` as a full self-contained HTML document. Ask for approval before locking it in.
4. **Approval gate** — only write approved components to the state file `{cwd}/.infographic/{project}.json`. Verbatim HTML, no re-generation.
5. **Assemble** on user command (`assemble`, `finalize`, `done`) — stitch approved components, wrap with header/footer, run Reduction Pass, export via `html-export.py`.

Full builder protocol (state file schema, approval vocabulary, assembly rules): [layout-patterns](resources/layout-patterns.md) and the `create-infographics` upstream SKILL.md.

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

Copy this checklist and track your progress as you run both passes:

**Anti-Frontend Checklist** (must all be ✓):
- [ ] No uniform card grids — at least 3 different component types used.
- [ ] No paragraph descriptions — body text is bullet points.
- [ ] Card padding 12–16px, body font 11–13px, gap 8–12px.
- [ ] Borders visible — minimum `rgba(primary, 0.25)`.
- [ ] Arrows/connectors present if content describes a process/flow.
- [ ] At least one table if data has comparisons/specs/rates.
- [ ] Content block count meets density target.

**Reduction Pass** — remove gridlines that aren't needed for reading values, axis tick marks where direct labels exist, decorative icons, borders/glows on elements already separated by whitespace, text that repeats what the visual shows. Strictness scales to aesthetic (see [style-details](resources/style-details.md) reduction table). Do NOT reduce information density.

**Final quality check** — no fabricated data, display font is not banned, Phosphor CDN included, canvas width matches platform, background mode matches request, footer present (unless user said no), all labels directly on charts (annotation-first), logo present (95% of real pieces), type-specific playbook applied if one fits.

## Technique selection

Pick a technique category below, then look up the specific TECH file in the
catalog at [_index](references/_index.md). Every TECH
file shares the same TOC structure (What it does · When to use · How it
works · CSS · HTML · Gotchas · Cross-references) plus 1–4 technique-specific
subsections.

- **Mode** — pick how to drive the run: Interactive Builder, One-Shot, or Guided Creative (3 modes; see _index.md "Modes" section).
- **Archetype** — pick the composition shape: Stacked Reference (default), Flow Poster, Hub & Spoke, Stat Poster, Cheat Sheet (5 archetypes).
- **Playbook** — content-type-specific palette / font / layout pack: Token-Economics (35%), Game-Overview (14%), Ecosystem (13%), Crypto-Explainer (17%), Airdrop-Guide (10%) — 5 playbooks total.
- **Component** — 15 building blocks: `bullet_panel` (default text), `bordered_section`, `stat_strip`, `dense_table`, `tier_comparison`, `step_process`, `flow_with_arrows`, `flywheel_loop`, character / NFT card grid, section bands & headers, section variety rule, outer canvas border, arrows & connectors, swim-lane architecture.
- **Chart** — 12 chart options: chart selection guide, SVG pie (#1 chart), CSS horizontal bar, line (Chart.js), radar, progress bar, waffle 10×10, slope before/after, annotated bar with benchmark, proportional circles, dot plot, annotation-first rule.
- **Color & typography** — 8 systems: signature palette (near-black + amber + teal/blue), 13 named palette recipes, per-content-type signature palettes, blockchain chain color-coding, glow system (neon), 5-font display hierarchy, type scale (1.25 minor third), inline `$TOKEN` coloring.
- **Copy** — 3 guides: bullets over paragraphs, number formatting, design brief intake.
- **Aesthetic systems** — 3 globals: dense editorial DNA, background depth (radial orbs / scanlines / paper texture), 24 template registry.
- **Pre-delivery / quality** — the 2-step gate: Anti-Frontend Checklist, Reduction Pass.
- **Pipeline / preview / export** — 4 runtime steps: platform sizing (7 canvases), live preview server, entrance animations, export (HTML to PNG/PDF/SVG).

For each category, [_index](references/_index.md) lists the
exact `TECH-<slug>.md` filename plus a one-line description per technique.
  > Table of Contents · Modes (3) · Archetypes (5) · Playbooks (5 content-type playbooks) · Components (15) · Charts (10) · Color & typography (8) · Copy (3) · Aesthetic systems (3) · Pre-delivery / quality (2) · Pipeline / preview / export (3) · Cross-references

## Prerequisites

- **runtime_binaries (system):** `python3 ≥ 3.8`.
- **runtime_binaries (installed via `/amw-init`):** Playwright + Chromium (`python3 -m playwright install chromium --with-deps`), optional Inkscape or pdf2svg for SVG export.
- **python_packages:** `playwright ≥ 1.40.0`.
- **npm_packages:** none required.
- **mcp_servers:** none.
- **CDN assets (run-time):** Google Fonts (Bebas Neue, Teko, Orbitron, Montserrat), Phosphor Icons, optional Chart.js. Offline environments need the CDN resolvable — `html-export.py` spins up a local HTTP server so Playwright resolves them cleanly.
- **Shared scripts:** `../../bin/amw-html-export.py` (PNG / PDF / SVG export), `../../bin/amw-preview-server.py` (Mode A live preview).

## Examples

`examples/` ships 15 rendered PNG reference outputs and `templates/` ships 24 fully-built reference HTML pieces with `{{PLACEHOLDER}}` variables.

**Token-economics example (One-Shot mode):** Input: a tokenomics brief with allocation %, vesting schedule, and brand color. Routing: `token-economics.html` template, [TECH-token-economics-playbook](references/TECH-token-economics-playbook.md), [TECH-stacked-reference-archetype](references/TECH-stacked-reference-archetype.md), [TECH-svg-pie-chart](references/TECH-svg-pie-chart.md), [TECH-progress-bar-vesting](references/TECH-progress-bar-vesting.md). Output: HTML + retina PNG + PDF at 1080×1440 with 11 content blocks.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — upstream orchestrator; route here only when the user has structured data and wants a dense editorial graphic.
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — final AI-slop scan every HTML output must pass.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
- [color-system](../amw-design-principles/color-system.md) — brand-color / WCAG AA validation when a custom color is supplied.
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — type-scale rules that compose with this skill's display-font hierarchy.
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- `../../bin/amw-html-export.py` — PNG / PDF / SVG export pipeline; shared with `hyperframes-bridge` and `ascii-to-html`.
- `../../bin/amw-preview-server.py` — Mode A live preview server, port 7883.
- [design-brief](resources/design-brief.md) — 5-question intake framework + aesthetic decision table.
  > The 5 Brief Questions · Question 2 → Aesthetic Decision Mapping · Question 3 → Platform Decision Mapping · Question 1 → Light/Dark Suitability · Thesis Extraction · From raw numbers: · From a topic brief: · Thesis formula: · Tone → Palette Mapping · Audience Sophistication → Density & Vocabulary · Skip-Brief Defaults · Brief → Design Decision Checklist
- [style-details](resources/style-details.md) — full 1062-line design system with component CSS patterns, type playbooks, reduction-pass rules.
- [layout-patterns](resources/layout-patterns.md) — full 842-line layout and archetype scaffold library with CSS grid implementations per archetype.
  > Layout Statistics · Your Dominant Infographic Types · Layout Recipes by Type · TOKEN-ECONOMICS (35% of your work — your specialty) · GAME-OVERVIEW (19% — your #2 type) · ECOSYSTEM (15% — partner/collaboration type) · CRYPTO-EXPLAINER (12% — educational type) · AIRDROP-GUIDE (8% — action-focused type) · NFT-SHOWCASE (5% — collectible type) · DENSE SPACING REFERENCE (apply across ALL types) · Composition Archetype CSS Implementations · ARCHETYPE 1: Stacked Reference (DEFAULT — 70%+ of pieces) · ARCHETYPE 2: Flow Poster · ARCHETYPE 3: Hub & Spoke · ARCHETYPE 4: Stat Poster · ARCHETYPE 5: Cheat Sheet · Stats Bar / KPI Strip (74/175 = 42%)
- [charts](resources/charts.md) — chart rules (bar / line / pie / radar / stat callouts) with annotation-first placement.
  > When to Use What · SVG Pie Chart (Token Allocation — Your Most-Used) · Color Rule · How SVG Pie Wedges Work · Segment Calculator · Template (4-segment example — amber primary shades) · CSS · CSS Horizontal Bar Chart (Vesting / Allocation Strips) · Chart.js — Complex Charts via CDN · Line Chart Template · Radar Chart Template (Game Stats) · Pure CSS Progress Bar (Vesting Timeline) · Waffle Chart (% of Total — Pure HTML/CSS) · Slope Chart (Before/After — Inline SVG) · Annotated Bar Chart (SVG — Hero Bar + Benchmark) · Proportional Circles (SVG — Area = Value) · Dot Plot (SVG — Distribution / Individual Points)
- [color-palettes](resources/color-palettes.md) — full palette library by type (token-economics amber, crypto-explainer purple, ecosystem teal, airdrop amber+blue, etc.).
  > Key Statistics · Per-Type Signature Palettes · Brand Distinction Strategy · Your Signature Background Colors · Your Most-Used Accent Colors (Primary) · Palette Recipes (Named Collections) · AMBER DARK (YOUR SIGNATURE — most used) · CYBER TEAL (Very popular) · GAMING RED (Action-focused) · HOT PINK WEB3 (Crypto-brand favorite) · EMERALD GAMING (Nature/fantasy) · ROYAL PURPLE GAMING (NFT/fantasy) · NAVY CRYPTO (Professional/DeFi) · WARM GOLD DARK (Premium/exclusive) · RETRO PIXEL / GAMING ARCADE · LIME CYBERPUNK · Standout / High-Contrast Palettes · NEON ACID (High energy / Disruptive) · SUNSET HORIZON (Warm / Premium Editorial) · EARTHY TECH (Organic / DePIN / Sustainable) · Glow Color Reference (Top confirmed glow colors) · Light Mode Palettes (When background: "light") · L1. CLEAN WHITE + AMBER (Light version of your signature) · L2. WARM EDITORIAL (Premium light) · L3. BLUE PROFESSIONAL (Clean SaaS / Finance)
- [font-pairings](resources/font-pairings.md) — display-font prevalence table and body-font pairings per type.
  > Key Statistics · Your Font Rules (Non-Negotiable) · Your Core Display Fonts (Ranked by usage) · ✦ 2025/2026 Additions (Premium / Fresh) · Your Body Font (Almost Always the Same) · Tested Font Pairings (Your Actual Combinations) · BEBAS NEUE + MONTSERRAT (Your Signature — 40%+ of work) · MONTSERRAT + INTER (Professional/Brand) · RAJDHANI + INTER (Gaming/Technical) · ORBITRON + INTER (Sci-Fi/DeFi) · PRESS START 2P + INTER (Pixel/Retro Gaming) · TEKO + INTER (Esports / Tokenomics) ✦ Confirmed · BUNGEE + INTER (Arcade / Bold Block) · BANGERS + INTER (Meme/Bold) · CINZEL + INTER (Fantasy/NFT Luxury) · SPACE GROTESK + INTER (Modern Web3) · SYNE + DM SANS (Ultra-Modern Web3 / Tech) ✦ New · PLUS JAKARTA SANS (Premium Report / Brand) ✦ New · OUTFIT + INTER (Clean Contemporary) ✦ New · Typography Constants (Always Apply)
- [platform-sizes](resources/platform-sizes.md) — 7 canvas sizes with per-platform layout/font adjustments and safe zones.
  > Quick Reference · Layout & Font Adjustments Per Platform · Twitter/X (Most Common) · Instagram Post (1:1 Square) · Instagram Story / TikTok (9:16 Vertical) · LinkedIn · Pinterest · Font Size Scaling by Platform · Watermark / Attribution Rule by Platform · export.py Commands by Platform
- [copy-guide](resources/copy-guide.md) — headline, callout, and label writing rules.
  > The Core Rule · Stat Formatting Rules · Numbers — How to Display Them · Labeling Stats · Currency Conventions · Headline Formulas · Rule: UPPERCASE + Verb-First or Noun-Phrase · Subtitle Rules · Per-Component Word Budgets · Color-Coded Keyword Highlighting · Disclaimers & Source Citations · Footer Disclaimer (Always Include) · Source Citation Format · Badge & Tag Copy · Body Copy Rules — Bullets Over Paragraphs · Rule: Bullet points, not paragraphs · Rule: One fact per line · Rule: Sentence fragments, not full sentences · Rule: Inline token coloring — always color `$TOKEN` names · Common Mistakes to Avoid
- `templates/` — 24 reference templates (see index above).
- `examples/` — 15 rendered PNG reference outputs for each template family.
- `evals/evals.json` — 5 scenario test prompts + expected outcomes.
- [_index](references/_index.md) — flat alphabetical/numeric catalog of every TECH file with one-line descriptions.

## Error Handling

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

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-infographics/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. self-contained HTML + retina PNG + print-ready PDF infographic posters). The output path is determined by **project inference**, NOT hardcoded. See [project-output-routing](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
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
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.
