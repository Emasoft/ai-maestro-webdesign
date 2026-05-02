---
name: TECH-uiux-lp-patterns-catalog
category: uiux-lp-pattern
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Landing-page patterns catalog (24 conversion-optimized structures)

## What it does

Ships 24 named landing-page patterns — end-to-end section sequences optimized for specific conversion intents. Each pattern specifies:

- **Section order** — which sections in what sequence (hero → problem → solution → proof → CTA etc.)
- **CTA placement cadence** — how many CTAs, where they repeat
- **Social-proof slots** — where logos, testimonials, metrics live
- **Hero archetype** — copy-only, copy + product screenshot, copy + video, animated demo
- **Conversion bias** — lead capture, signup, purchase, demo request, newsletter

## When to use

Fallback flow (`ui-ux-reasoning`) when the user has no reference and needs a plausible landing-page structure proposed. The 24 patterns are the structural counterpart to the 67 styles — once you pick a pattern, the style, palette, and fonts layer on top.

Skip on specialized page types (pricing, changelog, blog index) — the 24 patterns are LP-specific.

## How it works

Each pattern is addressable by name. Representative patterns (sample from 24):

| Pattern | Section order | Conversion bias | Anchor industry |
|---|---|---|---|
| Classic SaaS | Hero / Logos / Problem / Solution / Features / Pricing / FAQ / CTA footer | Signup + demo | SaaS, productivity |
| Data-First Dashboard | Hero / Live-data demo / Integration grid / Pricing / Case studies / Docs links | Demo request | Analytics, B2B |
| Progressive Disclosure | Hero / Expandable problem sections / Inline solution demos / Single CTA | Signup | Dev tools, AI products |
| Editorial Long-form | Magazine hero / Chapter nav / Story sections / Newsletter capture | Newsletter | Publications, personal brands |
| Proof-Heavy | Hero / 6-logo band / 3-metric band / Testimonial carousel / Case-study grid / CTA | Enterprise signup | Enterprise B2B |
| Product Demo First | Hero with 30-sec video / Feature grid / Pricing / FAQ / CTA | Signup | Consumer apps |
| Quick Buy | Hero with product + CTA / Feature bullets / Reviews / Related products / Checkout | Purchase | DTC ecom |
| Luxury Editorial | Full-bleed hero / Collections grid / Brand story / Newsletter | Newsletter + browse | Luxury ecom |
| Lead Magnet | Hero with value prop / 3-benefit grid / Email capture form / Social proof | Email capture | Infoproducts, courses |
| Event Landing | Hero with date/CTA / Agenda / Speakers / Registration form | Registration | Events, conferences |
| App Store Landing | Mobile mockup hero / Feature carousel / Download CTAs / App-store badges | Download | Mobile apps |
| Dev-tool Hero | Code block hero / Install command / Feature grid / Docs / GitHub | GitHub star + signup | Developer tools |

Full inventory: 24 patterns spanning SaaS, ecom, content, events, tools.

## Minimal example

```python
ds = gen.generate(description="B2B SaaS analytics for enterprise teams", stack="react")
print(ds.pattern)
# "Data-First Dashboard"
# Sections in order:
# 1. Hero (headline + sub + primary CTA + product screenshot)
# 2. Live-data demo (animated dashboard)
# 3. Integration grid (logos of supported sources)
# 4. Pricing (3-tier)
# 5. Case studies (3 named brands)
# 6. Docs + CTA footer
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- The patterns are opinionated but not universal — a luxury ecom brand using the "Classic SaaS" pattern will look generic. Cross-check pattern choice against the reasoning rule for the industry.
- Section order is a starting point, not an invariant. Progressive reveal, above-the-fold CTAs, and sticky headers are composable modifications.
- Patterns do NOT dictate copy, imagery, or illustration style — those layer on top via the style + palette + font-pairing catalogs.

## Cross-references

- [TECH-uiux-rules-catalog](TECH-uiux-rules-catalog.md) — 161 rules that reference these patterns
- [TECH-uiux-styles-catalog](TECH-uiux-styles-catalog.md), [TECH-uiux-palettes-catalog](TECH-uiux-palettes-catalog.md), [TECH-uiux-font-pairings-catalog](TECH-uiux-font-pairings-catalog.md)
- `../../amw-design-principles/starter-components/` — HTML starters that can be remixed into these patterns
- `../SKILL.md`
