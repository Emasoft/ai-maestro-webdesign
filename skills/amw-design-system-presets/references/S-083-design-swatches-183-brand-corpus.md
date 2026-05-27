---
id: S-083
name: Design-Swatches 183-Brand DESIGN.md Corpus
aesthetic_position: brand-derived-reference-superset
source_attribution: "blocked-A.md §design-swatches-main; `design-swatches-main/` 183 DESIGN.md files (186 with extras) — VoltAgent/awesome-design-md superset (MIT)."
license: MIT (direct-port — DESIGN.md files live at upstream MIT licence)
---

# S-083 — Design-Swatches 183-Brand DESIGN.md Corpus

## Identity

S-083 is the **183-brand superset** of S-081 — the full `design-swatches-main` corpus, comprising 183 (plus 3 extras = 186 total) Google-format DESIGN.md files. Each entry follows the canonical format: YAML frontmatter (palette + type + spacing + radius + shadow tokens) plus an 8–10 section markdown body (overview, principles, color system, typography, layout, components, motion, atmosphere). The corpus is **explicitly designed as a "voice reference" for new extractions** — read 2–3 exemplars in the same visual category before authoring a new DESIGN.md, so the tone and depth of the output matches the upstream craft.

This is the largest reference corpus in the plugin. Brands span: Apple, Stripe, Linear, Arc Browser, Raycast, A24, Polestar, Wired, Aceternity, Poolsuite, Spotify, Vercel, Supabase, Shadcn, Notion, Figma, Ferrari, Patagonia, Supreme, Pentagram, **plus 163 more**. The full file inventory lives at `SKILLS-TO-INTEGRATE/web-design/.../design-swatches-main/`.

Like S-081, S-083 is **descriptive, not prescriptive**. Use it as a creative voice library; never paste a brand's verbatim tokens onto a non-affiliated product.

## Companion tool: dembrandt CLI

The corpus pairs with the `dembrandt` CLI (from `design-swatches-main`) for new extractions:

```bash
npx dembrandt {URL} --save-output --pages 1 --screenshot screenshot.png --slow
```

`dembrandt` extracts structured JSON with 15 top-level keys: colors (palette + semantic + CSS variables), typography (styles + sources + contexts), spacing, borderRadius, borders, shadows, components (buttons, inputs, links, badges), breakpoints, iconSystem, frameworks. The output JSON is the raw material; the DESIGN.md is the curated voice document built from it.

## Categorical index (high-level)

The 183 brands span at least these aesthetic categories (representative examples; not exhaustive):

| Category | Representative brands | Voice signature |
|---|---|---|
| Editorial / Cinematic | A24, WIRED, Polestar, Pentagram | Binary contrast, hairline rules, restraint |
| Premium Fintech | Stripe, Coinbase, Revolut, Wise | Brand-tinted multi-layer shadow, ss01-style features |
| Developer Tool / Dark | Raycast, Cursor, Warp, Linear, Vercel | Near-black void, single accent, dense type |
| Consumer / Playful | Arc Browser, Pinterest, Spotify, Lovable | Warm canvas, vibrant accent, generous radius |
| AI / Foundation Model | Anthropic / Claude, OpenAI, xAI, Mistral, Together AI | Restrained editorial, single accent, no maximalism |
| Premium / Automotive | Apple, BMW, Ferrari, Lamborghini, Polestar | Cinematic imagery, low-contrast weight ranges, generous spacing |
| Heritage / Lifestyle | Patagonia, Supreme, Poolsuite, Sanity | Earthy palette OR pastel-retro, photography-driven |
| Documentation / Reading | Notion, Mintlify, Resend, Replicate | Warm canvas OR clean white, serif/sans split, single-column |
| Data / Analytics | Sentry, PostHog, Kraken, Supabase | Dark dashboard, tabular-nums, distinct series colours |
| Studio / Agency | Pentagram, Clay, design-led portfolios | Editorial typography, art-directed layout, asymmetric |

