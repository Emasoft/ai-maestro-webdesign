---
name: TECH-influence-and-persuasion
category: design-principles-process
source: long-tail R-20 specialist-agent CRO corpus (direct port, batch9 Wave 2 Round 3, T-173)
license: MIT (specialist-agent upstream is MIT; plugin re-licenses under its own MIT — see ../../../LICENSE)
also-in: TECH-microcopy-patterns.md (CTA copy that compounds with social-proof + scarcity); TECH-form-validation-patterns.md (inline-validation conversion data); TECH-form-async-submit.md (perceived-wait + skeleton numbers); ai-slop-avoid.md (rejects fake-urgency / fake-testimonials)
---

# Influence and persuasion patterns

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [The 7 Cialdini principles → UI patterns](#the-7-cialdini-principles--ui-patterns)
  - [1. Reciprocity](#1-reciprocity)
  - [2. Scarcity](#2-scarcity)
  - [3. Authority](#3-authority)
  - [4. Social proof](#4-social-proof)
  - [5. Liking](#5-liking)
  - [6. Commitment & consistency](#6-commitment--consistency)
  - [7. Unity](#7-unity)
- [The 8-category friction audit](#the-8-category-friction-audit)
- [Conversion-impact data (use to back proposals with numbers)](#conversion-impact-data-use-to-back-proposals-with-numbers)
- [Anti-patterns — when persuasion becomes dark UX](#anti-patterns--when-persuasion-becomes-dark-ux)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Catalogues evidence-based persuasion principles and conversion-rate-optimisation (CRO) data, then maps each principle to a concrete UI pattern. This file is what the orchestrator consults before signing off any landing page, pricing page, signup flow, checkout, or call-to-action block.

Two distinct things live here:
- **Cialdini's 7 principles of influence** (`Influence: Science and Practice`, Cialdini 2009; expanded to 7 with `Unity` in `Pre-Suasion`, 2016) — translated to web UI patterns.
- **An 8-category friction audit** — the questions every conversion-affecting screen must answer before it ships.

## When this file fires

Read this file when the user's brief contains any of:
- "increase signups" / "conversion" / "checkout" / "pricing" / "trial flow" / "lead capture"
- "CTA" / "call to action" / "hero button" / "above the fold"
- "abandoned cart" / "drop-off" / "funnel"
- competitive references like "Stripe", "Linear", "Notion", "Vercel" — those pages use Cialdini patterns liberally and the user expects them mirrored

Do NOT read this file for pure portfolio sites, art-direction-led work, internal admin tools, or anything where persuasion is irrelevant (e.g. compliance documentation pages).

## The 7 Cialdini principles → UI patterns

Each entry: principle → mechanism → concrete pattern → evidence-strength → breaks-if.

### 1. Reciprocity

**Mechanism.** People feel obligated to return favors. Give something of value first, and the recipient is statistically more likely to give back.

**UI patterns:**
- Free template / asset / calculator above the signup wall — Stripe Atlas guides, Linear's keyboard-shortcut PDF, Figma's free icon set.
- "Take this with you" downloadable artifact at the end of an interactive tool, before the CTA.
- Real value in the free tier (not crippleware) — the message is "we gave you something useful; consider going further with us."

**Evidence-strength.** Strong. Cialdini's original research (Regan 1971 Coke study) + 50 years of replication. Magnitude on web: free-resource pages typically convert at 3–8× the rate of pure-CTA landing pages for top-of-funnel.

**Breaks if.** The "free" thing is gated (email required to download): the perceived gift becomes a transaction, reciprocity does not activate.

### 2. Scarcity

**Mechanism.** Things less available feel more valuable; loss aversion is stronger than gain attraction.

**UI patterns:**
- Genuine inventory counts ("3 seats left at this price").
- Time-limited offers with **real** deadlines and visible countdown.
- Cohort caps ("Spring 2026 cohort closes April 28").
- Beta / waitlist gating ("invite-only until June").

**Evidence-strength.** Very strong when scarcity is **real**. Studies (Worchel et al., Cialdini 1985) show 2–5× lift on perceived value when scarcity is credible. Drops to 0× or negative when perceived as manufactured.

**Breaks if.** The countdown resets on refresh, the "only X left" is the same number every visit, the "ends tonight" sale runs daily for six months. The user notices; trust collapses; the rest of the principles stop working too.

### 3. Authority

**Mechanism.** People defer to experts and recognised institutions.

**UI patterns:**
- Press-logo strip below the hero ("As seen in: Wired, NYT, FT"). Honest credentials only.
- Customer-logo strip ("Trusted by Stripe, Vercel, Linear") — same rule.
- Author bylines on content with real credentials ("by Dr. X, Y years at Z").
- Independent certifications (SOC 2, ISO 27001, B Corp) — small badge near the footer or in security-critical contexts.

**Evidence-strength.** Strong, but degrades fast when faked. Logos require permission; misuse is legally actionable and ruins the page in a backlash.

**Breaks if.** Logos belong to companies that never used your product. Author "credentials" are fluff ("growth marketing expert with 10+ years experience" — meaningless). Badges link to nothing.

### 4. Social proof

**Mechanism.** People look at what others are doing to decide what they should do. Strongest when the "others" are similar to the viewer (peer proof beats celebrity proof for utility products).

**UI patterns:**
- **Specific** testimonials with full name + role + company + photo (vague "John D., Marketing" is read as fake).
- Customer counts ("Over 50,000 teams trust X") — must be honestly defensible.
- Use-case quotes embedded next to the feature they refer to (not in a generic testimonials strip).
- Star ratings + review counts from third-party services (G2, Capterra, Trustpilot).
- Live activity feeds ("Someone in Berlin just signed up") — only if real.

**Evidence-strength.** Very strong. Roughly 70% of buyers consult reviews before purchase (Spiegel Research Center, BrightLocal surveys 2017–2023). Magnitude: 1 unique-named testimonial near a CTA can shift conversion 10–30%.

**Breaks if.** Testimonials are stock photos + invented names. The user is good at spotting this — reverse-image-search of a "happy customer" finds the iStock URL.

### 5. Liking

**Mechanism.** People say yes more often to people (and brands) they like. Liking comes from similarity, compliments, association, and familiarity.

**UI patterns:**
- "About us" / team page with real photos and personality (not corporate suit-and-tie posed against a window).
- Personalised onboarding ("Hi Alex — let's set up X for the marketing team you mentioned").
- Brand voice consistent with the audience's voice (technical for technical; casual for casual).
- Behind-the-scenes content (changelog with personality, "what we shipped this week").

**Evidence-strength.** Moderate but compounding. Hard to measure in isolation; very visible when absent (sterile B2B sites that read like Wikipedia underperform).

**Breaks if.** Tone is forced — "we're a fun startup!!" written by people who don't believe it. Authenticity is the entire mechanism.

### 6. Commitment & consistency

**Mechanism.** Once a person commits to a small step, they want to remain consistent with that commitment. Small yes leads to bigger yes.

**UI patterns:**
- **Progress bars on multi-step forms** — once the user sees "step 1 of 4 complete", quitting feels like loss.
- Wizards that ask easy questions first ("what's your role?") before the hard ones (credit card).
- "Save as draft" CTAs that get the user into the system before asking for payment.
- Free-trial-without-credit-card → in-app upgrade prompts after the user has set up their workspace.

**Evidence-strength.** Strong. Multi-step forms with progress bars consistently outperform single-page equivalents on long flows; the data is in TECH-form-multi-step.md.

**Breaks if.** Step 1 is too high a commitment (asks credit card up front). The principle requires *small* first commitments.

### 7. Unity

**Mechanism.** "We" beats "you and me". When the audience shares an identity with the seller, the persuasion is automatic.

**UI patterns:**
- Audience-defining language in the hero ("For engineering teams shipping daily" — engineering teams are now "us").
- Community features (Slack / Discord / forum) prominently linked.
- "Made by [people like you]" — open-source projects, indie SaaS, founder-letter homepages.
- Industry-specific case studies ("How [specific competitor in your space] uses X").

**Evidence-strength.** Newest of the 7 (Cialdini added in 2016). Anecdotal-strong; less hard data than the original 6 but visible in the success of community-led GTM (Notion, Figma, Linear).

**Breaks if.** "Unity" is performative — corporate site claiming to be "by developers for developers" while the team has zero engineers visible.

## The 8-category friction audit

Before any conversion-affecting screen ships, walk this 8-question audit. Every "no" or "unknown" is a finding.

| # | Category | The question | Pass criterion |
|---|---|---|---|
| 1 | **Load** | Does the page hit Largest Contentful Paint < 2.5s on a slow-4G profile? | Lab + field both green |
| 2 | **Above-the-fold clarity** | Can a first-time visitor answer "what is this?" and "is it for me?" in 5 seconds without scrolling? | Three users in unmoderated test answer yes |
| 3 | **CTA visibility** | Is the primary CTA visually distinct (contrast, position, repetition below the fold)? | One unambiguous primary action; no two equally-weighted buttons |
| 4 | **Form friction** | How many fields are *required* in the primary flow? Are they ordered easy → hard? | Required-field count is the minimum the business actually needs (no "phone" for an email-only product) |
| 5 | **Validation** | Does the form give *inline*, *real-time*, *positive-first* validation? | Errors appear as the user leaves the field, not on submit. Successes appear with green tick |
| 6 | **Perceived wait** | Is every async action ≥ 400ms covered by a skeleton or progress indicator? | No silent waits longer than 400ms anywhere |
| 7 | **Mobile** | Tap targets ≥ 44×44px? Body copy ≥ 16px? Single-column at < 640px? | All three yes |
| 8 | **Recovery** | If the user makes a mistake (wrong card, expired token, lost connection), does the error explain what happened *and* what to do next? | Every error message names the cause and the next action |

Each failing category gets a one-line finding in the audit report, with the specific selector or screen ID. Findings link to the relevant TECH file (validation → `TECH-form-validation-patterns.md`, async → `TECH-form-async-submit.md`).

## Conversion-impact data (use to back proposals with numbers)

Numbers below are reported in widely-cited industry research; cite the source when used in client work — don't claim them as your own measurements.

- **Page load.** Every 1s of additional load time correlates with ~7% conversion drop on e-commerce (Akamai, 2017; Portent 2019 replication). Going from 1s → 3s on mobile typically triples bounce rate.
- **Mobile abandonment.** 53% of mobile sessions are abandoned if a page takes longer than 3s to load (Google / SOASTA 2017). The number has not moved much in subsequent studies.
- **Inline validation.** Replacing on-submit error blocks with field-level inline validation has been measured at ~22% conversion lift on signup forms (Luke Wroblewski / EightShapes case studies, 2009; replicated multiple times since).
- **Skeleton screens.** Skeleton placeholders reduce perceived wait by ~30% versus a blank screen or spinner during equivalent real waits (Lukew + Facebook / Linkedin design-team write-ups, ~2014).
- **Single CTA.** Pages with a single primary CTA convert at roughly 2× the rate of pages with multiple competing CTAs above the fold (HubSpot, WordStream studies — directional, varies wildly by category).
- **Required-field reduction.** Cutting required fields on a signup form from 11 to 4 has produced 120%+ conversion lifts in industry case studies (Expedia famously removed a single "Company" field and recovered ~$12M/year — anecdote, but the principle replicates).
- **Hero clarity.** Adding a 1-sentence value-proposition subhead below the headline (telling the user *what the product does*) typically lifts conversion 10–20% over a headline alone — most-quoted source is MarketingExperiments / Flint McGlaughlin's work.

Use these numbers in two situations:
1. To justify a recommendation ("LCP > 3s is costing us roughly 7%/s — fixing the largest image cuts 1.4s of load").
2. To set targets at the start of a project ("the friction audit needs all 8 boxes green before we ship; the conversion-impact data tells us each broken box costs 5–25% of conversion").

Do NOT use them to manufacture false urgency in copy ("studies show you should sign up now!" — this is anti-pattern, see below).

## Anti-patterns — when persuasion becomes dark UX

The 7 principles are powerful enough to be misused. The plugin-wide AI-slop rules already block several; this section names them explicitly so the audit catches them when they slip into client requests.

| Anti-pattern | Why it's broken |
|---|---|
| **Fake scarcity** — "Only 3 left!" that never decrements; "Sale ends tonight!" that runs daily | The user notices on repeat visits; trust collapses; CRO becomes negative |
| **Fake activity feeds** — "Someone in Berlin just bought X" generated by a JS random pick | Reverse-engineerable in 30 seconds via DevTools; reputational risk |
| **Confirmshaming** — "No thanks, I don't want to save money" as the opt-out copy | Annoys the conversions you got and burns the ones you didn't |
| **Hidden recurring charges** — small print on a "free trial" that auto-bills | Chargeback magnet, FTC liability, never worth the short-term gain |
| **Roach-motel cancel flows** — sign-up takes 30s, cancel takes 8 emails | Generates terminal hate; rule-makers (FTC, EU) increasingly outlawing |
| **Fake testimonials** — stock photo + invented name | Reverse-image-search finds the iStock URL within seconds |
| **Fake authority badges** — logos of customers who never used your product | Legally actionable; trivially verified |
| **Manipulative defaults** — pre-checked "subscribe to all marketing emails" boxes | EU GDPR violation; opt-IN, not opt-OUT |

Any time a brief asks for one of these, refuse and propose the honest version. The brief usually accepts.

## Breaks if

- The page promises scarcity / urgency / authority that doesn't survive a 30-second verification by the visitor. Persuasion principles only work when honest; faked ones invert the effect.
- The conversion numbers above are cited as if they were the team's own measurements. They are industry-aggregate; use them as direction, not as ground truth for the current site.
- The 8-category audit is run *once* before launch and never again. The audit is a recurring checklist — re-run at each significant content / layout change.
- The team uses the 7 principles to justify dark patterns. The principles are descriptive (what humans do); the ethics layer is normative (what should the team do). Both have to hold.

## Cross-references

- [TECH-microcopy-patterns.md](TECH-microcopy-patterns.md) — concrete CTA copy that bakes in social-proof + scarcity.
- [TECH-form-validation-patterns.md](TECH-form-validation-patterns.md) — inline-validation conversion data.
- [TECH-form-multi-step.md](TECH-form-multi-step.md) — commitment-and-consistency mechanism applied to long forms.
- [TECH-form-async-submit.md](TECH-form-async-submit.md) — perceived-wait + skeleton numbers.
- [ai-slop-avoid.md](../ai-slop-avoid.md) — the plugin-wide AI-slop list rejects fake-urgency, fake-testimonials, manipulative defaults.
- [TECH-landing-anatomy.md](TECH-landing-anatomy.md) — the section ordering this file's Cialdini patterns assume.
- [authority-hierarchy.md](authority-hierarchy.md) — `amw-legal-expert-agent` has VETO on any dark-pattern that risks GDPR / FTC exposure.
