# Style Preset Catalog — Routing Index (T-004)

Loaded by `amw-design-system-presets` (the orchestrator's preset skill).
**Catalog-first load**: read this index, shortlist 1-3 styles that match
the user's brief, then load only those `S-NNN-<slug>.md` files. Never
bulk-load all 45.

The styles are organized into **8 aesthetic positions**. Each style is
a complete token block + "breaks-if" invariants + a canonical render-test
pointer; per-file attribution preserves the upstream source.

## How the author-agent uses this

1. Read the user's brief (industry, audience, tone, named-style references).
2. Scan the one-line descriptors below — pick 1-3 styles whose aesthetic
   positioning is closest, OR whose name the user explicitly invoked.
3. Load only those files; apply the token blocks to the artifact.
4. Verify the "breaks-if" invariants in each loaded style before delivery.

## Index — 45 styles across 8 aesthetic positions

### 1. Classical / Modernist (1900s-1960s aesthetic foundations)

| ID | Style | One-line position |
|---|---|---|
| S-001 | [Swiss / International](S-001-swiss.md) | Black-on-white, Helvetica/Akzidenz, 1 accent (red/blue/orange), strict grid, 0 radius, no shadow. The Mueller-Brockmann benchmark. |
| S-002 | [Brutalism (classic)](S-002-brutalism.md) | System fonts only, primary primaries, 2-3px black borders, `8px 8px 0 #000` hard shadow, 0 radius. Web-design-as-architecture. |
| S-003 | [Neo-Brutalism](S-003-neo-brutalism.md) | 1 scream color on white, Space Grotesk bold, `4px 4px 0 #000`, 0 radius. Brutalism with one carefully placed chromatic moment. |
| S-028 | [Art Deco / Geometric](S-028-art-deco.md) | Deep navy/black + gold + cream, Cinzel/Cormorant, symmetry/chevron, 0-2px radius, gold hairline, no shadow. |
| S-041 | [Bauhaus](S-041-bauhaus.md) | Primary red/blue/yellow on white/black, Cabinet Grotesk + Satoshi, grid-heavy, 0 radius, geometric shapes. |
| S-042 | [Memphis / Neo-Memphis](S-042-memphis.md) | Warm paper, bold multi-accent pink/blue/yellow/mint/coral/lilac, Bowlby One, 3px ink borders, blob shapes, offset shadow. |

### 2. Material-systems / Corporate (commercial 2010s+)

| ID | Style | One-line position |
|---|---|---|
| S-008 | [Material Design 3](S-008-material-3.md) | HCT tonal palette, state layers 8/10/16%, tonal elevation 5 levels, 7-step shape scale, 15 type styles, 4dp grid. The Google canonical system. |
| S-017 | [Corporate Bold / Enterprise Solid](S-017-corporate-bold.md) | Navy + purple accent, Roboto/Inter, 6px radius, subtle shadow, dense grids. Enterprise trust palette. |
| S-021 | [Pnalism / Two-Tone Minimal](S-021-pnalism.md) | White + 1 accent + black, exactly 2 chromatic values, 1px borders only, 8px radius, zero shadows. |
| S-022 | [Minimal Pure / Ultra-Minimal Precision](S-022-minimal-pure.md) | Pure black/white, one typeface weight-only, 80-120px display, 0 radius, no shadow. |

### 3. Glass / Soft / Skeuomorphic

| ID | Style | One-line position |
|---|---|---|
| S-004 | [Glassmorphism](S-004-glassmorphism.md) | Gradient scene bg mandatory, frosted panels 5-15% fill, backdrop-blur 4-40px, white 20-40% border, 16px radius. iOS-7 lineage. |
| S-005 | [Neumorphism / Soft UI](S-005-neumorphism.md) | Single desaturated bg 88-92% L, dual shadow convex/concave, 135deg light, 12-16px radius, no borders. WCAG-AA challenge. |
| S-006 | [Skeuomorphism](S-006-skeuomorphism.md) | Material textures leather/metal/wood, surface gradient light-from-above, multi-layer drop-shadow, inner highlight. |
| S-007 | [Claymorphism](S-007-claymorphism.md) | Pastel fills, inner top highlight + outer drop + inner bottom darken, 20-40px radius, Nunito/Poppins, bounce easing. |
| S-034 | [Liquid Glass (Apple visionOS)](S-034-liquid-glass.md) | Translucent over photo/video, tint 0.1-0.3, WebGL refraction, 32-48px radius, spatial z-depth elevation. |

### 4. Dark / Cinematic / Cyber

| ID | Style | One-line position |
|---|---|---|
| S-009 | [Aurora UI / Aurora Maximalism](S-009-aurora.md) | Near-black bg, violet-to-pink-to-blue gradient as brand, glow boxes (not drop-shadow), huge type, spring physics. |
| S-010 | [Cyberpunk / Dark Neo-Noir](S-010-cyberpunk.md) | #0a0a12, neon cyan/magenta/toxic-green, multi-layer neon glow, Orbitron/Rajdhani, all-caps, 0 radius, glitch/scanlines. |
| S-010b | [Neon / Glow UI](S-010b-neon.md) | Near-black, 2 neon colors, multi-layer `0 0 5/20/40px` glow, Space Grotesk, glow-intensity dim/standard/vivid. *(backlog — Wave 1 swarm covered S-001..S-045; S-010b deferred to Wave 2)* |
| S-011 | [Retro-Futuristic / Synthwave](S-011-retro-futuristic.md) | Deep space bg, VT323/Orbitron, CRT scanlines repeating-linear-gradient, magenta+cyan OR phosphor+amber, neon glow. |
| S-012 | [Retro Terminal / Green-on-Black](S-012-retro-terminal.md) | #00FF41 on #0D0208, Fira Code mono only, green glow, typing/cursor anim, 0 radius. |
| S-036 | [Cinematic Dark / Immersive](S-036-cinematic-dark.md) | Near-black #06060A, film color-grade, large serif titles, fullscreen hero, sticky-scroll parallax, 700-1000ms transitions. |

### 5. Editorial / Warm / Paper

| ID | Style | One-line position |
|---|---|---|
| S-013 | [Industrial / Utilitarian](S-013-industrial.md) | Black-on-black + 1 signal color green/amber, IBM-Plex/JetBrains mono only, extreme density, 0 radius, no shadow. |
| S-014 | [Editorial Serif / Content-First](S-014-editorial-serif.md) | #111 on #F9F9F7, Playfair+Lora/Georgia, 18px/1.8 body, 720px column, deep-red accent, 0 radius, no shadow, rule dividers. |
| S-015 | [Fashion / Luxury Editorial](S-015-fashion-luxury-editorial.md) | Near-white/black, Didot/Bodoni/Cormorant 80-120px, gold accent, museum-frame gallery, 750ms transitions, no borders/radius/shadow. |
| S-016 | [Luxury Dark Warm](S-016-luxury-dark-warm.md) | Gold #D4AF37 on #12100E, Cinzel+Montserrat, 2px radius, deep shadow, beige text. |
| S-018 | [Understated Elegance / Warm Premium](S-018-understated-elegance.md) | Sage + terracotta on warm cream, Cormorant+Lato, 8px radius, ultra-soft shadow. |
| S-019 | [Heritage / Warm Editorial](S-019-heritage-warm-editorial.md) | Cream/sand/tan, Playfair+Dancing-Script, terracotta accent, organic oval masks, 0-4px radius. |
| S-020 | [Organic / Earthy / Blob](S-020-organic-earthy.md) | Sage/clay/terracotta/ochre/moss, Fraunces/Epilogue, 16-32px radius, blob border-radius, grain 1-3%, warm shadow. |
| S-030 | [Lo-Fi / Paper / Zine](S-030-lo-fi-paper.md) | Paper-yellow #E8E0C0, mixed system fonts, 2-8deg rotation, halftone/Riso misregistration, hard ink borders, no smooth motion. |
| S-031 | [Paper Collage / Handcraft](S-031-paper-collage.md) | Cream paper stock, hand-lettered, torn edges SVG/clip-path, polaroid/tape, scrapbook density, physical-feel motion. |
| S-037 | [Cream Editorial](S-037-cream-editorial.md) | #FAF8F4, Cormorant Garamond, 0px radius, serif-everywhere. |
| S-039 | [Warm Professional](S-039-warm-professional.md) | #F9F5F0, Source Serif 4 + Source Sans 3, moderate radius, business-trust. |
| S-040 | [Chinese Elegant](S-040-chinese-elegant.md) | #FAF9F4 warm paper, LXGW WenKai, 1.8 line-height, 2em first-paragraph indent, 4px radius. |
| S-043 | [Japanese Dark Editorial (Zutomayo)](S-043-japanese-dark-editorial.md) | Void #0e0d12, aged cream, acid-yellow/pink/cyan accents, Shippori Mincho + Cormorant italic + Yomogi, extreme whitespace, paper grain. |
| S-044 | [Dashboard Magazine / FT-style](S-044-dashboard-magazine.md) | Warm cream #fef3e6, Newsreader + IBM Plex Sans/Mono, 3-col broadsheet, masthead, claret/gold/green, paper grain, no shadow. |
| S-045 | [Warm Minimalism (Notion)](S-045-warm-minimalism.md) | Off-white/cream, serif headings, soft grey hierarchy, muted accent, 4-6px radius, very light shadow, single-column. |

### 6. Playful / Consumer / Bold

| ID | Style | One-line position |
|---|---|---|
| S-023 | [Vibrant Friendly / Playful SaaS](S-023-vibrant-friendly.md) | Brand blue/purple + multi-color, DM-Sans/Nunito, 8-16px radius, soft colored shadow, card grids. |
| S-024 | [Candy / Playful Consumer App](S-024-candy.md) | Hot pink/candy purple/lime, Poppins/Nunito, 16-24px or pill radius, colored shadow, confetti/scratch, bouncy spring. |
| S-025 | [Playful / Toy-Like](S-025-playful-toy.md) | High-chroma primaries, Nunito/Poppins heavy, 16-24px radius, colorful shadows, bounce/confetti. |
| S-026 | [Soft / Pastel](S-026-soft-pastel.md) | Desaturated pastels 30-50% sat, Nunito/rounded, 20-32px radius, soft shadow `0 8px 24px rgba(0,0,0,.06)`. |
| S-027 | [Maximalism / Chaotic Maximalism](S-027-maximalism.md) | 5+ clashing colors, multiple typefaces, extreme density/overlap, mixed radius; coherence-is-the-enemy. |

### 7. Developer / Terminal / Monospace

| ID | Style | One-line position |
|---|---|---|
| S-032 | [Retro Device / Physical UI](S-032-retro-device.md) | Beige plastic #C0BBAA, LCD screen, dot-matrix/VT323, bevelled border:outset, physical button depth, CRT flicker. |
| S-033 | [Win98 / Retro OS](S-033-win98.md) | Win98 grey #C0C0C0, navy title bars, inset/outset bevel box-shadow, hard 2px borders, panel/window metaphor. |
| S-038 | [Dark Tech](S-038-dark-tech.md) | #0A0A0A, Space Grotesk + JetBrains Mono, 2px radius, terminal-without-retro. |

### 8. AI / Future / Generative

| ID | Style | One-line position |
|---|---|---|
| S-029 | [Data Visualization Dark](S-029-data-viz-dark.md) | #1a1a2e, desaturated distinct series colors 20-30% below sat, tabular-nums mono, dotted gridlines, no chart shadow. |
| S-035 | [21st.dev / Aceternity Premium Dark Landing](S-035-21st-aceternity.md) | bg-zinc-950 NOT black, 1-2 color washes, 1 vivid accent, gradient borders white/10, bento grid, shimmer/marquee, depth via glow. |

## Selecting styles — quick decision rules

- **Brief: "minimalist / Swiss / grid-strict / institutional"** — start with S-001 Swiss.
- **Brief: "brutalist / raw / system fonts / hard shadows"** — start with S-002 classic Brutalism or S-003 Neo-Brutalism.
- **Brief: "glass / frosted / iOS / depth"** — start with S-004 Glassmorphism; S-034 Liquid Glass for the visionOS variant.
- **Brief: "neumorphism / soft / pillowy"** — start with S-005, BUT WARN about WCAG-AA contrast risk.
- **Brief: "Material / Google / tonal palette"** — S-008 Material 3.
- **Brief: "aurora / gradient / glow / dark+vibrant"** — S-009 Aurora.
- **Brief: "cyberpunk / neon / synthwave / glitch"** — S-010 Cyberpunk or S-011 Synthwave.
- **Brief: "terminal / green-on-black / monospace"** — S-012 Retro Terminal.
- **Brief: "editorial / serif / quarterly / magazine"** — S-014 Editorial Serif or S-044 Dashboard Magazine.
- **Brief: "luxury / fashion / high-end / gold"** — S-015 Fashion Luxury or S-016 Luxury Dark Warm.
- **Brief: "warm / earthy / organic / brand-friendly"** — S-018 Understated Elegance, S-019 Heritage, S-020 Organic.
- **Brief: "corporate / enterprise / B2B"** — S-017 Corporate Bold or S-008 Material 3.
- **Brief: "playful / consumer app / bouncy"** — S-023 Vibrant Friendly, S-024 Candy, S-025 Playful Toy-Like.
- **Brief: "art deco / geometric / gold + navy"** — S-028 Art Deco.
- **Brief: "developer / IDE / monospace / dark tech"** — S-038 Dark Tech or S-012 Retro Terminal.
- **Brief: "data dashboard / visualization / dark"** — S-029 Data Viz Dark.
- **Brief: "21st.dev / aceternity / bento / shimmer"** — S-035.
- **Brief: "retro / Win98 / classic OS"** — S-033 Win98 or S-032 Retro Device.
- **Brief: "Japanese / editorial Japan / Zutomayo"** — S-043.
- **Brief: "cinematic / immersive / film"** — S-036 Cinematic Dark.

Never load more than three styles at once. If the brief points to none of
the above, load none and synthesize from scratch using design-decision-rules
and writing-voice instead — borrowed structure is not a substitute for
original brand reasoning.

---

*Catalog authored 2026-05-26 for the ai-maestro-webdesign plugin. The
per-style files (S-NNN-<slug>.md) are direct-ports from the batch9
extraction with per-file MIT/Apache attribution. Catalog descriptors
are original summaries written for routing purposes. The first 45
styles (S-001..S-045) ship in Wave 1; the remaining S-046..S-083 are
Wave 2-3 backlog.*
