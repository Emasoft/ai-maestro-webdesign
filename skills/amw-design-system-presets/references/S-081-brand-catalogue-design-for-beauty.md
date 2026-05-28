---
id: S-081
name: Brand Catalogue (design-for-beauty — 50 DESIGN.md entries)
aesthetic_position: brand-derived-reference-corpus
source_attribution: "styles-A §Brand Reference Styles; `design-for-beauty-main/references/design-md/<slug>/DESIGN.md`; upstream `VoltAgent/awesome-design-md` (MIT)."
license: MIT (direct-port — DESIGN.md files live at upstream MIT licence)
---

# S-081 — Brand Catalogue (design-for-beauty)

## Identity

S-081 is NOT a single prescriptive aesthetic — it is a **brand-derived reference corpus** of ~50 named DESIGN.md entries authored against real-world brand websites. Each entry is a Google-format DESIGN.md (YAML frontmatter + 8-section body) that captures the brand's actual on-site palette, type system, spacing, motion, and "atmosphere" prose. Treat the corpus as a **voice reference** library: when a user asks for "something with Stripe's premium feel" or "BMW-like dark precision" or "Notion's warm minimalism", read the matching 1–3 entries before authoring a new DESIGN.md, so the tone and depth of the output matches the upstream craft.

Unlike S-001..S-080 which are prescriptive presets (token block + breaks-if + render-test), S-081 is **descriptive**: each row is a fingerprint of a live brand, not a recipe. Use the entries as creative references, NOT as paste-in token sources — every entry needs adaptation to the new brief's audience and product domain.

## Brand index (~50 entries)

The 50-brand catalog from `design-for-beauty-main/references/design-md/`. Each row's slug points to the upstream DESIGN.md file. One-line aesthetic summaries below; for full token blocks read the upstream files.

| Brand | One-line aesthetic | Category |
|---|---|---|
| Airbnb | Warm coral accent, photography-driven, rounded UI | Consumer / Travel |
| Apple | Premium white space, SF Pro, cinematic imagery | Premium consumer |
| BMW | Dark premium surfaces, precise German engineering | Automotive / Luxury |
| Cal.com | Clean neutral UI, developer-oriented simplicity | Developer SaaS |
| Clay | Organic shapes, soft gradients, art-directed layout | Creative / Studio |
| ClickHouse | Yellow-accented, technical documentation style | Developer / Data |
| Claude (Anthropic) | Warm terracotta accent, clean editorial layout | AI / Editorial |
| Coinbase | Clean blue identity, trust-focused, institutional feel | Fintech |
| Cursor | Sleek dark interface, gradient accents | Developer tool |
| ElevenLabs | Dark cinematic UI, audio-waveform aesthetics | AI / Media |
| Ferrari | Chiaroscuro black-white editorial, Ferrari Red, extreme sparseness | Automotive / Luxury |
| Figma | Vibrant multi-color, playful yet professional | Design tool |
| Framer | Bold black and blue, motion-first, design-forward | Design tool |
| HashiCorp | Enterprise-clean, black and white | Enterprise / DevOps |
| IBM | Carbon design system, structured blue palette | Enterprise |
| Kraken | Purple-accented dark UI, data-dense dashboards | Fintech / Crypto |
| Lamborghini | True black cathedral, gold accent, Neo-Grotesk | Automotive / Luxury |
| Linear | Ultra-minimal, precise, purple accent | Developer SaaS |
| Lovable | Playful gradients, friendly dev aesthetic | Developer SaaS |
| Mintlify | Clean, green-accented, reading-optimized | Documentation |
| Mistral AI | French-engineered minimalism, purple-toned | AI |
| MongoDB | Green leaf branding, developer documentation focus | Developer / Data |
| Miro | Bright yellow accent, infinite canvas aesthetic | Collaboration |
| Notion | Warm minimalism, serif headings, soft surfaces | Productivity |
| NVIDIA | Green-black energy, technical power aesthetic | Hardware / AI |
| Ollama | Terminal-first, monochrome simplicity | Developer tool |
| Pinterest | Red accent, masonry grid, image-first | Consumer / Visual |
| PostHog | Playful hedgehog branding, developer-friendly dark UI | Developer analytics |
| Raycast | Sleek dark chrome, vibrant gradient accents | Developer tool |
| Renault | Vivid aurora gradients, NouvelR typeface, zero-radius buttons | Automotive |
| Replicate | Clean white canvas, code-forward | AI / Developer |
| Resend | Minimal dark theme, monospace accents | Developer / API |
| Revolut | Sleek dark interface, gradient cards, fintech precision | Fintech |
| RunwayML | Cinematic dark UI, media-rich layout | AI / Media |
| Sanity | Red accent, content-first editorial layout | CMS |
| Sentry | Dark dashboard, data-dense, pink-purple accent | Developer / Monitoring |
| SpaceX | Stark black and white, full-bleed imagery, futuristic | Aerospace |
| Spotify | Vibrant green on dark, bold type, album-art-driven | Consumer / Media |
| Stripe | Signature purple gradients, weight-300 elegance | Fintech |
| Supabase | Dark emerald theme, code-first | Developer / Data |
| Superhuman | Premium dark UI, keyboard-first, purple glow | Productivity |
| Together AI | Technical, blueprint-style design | AI infra |
| Uber | Bold black and white, tight type, urban energy | Consumer / Mobility |
| Vercel | Black and white precision, Geist font | Developer / Hosting |
| VoltAgent | Void-black canvas, emerald accent, terminal-native | Developer / AI |
| Warp | Dark IDE-like interface, block-based command UI | Developer tool |
| Webflow | Blue-accented, polished marketing site aesthetic | No-code |
| Wise | Bright green accent, friendly and clear | Fintech |
| xAI | Stark monochrome, futuristic minimalism | AI |
| Zapier | Warm orange, friendly illustration-driven | Automation |

