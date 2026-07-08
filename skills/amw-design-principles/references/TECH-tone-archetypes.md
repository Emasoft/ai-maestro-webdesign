---
name: TECH-tone-archetypes
category: design-principles-aesthetic
source: Bexa design-principles cluster (direct port, batch9 Wave 2 Round 2, T-050)
license: MIT (Bexa upstream is MIT; plugin re-licenses under its own MIT — see the plugin root LICENSE file)
also-in: TECH-voice-tone-archetypes.md (the 7 COPY tones for words — distinct from this file's 11 VISUAL archetypes); skills/amw-design-system-presets/references/catalogue.md (the 45 enumerated graphic presets that anchor these archetypes)
---

# Visual tone archetypes

## Table of Contents

- [What it does (and what it does not do)](#what-it-does-and-what-it-does-not-do)
- [The 11 visual archetypes](#the-11-visual-archetypes)
  - [1. brutally-minimal](#1-brutally-minimal)
  - [2. maximalist-chaos](#2-maximalist-chaos)
  - [3. retro-futuristic](#3-retro-futuristic)
  - [4. organic](#4-organic)
  - [5. luxury-refined](#5-luxury-refined)
  - [6. playful-toy](#6-playful-toy)
  - [7. editorial-magazine](#7-editorial-magazine)
  - [8. brutalist-raw](#8-brutalist-raw)
  - [9. art-deco-geometric](#9-art-deco-geometric)
  - [10. soft-pastel](#10-soft-pastel)
  - [11. industrial-utilitarian](#11-industrial-utilitarian)
- [How archetype routes to a graphic preset](#how-archetype-routes-to-a-graphic-preset)
- [Distinguishing visual archetype from copy archetype](#distinguishing-visual-archetype-from-copy-archetype)
- [Cross-references](#cross-references)

## What it does (and what it does not do)

This file defines an 11-name **shared aesthetic vocabulary** the orchestrator (`amw-design-principles/SKILL.md`) uses to discuss visual direction with the user during Phase A before any graphic-style preset is selected.

It is **not** a list of design systems. The design systems live in `skills/amw-design-system-presets/references/S-001..S-045.md` — those are concrete token sets, font choices, spacing scales, and component looks. This file is a layer above: 11 named *feelings* the user can pick from in conversation, each mapping to a small cluster of presets.

The user says "I want it to feel retro-futuristic" → the orchestrator routes to the preset cluster mapped under retro-futuristic → the user iterates among the 2–4 concrete presets in that cluster → one is chosen.

The vocabulary is shared because both the user-facing main-agent AND the brand-researcher / wireframe-builder / motion-designer sub-agents all reference the same 11 names. Without a shared vocabulary, "playful" means different things to different agents and the Phase A discovery loop fragments.

## The 11 visual archetypes

### 1. brutally-minimal

**Reads as.** Stripped to essentials. Whitespace as material. One typographic voice. Geometry that earns its space.

**Type.** A single sans-serif used at extreme size contrast — display 96px, body 16px, nothing in between. Mono for accents.

**Color.** Two-tone (black + white + ONE accent under 5% surface coverage), or grayscale-only.

**Texture / decoration.** None. No drop shadows, no gradients, no decorative borders.

**Mapped presets.** `S-001-swiss`, `S-022-minimal-pure`, `S-045-warm-minimalism`.

**Use when.** The brand has earned restraint (premium SaaS, design-led agency, editorial site). The user explicitly says "stripped down" / "less is more" / "minimal".

**Don't use when.** The brand needs to convey energy, novelty, or warmth — minimalism reads as cold and slow to those audiences.

### 2. maximalist-chaos

**Reads as.** Density as a feature. Many simultaneous visual systems intentionally fighting for attention. Cultivated overload.

**Type.** 4+ typefaces in one composition. Variable weights and sizes. Text-as-image.

**Color.** 6+ saturated hues simultaneously. Pattern fills, halftones, screen-print textures.

**Texture / decoration.** Stickers, badges, hand-drawn arrows, tape, scribbles, gradients, drop shadows ALL at once.

**Mapped presets.** `S-027-maximalism`, `S-031-paper-collage`, `S-042-memphis`.

**Use when.** Brand IS personality (creator-economy, lifestyle, magazine-style commerce). Younger audiences. The user explicitly says "loud" / "busy" / "lots happening".

**Don't use when.** Trust signals matter — finance, healthcare, government. The chaos reads as amateurism in those contexts.

**Note.** Maximalism is the ONE archetype where the voltage rule (`TECH-brand-voltage.md`) explicitly does not apply. Document the override in DESIGN.md.

### 3. retro-futuristic

**Reads as.** A future imagined from the past. CRT scanlines, chrome bevels, neon. Y2K, 80s synthwave, 90s sci-fi UI.

**Type.** Geometric sans with techno feel — Eurostile, Orbitron-like, Audiowide. Or pixelated bitmap fonts.

**Color.** Saturated purple, cyan, magenta, electric blue. Black backgrounds. Neon glow effects.

**Texture / decoration.** Grids that recede in perspective. Scanlines. Chrome reflections. Vector polygons.

**Mapped presets.** `S-009-aurora`, `S-010-cyberpunk`, `S-011-retro-futuristic`, `S-012-retro-terminal`, `S-032-retro-device`.

**Use when.** Gaming, web3, indie creative tools, music tech. Brands that want "computer culture" as identity.

**Don't use when.** Professional services, healthcare, finance — the aesthetic reads as decorative-not-serious.

### 4. organic

**Reads as.** Hand-touched, earth-rooted, time-worn. Imperfection as warmth.

**Type.** Humanist sans with visible stroke variation. Serif with soft terminals. Slab-serifs with rounded corners.

**Color.** Muted earth tones — terracotta, sage, moss, cream, sand. Low saturation across the board.

**Texture / decoration.** Paper textures, watercolor washes, hand-drawn underlines, soft botanical illustration.

**Mapped presets.** `S-019-heritage-warm-editorial`, `S-020-organic-earthy`, `S-030-lo-fi-paper`, `S-039-warm-professional`.

**Use when.** Wellness, slow-food, sustainability, artisan goods, mid-tier hospitality. Brands selling provenance.

**Don't use when.** Speed / efficiency / scale are the value proposition — the slowness undermines the message.

### 5. luxury-refined

**Reads as.** Quiet confidence. Restraint. Material specificity. The brand assumes the reader belongs.

**Type.** High-contrast serif (didone family — Bodoni, Didot). Or extremely refined geometric sans (Neue Haas Grotesk Display).

**Color.** Desaturated foundations — cream, deep charcoal, oxblood, gold leaf. Saturated accents below 30%.

**Texture / decoration.** Foil-stamp effects, hairline rules, generous letterspacing on small caps. Almost no decoration.

**Mapped presets.** `S-015-fashion-luxury-editorial`, `S-016-luxury-dark-warm`, `S-018-understated-elegance`.

**Use when.** Hospitality 5-star, jewelry, private aviation, wine, fashion above $500 SKU. The audience EXPECTS restraint.

**Don't use when.** The audience needs persuasion — luxury-refined assumes the buyer is already in the room.

### 6. playful-toy

**Reads as.** Welcoming, friendly, "designed by a designer who likes people". Soft geometry. Bright but not aggressive.

**Type.** Rounded sans (DM Sans, Inter Rounded, custom rounded sans). Often display-weight for emphasis.

**Color.** Bright but not saturated — sky blue, soft red, warm yellow, mint. Backgrounds in pastel tints.

**Texture / decoration.** Rounded everything — rounded buttons, rounded cards, rounded icons. Soft drop shadows. Maybe one mascot.

**Mapped presets.** `S-023-vibrant-friendly`, `S-024-candy`, `S-025-playful-toy`, `S-026-soft-pastel`.

**Use when.** Consumer DTC, education for kids/teens, fintech-for-Gen-Z, casual gaming, hobby apps.

**Don't use when.** B2B procurement, enterprise compliance, legal services — reads as unprofessional.

### 7. editorial-magazine

**Reads as.** A long-form magazine in browser form. Strong typographic hierarchy. Story-first. Beautifully ranged photography.

**Type.** Serif + sans pairing with intentional contrast — serif for body / display, sans for captions / metadata. Or all-serif heritage.

**Color.** Restrained — black + white + ONE editorial accent (deep red, navy, forest, ochre).

**Texture / decoration.** Editorial conventions — drop caps, pull quotes, byline metadata, photo captions in italic.

**Mapped presets.** `S-014-editorial-serif`, `S-037-cream-editorial`, `S-043-japanese-dark-editorial`, `S-044-dashboard-magazine`.

**Use when.** Long-form content (publications, agencies, portfolios, journalism, research org sites). Brands selling expertise via narrative.

**Don't use when.** The page must convert in one screen — magazine layout asks the reader to settle in.

### 8. brutalist-raw

**Reads as.** Unstyled-on-purpose. System fonts. Default form controls. Aggressive grid violations. "Web 1.0 with intent".

**Type.** System fonts only (Times, Arial, Courier, Monaco) — or one extremely loud display face deliberately fighting the system font.

**Color.** Default browser colors as a design choice (`#0000EE` link blue, `#FF0000` for emphasis). Or pure two-tone (black + one shocking color).

**Texture / decoration.** Visible page rulers, debug-mode borders, monospaced metadata, file-extension-style labels.

**Mapped presets.** `S-002-brutalism`, `S-003-neo-brutalism`, `S-013-industrial`, `S-033-win98`.

**Use when.** Design-aware audiences who appreciate the joke (creative agencies, art spaces, certain dev-tools brands). The brand wants to signal "we don't care about the rules".

**Don't use when.** The audience doesn't recognise the reference — to them it reads as broken.

### 9. art-deco-geometric

**Reads as.** Symmetry, gold, polished surfaces, 1920s prosperity, the Chrysler Building.

**Type.** Geometric sans with strong vertical emphasis. Display in faux-engraved metallic. Often custom letterforms.

**Color.** Black + ivory + metallic (gold, bronze, copper). Deep jewel-tone accents — emerald, sapphire, ruby.

**Texture / decoration.** Sunburst patterns, stepped geometry, zigzag borders, gold-leaf gradients. Symmetric compositions.

**Mapped presets.** `S-028-art-deco`, `S-041-bauhaus`.

**Use when.** Hospitality (steakhouses, hotel bars), spirits brands, theatre, premium tobacco-alternative, vintage-revival lifestyle.

**Don't use when.** Modern tech — the aesthetic reads as a costume.

### 10. soft-pastel

**Reads as.** Calm, considered, almost cosmetic. Surfaces feel powdered. Cosmetics, wellness, gentle finance.

**Type.** Light-weight sans with generous leading. Sometimes paired with a thin serif for headings.

**Color.** Desaturated pastels — dusty rose, sage, lavender, butter, sky. Backgrounds tinted near-white.

**Texture / decoration.** Soft blurs, gradients between adjacent pastels, very soft drop shadows.

**Mapped presets.** `S-026-soft-pastel`, `S-007-claymorphism`, `S-034-liquid-glass`.

**Use when.** Wellness apps, women's health, cosmetics e-commerce, meditation / sleep apps. The brand signals "we are here to be gentle with you".

**Don't use when.** Brand voice is direct, urgent, or technical — pastels undercut authority.

### 11. industrial-utilitarian

**Reads as.** Machine UI. Function over decoration. Monospace prevalent. Data-dense. Built for operators, not browsers.

**Type.** Monospace for data + UI labels. Geometric sans for headings. Tabular figures throughout.

**Color.** Workshop palette — steel grey, safety yellow, oxide red, deep navy. Dark mode often default.

**Texture / decoration.** Engineering dimension lines, drafting-style annotations, dotted construction grids. Borders are 1px solid.

**Mapped presets.** `S-013-industrial`, `S-017-corporate-bold`, `S-029-data-viz-dark`, `S-038-dark-tech`.

**Use when.** Devtools, observability platforms, industrial SaaS, professional creative tools (3D, video, audio), trading platforms.

**Don't use when.** The audience is consumer — the aesthetic reads as forbidding.

## How archetype routes to a graphic preset

The Phase A loop typically goes:

1. **Orchestrator asks** "What feeling are we going for?" — offers the 11 archetype names.
2. **User picks one** — or picks two and asks for a fusion.
3. **Orchestrator pulls the mapped presets** from this file's "Mapped presets" rows.
4. **Orchestrator runs `amw-ascii-sketch` to generate variants** — each variant uses a DIFFERENT preset from the chosen archetype's cluster.
5. **User picks one variant** — that variant's preset becomes the frozen design system for Phase B.

Example: user says "luxury-refined". Cluster is `S-015`, `S-016`, `S-018`. Three ASCII variants generate — one per preset. User picks variant 2 (the S-016 luxury-dark-warm variant). Phase B builds against S-016 tokens.

Cross-archetype fusions are allowed but flagged as RISK in DESIGN.md. Example: "luxury-refined + retro-futuristic" → a futuristic luxury watch brand. The orchestrator picks ONE preset from each cluster and asks the user to commit to which is the dominant. Without commitment to dominance, fusions read as confused.

## Distinguishing visual archetype from copy archetype

The user often mixes the two:

- "I want it to feel luxury" — this is a VISUAL archetype request (this file).
- "I want the copy to feel luxury" — this is a COPY archetype request (`TECH-voice-tone-archetypes.md`, the Quiet + Reverent row).

The orchestrator clarifies which axis the user means. The two archetypes do not have to align — a luxury-refined visual design can be paired with a Direct + Functional copy archetype (the look is restrained; the words are operational). What's NOT allowed is a maximalist-chaos visual paired with a Quiet + Reverent copy — they would actively undermine each other.

When the user is silent on which axis, the orchestrator infers:
- "feel" / "look" / "vibe" / "aesthetic" → VISUAL (this file).
- "voice" / "tone" / "writing" / "copy" / "words" → COPY (`TECH-voice-tone-archetypes.md`).
- "personality" / "brand" → BOTH; ask one clarifying question.

## Cross-references

- [TECH-voice-tone-archetypes.md](./TECH-voice-tone-archetypes.md) — the 7 COPY archetypes for words (distinct from this file's 11 VISUAL archetypes)
- [TECH-brand-voltage.md](./TECH-brand-voltage.md) — scarcity rule applied AFTER an archetype is chosen (maximalist-chaos explicitly opts out)
- [TECH-brand-color-by-product.md](./TECH-brand-color-by-product.md) — product-type-to-hue table that constrains palette choices within the chosen archetype
- [TECH-variant-hard-constraints.md](./TECH-variant-hard-constraints.md) — uses these archetype clusters to generate the mandatory 3 variants
- [skills/amw-design-system-presets/references/catalogue.md](../../amw-design-system-presets/references/catalogue.md) — the 45 enumerated graphic presets that anchor these archetypes
- [skills/amw-ascii-sketch/SKILL.md](../../amw-ascii-sketch/SKILL.md) — variant generator that consumes an archetype + 3 presets
- [agents/amw-brand-researcher-agent.md](../../../agents/amw-brand-researcher-agent.md) — when extracting from a reference URL, the researcher tags it with one of these 11 archetype names
- [agents/ai-maestro-webdesign-main-agent.md](../../../agents/ai-maestro-webdesign-main-agent.md) — Phase A orchestrator that uses this vocabulary in the discovery conversation
- [skills/amw-design-principles/SKILL.md](../SKILL.md) — orchestrator
