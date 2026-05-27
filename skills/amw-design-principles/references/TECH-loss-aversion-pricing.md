<!-- Clean-room synthesis of Kahneman & Tversky's published prospect-theory and loss-aversion research as commonly reproduced in behavioural-economics and pricing literature. No copyrighted-book passages reproduced; concepts re-explained in plugin-original prose. Authored for batch9 Wave 2 Round 4, T-168. -->

---
name: TECH-loss-aversion-pricing
category: design-principles-process
source: clean-room synthesis of Kahneman-Tversky prospect theory and loss-aversion research (batch9 Wave 2 Round 4, T-168)
license: MIT (plugin-original under ../../../LICENSE)
also-in: TECH-cialdini-influence-principles.md (anchoring composes with social proof; endowment composes with reciprocity); TECH-fogg-behavior-model.md (loss framing is a Motivation lever); TECH-microcopy-patterns.md (concrete pricing-CTA copy); TECH-form-validation-patterns.md (default checkbox states matter for opt-in/opt-out)
---

# Loss aversion — pricing, checkout, and default-state design

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [The four mechanisms in one paragraph](#the-four-mechanisms-in-one-paragraph)
- [Token block — pricing-page variables](#token-block--pricing-page-variables)
- [Anchoring — the reference price beats the actual price](#anchoring--the-reference-price-beats-the-actual-price)
- [Framing — gain vs loss is not symmetric](#framing--gain-vs-loss-is-not-symmetric)
- [Endowment — what they have is worth more than what they don't](#endowment--what-they-have-is-worth-more-than-what-they-dont)
- [Defaults — pre-selected state is the chosen state](#defaults--pre-selected-state-is-the-chosen-state)
- [The ethical line — defaults vs dark patterns](#the-ethical-line--defaults-vs-dark-patterns)
- [Worked example — trial-end conversion](#worked-example--trial-end-conversion)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Catalogues four loss-aversion mechanisms from behavioural-economics research and maps each to a concrete pricing / checkout / consent UI pattern.

The four mechanisms:
1. **Anchoring** — the first number the visitor sees becomes the reference; every other number is judged relative to it.
2. **Framing** — losing X feels worse than gaining X feels good (roughly 2× as strong). Same outcome, different copy, different conversion.
3. **Endowment** — possession changes value. What the user has (trial data, custom workflows, saved templates) is worth more to them than the same thing offered to a non-owner.
4. **Defaults** — the pre-selected option has 5–10× the take-rate of the same option offered as a positive choice.

This file gives the UI patterns and the boundary between honest application (acceptable, increases conversion) and dark-pattern application (unacceptable, eventually punished by regulators and trust collapse).

## When this file fires

- "Redesign the pricing page" / "trial-to-paid is too low" / "users abandon at checkout"
- "Should the annual plan be the default?" / "should auto-renew be opt-in?"
- "Frame this as a saving or a discount?" / "how do we show the strikethrough price?"
- A flow that asks the user to consent to recurring charges, marketing emails, data sharing

Do NOT read this file for:
- Pure free / no-charge flows where there's no pricing surface
- Documentation / API reference pages
- Compliance pages (the regulated copy overrides framing tactics)

## The four mechanisms in one paragraph

The brain doesn't process numbers absolutely; it processes them relative to a reference point. The reference point is set by the first number the visitor sees (anchoring). Once a reference exists, losses below it feel about twice as strong as gains above it (loss aversion). What the user already possesses raises the reference (endowment), and the pre-selected option signals what the designer considers the reference (defaults). All four mechanisms move in the same direction: the visitor minimises the distance from their reference. The product team's job is to set the reference honestly and let the visitor move toward it.

## Token block — pricing-page variables

```css
:root {
  /* Anchor / strike-through pricing */
  --price-original: oklch(55% 0.02 250);     /* muted, smaller */
  --price-original-decoration: line-through;
  --price-current: oklch(20% 0.02 250);      /* loud, large */
  --price-savings: oklch(60% 0.15 145);      /* trust green */

  /* Annual-vs-monthly toggle */
  --plan-toggle-bg: oklch(96% 0.01 250);
  --plan-toggle-active-bg: oklch(20% 0.02 250);
  --plan-toggle-active-fg: oklch(98% 0.005 250);
  --plan-toggle-savings-badge: oklch(60% 0.15 145);

  /* Recommended plan emphasis */
  --plan-recommended-border: oklch(60% 0.20 250);
  --plan-recommended-shadow: 0 6px 24px oklch(60% 0.20 250 / 0.15);
  --plan-recommended-badge: oklch(60% 0.20 250);

  /* Plan-card hierarchy */
  --plan-card-bg: oklch(99% 0.005 250);
  --plan-card-border: oklch(90% 0.02 250);
  --plan-card-shadow: 0 1px 2px oklch(0% 0 0 / 0.06);

  /* Sizes */
  --price-current-size: clamp(2rem, 4vw, 3rem);
  --price-original-size: 1rem;
  --price-savings-size: 0.875rem;
}
```

Three rules that always hold:
1. The current price (loud) must be the visual focus; the strikethrough (muted) is supporting.
2. The recommended plan gets exactly one badge and one border-color emphasis; loud-on-loud reads as desperate.
3. Any "save 30%" claim must be derivable from the displayed numbers; if a reader can't do the math, the claim is decoration.

## Anchoring — the reference price beats the actual price

**Mechanism.** The first number the visitor sees sets the reference. A $99 plan looks expensive on its own; the same $99 plan next to a $299 plan looks like a bargain. The reference doesn't have to be a real alternative — even a struck-through "original price" with no historical basis still anchors.

**Ethical pattern.** Show real comparison points. Three real plans at $19, $49, $149, with the middle plan badged "Most popular" so the anchor is established by genuine peer pricing. If the team genuinely lowered the price, show the actual prior price as a strikethrough with a date ("$59 → $49 since May 1").

```html
<section class="pricing">
  <div class="plan plan--basic">
    <h3>Solo</h3>
    <p class="price"><span class="price__current">$19</span> /month</p>
    <ul>…</ul>
    <button>Start free trial</button>
  </div>

  <div class="plan plan--recommended">
    <span class="plan__badge">Most popular</span>
    <h3>Team</h3>
    <p class="price"><span class="price__current">$49</span> /month</p>
    <p class="price__per-seat">$10 per seat included</p>
    <ul>…</ul>
    <button class="btn-primary">Start free trial</button>
  </div>

  <div class="plan plan--enterprise">
    <h3>Enterprise</h3>
    <p class="price"><span class="price__current">$149</span> /month</p>
    <p class="price__per-seat">Unlimited seats</p>
    <ul>…</ul>
    <button>Talk to sales</button>
  </div>
</section>
```

**Dark pattern.** Strikethrough an "original price" that the product was never sold at. Common in e-commerce: a $40 t-shirt with "$80" struck through and "50% off!" plastered on it; the $80 price exists only in this banner. Increasingly regulated (EU Directive 98/6/EC requires the strikethrough to be the lowest price from the preceding 30 days; US states are tightening similar rules).

**The line.** A strikethrough is honest when the strikethrough price is verifiable — a date the product was actually sold at that price, a peer plan that genuinely costs more, a competitor's actual public price. The line moves on jurisdiction: EU is strict, US patchwork, but the safe rule is "if you can't show the receipt at the higher price, don't show the strikethrough."

**Concrete UI cases.**
- Annual plan shows "$10/mo billed annually" with "$15/mo billed monthly" struck through. Both are real; both are the team's published prices. Acceptable.
- One-time purchase with "WAS $79 — NOW $39" and the $79 price never existed on the public site. Dark pattern. Increasingly illegal.
- "Compare against the alternative: typical agency engagement is $5,000-$10,000". Anchoring through a non-product comparison. Acceptable if the comparison is genuine and verifiable.

## Framing — gain vs loss is not symmetric

**Mechanism.** Losing $30 feels worse than gaining $30 feels good, by roughly a 2:1 ratio. The same outcome framed as a loss converts higher than framed as a gain, when the user already feels they have the thing.

**Ethical pattern.** Frame *real* losses that the user genuinely experiences. A trial-end banner that says "Your 12 workflows will pause on May 22 unless you upgrade" is loss-framed and accurate; the workflows do pause. A renewal-reminder email that says "Your subscription expires Friday — you'll lose access to your team's saved templates" is loss-framed and accurate; the access does end.

**Gain frame vs loss frame in pricing copy:**

| Same outcome | Gain frame | Loss frame |
|---|---|---|
| Upgrade saves time | "Save 2 hours/day" | "Stop losing 2 hours/day" |
| Annual plan is cheaper | "Save $120/year with annual" | "Stop paying 25% more on monthly" |
| Feature unlocks | "Get unlimited workflows" | "Don't get capped at 5 workflows" |
| Trial-end | "Upgrade to keep your data active" | "Your data pauses if you don't upgrade" |

Loss frames typically convert 1.5–2× higher than the matched gain frame — but only when the loss is real. Loss-framing a non-existent loss reads as fear-mongering and inverts the effect.

**Dark pattern.** Frame an *invented* loss to drive conversion. "Don't lose your spot — only 3 left!" on inventory the company has 10,000 of. "Don't miss out on our biggest sale ever" when the same sale runs every quarter. The loss isn't real; the user's gut detects it on the second visit; trust collapses.

**The line.** Loss-frame what the user actually has. Don't loss-frame what they don't have. "Lose your saved data" is honest if the data does pause. "Lose your discount" is honest if the discount does expire. "Lose your spot" is dishonest if there is no real spot to lose.

## Endowment — what they have is worth more than what they don't

**Mechanism.** Possession changes value by 2-4× in lab experiments. The user with a free-trial dashboard full of their own data values that dashboard more than a non-user evaluating the same feature list. The implication: free trials, user-generated content, and customisation are conversion engines because they create endowment.

**Ethical pattern.** A 14-day free trial that lets the user import real data, build real workflows, save real preferences. On day 11, a banner appears: "Your workspace: 47 records, 12 workflows, 5 saved views. To keep these active after May 22, add payment." The user is being shown what they've *built*, not what they could *have*; endowment is real.

```html
<aside class="trial-status" data-day="11-of-14">
  <h3>Your trial ends in 3 days</h3>
  <dl class="trial-status__inventory">
    <div><dt>Records</dt><dd>47</dd></div>
    <div><dt>Workflows</dt><dd>12</dd></div>
    <div><dt>Saved views</dt><dd>5</dd></div>
    <div><dt>Team members invited</dt><dd>3</dd></div>
  </dl>
  <p>After May 22, workflows pause and views become read-only. Your data
    is preserved indefinitely — you can re-enable everything any time
    by upgrading. No data deletion.</p>
  <a href="/billing" class="btn-primary">Upgrade to keep workflows active</a>
</aside>
```

**Dark pattern.** Block access to *all* user data at trial end, even read-only, even after a graceful pause. The trial users built real content; locking them out completely is engineering hostility, not endowment. They churn; they write angry reviews; the conversion lift on the desperate few is dwarfed by the long-term acquisition damage.

**The line.** Honest endowment shows the user what they built and frames the upgrade as keeping it active. Dark endowment uses access-revocation as a hostage situation. The difference is whether the user can keep their data (or export it) even if they don't upgrade.

**Cross-link.** Endowment is the mechanism behind the second worked example in `TECH-fogg-behavior-model.md`. The Motivation lever there is loss aversion; the loss is endowment-based.

## Defaults — pre-selected state is the chosen state

**Mechanism.** Pre-selected options take 5–10× the rate of the same option offered as an explicit choice. The pre-selection signals "this is the recommendation" and the visitor has to actively choose otherwise. The mechanism is partly cognitive (each opt-out is a decision the user has to make) and partly motivational (deviating from the default feels like a stronger commitment than going with it).

**Ethical default — annual plan pre-selected.** The annual-monthly toggle defaults to annual on a fresh page load, with "Save 25%" badged. The user can flip to monthly with one click. Both options are visible; the price is honestly displayed for both. The pre-selection signals the team's recommendation; the cost is genuinely lower.

```html
<div class="billing-toggle">
  <button data-billing="monthly">Monthly</button>
  <button data-billing="annual" aria-pressed="true">
    Annual
    <span class="badge">Save 25%</span>
  </button>
</div>

<div class="plan" data-current-billing="annual">
  <p class="price">
    <strong>$15</strong>
    <span class="muted">/month, billed annually</span>
  </p>
  <p class="price__monthly-equivalent muted">$20/month if billed monthly</p>
</div>
```

**Ethical default — newsletter opt-in.** A signup flow includes "Email me product updates (about 1/month)" as an UNCHECKED checkbox, with clear copy about what the email is and how to unsubscribe. The pre-selection signals "your call"; the conversion is lower than a pre-checked box would be, but the signups are qualified and GDPR-compliant.

**Dark default — pre-checked marketing-email opt-in.** A signup flow includes "Subscribe to our weekly newsletter, promotions, partner offers, and surveys" as a PRE-CHECKED checkbox, often near the bottom of a form full of other settings. Most users don't notice; subscriber count inflates; engagement collapses because the subscribers never wanted to be there.

**Dark default — auto-enrol in paid plan after free trial.** The free trial requires a credit card upfront. The default behaviour is "auto-charge on day 15 unless cancelled". The user has to remember to cancel. The signup copy buries this; the chargebacks pile up.

**The line.** Defaults are ethical when they're the team's honest recommendation and the user can reverse them in one click. Defaults are dark patterns when the user is opted into something they would not have actively chosen and reversing it takes more than one click. The GDPR test is simple: any opt-in for marketing / tracking / data sharing must be unchecked by default and must require an affirmative click. EU regulators have fined dozens of companies for pre-checked consent boxes.

## The ethical line — defaults vs dark patterns

A three-question filter every default-pre-selection has to pass:

1. **Is the pre-selected option the user's most likely informed preference?** If most informed users would choose this, the default is honest. If most informed users would actively reject it, the default is a dark pattern.
2. **Can the user reverse the default in one click on the same screen?** If yes, the default is honest friction-reduction. If reversal requires 3 clicks, a phone call, or an email exchange, it's a dark pattern.
3. **Does the default comply with applicable consent law (GDPR, CCPA, ePrivacy, COPPA)?** Marketing emails, behavioural tracking, data sharing must be opt-in (unchecked default) in the EU and several US states. Pre-checked = legal exposure.

A pattern passing all three is acceptable. Failing any one is a dark pattern; the `amw-legal-expert-agent` has VETO power on patterns that fail filter 3.

## Worked example — trial-end conversion

**Setup.** A SaaS product offers a 14-day free trial that imports the user's data, builds workflows, and saves preferences. Trial-to-paid conversion is 8%; industry benchmark is 15–25%.

**Diagnosis (using the four mechanisms).**
- **Anchoring** — pricing page shows only one plan ($49/mo). No reference point; the price feels expensive.
- **Framing** — trial-end email says "Upgrade to unlock unlimited workflows" (gain frame). The user doesn't feel they have anything to lose.
- **Endowment** — trial-end email doesn't mention the user's actual data. The user doesn't know they've built 47 records, 12 workflows, 5 saved views.
- **Defaults** — annual plan toggle defaults to monthly. Users pick monthly because it's default; revenue per signup is lower.

**Fix.**

1. **Anchoring** — add three plans ($19 / $49 / $149) with the middle plan badged "Most popular". The $49 plan now has a peer reference.
2. **Framing** — change trial-end email to "Your 12 workflows pause on May 22 — upgrade to keep them active". Loss frame on a real loss.
3. **Endowment** — embed the trial-status inventory (47 records, 12 workflows, 5 saved views) inside the email and the in-app banner. The user sees what they've built.
4. **Defaults** — pricing page defaults to annual billing with "Save 25%" badged. Users flip to monthly only if they prefer it.

**Outcome.** Trial-to-paid lifts to 18-22% (matches industry benchmark). Average revenue per signup grows ~20% from the annual-plan default. No dark patterns introduced; every claim is verifiable.

## Breaks if

- Strikethrough prices show numbers the product was never sold at; EU regulators and US AGs are pursuing this aggressively.
- Loss-framing is applied to losses the user doesn't actually have; the visitor returns and notices nothing was at risk.
- Endowment is engineered through access-revocation hostility rather than genuine user-built value.
- Defaults sneak users into recurring charges or marketing-email lists they wouldn't have actively chosen. Regulators fine; trust collapses.
- All four mechanisms are stacked on the same page at maximum loudness. Pricing pages turn into infomercials; conversion can *fall* below the baseline.

## Cross-references

- [TECH-cialdini-influence-principles.md](TECH-cialdini-influence-principles.md) — anchoring composes with social proof on pricing pages; endowment composes with reciprocity.
- [TECH-fogg-behavior-model.md](TECH-fogg-behavior-model.md) — loss-aversion framing is a Motivation lever; the second worked example in that file uses endowment.
- [TECH-microcopy-patterns.md](TECH-microcopy-patterns.md) — concrete pricing-CTA copy that bakes in the loss frame and the savings badge.
- [TECH-form-validation-patterns.md](TECH-form-validation-patterns.md) — default checkbox states for opt-in / opt-out compliance.
- [TECH-influence-and-persuasion.md](TECH-influence-and-persuasion.md) — R3 sibling with the 8-category friction audit (defaults audit is one category).
- [ai-slop-avoid.md](../ai-slop-avoid.md) — rejects fake strikethrough prices, fake countdown timers, pre-checked consent boxes.
- [authority-hierarchy.md](authority-hierarchy.md) — `amw-legal-expert-agent` has VETO on defaults that fail GDPR / CCPA consent law.