## How to use this catalogue (workflow)

1. **User brief:** "We want something that feels like Linear / Stripe / Notion / BMW."
2. **Locate the matching row(s)** in the table above — 1–3 brands at most.
3. **Open the upstream DESIGN.md** for each match at `design-for-beauty-main/references/design-md/<slug>/DESIGN.md` and read end-to-end.
4. **Identify the structural fingerprint** — palette, type families, spacing rhythm, radius/shadow scale, motion duration, atmosphere paragraph.
5. **Synthesize a new DESIGN.md** for the user's product that borrows the structural fingerprint (palette logic, type-family family, spacing scale, atmosphere voice) WITHOUT lifting verbatim colour hex values, brand fonts, or proprietary visual language.
6. **Validate** the synthesized DESIGN.md with `bin/amw-design-md-lint.sh` + `bin/amw-design-md-contrast.py`.

The brand entries are **inspiration**, not paste-in tokens. Lifting BMW's true black + gold verbatim onto an SMB SaaS is plagiarism; lifting BMW's "dark premium German precision" voice into a fintech rebrand is craft.

## "Breaks if" invariants (corpus-level)

- Breaks if a brand's verbatim hex palette is shipped on a non-affiliated product — that's IP infringement, not influence.
- Breaks if the corpus is treated as prescriptive (selecting "Stripe" as a preset and applying its token block) rather than descriptive (reading "Stripe" as a voice reference for premium fintech).
- Breaks if more than 3 entries are loaded at once — the corpus is too noisy for direct comparison beyond 3 brands.
- Breaks if the entries are dated (a brand's site re-skin in 2027 will diverge from the captured DESIGN.md) — check the upstream `updated:` field and prefer fresh extractions if the brand has re-launched.
- Breaks if a competitor's DESIGN.md is referenced in the new product's own DESIGN.md as a "borrowed asset" — voice references stay in the design process, not in the artefact.

## Canonical render-test pointer

Render-test: N/A at corpus level — each individual brand entry has its own canonical reference (the live brand site URL captured at the date the DESIGN.md was authored).
Source render: `design-for-beauty-main/references/design-md/<slug>/DESIGN.md` files; live brand sites at time of capture.
Parity threshold: A-class justified (descriptive reference corpus, not a prescriptive preset).

## Render-test verdict

JOD: A-class (brand-corpus) — 2026-05-29
Reason: descriptive brand-token corpus — no single injectable 13-slot preset; each entry references its own brand source. Not skeleton-render-testable.

## Cross-references

- **Companion preset:** S-083 (183-brand DESIGN.md superset from `design-swatches-main`) — same authoring pattern at larger scale.
- **Companion preset:** S-082 (8 hand-extracted brand token sets with full CSS custom-property blocks) — the prescriptive complement to S-081's descriptive corpus.
- **Brand-derived prescriptive presets:** S-045 Warm Minimalism (Notion-derived, clean-room), S-035 21st.dev / Aceternity Premium Dark, S-044 Dashboard Magazine (FT-style), S-040 Chinese Elegant, S-043 Japanese Dark Editorial (Zutomayo).
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- Source attribution: `reports/batch9-harvest/styles-A.md` §Brand Reference Styles

## Attribution

Brand list direct-ported from `styles-A.md §Brand Reference Styles (from design-for-beauty catalog — 60 DESIGN.md entries)`, which transcribes the corpus catalogued at `design-for-beauty-main/references/design-md/<slug>/DESIGN.md`. The upstream source is `VoltAgent/awesome-design-md` (MIT). The category column is original synthesis for routing convenience. Each brand DESIGN.md remains the property of its respective brand owner; the design-for-beauty corpus captures publicly visible visual fingerprints under fair-use editorial commentary. Treat as voice reference, not asset library.
