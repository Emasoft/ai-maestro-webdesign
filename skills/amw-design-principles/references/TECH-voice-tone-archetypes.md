---
name: TECH-voice-tone-archetypes
category: design-principles-copywriting
source: synthesized from common marketing-copy archetype taxonomies (PAS / AIDA / BAB / FAB / 4Ps / Hook-Story-Offer are common-knowledge frameworks); structured per copywriter agent's needs in this plugin
license: MIT (plugin license)
also-in: globalCC skill `technical-writing` for prose voice; `content-marketing-strategist` (stratarts) for channel-specific voice
---

# Voice and tone archetypes

## Table of Contents

- [What it does](#what-it-does)
- [When to choose an archetype](#when-to-choose-an-archetype)
- [The 7 archetypes](#the-7-archetypes)
  - [1. Crisp + Authoritative](#1-crisp--authoritative)
  - [2. Warm + Conversational](#2-warm--conversational)
  - [3. Playful + Confident](#3-playful--confident)
  - [4. Technical + Precise](#4-technical--precise)
  - [5. Aspirational + Inspiring](#5-aspirational--inspiring)
  - [6. Quiet + Reverent](#6-quiet--reverent)
  - [7. Direct + Functional](#7-direct--functional)
- [Conflict patterns between archetype and locale](#conflict-patterns-between-archetype-and-locale)
- [Cross-references](#cross-references)

## What it does

Catalog of 7 voice-and-tone archetypes the multilingual-copywriter agent uses to anchor every piece of copy it produces. The brief's `tone` field maps to one of these archetypes; subsequent copy decisions (sentence length, vocabulary register, idiom density, exclamation policy) follow from the chosen archetype.

Voice = the brand's enduring character (does not change between campaigns). Tone = the local adjustment for context (a calm Crisp+Authoritative brand still softens its tone in an apology email vs. a product launch). The archetypes below define **voice**; tone is the modulation around that voice for a specific surface.

## When to choose an archetype

- The brief mentions a specific tone keyword (formal / casual / playful / luxury / technical / aspirational) — map directly to the archetype below.
- The brief is silent on tone — the copywriter agent infers from the project type:
  - Luxury hospitality / private banking / executive-search → Quiet + Reverent or Aspirational + Inspiring.
  - SaaS / dev-tools / B2B platform → Direct + Functional or Crisp + Authoritative.
  - Consumer e-commerce / D2C → Warm + Conversational or Playful + Confident.
  - Healthcare / legal / financial-services → Crisp + Authoritative with tone-softened apology surfaces.
  - Documentation / API reference → Technical + Precise.
  - Editorial / media / opinion content → Aspirational + Inspiring or Quiet + Reverent.
- The brief contradicts the project type — the explicit brief wins; document the override in the agent's locale notes.

## The 7 archetypes

### 1. Crisp + Authoritative

**When to choose.** B2B SaaS that sells to engineering / security / compliance buyers. Financial services. Healthcare-adjacent products where the audience expects competence-first signaling. Government and enterprise-procurement contexts.

**Sentence shape.** Short to medium. Declarative. Active voice. Specific nouns. Numbers when available.

**Sample sentences.**
- "Encrypt every backup. Restore in under 60 seconds."
- "Built for teams managing more than 50,000 endpoints."
- "Compliance reports for SOC 2, HIPAA, and ISO 27001 — generated on demand."

**Do.**
- Open with the outcome the buyer cares about.
- Cite measurable facts (percentages, seconds, team sizes).
- Use industry-standard vocabulary (the buyer is technical; jargon is a feature, not a bug, when accurate).

**Don't.**
- Open with the company's history. The buyer reads competence; "Since 1998" buys nothing.
- Use superlatives ("the best", "world-class") without proof.
- Apologize for the price.

### 2. Warm + Conversational

**When to choose.** Consumer DTC brands selling a moderately considered purchase (cookware, mattresses, vitamins, mid-tier subscription services). Coaching / wellness apps. Onboarding flows for any product where the user is forming a first impression.

**Sentence shape.** Medium length. Personal pronouns ("you", "we", occasionally "I" in founder voice). Contractions allowed. Asides in parentheses are fine.

**Sample sentences.**
- "Pick the meals you actually want to eat this week — and we'll handle the rest."
- "We send one email a week. Real recipes from real cooks. Unsubscribe whenever."
- "Tell us how the workout went, and your next plan will adjust automatically."

**Do.**
- Address the reader directly with "you".
- Acknowledge that the reader is a person making a decision, not a unit being acquired.
- Use contractions ("we'll", "you're", "don't") — they make the voice sound like a person, not a corporation.

**Don't.**
- Over-perform empathy ("We get it! Life is HARD!"). Sincere warmth, not staged warmth.
- Use exclamation points to manufacture energy. One exclamation per page maximum.
- Make every sentence about feelings. The reader has a job to do; warmth supports it, doesn't replace it.

### 3. Playful + Confident

**When to choose.** Brands where personality is part of the product (gaming, creative tools, hobbies, certain DTC categories like pet brands, novelty food/drink). Younger audiences. Product surfaces where the user is exploring, not transacting yet.

**Sentence shape.** Variable. Mixing short punchlines with longer setups. Wordplay, metaphor, occasional sentence fragments for rhythm. Self-aware references to common UX patterns.

**Sample sentences.**
- "Wishlist? Stuffed. Cart? Empty. Let's fix that."
- "Three filters. Eight categories. Twelve thousand records. Yeah, we built a search bar for that."
- "Pour-over coffee for people who refuse to call it 'pour-over coffee'."

**Do.**
- Pay off setups. A pun-heavy headline needs a body that delivers on the implied promise.
- Show range — sometimes funny, sometimes blunt. Constant joking reads as nervous; confidence is the ground note.
- Keep CTAs literal even when the surrounding copy is playful. "Add to cart" is still the right CTA, not "Let's get weird with it."

**Don't.**
- Joke at the user's expense.
- Be playful in error states. Error messages stay matter-of-fact regardless of brand voice.
- Be playful in legal / privacy / billing surfaces. The reader is reading carefully there; playfulness reads as evasion.

### 4. Technical + Precise

**When to choose.** API reference documentation. Developer-facing changelogs. Engineering blog posts. Whitepapers. Surfaces where the reader is reading to understand a system, not to be persuaded.

**Sentence shape.** Medium to long. Subordinate clauses where they clarify causation. Defined-once-then-used terminology (no synonym-switching mid-document). Numbers, units, version strings, exact API names.

**Sample sentences.**
- "POST `/api/v2/sessions` returns a 201 with the session ID; the session expires after 60 minutes of inactivity."
- "Replication lag is measured at the read replica in seconds, sampled every 30 seconds, and surfaced as the `replica_lag_seconds` metric."
- "The breaking change in v3.2 affects callers that pass `null` to `setTimeout()` — prior versions coerced `null` to 0, the new version throws."

**Do.**
- Use exact identifiers. `useState` not "the state hook". `200 OK` not "a success response".
- Disambiguate every term on first use, then reuse the exact same word — switching between "user", "account", "principal", "identity" inside one document is hostile to the reader.
- Show, then explain. Code sample first, prose second.

**Don't.**
- Marketize. A technical doc page that opens with "Unleash the power of our API!" loses the audience in one sentence.
- Hide caveats in footnotes. Technical readers want the caveat next to the claim, not after.
- Use unexplained acronyms.

### 5. Aspirational + Inspiring

**When to choose.** Mission-driven brands (climate, education, healthcare access). Long-form editorial content. Hero sections of brand sites where the buyer is choosing alignment, not features. Investor-facing decks.

**Sentence shape.** Longer than the conversational archetype. Rhetorical structure (parallel phrases, antithesis, the rule of three). Concrete imagery balanced against abstract aspiration.

**Sample sentences.**
- "We build classrooms where the teacher is the question and the answer is the conversation."
- "Climate work is slow until it isn't. We're funding the work that closes the gap."
- "Patient care begins before the first appointment — in the form letter, in the parking lot, in the waiting room."

**Do.**
- Anchor every abstract claim with a concrete image. "Climate work" is abstract; "the work that closes the gap" is a metaphor; the reader needs at least one concrete thing — a project, a person, a number — to believe.
- Earn the rhetoric. Aspirational copy without proof reads as hollow. Pair the hero copy with a stat, a story, or a citation below.

**Don't.**
- Use stock-photo abstractions. "Empowering communities through innovation" is meaningless without specifics.
- Over-promise. "We will end hunger by 2030." reads as a slogan, not a plan; "We feed 4,200 schoolchildren a hot meal every weekday in three districts." is a verifiable claim.

### 6. Quiet + Reverent

**When to choose.** Luxury hospitality. Private banking, fine art galleries, high-end jewelry, sommelier services. Memorial or grief-adjacent products. Surfaces where the buyer expects restraint, and any visible effort to sell reads as cheap.

**Sentence shape.** Short, declarative. Spare adjectives. Almost no adverbs. Specific sensory or material nouns (wood, water, silk, dawn, terroir). Whitespace around the words on the page is part of the voice.

**Sample sentences.**
- "Overwater villas, private terraces, the lagoon at first light."
- "A pied-à-terre on rue de Varenne. By introduction."
- "A single tasting menu, served Wednesday through Saturday."

**Do.**
- Trust the reader. The buyer of a $25,000-a-night villa does not need exclamation points.
- Use specific material details — "Italian linen", "Burgundy chardonnay", "1930s Cartier" — rather than abstract claims of luxury.
- Leave room. Quiet copy means short sentences and visible whitespace around each line.

**Don't.**
- Use words like "exclusive", "elite", "unparalleled" — they signal trying-too-hard.
- Stack adjectives. One precise noun beats three vague adjectives.
- Use the word "luxury" itself in the copy. Show it through specifics.

### 7. Direct + Functional

**When to choose.** Utility surfaces (settings, account pages, dashboard internals, internal-tools, admin consoles). Receipts, invoices, transactional emails. Onboarding-step labels. Forms.

**Sentence shape.** Imperative or labeling. No flourish. Optimized for the reader who is scanning, not reading.

**Sample sentences.**
- "Add a payment method to continue."
- "Last login: 14 May 2026, from Brooklyn, NY. Not you? [Secure your account]"
- "Step 2 of 4: Verify your email address."

**Do.**
- Lead with the verb when the reader needs to act.
- Lead with the state when the reader needs to read.
- Use the same word for the same thing every time. The account-settings page says "email address"; the signup form says "email address"; the password-reset email says "email address". No synonym switching.

**Don't.**
- Try to be charming. The user is here to do a task.
- Use brand voice in error messages or transactional emails when the brand voice elsewhere is Playful — keep utility surfaces in Direct + Functional regardless of the brand's headline voice.

## Conflict patterns between archetype and locale

The same archetype reads differently in different locales. The copywriter agent adjusts tone (the local modulation), not voice (the brand archetype).

| Archetype | Adjustment in Japanese (ja) | Adjustment in German (de) | Adjustment in Spanish (es-419) |
|---|---|---|---|
| Crisp + Authoritative | Slightly more polite register (丁寧); the directness is in the precision of facts, not in clipped sentence shape. | Sie-form; longer compound nouns; the directness reads as competence, not coldness. | Usted-form for B2B; ustedes for plural; tu in DTC contexts; modal verb softening ("Puede confiar...") is welcome. |
| Warm + Conversational | Polite register; first-person plural ("私たち") preferred over second-person directness ("あなた"); softens warmth into hospitality. | Du-form is rarer than in English equivalents — most warm-conversational German B2C still uses Sie; warmth comes from word choice, not pronoun. | Tu-form for younger DTC; the warmth scales well in Romance languages because the language has built-in warmth markers. |
| Playful + Confident | Heavy adjustment — overt playfulness in Japanese marketing reads as juvenile. Wit becomes irony or specificity. | German playfulness exists but reads dry; puns translate poorly. Lean on understatement. | Plays well in Spanish; wordplay translates if cultural references are local (regional Spanish varies). |
| Technical + Precise | Same shape; honorific register at the very surface level (one polite verb in the doc's lead, then neutral throughout). | Same shape; German technical writing is direct already. | Same shape; consistent vocabulary across the doc is the main challenge. |
| Aspirational + Inspiring | Indirect-aspirational; explicit "we will change the world" reads as hubris. Show the change through specifics; let the reader infer the mission. | Aspirational works if grounded in concrete fact; abstract aspiration alone reads as evasive. | Aspirational scales well in Romance languages; sentence rhythm is naturally rhetorical. |
| Quiet + Reverent | Pairs naturally with Japanese register; ma 間 (the space between) is a real concept in Japanese aesthetics. | Pairs well; the brevity is welcome. | Quieter in Spanish needs short sentences; Spanish naturally lengthens compared to English. |
| Direct + Functional | Polite-direct (丁寧 + imperative form softened to request form). | Most natural fit; German UI copy is already Direct + Functional by default. | Direct + Functional with usted-form in B2B contexts; tu-form in B2C utility surfaces. |

When the brand's chosen archetype conflicts with the locale's cultural norm (e.g., Playful + Confident in a Japanese hospitality landing page), the copywriter agent adapts toward the locale convention and documents the adjustment in **Locale notes** (per agent §11 Conflict 3).

## Cross-references

- [TECH-microcopy-patterns.md](./TECH-microcopy-patterns.md) — the surface patterns (buttons, errors, empty states) that this voice colors
- [agents/amw-multilanguage-copywriter-agent.md](../../../agents/amw-multilanguage-copywriter-agent.md) §2 Mental Model + §9 Skill-Decision Matrix — agent reads this file
- [skills/amw-design-principles/SKILL.md](../SKILL.md) — orchestrator
- [skills/amw-design-principles/ai-slop-avoid.md](../ai-slop-avoid.md) — the banned phrases that this archetype catalog routes around
- [skills/amw-design-principles/references/authority-hierarchy.md](./authority-hierarchy.md) — when the SEO agent's keyword rewrite collides with the copywriter's archetype choice, who wins
