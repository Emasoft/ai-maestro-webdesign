---
name: TECH-uiux-rules-catalog
category: uiux-rule
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Top 10 distinctive rules — broken out as individual TECH files](#top-10-distinctive-rules-broken-out-as-individual-tech-files)
- [Cross-references](#cross-references)

# TECH: Reasoning-rules catalog (161 rules)

## What it does

The ui-ux-pro-max skill ships **161 industry-specific reasoning rules**. Each rule names an industry / product type (e.g. *Fintech/Crypto*, *Healthcare/Medical*, *SaaS Dashboard*, *Luxury E-commerce*) and encodes four decisions the fallback library makes for that category:

- **Pattern** — recommended landing-page or dashboard structure (which sections, CTA placement, social-proof cadence).
- **Style priority** — ordered list of UI styles (pulled from the 67-style catalog) best suited to the industry.
- **Color mood** — palette keywords (trust / clinical / playful / luxury / energetic / calm).
- **Anti-patterns** — patterns that erode trust or clarity for that industry.

## When to use

- The fallback path activates (`ui-ux-reasoning` trigger conditions met — "no design system, pick for me") and the orchestrator needs three style + palette candidates.
- The user names an industry the agent wants to sanity-check against the catalog's anti-pattern list before emitting recommendations.
- A downstream skill (e.g. `seo/`, `ux-evaluator/`) wants the industry's anti-patterns as a filter rule.

Skip when a concrete design reference exists — the reasoning rules are for the no-anchor fallback path, not the happy path.

## How it works

Each rule is addressable by a category + pattern key. The library returns the rule's `pattern`, `style_priority`, `color_mood`, and `anti_patterns` fields. Queries use BM25 relevance against the user's description (e.g. `"fintech payment app"` matches the Fintech rule closest).

Representative industries covered (sample):

| Industry | Pattern anchor | Style priority | Anti-patterns |
|---|---|---|---|
| Fintech / Crypto | Data-first, compliance footer | Professional Minimalism, Data-Dense | Playful fonts, neon colors, AI purple gradients, gamified money flows |
| Healthcare | Trust-first, credentials above fold | Clean Minimalism, Soft UI | Red primary buttons (emergency connotation), dark mode on medical data |
| Luxury e-commerce | Editorial, generous whitespace | Minimalism, Editorial | Cluttered grids, rainbow promos, emoji as primary icons |
| SaaS Dashboard | Progressive disclosure, Bento sections | Glassmorphism, Bento Grid, AI-Native UI | Rainbow gradients, stock photos, clip art |
| Food & Restaurant | Photography-forward, warm surface | Warm Minimalism | Cold blues, low-contrast text over food photos |

Full inventory: 161 rules across Tech/SaaS, E-commerce, Healthcare, Finance, Food, Education, Travel, Entertainment, Real Estate, Automotive, Legal, Non-profit, Government, Personal portfolios, Agency sites, Developer tools, etc.

## Minimal example

```python
from uiuxpro import ReasoningEngine
engine = ReasoningEngine()

rules = engine.search("fintech payment app")
# rules[0]:
#   category = "Fintech/Crypto"
#   pattern = "Data-first + compliance footer"
#   style_priority = ["Professional Minimalism", "Data-Dense UI"]
#   color_mood = ["deep blue", "neutral grey", "trust-green accent"]
#   anti_patterns = ["playful rounded fonts", "neon colors", "AI purple gradients"]
```

*Attributed to ui-ux-pro-max-skill by ara.so — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- The raw catalog is permissive — it lists patterns observed on real sites, not all of them ai-slop-free. Always filter the output against [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) BEFORE proposing to the user.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- BM25 relevance can misfire on highly specific product descriptions — `"autonomous drone delivery fleet"` may resolve to a generic "logistics" rule. Inspect the returned category before committing to its anti-pattern list.
- The catalog is a taxonomy credit to the upstream author; the plugin does NOT vendor the 161-rule data file itself. Agents can drill into specific rules via the upstream CLI (`npx uipro-cli rules search "<industry>"`) or treat this file as a conceptual reference.

## Top 10 distinctive rules — broken out as individual TECH files

- [TECH-uiux-rule-fintech](TECH-uiux-rule-fintech.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-uiux-rule-healthcare](TECH-uiux-rule-healthcare.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-uiux-rule-luxury-ecommerce](TECH-uiux-rule-luxury-ecommerce.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-uiux-rule-saas-dashboard](TECH-uiux-rule-saas-dashboard.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-uiux-rule-food-restaurant](TECH-uiux-rule-food-restaurant.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

Remaining 156 rules are addressable via the upstream CLI; this catalog documents their structure.

## Cross-references

- [TECH-uiux-styles-catalog](TECH-uiux-styles-catalog.md), [TECH-uiux-palettes-catalog](TECH-uiux-palettes-catalog.md), [TECH-uiux-font-pairings-catalog](TECH-uiux-font-pairings-catalog.md), [TECH-uiux-lp-patterns-catalog](TECH-uiux-lp-patterns-catalog.md) — sibling catalogs
  > What it does · When to use · How it works · Representative styles (partial list — full 67 are in the upstream corpus) · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — mandatory filter applied BEFORE emission
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
