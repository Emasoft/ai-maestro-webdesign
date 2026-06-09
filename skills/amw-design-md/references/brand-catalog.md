# Brand Library — Catalog (T-040)

Loaded by `amw-design-md` (the orchestrator's DESIGN.md skill) and consumed
by `amw-design-md-author-agent` during Phase A. **Catalog-first load**: read
this index, shortlist 1–3 brand files that match the user's brief, then load
only those into the author-agent's context. Never bulk-load all 14.

The exemplars are direct-ported (verbatim, with attribution) from
[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
(MIT, 2026). They are **authoring references**, not the user's project file.

## How the author-agent uses this

1. Read the user's brief (industry, audience, tone, references).
2. Scan the one-line descriptors below — pick 1–3 brands whose aesthetic
   positioning is closest, OR pick 1–3 brands that the user explicitly named.
3. Load only those files; treat them as calibration material for the
   blind-component test and palette-swap test (see `writing-voice.md` §X).
4. Cite the brand exemplar(s) consulted in the DESIGN.md's Known-Gaps or
   commit message — never claim originality on copied structure.

## Index — 14 exemplars across 5 aesthetic positions

### Premium SaaS / fintech canon

| Brand | File | One-line position |
|---|---|---|
| Stripe | [`brand-stripe.md`](brand-stripe.md) | The premium-fintech reference: blue/violet brand color with deep grayscale neutrals, dense data layout, restrained motion, near-platonic geometric clarity. Benchmark for "trustworthy commercial SaaS". |
| Linear | [`brand-linear.md`](brand-linear.md) | Devtool minimalism: near-black UI with a single chromatic accent, IBM Plex pairings, tight grid, performance-as-aesthetic. The canonical "Linear style" reference for productivity tools. |
| Notion | [`brand-notion.md`](brand-notion.md) | Warm-minimal content-first: off-white surfaces, serif headings against geometric sans body, generous whitespace, soft greys, single-column reading width — restraint over decoration. |
| Vercel | [`brand-vercel.md`](brand-vercel.md) | Geist-driven near-neutral dark-first surface with a single emerald-like signal. Documentation as artifact: high typographic hierarchy, low chroma elsewhere. |

### Editorial / warm

| Brand | File | One-line position |
|---|---|---|
| Mintlify | [`brand-mintlify.md`](brand-mintlify.md) | Warm editorial for technical docs: cream/sand surfaces, soft accents, serif accents on a sans body, documentation that reads like a quarterly journal. |
| Resend | [`brand-resend.md`](brand-resend.md) | Warm minimal SaaS: paper-toned surface, restrained black-on-cream, hairline rules, transactional but not cold. |

### Dark devtool / terminal-adjacent

| Brand | File | One-line position |
|---|---|---|
| Cursor | [`brand-cursor.md`](brand-cursor.md) | Dark IDE-native: deep-blue/black canvas, monospaced accent type, code-block-first information density, electric accent color. |
| Raycast | [`brand-raycast.md`](brand-raycast.md) | macOS-native dark: vibrant brand reds against deep grays, native-feeling controls, command-palette emphasis, animations tied to gesture. |
| Warp | [`brand-warp.md`](brand-warp.md) | Terminal modernized: phosphor-derived accents on warm-dark backgrounds, monospaced display type, depth via gradient rather than borders. |

### Bold / mission-driven / consumer

| Brand | File | One-line position |
|---|---|---|
| SpaceX | [`brand-spacex.md`](brand-spacex.md) | Engineering-grand: oversized display type on near-black, hairline data labels, mission-payload information density, zero ornament. |
| Webflow | [`brand-webflow.md`](brand-webflow.md) | Colorful prosumer creative: brand blue against warm whites, accessible component palette, motion-as-feedback, designer-facing voice. |

### AI products

| Brand | File | One-line position |
|---|---|---|
| Claude (Anthropic) | [`brand-claude.md`](brand-claude.md) | Quiet luminous: warm cream surfaces, terracotta accents, conversational restraint, serif/sans pairings tuned for long reading. |
| ElevenLabs | [`brand-elevenlabs.md`](brand-elevenlabs.md) | Voice-first consumer AI: dark canvas with vivid accent, generous display sizes for "your voice on the page", interactive demos foregrounded. |
| Mistral | [`brand-mistral.md`](brand-mistral.md) | French-AI editorial: tricolor-informed accents on white, geometric sans, paper-feeling whitespace, restraint over neon. |

## Selecting exemplars — quick decision rules

- **User brief contains "fintech / banking / commerce / trust"** → start with Stripe.
- **User brief contains "devtool / productivity / SaaS / B2B"** → start with Linear or Vercel.
- **User brief contains "content / reading / docs / publication"** → start with Notion or Mintlify.
- **User brief contains "editor / IDE / terminal / dark"** → start with Cursor, Raycast, or Warp.
- **User brief contains "mission / aerospace / hardware / engineering-grand"** → start with SpaceX.
- **User brief contains "AI / LLM / model / agent"** → start with Claude, ElevenLabs, or Mistral.
- **User brief contains "consumer / playful / creator"** → start with Webflow.
- **User brief contains "warm / editorial / quarterly / paper"** → start with Mintlify or Resend.

Never load more than three at once. If the brief points to none of the
above, load none and synthesize from scratch using `design-decision-rules.md`
and `writing-voice.md` instead — borrowed structure is not a substitute for
original brand reasoning.

---

*Index authored 2026-05-26 for the ai-maestro-webdesign plugin. Brand exemplars
are direct-ported from [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
under the MIT license; attribution appears in each individual brand file's
header and footer. Catalog descriptors are original summaries written for
routing purposes.*
