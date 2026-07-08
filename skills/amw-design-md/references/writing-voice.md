# Writing Voice — Prose Quality Principles for DESIGN.md Authoring

Tokens tell an agent what colors and sizes to use. Prose tells the agent **why one brand looks like this and not like every other site.** Without the prose voice, an agent produces generic UI even with a perfect token set. Read this file before writing the prose sections of any DESIGN.md.

Loaded by `amw-design-md` (the orchestrator's DESIGN.md skill) and consumed by `amw-design-md-author-agent` during Phase A/B.

---

## Table of Contents

- [I. Principle 1 — Specific words beat generic words](#i-principle-1--specific-words-beat-generic-words)
- [II. Principle 2 — Compare to the peer category](#ii-principle-2--compare-to-the-peer-category)
- [III. Principle 3 — Document scarcity rules explicitly](#iii-principle-3--document-scarcity-rules-explicitly)
- [IV. Principle 4 — Don'ts are half the document's value](#iv-principle-4--donts-are-half-the-documents-value)
- [V. Principle 5 — Semantic role names, not literal names](#v-principle-5--semantic-role-names-not-literal-names)
- [VI. Principle 6 — Cross-reference tokens, not raw hex](#vi-principle-6--cross-reference-tokens-not-raw-hex)
- [VII. Principle 7 — Document Known Gaps honestly](#vii-principle-7--document-known-gaps-honestly)
- [VIII. Sentence patterns that work](#viii-sentence-patterns-that-work)
- [IX. Things to avoid](#ix-things-to-avoid)
- [X. Test the result](#x-test-the-result)

---

## I. Principle 1 — Specific words beat generic words

Bad prose states facts without anchoring them to identity:

> "The brand uses a deep green primary color."

Good prose names the specific token, distinguishes it from a generic variant of the same hue, and implies the design intent:

> "The primary is a saturated forest green (`#1b5e3b`) — denser and more terrestrial than the pale sage you see on wellness apps. It reads as botanical precision, not spa calm."

The prose carries opinion AND a contrast that anchors the choice. The reader should not be able to replace the brand name with any other brand and have the sentence still feel true.

**Rule:** Every color description, typography rule, and spacing principle must include a specific token value AND a clause that distinguishes it from a generic version of the same choice.

---

## II. Principle 2 — Compare to the peer category

Brand voice lives in opposition. A brand's identity is defined as much by what it refuses to do as by what it does. Always position the brand against 2–3 peers or category defaults:

> "Where most fintech brands anchor on confident royal blue, this brand grounds on deep navy (`#0a1f3c`) — a color that reads as institutional and measured rather than aggressively modern."
>
> "Linear's canvas is near-black (`#08090a`). Where other dark-mode products drift toward mid-gray, Linear goes almost to absolute dark — signaling depth over comfort."
>
> "This is the opposite of the 'bold hero headline' convention. Weight 300 at 56px commands attention because it does not need to shout."

A comparative claim gives the agent a default direction: when in doubt, bias against the category norm. A DESIGN.md with no comparative claims leaves the agent without that guidance.

---

## III. Principle 3 — Document scarcity rules explicitly

The most common failure mode of brand-naive agents is over-applying the accent color. Combat this by listing every location where the accent appears — and only those locations.

Every accent or signature color must have its own scarcity sentence:

> "Use `{colors.primary}` lavender only for: brand mark, primary CTA, focus ring, link emphasis. Nowhere else."
>
> "Reserve `{colors.ink-coral}` for primary CTAs and full-bleed callout-card moments. Do not scatter coral across decorative touches."
>
> "Workflow accent colors — Ship Red, Preview Pink, Develop Blue — appear only on workflow-step labels, never on buttons or navigation links."

When you write this rule, it must appear in two places: the Overview section prose, and the Do's/Don'ts list. A scarcity rule buried in only one section often goes unread.

---

## IV. Principle 4 — Don'ts are half the document's value

Most design documentation focuses on what to do. DESIGN.md leans hard on what not to do. The Don'ts encode the negative space of the brand — the patterns an agent would naturally reach for but that would break the identity.

A strong Don't has three properties:

1. **Concrete** — names a specific value or pattern, not a vibe.
2. **Anti-default** — opposes a generic AI tendency.
3. **Reasoned** — implies why this is wrong, even briefly.

Examples of strong Don'ts:

> "Don't use `#000000` true black as the canvas." (Concrete — names the exact wrong hex.)
>
> "Don't pill-round CTAs." (Concrete — names the exact wrong shape.)
>
> "Don't use weight 600–700 for headline text — weight 300 is the brand voice." (Anti-default + reasoned.)
>
> "Don't introduce a second chromatic accent (orange, pink, teal for seasonal marketing). The system uses one accent color precisely because scarcity is its mechanism." (Anti-default + reasoned.)
>
> "Don't use a neutral gray shadow. Shadows must always be tinted." (Anti-default + alternative implied.)

Weak Don'ts to avoid: "Don't make it ugly." "Don't be inconsistent." "Don't ignore accessibility." These are generic, unfalsifiable, and useless. Every Don't should describe a specific, plausible, on-brand mistake.

---

## V. Principle 5 — Semantic role names, not literal names

Never write "the white color" — write "the canvas" or "the page background." Never write "the gray text" — write "the muted body copy" or "the tertiary ink." Role names travel; literal names lock to one value and break when the palette shifts.

In Variant 1 (frontmatter format), the role IS the token name: `{colors.canvas}`, `{colors.ink-muted}`. In the numbered community format, write the role beside the literal: "Stripe Purple (`#533afd`), Deep Navy (`#061b31`), Slate (`#64748d`)."

The test: replace every hex in the token table with placeholder X. The prose should still be unambiguous about which role does what and why. If it collapses into vagueness without the hex values, the naming is not semantic enough.

---

## VI. Principle 6 — Cross-reference tokens, not raw hex

In Variant 1 (frontmatter format), prose mentions of design values use the token reference rather than the raw value:

Good:

> "The default page floor is `{colors.canvas}` — a tinted cream that avoids the clinical flatness of pure white."

Bad:

> "The default page floor is `#faf9f5` — a tinted cream that avoids the clinical flatness of pure white."

Token references keep the document machine-rewritable: change the YAML once, and every prose mention stays correct without a find-and-replace pass. The hex in parentheses is acceptable as a human-readable gloss, but the primary reference must be the token name.

In Variant 2 (numbered format), hex stays inline since there is no YAML source of truth. Pair it with a role name on first introduction: "the accent lavender (`#5e6ad2`)."

---

## VII. Principle 7 — Document Known Gaps honestly

Every DESIGN.md ends with a Known Gaps or Limitations section (Variant 1 frontmatter: `warnings` block; Variant 2 numbered: explicit last section or gap-flags scattered throughout). Honesty here prevents the agent from hallucinating values that were never in the source.

Common gaps to acknowledge:

- Light mode not extracted (or dark mode, depending on which canvas the source exposes).
- Form validation states beyond focus (error, disabled, success in-context).
- Animation and transition timings — durations, easing functions.
- Proprietary fonts not publicly distributed, with a named substitute already specified.
- Sub-product surfaces (in-app UI vs. marketing surface — these often differ significantly).
- Micro-interaction hover states on tertiary elements.
- Responsive typography scale for mobile (if only desktop was examined).

The acceptable pattern is direct: "Light-mode surface colors were not extracted — this DESIGN.md covers the dark canvas only. For light mode, treat `{colors.canvas}` as `TODO`." Do not apologize or hedge with "hopefully" or "we tried." State what was extracted and what was not.

---

## VIII. Sentence patterns that work

These patterns appear throughout strong DESIGN.md prose and reliably produce the right voice.

**The category-defining sentence** (open the Overview with this):

> "`<Brand>`'s website is `<category descriptor>` — a system that `<distinguishing trait>`."

Examples:
- "Stripe's website is the gold standard of fintech design — a system that manages to feel simultaneously technical and luxurious."
- "Vercel's website is the visual thesis of developer infrastructure made invisible — a design so restrained it approaches philosophical."

**The token-plus-characterization sentence**:

> "`<Semantic name>` (`#hex`) — `<one-line characterization that distinguishes it from a generic version of the same color>`."

Examples:
- "Lavender-blue (`#5e6ad2`) — a confident, mid-saturation blue that stands alone as the only chromatic color in the entire interface."
- "Vercel Black (`#171717`) — not pure black; the slight warmth prevents harshness."

**The scarcity sentence**:

> "`<Color>` appears `<only here, and here>` — never `<where you might expect it>`."

Examples:
- "The accent lavender appears on the brand mark, focus rings, and primary CTAs — never decoratively."
- "Electric Blue is used exclusively for primary CTA buttons. The brand deliberately avoids color variety."

**The negative-space sentence** (for Overview):

> "There are no `<thing>`, no `<other thing>`, no `<third thing>`."

Examples:
- "There are no decorative borders, no gradients, no patterns, no shadows."
- "No second chromatic color. No atmospheric gradients. No spotlight cards."

These negative-space sentences are powerful because they enumerate what is absent. Agents respond to explicit absence lists as reliably as to positive rules.

**The contagious detail sentence** (one specific, unusual technical fact):

> "`<Brand>` uses `<specific technique>` — `<explanation of why it matters>`."

Examples:
- "Stripe enables OpenType `\"ss01\"` globally on all body text — a stylistic set that modifies specific glyphs and defines the brand's letterforms."
- "Linear uses `box-shadow: 0 0 0 1px rgba(255,255,255,0.08)` as its card border — a ring-shadow that creates a border-like edge without box-model implications."

---

## IX. Things to avoid

**Filler adjectives** — "modern," "clean," "sleek," "professional," "polished," "elegant." These describe nothing. Every adjective should be replaceable with a specific fact.

**Marketing-speak** — "delights users," "industry-leading," "thoughtfully crafted." Out of register for this format.

**Vague comparisons** — "feels premium," "looks high-end," "has a luxurious feel." Specify which concrete decisions produce the perception.

**Overclaiming with "always" / "never"** — only when the brand actually enforces it. "All headlines are weight 300" is false if even one level is not. Hedge accurately: "the dominant headline weight is 300," "primarily weight 300."

**Apologetic gaps** — "Hopefully this captures...," "We tried our best to...," "This may not be complete...". State what was extracted and what was not. Omit the apology entirely.

---

## X. Test the result

After drafting any section, ask two questions.

### Blind-component test

Could an agent reading only §1 (Visual Theme and Decision Rules) and §9 (Agent Prompt Guide) build a new, unseen component — say, a toast notification or a settings panel — that a designer would immediately recognize as belonging to this brand?

If the answer is "kind of" or "the agent would need to guess," the section is underwritten. The Decision Rules and Agent Prompt Guide must together be sufficient for component invention.

### Palette-swap test

Mentally replace every color in the document with a completely different palette. Read the Overview prose and Decision Rules again. If they still sound correct for the swapped palette, the identity description is too generic — it is describing token values, not the design's soul. Rewrite until the prose would be wrong for a different color scheme.

If both tests pass, the document is done.

---

*Source: adapted and rephrased from `claude-skill-design-md` (Apache-2.0, João Alano, 2026) `references/writing-voice.md` and `design.skill` (MIT) `reference/format-spec.md` §1 Design Decision Rules + Genericness Test.*
