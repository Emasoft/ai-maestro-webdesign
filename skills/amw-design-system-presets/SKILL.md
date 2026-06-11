---
name: amw-design-system-presets
description: >-
  Catalog of ~45 named graphic-style presets (Swiss, Brutalist,
  Glassmorphism, Material 3, Aurora, Cyberpunk, etc.), each shipped as a
  complete token block plus breaks-if invariants and a canonical render-test
  pointer. Activates on narrow style-name triggers — "use Brutalist style",
  "apply Glassmorphism preset", "Aurora style tokens", "Swiss minimal
  layout", "Material 3 tokens", or "show available style presets". Does NOT
  activate on broad design vocabulary ("design a page", "build a UI") — those
  route to amw-design-principles. Read references/catalogue.md first to
  shortlist matching styles.
version: 0.1.0
author: ai-maestro-webdesign (curated catalogue; per-style attributions live in each S-NNN file)
---

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are explicit style-name or "style preset" triggers only — `amw-design-principles` routes here when the user picks a named aesthetic. Provides ~45 ready-to-use token blocks plus the contracts each style enforces.

## Overview

`amw-design-system-presets` is the style-preset catalogue for the ai-maestro-webdesign plugin. It ships 84 named graphic-style presets organized across 8 aesthetic positions: each preset is a complete, self-contained token bundle (colors, typography, spacing, radius, shadow, motion) plus a set of "breaks-if" invariants and a canonical render-test pointer.

**Catalog-first load protocol.** This skill is NOT a bulk-loader. The full catalogue has 84 styles across multiple reference files; loading all of them simultaneously would waste tokens and produce a cluttered decision surface. The canonical protocol is:

1. Read [catalogue](references/catalogue.md) to shortlist 1-3 styles matching the user's brief.
2. Load ONLY those S-NNN files.
3. Apply the token block to the artifact.
4. Verify all "breaks-if" invariants before delivery.

Each `S-NNN-<slug>.md` file is a self-contained contract: it defines every token the style requires, lists every invariant that must not be violated, and points to a canonical render-test. No style relies on another style's tokens.

**Full catalogue scope.** This skill ships S-001..S-083 (84 styles total across Waves 1–3).

## How the catalog is used

The 4-step recipe:

**(a) Read the user brief.** Identify: industry, audience, tone, any explicit style name, any reference URLs the user provided. Note keywords: "minimal", "brutalist", "glassmorphism", "editorial", "cyberpunk", "warm", "playful", "corporate", etc.

**(b) Shortlist 1-3 styles from [catalogue](references/catalogue.md).** The catalogue has one-line aesthetic-position descriptors for all 84 styles plus a "quick decision rules" section. Use it. Do NOT rely on recall — always read the catalogue file to shortlist. If the user named a specific style explicitly (e.g., "I want Glassmorphism"), load that style directly; still read the catalogue to confirm the S-NNN file path.

**(c) Load only those S-NNN files.** Each is in `references/S-NNN-<slug>.md`. Read the `## Token block` section and the `## "Breaks if" invariants` section.

**(d) Apply the token block and verify invariants.** Inject the CSS custom properties from the token block into the artifact HTML. Before delivery, scan the artifact against every invariant in the loaded style(s). Invariants are hard rules — they cannot be softened by the user's aesthetic preference unless the user is explicitly replacing the preset with a custom design. If the user supplies brand tokens that conflict with preset tokens, brand tokens win (see Non-negotiables §5).

## Catalog (canonical index)

The routing index with all 45 style descriptors lives at:

- [catalogue](references/catalogue.md)
> [catalogue.md] How the author-agent uses this · Index — 45 styles across 8 aesthetic positions · Selecting styles — quick decision rules · Wave 2 — Round 4 additions (S-010b, S-046..S-083)

The SKILL.md does NOT duplicate per-style descriptors here. The catalogue is the authoritative routing surface; this file describes the machinery.

## Per-style file shape

Every `references/S-NNN-<slug>.md` file created by Track H1..H9 swarm agents MUST follow this exact contract (deviation blocks delivery):

### Required frontmatter
```yaml
---
id: S-NNN
name: <style name>
aesthetic_position: <2-4 word positioning phrase>
source_attribution: <upstream repo / skill / article URL>
license: <MIT | Apache-2.0 | CC-BY-4.0 | original summary>
---
```

### Required body sections (in order)

**`## Identity`** — 2-3 sentences describing the style's aesthetic roots, visual fingerprint, and intended audience. Concrete nouns only — no vague adjectives ("elegant", "modern") without a structural anchor.

**`## Token block`** — The complete token bundle as CSS custom properties AND a Tailwind theme extension. Must cover all of:
- `--color-*` (bg, surface, text, text-muted, primary, accent, border; all as hex or CSS-valid values)
- `--font-display`, `--font-body`, `--font-mono` (with full fallback stack)
- `--spacing` (base unit in px)
- `--radius` (card/button radius; may be 0)
- `--shadow` (full box-shadow value; may be "none")
- `--motion-duration`, `--motion-easing` (transition values)
- Optional: `--border-width`, `--gradient-*`, `--glow-*` when the style requires them

The Tailwind extension block follows the CSS block in the same section as a fenced TypeScript/JS object.

**`## "Breaks if" invariants`** — Explicit bulleted list of changes that violate the style. Each invariant is a single falsifiable statement prefixed with "breaks if". Examples:
- "breaks if `border-radius` exceeds 4px"
- "breaks if a second chromatic color is introduced alongside the accent"
- "breaks if body font is not monospace"

