<!-- Clean-room synthesis of Cialdini's published behavioural-influence research as commonly reproduced in marketing and conversion-rate-optimisation literature. No copyrighted book passages reproduced; concepts described in plugin-original prose. Authored for batch9 Wave 2 Round 4, T-166. -->

---
name: TECH-cialdini-influence-principles
category: design-principles-process
source: clean-room synthesis of Cialdini behavioural-influence research (batch9 Wave 2 Round 4, T-166)
license: MIT (plugin-original under ../../../LICENSE)
also-in: TECH-influence-and-persuasion.md (sibling reference; R3 covered the 7-principle catalogue and CRO numbers; this file goes deep on each principle's UI surface and the ethical line); TECH-fogg-behavior-model.md (Trigger maps to Cialdini cues; Motivation maps to scarcity/social-proof); TECH-loss-aversion-pricing.md (anchoring + endowment compose with reciprocity for pricing pages); ai-slop-avoid.md (rejects fake-urgency + fake-testimonials)
---

# Cialdini influence principles — deep UI surface

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [Token block — persuasion-layer variables](#token-block--persuasion-layer-variables)
- [Reciprocity — give first, ask second](#reciprocity--give-first-ask-second)
- [Commitment and consistency — small yes then big yes](#commitment-and-consistency--small-yes-then-big-yes)
- [Social proof — what others did](#social-proof--what-others-did)
- [Authority — credible sources](#authority--credible-sources)
- [Liking — relatability and warmth](#liking--relatability-and-warmth)
- [Scarcity — limited supply or time](#scarcity--limited-supply-or-time)
- [Compounding two principles in one block](#compounding-two-principles-in-one-block)
- [The ethical line — three filters](#the-ethical-line--three-filters)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

The sibling file `TECH-influence-and-persuasion.md` (R3, T-173) catalogued all seven Cialdini principles in one-line summaries with industry-aggregate conversion numbers. This file goes one level deeper: each of the six classical principles (reciprocity, commitment and consistency, social proof, authority, liking, scarcity) gets a full section with mechanism, two concrete UI examples (one ethical, one dark-pattern), the boundary between them, and the breaks-if cases.

Read this file when:
- A conversion-affecting screen needs more than a one-line CRO citation — the team wants to understand *why* the pattern works.
- A brief proposes a pattern that smells like a dark pattern; this file gives the ethical filter and the honest alternative.
- A designer needs to compound two principles into one block (the most common production case) without breaking either.

The seventh principle (Unity) was added by Cialdini in his 2016 follow-up work; it lives in `TECH-influence-and-persuasion.md` because its UI surface is much smaller than the original six and the sibling file already covers it adequately.

## When this file fires

- "Increase signups" / "improve conversion" / "redesign the pricing page"
- "Why does Stripe's pricing work?" / "Why does Linear's testimonial section feel different?"
- "Is this a dark pattern?" / "Can we ethically add scarcity here?"
- "Compose social proof with scarcity without the page looking spammy"

Do NOT read this file for:
- Internal admin tools (no persuasion needed)
- Documentation / API reference pages
- Compliance / legal / privacy-policy pages (regulated copy, not marketing)

## Token block — persuasion-layer variables

Most persuasion is copy and layout, not color, but the ones that *are* visual use a small predictable token set. Bind these in `design-tokens.css` so every persuasion block shares the same palette.

```css
:root {
  /* Social-proof colors */
  --proof-rating-fill: oklch(80% 0.18 85);     /* star yellow */
  --proof-rating-empty: oklch(85% 0.02 250);   /* muted gray */
  --proof-verified-badge: oklch(60% 0.15 145); /* trust green */

  /* Scarcity colors (sparingly) */
  --scarcity-soft: oklch(75% 0.12 50);    /* amber, low-stock badge */
  --scarcity-urgent: oklch(60% 0.20 25);  /* red, last-hour banner */

  /* Authority badge surface */
  --authority-surface: oklch(98% 0.005 250);
  --authority-border: oklch(85% 0.02 250);

  /* Reciprocity-CTA palette (calmer than primary CTA) */
  --reciprocity-cta-bg: oklch(96% 0.01 230);
  --reciprocity-cta-fg: oklch(35% 0.05 230);
}
```

The visual loudness ranking is `--scarcity-urgent` > primary CTA > `--scarcity-soft` > `--proof-verified-badge` > `--reciprocity-cta`. Never invert this; a calm reciprocity-CTA next to a red scarcity-urgent banner reads as a manipulative bait-and-switch.

## Reciprocity — give first, ask second

**Mechanism.** People feel obligated to repay a gift, even an unsolicited small one. The obligation is strongest right after the gift; it decays over hours and days. In a web context the gift is usually a free resource (template, calculator, mini-tool, content download, free trial) that the user gets *before* the ask (signup, upgrade, purchase).

**Ethical UI example.** A SaaS landing page leads with a free, no-signup calculator (e.g. "How much do you spend on cloud hosting per month?"). The user runs the calculator, gets a useful answer, and at the result screen sees a soft CTA: "Want to cut that 30%? See how our product would price your usage" → links to a pricing page. The free tool is genuinely useful and works without an email; the CTA is calm, not lifelocked behind it.

```html
<!-- Result screen of the free calculator -->
<div class="calc-result">
  <p>Your estimated monthly spend: <strong>$2,840</strong></p>
  <p class="muted">Based on the inputs you entered. Not stored.</p>

  <aside class="reciprocity-cta">
    <p>If you want to compare this against our pricing, we publish a full breakdown.</p>
    <a href="/pricing" class="btn-soft">See pricing</a>
  </aside>
</div>
```

**Dark-pattern UI example.** A landing page promises a "free guide" but the download is gated behind a signup that auto-subscribes the user to a 12-email drip campaign with no unsubscribe link in the welcome email. The "gift" is actually a trojan horse for an email-marketing acquisition.

**The line.** A gift is a gift only if the user can use it without giving anything back. A gift that costs an email address is a transaction labelled as a gift; the user notices on the second visit and trust inverts.

**Breaks if.** The "free" thing requires a credit card. The free thing only works the first time. The follow-up CTA appears as a modal overlay on the result screen (the user feels ambushed). The gift is the same content the user could find on the marketing blog without signing up (it's not really a gift, it's a recategorisation).

## Commitment and consistency — small yes then big yes

**Mechanism.** People want their behaviour to be consistent with prior choices. A small public commitment (clicking a "I'm interested" button, selecting a use-case on a landing page, taking a 2-question quiz) creates a self-perception that biases subsequent decisions toward consistency with the first.

**Ethical UI example.** A pricing page presents the same plans as three personalised columns, depending on a one-question selector at the top: "What's your team size? `< 10` / `10-50` / `50+`". The user clicks `10-50`, and the page rerenders with the mid-tier plan recommended (with a soft "Recommended for teams like yours" badge). The user has made a small public commitment (team size) and the page now shows them a consistent next step (the matching plan). All three plans are still visible; the recommendation is a suggestion, not a removal.

```html
<div class="team-size-selector">
  <p>How big is your team?</p>
  <div class="btn-group">
    <button data-team="small">Under 10</button>
    <button data-team="mid" aria-pressed="true">10 – 50</button>
    <button data-team="large">50+</button>
  </div>
</div>

<div class="pricing-grid">
  <article class="plan">…</article>
  <article class="plan plan--recommended">
    <span class="badge">Recommended for teams like yours</span>
    …
  </article>
  <article class="plan">…</article>
</div>
```

**Dark-pattern UI example.** A multi-step signup asks for an email on step 1, then progressively for credit card, billing address, mailing-list opt-ins on steps 2–4, with no "back" button and a progress bar that lies about how much is left. Each step exploits the user's prior commitment to finishing; the friction the user expected (a credit card form) appears only after the user has invested 60 seconds and feels too far in to leave.

**The line.** A multi-step flow is honest when each step's purpose is announced *before* the user starts. "5 questions, takes 60 seconds, no credit card" → users finish more than half the time. "Get started for free" → credit card on step 3 → users feel tricked. The phrase "no credit card required" is one of the highest-converting micro-copy patterns precisely because it short-circuits this anxiety.

**Breaks if.** The progress bar lies (says 2/3 when it's actually 2/8). The first step is trivial (email only) but the last step is a 9-field credit-card form. The user can't go back without losing all prior input. The flow's commitment is treated as a contract instead of a soft yes — once the user starts, they can't change their mind without re-entering everything.

## Social proof — what others did

**Mechanism.** When uncertain, people imitate similar others. The closer the proof-source matches the visitor's self-image, the stronger the effect. Numeric scale also matters: "10,000+ companies trust us" is weak; "Stripe, Notion, and Linear use this" is strong if the visitor admires those companies.

**Ethical UI example.** A B2B SaaS landing page shows 6 customer logos above the fold, all real and recognisable in the target market. Below the logos, three testimonial cards with the customer's name, role, company, photo, and a 2-sentence quote about a specific problem the product solved. Each testimonial is linked to a case-study page with full context. The numbers ("trusted by 8,000+ teams") appear once, near the testimonials, and are independently verifiable on the company's customer-list page.

```html
<section class="proof">
  <p class="proof__lead">Used by teams at</p>
  <div class="proof__logos">
    <img src="/logos/stripe.svg" alt="Stripe">
    <img src="/logos/notion.svg" alt="Notion">
    <img src="/logos/linear.svg" alt="Linear">
    <!-- ... 3 more ... -->
  </div>

  <div class="proof__testimonials">
    <figure>
      <blockquote>Cut our onboarding time from 3 days to 4 hours. The default
        templates covered 80% of our cases out of the box.</blockquote>
      <figcaption>
        <img src="/avatars/jane.jpg" alt="">
        <strong>Jane Park</strong>, Engineering Lead at <a href="/case/acme">Acme</a>
      </figcaption>
    </figure>
    <!-- ... 2 more ... -->
  </div>
</section>
```

**Dark-pattern UI example.** A landing page shows a live activity feed: "Someone in Berlin just signed up — 12 seconds ago", "Someone in Tokyo just upgraded — 38 seconds ago". The names are pulled from a wordlist, the cities from the visitor's IP geolocation, and the timestamps are random. A 30-second DevTools session reveals the JavaScript that generates them; the brand permanently loses credibility for anyone who notices.

**The line.** Real social proof is verifiable: real names, real photos (or none — better than stock), real companies with public attribution, real numbers that match the public customer-list page. Fake social proof is the most reverse-engineerable dark pattern on the web; anyone with DevTools and a curious mood can expose it in under a minute.

**Breaks if.** Testimonials use stock-photo headshots (reverse-image-search finds the iStock URL in seconds). The customer logo strip includes companies that never used the product (legally actionable in most jurisdictions). The "10,000+ users" number is unverifiable and gets repeated unchanged for 3 years. Review counts have no review platform link backing them up.

## Authority — credible sources

**Mechanism.** People defer to experts and to symbols of expertise (titles, certifications, peer-reviewed citations, recognisable employer logos). The deference is strongest when the authority is *relevant to the decision* — a doctor's endorsement of a medical device, a security engineer's endorsement of a security tool.

**Ethical UI example.** A security product's landing page features a quote from the CISO of a recognisable company, with the person's actual title, photo (real), LinkedIn link, and a 2-sentence specific endorsement: "We adopted X after auditing 4 alternatives; the SOC 2 Type II audit trail was the deciding factor." Below the quote, the actual SOC 2 audit certificate is linked (PDF) along with the auditor's name. The authority is named, verifiable, and the claim is specific.

```html
<aside class="authority">
  <blockquote>We adopted Foo after auditing 4 alternatives; the SOC 2
    Type II audit trail was the deciding factor.</blockquote>
  <figcaption>
    <img src="/people/alex-park.jpg" alt="">
    <p><strong>Alex Park</strong>, CISO at <a href="https://example.com">Example Corp</a></p>
    <p class="muted">
      <a href="https://linkedin.com/in/alexpark">LinkedIn</a> ·
      <a href="/audits/soc2-2025.pdf">SOC 2 Type II audit (2025)</a>
    </p>
  </figcaption>
</aside>
```

**Dark-pattern UI example.** A health-supplement page shows a stock photo of a person in a white coat with a stethoscope and a quote "As a doctor, I recommend X to my patients." There is no name, no medical board, no credentials. The white coat is the only authority signal. The visitor's gut says "doctor"; the explicit content says nothing verifiable.

**The line.** Authority needs a name, a credential, and a way to verify both. A title without a name is theater. A name without a credential check is theater. An endorsement quote without a specific reason is theater.

**Breaks if.** The "expert" is unnamed (or named but unsearchable). The credential is irrelevant to the decision (a yoga teacher endorsing financial software). The endorsement is a vague platitude ("life-changing") rather than a specific claim with a reason. The badge is purely decorative (a "Top SaaS 2025" badge from a publication that doesn't exist).

## Liking — relatability and warmth

**Mechanism.** People are more likely to be persuaded by sources they like. Liking is built through similarity (the source resembles me), familiarity (I've seen this brand before), praise (the source compliments me), and association (the source is paired with things I already like).

**Ethical UI example.** A productivity tool's landing page is written in second person ("you", "your team") and uses the language a target-customer would use ("standups", "PRs", "retros" for a dev-team product). The hero photo shows a small, diverse team in a real-looking office (not a stock-shoot of suits high-fiving). The about page has the founders' actual names, faces, and a short personal note about why they built the product. The brand voice is consistent across landing, docs, support emails, and the changelog.

```html
<section class="hero">
  <h1>The standup that doesn't waste your morning.</h1>
  <p>Async updates, threaded blockers, and a 9 AM digest. Built by a team
    that ran daily 30-minute Zoom standups for 4 years and got tired of it.</p>
  <a href="/signup" class="btn-primary">Try it free for 14 days</a>
  <p class="muted">No credit card. Cancel any time.</p>
</section>
```

**Dark-pattern UI example.** A landing page uses fake first-name personalisation ("Hi $first_name, welcome to X!") that breaks when the variable doesn't resolve, leaving "Hi $first_name" visible. Or worse — a sales email that mimics a personal note ("Hey Alex, I was browsing your LinkedIn and...") that is provably auto-generated by an LLM. Manufactured intimacy reads as creepy.

**The line.** Real liking is built by showing real humans, using the target audience's language without parodying it, and being internally consistent across all touchpoints. Fake liking is built by automated personalisation that doesn't survive a second visit.

**Breaks if.** Personalisation variables leak (`Hi $first_name`). The "team" page is the same 4 stock-photo headshots that other competitors also use. The brand voice on the landing page is friendly-startup but the support emails are robotic-corporate. The "we built this because..." story turns out to be the same story 6 other competitors tell.

## Scarcity — limited supply or time

**Mechanism.** People want what's hard to get; impending unavailability raises perceived value. Scarcity has two forms: supply ("only 3 left in stock") and time ("sale ends in 4 hours"). Both work; both are heavily abused.

**Ethical UI example.** A workshop-booking page shows the actual number of seats remaining (pulled from the booking system in real time), the actual workshop date, and a single calendar showing the actual ticket-sale close date. As seats sell, the number decrements. When the date passes, the page changes to "Sold out — join the waitlist for the next session."

```html
<section class="event">
  <h1>Async-first workshop, May 14</h1>
  <p class="event__capacity">
    <strong data-capacity="live">14 of 25 seats remaining</strong>
    <span class="muted">Registration closes May 7 at 23:59 UTC</span>
  </p>
  <button class="btn-primary">Register</button>
</section>

<script>
  // The number is fetched from the booking system on page load.
  // No JavaScript random decrement; if it shows 14, there are 14.
</script>
```

**Dark-pattern UI example.** An e-commerce product page shows "Only 2 left!" on every product variant, every day, regardless of actual inventory. A countdown timer "Sale ends in 4:32:18" resets to 5 hours every time the page is refreshed. Both signals are noise; both train regular customers to ignore all urgency cues from the site, including the real ones during legitimate sales.

**The line.** Scarcity is honest when the constraint is real and verifiable. A workshop has a real seat count. A flash sale has a real end time the team will not extend. A limited-edition product has a real production batch. Faked scarcity is the second-most-reverse-engineerable dark pattern on the web; visitors who notice never trust the site again.

**Breaks if.** The "only N left" number is the same on every product. The countdown timer resets on page refresh. The "sale ends" date passes without the prices going up. Limited-edition is a misnomer for "always in stock". The scarcity badge appears on items that have been in the store catalogue for 2 years.

## Compounding two principles in one block

The most common production case is two principles working together in one section. The compound is stronger than either alone, but only when the principles are compatible. The most useful compounds and their typical UI shapes:

| Compound | Typical UI |
|---|---|
| **Social proof + authority** | Customer logos paired with the customer's CISO or CTO testimonial. Both verifiable. |
| **Reciprocity + commitment** | Free tool → small commitment (save your result, get email reminder). The reciprocity earns goodwill; the commitment converts later. |
| **Scarcity + social proof** | "12 seats left. Last quarter's workshop sold out 3 days early." Real scarcity, real proof. |
| **Authority + liking** | A founder who is also a domain expert tells the company-origin story. The expertise builds authority; the personal voice builds liking. |
| **Commitment + reciprocity** | Multi-step assessment → personalised report at the end. Each step costs little; the final report is the gift. |

Incompatible compounds to avoid:
- **Liking + raw scarcity-urgent** — A warm relatable brand voice next to a flashing red countdown reads as a personality split.
- **Authority + dark scarcity** — A CISO testimonial next to fake "only 2 left" badges nukes the authority's credibility.
- **Social proof + fake authority** — A customer logo strip next to a stock-photo "doctor" makes both look fake.

## The ethical line — three filters

Before shipping any persuasion-heavy block, run it through three filters. If the answer to any is no, the pattern is a dark pattern and the brief gets pushed back.

1. **Is the underlying claim true?** Does the page actually have N seats left? Did Stripe actually use the product? Is the doctor actually a doctor? If no, the pattern is fraud — not just a dark pattern.
2. **Is the claim verifiable in 30 seconds by the visitor?** Can a curious visitor open DevTools, refresh the page, or check the company's customer list and confirm the claim? If verification fails, the pattern is reverse-engineerable and trust will collapse on the second visit.
3. **Would the visitor still take the action if they understood the mechanism?** Would they still sign up for the trial knowing the gift is real? Would they still buy the workshop knowing the seats are real? If no, the pattern is exploiting an asymmetry the visitor would object to.

A pattern that passes all three filters is honest persuasion. A pattern that fails any one is a dark pattern; the `amw-legal-expert-agent` has VETO power on dark patterns that risk GDPR / FTC / consumer-protection exposure.

## Breaks if

- The persuasion block compounds two principles that fight each other (warm voice + red urgency banner; expert authority + fake testimonials).
- The visual loudness order (in the token block above) gets inverted — scarcity colors louder than primary CTA only when the scarcity is real and the page is genuinely the last-chance moment.
- Any persuasion claim cannot survive a 30-second DevTools verification; reverse-engineerable dark patterns invert the conversion effect on repeat visits.
- The team treats this file as a copy-paste list of CTAs instead of a set of principles. The principles describe what makes humans persuasive; the UI patterns are the local implementation. Re-implement the principle for the project's tone, never paste the example verbatim.

## Cross-references

- [TECH-influence-and-persuasion.md](TECH-influence-and-persuasion.md) — R3 sibling with the one-liner catalogue, the 8-category friction audit, and CRO conversion-impact numbers.
- [TECH-fogg-behavior-model.md](TECH-fogg-behavior-model.md) — B = M × A × T frames where each Cialdini principle plugs in (Trigger = scarcity cue; Motivation = social proof; Ability = no-credit-card friction removal).
- [TECH-loss-aversion-pricing.md](TECH-loss-aversion-pricing.md) — anchoring, framing, and endowment effect compound with reciprocity and commitment on pricing pages.
- [TECH-microcopy-patterns.md](TECH-microcopy-patterns.md) — concrete CTA copy variants that bake in the principles described here.
- [TECH-form-multi-step.md](TECH-form-multi-step.md) — commitment-and-consistency applied to long forms, with progress-bar honesty rules.
- [ai-slop-avoid.md](../ai-slop-avoid.md) — plugin-wide rejection of fake-urgency, fake-testimonials, manipulative defaults.
- [authority-hierarchy.md](authority-hierarchy.md) — `amw-legal-expert-agent` has VETO on any persuasion block that fails the three-filter ethical check.
