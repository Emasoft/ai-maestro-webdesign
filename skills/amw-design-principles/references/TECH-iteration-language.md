---
name: TECH-iteration-language
category: design-principles-workflow
source: clean-room reimplementation (T-056 batch9 Wave 2; the vague → concrete translation pattern is standard product/design coaching — common knowledge from design-review pedagogy and design-critique conventions)
license: this file = MIT (plugin license); NO verbatim copy from any GPL-2.0 source — written fresh in plugin idiom
also-in: `amw-ascii-sketch` (Phase A iteration loop reads this); `agents/ai-maestro-webdesign-main-agent.md` (translates user feedback during Phase A); `references/TECH-dial-configuration.md` (some translations adjust dials rather than freeform edits)
---

# Iteration language — vague feedback → concrete edits

## Table of Contents

- [What this is](#what-this-is)
- [Why vague feedback wastes tokens](#why-vague-feedback-wastes-tokens)
- [The translation table](#the-translation-table)
- [The reframe protocol](#the-reframe-protocol)
- [When to push back vs. translate](#when-to-push-back-vs-translate)
- [Multi-direction asks](#multi-direction-asks)
- [Cross-references](#cross-references)

## What this is

A coaching reference for the orchestrator (`ai-maestro-webdesign-main-agent`) and for `amw-ascii-sketch` during Phase A iteration. When the user says something like *"make it nicer"* or *"more premium"* or *"feel less corporate,"* the orchestrator must translate the adjective into one or more concrete edits before running another variant. Without translation, the model interprets the adjective every time and produces drift — three iterations later, "premium" has become five different things across five variants.

The translation has two layers:

1. **Vocabulary translation** — the table below maps the most common vague terms to one or more concrete edit-actions.
2. **Reframe protocol** — when the table doesn't cover the user's adjective, the orchestrator surfaces the proposed translation as a question and waits for confirmation before iterating.

## Why vague feedback wastes tokens

A vague feedback round costs ~3× a concrete one because:

- The model has to guess which axis the user means (visual? motion? copy? layout?).
- The model produces an output that may move 4 axes when the user only wanted 1.
- The user then has to identify which of the 4 moves they actually wanted (and undo the rest).
- Each undo is a new iteration round.

Translating *before* iterating reduces this to a single round: the user confirms or corrects the translation in chat, then iteration produces exactly the intended change.

## The translation table

| Vague feedback | Concrete edit(s) |
|---|---|
| "Make it nicer" | (Ask for axis.) Translation depends on what's wrong. See [The reframe protocol](#the-reframe-protocol). |
| "More premium" | Reduce palette to **black + white + 1 accent**; increase whitespace (DATA_DENSITY → 3); reduce VISUAL_COMPLEXITY to 4–5; use a serif headline OR a tighter sans-serif at higher weight |
| "Less premium / more friendly" | Allow a second accent color; increase BRAND_INTENSITY to 7; slightly playful typography (rounded sans-serif); MOTION_DRAMA → 6 |
| "More modern" | Remove decorative borders, replace with hairlines; flatten shadow tier; increase whitespace; switch to a 2024–2026 sans-serif (Inter, Geist, Söhne); kill any gradients-on-text |
| "Looks dated / old-fashioned" | Same as "more modern" + remove rounded-corner radii > 12 px (rounding above that reads as 2008–2014); remove drop shadows with offset > 4 px |
| "Less corporate" | Allow 1 personality element (illustration, ornamented numeric, brand mascot, hand-drawn arrow); increase MOTION_DRAMA to 6; soften palette (replace pure black with charcoal, pure white with off-white) |
| "More minimal" | VISUAL_COMPLEXITY → 2; remove decorations; reduce palette to 2 colors total; kill all material moments except one (or zero) |
| "More maximal / more interesting" | VISUAL_COMPLEXITY → 7–8; add 1 ornament (pre-text divider, big ornamented section numbers, asymmetric layout); MOTION_DRAMA → 7 |
| "More polished" | Audit alignment grid (fix any off-grid element); kerning pass on display type; replace any default rounded-corner radius with a brand-consistent radius; verify all interactive states have hover/focus/active treatments |
| "Feels generic / could be any SaaS" | Pick one brand-distinctive element (color, typeface, ornament, motion) and dial it to 8+; everything else stays calm — generic comes from "everything at 5" |
| "More punchy" | Bigger H1 (≥ 64 px); higher contrast (pure black or near-black on white); brand color appears in CTA + section accents; tight tracking on display type |
| "Calmer / quieter" | Reduce H1 to ≤ 48 px; soften contrast (charcoal not black); remove any motion above 250 ms duration; remove ambient motion entirely |
| "More text contrast" | Body text → near-black (#171717) or pure black; reduce muted-text usage; verify ≥ 7:1 contrast on body, ≥ 4.5:1 on muted |
| "Slower, more elastic motion" | Replace all `ease-out` curves with elastic / spring curves; lengthen durations by ~40%; add small overshoot on entrances |
| "Snappier motion" | All durations ≤ 200 ms; ease-out curves; no overshoot; no spring physics |
| "Make the CTA pop more" | Brand color background; increase button height by 8 px; add subtle glow on hover; reduce visual competition in the same section (remove secondary CTA, simplify surrounding copy) |
| "Show 3 alt layouts with same content" | Run variant spread per [TECH-dial-configuration.md](#cross-references) §Variant-spread-rule with content frozen |
| "The Hero is doing too much" | List every element in the Hero; force-rank by conversion job; remove the bottom 30%; restate H1 in ≤ 12 words |
| "I can't tell what this product does" | Rewrite H1 using the formula `[OUTCOME] for [WHO] [HOW]` per [TECH-landing-anatomy.md](#cross-references) §Hero-copy-formula |
| "It looks AI-generated" | Audit against `ai-slop-avoid.md`; usually one of: too many material moments, gradient-on-text, neon glow on non-emissive elements, perfect symmetry, default rounded radius on every element |
| "Trust me, less" | Remove any "best", "world-class", "industry-leading" superlatives; replace with named-customer quote, quantified metric, or specific product demo |
| "More confident" | Reduce word count by 30% across all copy; remove softening hedges ("we believe", "we think", "perhaps"); use declarative present tense |
| "Add some breathing room" | Increase section padding by 1.5×; increase line-height to ≥ 1.5 for body; increase margin between H2 and following paragraph by 1.5× |
| "Too dense / overwhelming" | DATA_DENSITY → 3; collapse Features 3-up grid into a 1-up stack; remove FAQ section temporarily; cut Hero subhead by half |
| "Too sparse / not enough info" | DATA_DENSITY → 7; add a Features section if missing; add named customer logos or quantified social proof; expand Hero subhead with one specific outcome |
| "Doesn't feel cohesive" | Audit token usage — every color should come from the 3–5 token palette; every spacing value from the 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 scale; every radius from a 2–3 value set |
| "The colors fight each other" | Pick a dominant color (60% surface area), one secondary (30%), one accent (10%); recalculate any pair that fails 60-30-10 |

## The reframe protocol

When the user gives feedback the table doesn't cover, the orchestrator MUST surface the translation as a question, not iterate blindly. The pattern:

```
User: "Make it nicer."

Orchestrator: "Three concrete directions I can push toward 'nicer'.
  Pick one or describe a fourth:
  1. More premium     → black + white + 1 accent, more whitespace, serif headline
  2. More playful     → second accent, softer palette, rounded type
  3. More confident   → shorter copy, larger H1, brand color on CTA
Or describe what specifically feels wrong about the current variant."
```

Then iterate only after the user confirms a direction. This costs one short chat exchange and saves a full iteration round per ambiguous feedback.

**The protocol is non-negotiable** when the user's adjective could map to 2+ concrete edits with different visual outcomes. "Make it nicer" qualifies. "Make the CTA pop" does not — the table has one canonical translation.

## When to push back vs. translate

Some user feedback is not a translation problem — it's a direction problem. The orchestrator pushes back (politely) rather than translating, when:

| User says | Push-back response |
|---|---|
| "Add some sparkle / make it pop / wow factor" | "Sparkle/pop/wow are slop-adjacent. The page currently uses N material moments (cap is 1–2). Which job needs more visual weight: the Hero, the CTA, or the social proof?" |
| "More AI-feeling" | "AI-feeling is a brand-positioning choice, not a visual one. Do you want the brand to read as 'cutting-edge product' (Linear/Vercel direction), 'enterprise serious' (OpenAI direction), or 'consumer playful' (Notion/Anthropic direction)?" |
| "Use [trendy effect, e.g. glass everywhere]" | "Glassmorphism only reads premium when used 1× per page. Where in the page does the glass need to live: nav, hero, or pricing card?" |
| "Just make it look like [URL]" | "Running brand-research on [URL] now via amw-brand-researcher-agent to extract tokens." (Don't iterate freeform; extract first.) |
| "Make it more like a real designer would do" | "I'll re-audit the current variant against the AI-slop checklist and surface anything that fails. The most common cause is more than 2 material moments, gradients without physical origin, or default rounded corners on every element." |
| "I don't like it but I can't say why" | "Three diagnostic questions: (1) Is the H1 saying what the product does in your own words? (2) Does the Hero look credible — i.e., is the social proof visible above the fold? (3) Is there anything visually that reads as 'AI made this'?" |

Push-back is collaborative, not adversarial. The point is to surface the actual design question hiding behind the vague feedback, not to refuse to iterate.

## Multi-direction asks

When the user gives feedback that combines multiple axes ("more premium AND more playful"), don't blend — split into variants:

```
User: "More premium but also more playful."

Orchestrator: "Those pull in opposite directions. I can produce two variants:
  - Variant A: more premium (less complexity, restrained palette, serif headline)
  - Variant B: more playful (rounded type, second accent, slight motion)
Pick one for the next iteration round, OR I can produce both for side-by-side comparison."
```

This is cheaper than blending (which usually fails) and gives the user the actual choice their feedback implied.

## Cross-references

- `agents/ai-maestro-webdesign-main-agent.md` — runs the Phase A iteration loop; reads this file to translate vague feedback before iterating.
- `skills/amw-ascii-sketch/SKILL.md` — Phase A iteration tooling; each iteration round expects already-translated input from the orchestrator.
- `references/TECH-dial-configuration.md` — many translations adjust dials (MOTION_DRAMA, VISUAL_COMPLEXITY, etc.) rather than freeform edits; iteration becomes a dial-change in those cases.
- `references/TECH-landing-anatomy.md` — Hero copy formula and banned CTA list are referenced from several translations.
- `skills/amw-design-principles/ai-slop-avoid.md` — "looks AI-generated" translation audits against this file.
- `references/component-taste.md` — "more polished" translation includes audits this file's per-component standards.
- `references/iteration-budget.md` — caps total iteration rounds per Phase A; translation reduces rounds-per-feedback to ~1.