**`## Canonical render-test pointer`** — Single line naming the render-test HTML path (generated from `references/_test-skeleton.html` + this file's tokens) and the upstream source URL or local HTML used for fcvvdp parity comparison.

**`## Render-test verdict`** — JOD score from the Wave 0 parity harness (populated after Track H-verify runs). Format: `JOD: X.X (PASS | FAIL) — <date>`. Placeholder before verify: `JOD: pending`.

**`## Cross-references`** — sibling styles + source attribution URL(s).

## Test skeleton

`references/_test-skeleton.html` is the canonical render-test scaffold used by every per-style render-test. It implements 8 standard UI primitives:

1. Header with logo + nav
2. Hero with headline, sub, and primary CTA
3. 3-card feature row
4. Quote / testimonial block
5. Pricing table (3 tiers)
6. Form (email + submit)
7. Footer with mini-nav + copyright
8. Modal / dialog (off-canvas variation)

The skeleton uses ONLY CSS custom-property references (`var(--token-name)`) — no hard-coded colors, font names, radii, or shadows anywhere in the CSS. Per-style render-tests inject the style's token block by substituting the `{{TOKEN}}` markers at the top of the file, producing a fully-styled HTML page from a single token swap.

Light/dark variants: inject dark vs light token bundles into the same skeleton. Mobile variant: the skeleton is responsive; render at 375×812 when the style ships mobile-specific invariants.

See [_harness-wiring](references/_harness-wiring.md) for the full pipeline (token injection → render mine → render source → fcvvdp parity check).

## Catalogue scope (S-001..S-083)

This skill ships 84 prescriptive styles across 8 aesthetic positions (Wave 1: S-001..S-045; Waves 2–3: S-046..S-083):

| Position | IDs |
|---|---|
| Classical / Modernist | S-001 Swiss, S-002 Brutalism, S-003 Neo-Brutalism, S-028 Art Deco, S-041 Bauhaus, S-042 Memphis |
| Material / Corporate | S-008 Material 3, S-017 Corporate Bold, S-021 Pnalism, S-022 Minimal Pure |
| Glass / Soft / Skeuomorphic | S-004 Glassmorphism, S-005 Neumorphism, S-006 Skeuomorphism, S-007 Claymorphism, S-034 Liquid Glass |
| Dark / Cinematic / Cyber | S-009 Aurora, S-010 Cyberpunk, S-010b Neon, S-011 Synthwave, S-012 Retro Terminal, S-036 Cinematic Dark |
| Editorial / Warm / Paper | S-013 Industrial, S-014 Editorial Serif, S-015 Fashion Luxury, S-016 Luxury Dark, S-018 Understated Elegance, S-019 Heritage, S-020 Organic, S-030 Lo-Fi Paper, S-031 Paper Collage, S-037 Cream Editorial, S-039 Warm Professional, S-040 Chinese Elegant, S-043 Japanese Dark, S-044 Dashboard Magazine, S-045 Warm Minimalism |
| Playful / Consumer / Bold | S-023 Vibrant Friendly, S-024 Candy, S-025 Playful Toy-Like, S-026 Soft Pastel, S-027 Maximalism |
| Developer / Terminal | S-032 Retro Device, S-033 Win98, S-038 Dark Tech |
| Specialized | S-029 Data Viz Dark, S-035 21st.dev/Aceternity |

S-046..S-083 are ported and available. See [catalogue](references/catalogue.md) for the full listing.

## Resources

- [catalogue](references/catalogue.md) — canonical routing index (read this first, always)
> [catalogue.md] How the author-agent uses this · Index — 45 styles across 8 aesthetic positions · Selecting styles — quick decision rules · Wave 2 — Round 4 additions (S-010b, S-046..S-083)
- [`references/_test-skeleton.html`](references/_test-skeleton.html) — render-test scaffold (inject tokens here)
- [_harness-wiring](references/_harness-wiring.md) — parity-check pipeline documentation
> [_harness-wiring.md] The pipeline (per style) · Light + dark variants · Mobile variant · Acceptance thresholds · A-class exemptions · Report locations · What this is NOT · Cross-references
- Per-style files: `references/S-NNN-<slug>.md` (Track H1..H9 swarm creates these)

## Non-negotiables

1. **Catalog-first load.** Always read [catalogue](references/catalogue.md) before loading any S-NNN file. Never bulk-load all 84.
> [catalogue.md] How the author-agent uses this · Index — 45 styles across 8 aesthetic positions · Selecting styles — quick decision rules · Wave 2 — Round 4 additions (S-010b, S-046..S-083)
2. **Token block is the contract.** Apply the style's CSS custom properties verbatim. Do not partially apply a preset — all tokens or none.
3. **"Breaks-if" invariants are non-negotiable.** Violating a "breaks-if" rule produces a style that is no longer the named preset. If the user requests a change that would break an invariant, warn them: "this change would exit the [Swiss] preset; I can make it a custom variant, but it will no longer be labeled Swiss."
4. **Source attribution preserved.** Every S-NNN file carries its `source_attribution` in frontmatter. Do not strip it from delivered artifacts that directly port upstream token values.
5. **Brand tokens override preset tokens.** When the user supplies brand colors, fonts, or spacing, brand values take precedence over the preset's tokens in those specific properties. The preset provides the structural contract (radius, shadow, motion, layout density); brand tokens fill the identity slots (colors, typography).
6. **No new styles without a catalogue slot.** Every new style added to `references/` must have a corresponding row in [catalogue](references/catalogue.md). An S-NNN file without a catalogue entry is invisible to the routing protocol.
> [catalogue.md] How the author-agent uses this · Index — 45 styles across 8 aesthetic positions · Selecting styles — quick decision rules · Wave 2 — Round 4 additions (S-010b, S-046..S-083)
7. **_test-skeleton.html stays var()-only.** Never introduce hard-coded hex, rgb, hsl, or font names into the test skeleton. The entire point of the skeleton is that it renders purely from injected tokens.
