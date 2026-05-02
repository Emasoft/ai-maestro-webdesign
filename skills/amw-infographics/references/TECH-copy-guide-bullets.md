---
name: TECH-copy-guide-bullets
category: infographic-archetype
source: image-generation/create-infographics/resources/copy-guide.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [Why](#why)
- [Rule 1 — Bullets, not paragraphs](#rule-1-bullets-not-paragraphs)
- [Rule 2 — One fact per bullet](#rule-2-one-fact-per-bullet)
- [Rule 3 — Sentence fragments, not full sentences](#rule-3-sentence-fragments-not-full-sentences)
- [Rule 4 — Inline token coloring](#rule-4-inline-token-coloring)
- [Rule 5 — Color-coded keyword highlighting (beyond tokens)](#rule-5-color-coded-keyword-highlighting-beyond-tokens)
- [Badge / tag rules](#badge-tag-rules)
- [Disclaimer (always include in footer)](#disclaimer-always-include-in-footer)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Bullet points rule — over paragraphs, always

## What it does

The rule: body text inside any card, panel, or callout MUST be
bullet points, never prose paragraphs. The ONLY paragraph allowed
in an entire infographic is 1-2 sentences in the hero intro.

## Why

Infographics read like structured data, not prose. Paragraphs inside
components are the #1 giveaway that the piece is a marketing
website, not editorial reference material.

## Rule 1 — Bullets, not paragraphs

```
✅ Inside a card:
• Earns 8% APY on staked tokens
• 30-day lock period after deposit
• Compounding every 24 hours

❌ Inside a card:
"Users who stake their tokens will earn an 8% annual percentage yield
on their deposited assets, with a 30-day lock period that applies
after each deposit, and rewards that compound every 24 hours."
```

## Rule 2 — One fact per bullet

Never wrap explanations into multi-sentence bullets. Each bullet =
one fact, one condition, one number.

```
✅ One fact per bullet:
• Min stake: 500 $TKN
• Lock period: 30 days
• APY: 8% (compounding daily)

❌ Multi-sentence bullet:
• Users must stake at least 500 $TKN tokens and maintain the lock
  for 30 days to earn the 8% APY, which compounds every day.
```

## Rule 3 — Sentence fragments, not full sentences

Use the shortest phrase that conveys the fact. Drop articles
("the", "a"), drop "users can", drop "this allows":

```
✅ Fragment style:
• Daily rate based on Temperature factor
• 3 egg types: Common, Rare, Legendary
• Snapshot: March 31, 2026

❌ Full sentence style:
• The daily rate is calculated based on the Temperature nurturing factor.
• There are 3 types of eggs available: Common, Rare, and Legendary.
• The snapshot will take place on March 31, 2026.
```

## Rule 4 — Inline token coloring

Token names mentioned inline MUST be wrapped in an accent `<span>`:

```html
<!-- source: image-generation/create-infographics/resources/copy-guide.md -->
✅ Colored token reference:
<li>Hold <span class="highlight">500 $TKN</span> before snapshot</li>
<li>Earn <span class="highlight">$ARENA</span> + <span class="highlight">$ENERGY</span> daily</li>

❌ Uncolored token reference:
<li>Hold 500 $TKN before snapshot</li>
```

```css
.highlight {
  color: var(--primary);
  font-weight: 600;
}
/* Or with background tint: */
.highlight-bg {
  background: rgba(var(--primary-rgb), 0.15);
  color: var(--primary);
  padding: 1px 5px;
  border-radius: 3px;
  font-weight: 600;
}
```

Limit: max 2 highlights per bullet. Token names always get colored;
limit other highlights to key numbers.

## Rule 5 — Color-coded keyword highlighting (beyond tokens)

Highlight key terms (dates, thresholds) within body text:

```html
<p class="card-body">
  Hold a minimum of
  <span class="highlight">500 $TKN</span>
  in your wallet before the
  <span class="highlight">March 31st</span>
  snapshot date.
</p>
```

Max 2 highlights per paragraph — more loses emphasis.

## Badge / tag rules

- 1-2 words MAX
- ALL CAPS
- Never complete sentences

```
✅ LIVE NOW     SEASON 2    BETA     NEW     Q1 2026
✅ FREE MINT    LIMITED     SOLD OUT V2 LAUNCH
❌ NOW AVAILABLE TO USERS
❌ Currently in beta testing
```

## Disclaimer (always include in footer)

Full: "This infographic is for informational purposes only and does
not constitute financial advice."

Short: "Not financial advice. DYOR."

## Gotchas

- Multi-sentence bullets feel like you're being thorough but they
  read as bloat. Split into multiple bullets.
- "Users can" / "This allows" are filler — strip them.
- 2 highlights per bullet is the cap — 3+ loses the emphasis effect.

## Cross-references

- [TECH-inline-token-coloring](TECH-inline-token-coloring.md) — the token-coloring implementation.
- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — the "no paragraphs" rule.
- [TECH-bullet-panel-component](TECH-bullet-panel-component.md) — the container pattern.
- [`../SKILL.md`](../SKILL.md) — parent skill

