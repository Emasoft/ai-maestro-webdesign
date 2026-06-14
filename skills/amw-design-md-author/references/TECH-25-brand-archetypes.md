---
name: TECH-25-brand-archetypes
category: extraction-prefill
source: awesome-design-md brand-archetypes pattern library (58 pre-paywall examples observed)
license: MIT
also-in: TECH-07-url-extraction.md, TECH-08-codebase-extraction.md, TECH-21-style-references-companion.md
status: stable
---

# TECH: Brand archetypes (5-pattern pre-fill library)

## Table of Contents

- [What it does](#what-it-does)
- [Why archetypes accelerate extraction](#why-archetypes-accelerate-extraction)
- [The five archetypes](#the-five-archetypes)
  - [Archetype 1 — Dark Technical](#archetype-1--dark-technical)
  - [Archetype 2 — Luxury Automotive](#archetype-2--luxury-automotive)
  - [Archetype 3 — Fintech / Crypto](#archetype-3--fintech--crypto)
  - [Archetype 4 — Developer Platform](#archetype-4--developer-platform)
  - [Archetype 5 — AI / ML Product](#archetype-5--ai--ml-product)
- [How to detect an archetype](#how-to-detect-an-archetype)
- [Pre-fill workflow](#pre-fill-workflow)
- [Cautions](#cautions)
- [Cross-references](#cross-references)

## What it does

Documents five recurring brand archetypes observed across the 58 pre-paywall awesome-design-md examples. Each archetype carries structural tendencies — likely color palette range, type pairing, spacing rhythm, elevation choice, motion vocabulary, and microcopy voice. An extractor that detects the archetype before extracting tokens can pre-fill the DESIGN.md scaffold with archetype defaults, then refine those defaults from the actual source. This shortens extraction time and reduces hallucination on sections where the source provides ambiguous signal.

## Why archetypes accelerate extraction

Token extraction from a live URL recovers about 60% of the eventual DESIGN.md content directly: colors, typography roles, spacing values, component shapes. The remaining 40% — voice, anti-references, do/don't rules, iteration guide — must be inferred from the source's overall character. The five archetypes give the extractor structural defaults for that inferential 40%, derived from the patterns observed across 58 real-world examples.

Concretely: if the extractor detects "this is a Developer Platform archetype", it pre-fills `STYLE-REFERENCES.md §5 Style Vocabulary` with `"technical, terse, lowercase"` and §3 Anti-References with `"HubSpot, Mailchimp, Squarespace"`. The human author then refines those defaults — but starts from a reasonable position rather than a blank file.

## The five archetypes

### Archetype 1 — Dark Technical

Examples observed: Anthropic, Linear (some pages), Vercel docs, Stripe Workbench, Replicate, Modal.

Color signal:
- Primary backgrounds in the range `#0A0A0A` — `#1A1C1E` (near-black, slight warm tilt).
- Foreground text in cool whites `#F7F5F2` — `#FAFAFA`.
- Single accent color, often a warm orange `#B8422E` — `#E25822` or a cool cyan `#5BCEFA` — `#7DD3FC`.
- Neutral mid-tones in a 5-7 step scale clustered between `#3F4146` and `#A3A6AA`.

Typography signal:
- Display face is a geometric or grotesque sans (Inter, Söhne, Geist, Manrope).
- Body face matches display (single-family system).
- Sometimes a monospaced face for code (JetBrains Mono, Geist Mono, IBM Plex Mono).
- Weights restricted to {400, 500, 600} — no 700, no 300.

Spacing & elevation signal:
- 8px base unit.
- Generous vertical rhythm; hero sections at 96-160px padding.
- Elevation via 1px rule lines, NOT shadows.
- Shadow Philosophy: "shadows only for floating elements; cards use rule lines".

Motion signal:
- Subtle, ease-out, 150-200ms.
- Hover states shift opacity or border color, not transform.
- No bounce, no spring physics.

Microcopy voice:
- Restrained, lowercase where idiomatic, no exclamation marks.
- Sounds like an engineer documenting a tool.
- Avoids "we", "you", marketing-y verbs.

### Archetype 2 — Luxury Automotive

Examples observed: Porsche, Aston Martin, Bentley, Polestar, Lucid.

Color signal:
- Primary background often a deep neutral (`#0F0F0F` near-black or `#FAFAFA` near-white — strong commitment to one or the other).
- Accent is a brand metallic (gold `#C9A85B`, silver `#C0C0C0`, or chrome `#B0B0B0`).
- Sometimes a single saturated brand color (Porsche red `#D5001C`, Polestar yellow `#F5D04E`).
- Wide tonal gap between primary and on-primary (high contrast — emphasizes precision).

Typography signal:
- Display face is a serif or modern serif (Tiempos, Söhne Schmal, Canela, custom serif).
- Body face is a clean sans (Helvetica Neue, Söhne, Inter).
- Heavy weight contrast: display in 600-700, body in 300-400.
- Letter-spacing widened on uppercase display text.

Spacing & elevation signal:
- 8px base.
- Hero sections at 160-240px padding (more generous than Archetype 1).
- Elevation rarely via shadow; usually via spatial separation alone.
- Shadow Philosophy: "no shadows; reliance on whitespace and rule lines".

Motion signal:
- Slow, ease-out, 400-600ms.
- Image reveals on scroll.
- Smooth scroll snapping between sections.

Microcopy voice:
- Editorial, third-person, complete sentences.
- Long-form prose with semicolons and em-dashes.
- Headings are noun phrases ("The new 911. Engineered for tomorrow.").

### Archetype 3 — Fintech / Crypto

Examples observed: Stripe (some surfaces), Plaid, Mercury, Ramp, Bridge, Privy.

Color signal:
- Primary background is white or near-white (`#FFFFFF` — `#FAFAFA`).
- Secondary surface in warm cream (`#F7F5F2` — `#FAF8F3`).
- Single bold accent in saturated brand color (Stripe purple `#635BFF`, Ramp orange `#F45D22`, Mercury blue `#1551F0`).
- Frequent use of a chart-color palette (4-7 distinct colors for data viz).
- Sometimes a secondary brand color used for highlights or callouts.

Typography signal:
- Display and body share a face (single-family system).
- Face is geometric sans or humanist sans (Söhne, Inter, Plus Jakarta, Suisse Int'l).
- Weights span {400, 500, 600, 700} — wider range than Archetype 1.
- Tabular figures enabled (numeric data alignment is critical).

Spacing & elevation signal:
- 8px base, but with tighter inline gaps (4px sub-step common).
- Cards used heavily; elevated via 1-2px borders.
- Shadow Philosophy: "shadows for popovers, modals, dropdowns; cards use borders".

Motion signal:
- Crisp, ease-in-out, 200-300ms.
- Hover lifts on interactive cards (translate-y -2px).
- Form-validation feedback uses color-shift not motion.

Microcopy voice:
- Direct, plain English, sentence case.
- Numeric precision ("99.99% uptime", "$0.30 per transaction").
- CTA copy is verb-first ("Get started", "Open account", "Read the docs").

### Archetype 4 — Developer Platform

Examples observed: GitHub, GitLab, Vercel, Netlify, PlanetScale, Fly.io, Supabase.

Color signal:
- Both light and dark mode declared.
- Light mode primary `#FFFFFF`, dark mode primary `#0D1117` (GitHub) or `#000000` (Vercel).
- Accent often a brand-specific saturated color (Vercel black/white, Supabase green `#3ECF8E`, Netlify teal `#33C7C7`).
- Neutral scale dense (9-11 steps) to support documentation typography.
- Code-block backgrounds in a slightly off-color tint.

Typography signal:
- Three faces: display (often custom or Inter), body (Inter), mono (JetBrains Mono / Geist Mono / IBM Plex Mono).
- Mono face critical — used in headings, inline, code blocks, navigation.
- Body line-height generous (1.55-1.7) for documentation density.
- Documentation-specific roles: caption, code, kbd, inline-code.

Spacing & elevation signal:
- 8px base.
- Documentation reading width capped (640-720px max).
- Cards use 1px borders; modals use shadows.
- Shadow Philosophy: "shadows reserved for floating UI; documentation surfaces are flat".

Motion signal:
- Minimal — documentation prioritizes readability over motion.
- Hover states color-shift only.
- Page transitions via fade or none.

Microcopy voice:
- Technical, terse, lowercase headings.
- Code-embedded prose ("Run `npm install`", "Set the `DATABASE_URL` env var").
- CTA copy is technical ("Deploy", "Connect", "Configure", "Run").

### Archetype 5 — AI / ML Product

Examples observed: Anthropic Claude.ai, OpenAI ChatGPT, Cohere, Replicate, Together AI, Modal, Pinecone.

Color signal:
- Often dark-first or light-with-warm-neutral primary.
- Warm neutrals dominate (cream `#F5F1EA`, near-black `#1A1A1A`).
- Accent often a warm brand color (Anthropic terracotta `#CC785C`, OpenAI black, Cohere coral `#FF7759`).
- Avoids saturated blues — distinct from Archetype 3 fintech blues.

Typography signal:
- Display face often a humanist serif or sans-serif with humanist undertones (Tiempos, Söhne, Charter, Inter).
- Body face matches or contrasts (serif-display + sans-body is common).
- Generous body line-height (1.6-1.8) — long-form reading.
- Sometimes a typewriter or monospaced display face for "computational" feel.

Spacing & elevation signal:
- 8px base.
- Hero sections at 120-200px padding.
- Elevation via subtle gradient or rule-line; shadows rare.
- Shadow Philosophy: "warmth via background tint, not via shadow elevation".

Motion signal:
- Soft, ease-out, 300-500ms.
- Streaming-text reveals (token-by-token) common in product surfaces.
- Subtle "thinking" indicators (cursor pulse, dot-dot-dot).

Microcopy voice:
- Conversational, second-person, complete sentences.
- Sounds like a thoughtful colleague, not a marketing voice.
- Avoids hype words ("revolutionary", "10x", "game-changing").
- CTA copy is direct but warm ("Try Claude", "Start chatting", "Run a model").

## How to detect an archetype

The extractor applies a simple decision tree on the source URL:

1. **Background color check.** If primary background is near-black (`#000000` — `#1A1C1E`), candidate is Archetype 1 (Dark Technical) or Archetype 2 (Luxury Automotive).
   - Sub-check: serif display face → Archetype 2; sans-only → Archetype 1.
2. **Cream / warm-neutral background check.** If primary background is `#F5F1EA` — `#FAF8F3`, candidate is Archetype 5 (AI / ML Product).
3. **White background with accent saturation check.** If background is `#FFFFFF` and accent is a saturated brand color, candidate is Archetype 3 (Fintech / Crypto) or Archetype 4 (Developer Platform).
   - Sub-check: presence of monospaced typeface in headings or navigation → Archetype 4; tabular figures and chart colors → Archetype 3.
4. **None of the above** → no archetype detected; extractor falls back to fully manual filling.

The detection is heuristic, not authoritative. The author overrides the detected archetype when wrong.

## Pre-fill workflow

Once an archetype is detected, the extractor:

1. Pre-fills `STYLE-REFERENCES.md §1 Design Lineage` with the archetype's ancestor list.
2. Pre-fills `STYLE-REFERENCES.md §2 Peer References` with examples from the archetype's "observed in" list (filtered to exclude the source brand itself).
3. Pre-fills `STYLE-REFERENCES.md §3 Anti-References` with brands from OTHER archetypes (Archetype 4 anti-references include Archetype 3 fintech blues).
4. Pre-fills `STYLE-REFERENCES.md §5 Style Vocabulary` with the archetype's voice descriptors.
5. Pre-fills DESIGN.md §8 Do's and Don'ts with archetype-typical rules (e.g. "Don't use box-shadow on cards" for Archetype 1).
6. Pre-fills the §6 Shadow Philosophy paragraph with the archetype's typical stance.
7. Leaves all token tables (§2-§4) and the elevation table (§5) empty — those are extracted from the source.

The human author then reviews the pre-fills and accepts, edits, or rejects each.

## Cautions

- Archetypes are not exhaustive. About 15% of the 58 observed examples did not fit cleanly into any of the 5 — they were marked "hybrid" or "unique" in the extraction notes.
- Brand evolution shifts archetype. A company that was Archetype 4 (Developer Platform) in 2020 may have rebranded to Archetype 5 (AI / ML Product) in 2024.
- Archetype detection from a single page is unreliable. Use the homepage, the docs index, and at least one pricing/product page before committing to an archetype.
- Never let the archetype defaults survive into the final DESIGN.md unchecked. The human author MUST review every pre-fill before lint.

## Cross-references

- [TECH-07-url-extraction](TECH-07-url-extraction.md) — URL extraction pipeline that triggers archetype detection
- [TECH-08-codebase-extraction](TECH-08-codebase-extraction.md) — codebase scan applies archetype detection from CSS-var patterns
- [TECH-21-style-references-companion](TECH-21-style-references-companion.md) — STYLE-REFERENCES.md sections the archetype pre-fills populate
- [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md) — Iteration Guide / Known Gaps populated from archetype defaults
- [TECH-26-extended-sections-7-8](TECH-26-extended-sections-7-8.md) — Motion section pre-fills derived from archetype motion signal