For the precise brand-to-category mapping, read the DESIGN.md frontmatter `category:` field in each upstream file.

## How to use this corpus (workflow)

1. **User brief identifies a category or names a brand** — "we want something editorial like Polestar" or "Ferrari-class luxury without the automotive".
2. **Read 2–3 DESIGN.md entries in the matching category** end-to-end, including the atmosphere/voice paragraph. Goal: internalise the tone, not the tokens.
3. **Identify the structural fingerprint** common across the 2–3 reference brands — e.g. for "premium fintech" the pattern is `white-canvas + deep-navy ink + single brand accent + brand-tinted multi-layer shadow + light-weight display + ss01-style features`.
4. **Synthesize a new DESIGN.md** for the user's product that captures the structural fingerprint with original palette / typeface choices appropriate to the user's audience and product domain.
5. **Validate** with `bin/amw-design-md-lint.sh` + `bin/amw-design-md-contrast.py`.
6. **(Optional)** run `npx dembrandt {your-staging-url} --save-output` once your synthesized site is live, to capture the live tokens back into JSON for a self-check.

The 183 brands are inspiration, NOT paste-in tokens. The lift-tokens-verbatim use case is restricted to the 8 brands in S-082; everything beyond those 8 is voice-reference only.

## "Breaks if" invariants (corpus-level)

- Breaks if a brand's verbatim hex palette is shipped on a non-affiliated commercial product — design-trade-dress infringement.
- Breaks if more than 3 DESIGN.md entries are loaded at once for active comparison — at 3+ the patterns blur and the structural fingerprint becomes noise. Pick a category, sample ≤3, sketch original.
- Breaks if the corpus is treated as prescriptive ("apply S-083:Patagonia preset" — there is no such operation; S-083 IS the voice library, not a token bundle).
- Breaks if entries are loaded without checking their freshness — brand sites re-launch; the captured DESIGN.md may diverge from the current live site. Prefer fresh `dembrandt` extractions if the brand has materially re-skinned.
- Breaks if competitor DESIGN.md content (palette, atmosphere prose) ends up in the new product's shipped DESIGN.md — voice references must stay in the design process, not in the artefact.

## Canonical render-test pointer

Render-test: N/A at corpus level — each individual brand entry references the live brand site URL.
Source render: `design-swatches-main/<brand-slug>/DESIGN.md` files; live brand sites at time of capture; `dembrandt` re-extraction for staleness check.
Parity threshold: A-class justified (descriptive reference superset; no preset to render-test).

## Render-test verdict

JOD: N/A (descriptive corpus — render-test does not apply at superset level)

## Cross-references

- **Subset:** S-081 (50-brand subset from design-for-beauty) — smaller curated voice reference.
- **Prescriptive complement:** S-082 (8 hand-extracted token sets with full paste-able CSS) — the prescriptive complement to S-081/S-083's descriptive corpora.
- **Companion CLI:** `dembrandt` (from design-swatches-main) — extracts new DESIGN.md from any URL.
- **Brand-derived prescriptive presets** worth cross-referencing: S-014 Editorial Serif, S-035 21st.dev / Aceternity, S-044 Dashboard Magazine (FT-style), S-045 Warm Minimalism (Notion-derived).
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- Source attribution: `reports/batch9-harvest/blocked-A.md` §design-swatches-main

## Attribution

Brand corpus direct-ported from `blocked-A.md §design-swatches-main` which transcribes the catalogue at `design-swatches-main/<brand>/DESIGN.md`. The upstream source is the VoltAgent superset (MIT licence; see `design-swatches-main/LICENSE`). The category synthesis table above is original routing convenience, not a verbatim transcript of any upstream taxonomy. Each brand DESIGN.md remains the property of its respective brand owner; the design-swatches corpus captures publicly visible visual fingerprints under fair-use editorial commentary. The `dembrandt` CLI is referenced as a companion tool; install per its own upstream documentation. Treat the corpus as voice reference, not asset library.
