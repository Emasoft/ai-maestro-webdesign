---
name: TECH-fogg-behavior-model
category: design-principles-process
source: clean-room synthesis of Fogg Behavior Model (batch9 Wave 2 Round 4, T-167)
license: MIT (plugin-original under the plugin root LICENSE file)
also-in: TECH-cialdini-influence-principles.md (Motivation lever maps to scarcity/social-proof; Trigger lever maps to authority/reciprocity); TECH-loss-aversion-pricing.md (Motivation through pain-avoidance framing); TECH-microcopy-patterns.md (Triggers are usually copy); TECH-form-validation-patterns.md (Ability barrier reduction)
---

<!-- Clean-room synthesis of B.J. Fogg's published Behavior Model (B = M × A × T) as commonly reproduced in HCI and product-design literature. No copyrighted-book passages reproduced; framework re-explained in plugin-original prose. Authored for batch9 Wave 2 Round 4, T-167. -->

# Fogg Behavior Model — when each lever matters

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [The model in one line](#the-model-in-one-line)
- [Token block — CTA-state variables](#token-block--cta-state-variables)
- [Motivation — when to raise it](#motivation--when-to-raise-it)
- [Ability — when to lower the barrier](#ability--when-to-lower-the-barrier)
- [Trigger — when to add the cue](#trigger--when-to-add-the-cue)
- [Diagnosing a low-converting CTA](#diagnosing-a-low-converting-cta)
- [Two worked UI examples](#two-worked-ui-examples)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

The Fogg Behavior Model says a behaviour happens only when motivation, ability, and a trigger converge at the same moment: **B = M × A × T**. Any of the three at zero means the behaviour does not happen. The model is a diagnostic tool, not a checklist: when a CTA is underperforming, you ask which of the three is missing.

The web-design version of the model:
- **Motivation** — why would the visitor act *now*? Pleasure / pain / hope / fear / social acceptance / rejection.
- **Ability** — how easy is the action? Time / money / physical effort / mental effort / social deviance / non-routine.
- **Trigger** — what cue tells them to act now? Visible CTA, notification, scarcity badge, completed-progress nudge.

This file maps each lever to the concrete UI affordances that raise or lower it, with explicit guidance on which lever to pull when conversion is low.

## When this file fires

- "This CTA isn't converting" / "drop-off at this step is too high" / "users see the button but don't click"
- "Should we add urgency?" / "should we shorten the form?" / "should we change the button copy?"
- A pricing page or signup flow needs diagnosis, not redesign
- The team has 10 hypotheses and needs a framework to prioritise

Do NOT read this file when:
- The product itself isn't ready (the bottleneck is not the funnel)
- The traffic isn't qualified (no motivation upstream → no funnel optimisation will fix it)
- The page is a pure documentation surface with no conversion goal

## The model in one line

**Behaviour happens at the intersection of Motivation, Ability, and a Trigger.** All three must clear a threshold simultaneously. If a visitor has high motivation and low ability, even a perfect trigger fails. If a visitor has high ability and a clear trigger but low motivation, the action doesn't happen. The product team's job is to identify which lever is below threshold and pull it up.

The classic Fogg diagram plots motivation on the Y axis, ability on the X axis, and draws a downward-sloping "action threshold" curve. Triggers above the curve produce behaviour; triggers below it do not. High motivation can compensate for low ability (people will struggle through a complex form if they want the thing badly), and high ability can compensate for low motivation (people will tap a frictionless button for things they're only mildly curious about).

## Token block — CTA-state variables

CTA buttons have visual states that correspond to Motivation × Ability × Trigger combinations. Bind these in `design-tokens.css`:

```css
:root {
  /* Primary CTA — the visible Trigger */
  --cta-bg: oklch(60% 0.20 250);
  --cta-fg: oklch(98% 0.005 250);
  --cta-bg-hover: oklch(55% 0.22 250);
  --cta-shadow: 0 1px 2px oklch(0% 0 0 / 0.1);

  /* Reassurance row (lowers anxiety = raises Motivation indirectly) */
  --cta-reassure-fg: oklch(55% 0.02 250);
  --cta-reassure-size: 0.8125rem;

  /* Ability indicator (e.g. "Takes 30 seconds") */
  --cta-ability-bg: oklch(96% 0.01 250);
  --cta-ability-fg: oklch(35% 0.05 250);

  /* Secondary CTA (lower-commitment branch) */
  --cta-secondary-bg: transparent;
  --cta-secondary-fg: oklch(40% 0.05 250);
  --cta-secondary-border: oklch(85% 0.02 250);
}
```

The standard CTA stack from top to bottom is: button (Trigger) → reassurance copy (Motivation lift) → ability indicator (Ability proof). All three pieces visible at once communicate that the friction is real-low without overpromising.

## Motivation — when to raise it

Motivation is the visitor's reason to act *now*, not in 6 months. Six common motivation levers from web research:

| Lever | UI surface | When it works | When it backfires |
|---|---|---|---|
| **Pain avoidance** | "Stop losing 2 hours/day to standup meetings" | Audience has lived the pain | Audience hasn't experienced the pain → reads as hypothetical |
| **Hope of gain** | "Cut your AWS bill by 30%" | Specific, quantified | Vague ("save money") → reads as marketing-speak |
| **Social acceptance** | "Join 8,000 engineering teams using X" | Numbers are real and recognisable | Inflated or unverifiable → trust collapses |
| **Fear of missing out** | "Sale ends Friday" | Constraint is real | Fake countdown → reverse-engineerable in seconds |
| **Curiosity** | "See your team's workflow as a heatmap" | Visualisation is genuinely novel | Promised insight doesn't materialise → bounce |
| **Identity alignment** | "For teams who ship every day" | Audience self-identifies | Vague "for ambitious builders" → reads as everyone |

Raise motivation when:
- The product is genuinely good but the value isn't visible in 5 seconds. Add a calculator, a before/after screenshot, a 30-second demo video.
- The CTA is fine but the visitor's reason-to-act-now is unclear. Add a specific number ("save 30%"), a deadline ("offer until Friday"), or a peer reference ("Used by Stripe, Notion, Linear").
- The visitor has high ability (the form is one field) but conversion is still low. The bottleneck is motivation, not friction.

Do NOT raise motivation by:
- Inventing urgency that isn't real. The visitor returns, sees the same countdown, and stops trusting all your CTAs.
- Inflating social-proof numbers. One reverse-image-search on a stock-photo testimonial collapses the whole proof block.
- Stacking 6 different motivation levers in one section. The page reads as desperate; trust drops.

## Ability — when to lower the barrier

Ability is what the visitor has to give up (time, money, cognitive effort, identity stretch) to act. Lower the barrier when the friction is causing the drop-off.

Five common ability levers:

| Lever | UI surface | Friction reduction |
|---|---|---|
| **Time cost** | "Takes 30 seconds" / progress bar with 3 steps | Visible upfront, accurate |
| **Money cost** | "Free for 14 days, no credit card" | Removes the largest barrier |
| **Mental effort** | Smart defaults / pre-filled fields / one-click options | Each removed decision = +10–20% conversion |
| **Physical effort** | Single-click signup / SSO / passkey | One click vs typing email + password |
| **Social deviance** | "Join 8,000+ teams" (the action is normal) | Reduces the "am I weird?" check |

Lower the ability barrier when:
- The motivation is high (the visitor clearly wants the product — they read 3 pages, scrolled to pricing) but conversion is still low. The bottleneck is friction.
- The signup flow has 5+ fields and the visitor's job-to-be-done doesn't require all 5 upfront. Move fields to onboarding-after-signup.
- The credit card requirement appears on step 1 of a trial flow. Move it to the end, after the user has experienced value.
- The form errors are inline-visible only after submit. Add live validation; conversion lifts 10–15% on average.

Do NOT lower the ability barrier by:
- Hiding the real cost. "Free trial" that auto-bills without warning is a dark pattern, not friction removal.
- Removing legally-required steps (consent, age check, jurisdictional disclaimer). Compliance overrides conversion.
- Removing the credit card requirement when the product cannot survive without paying users. The visitors who sign up are unqualified; conversion of trial→paid will be brutal.

## Trigger — when to add the cue

The Trigger is the cue that tells the user "act now". Triggers come in three forms:

1. **Spark** — the trigger raises motivation in the moment of action (e.g. a scarcity badge appearing as the user reaches the pricing section). Used when motivation is low.
2. **Facilitator** — the trigger lowers the friction in the moment of action (e.g. a "use Google to sign up" button as the user reaches the form). Used when ability is low.
3. **Signal** — the trigger is a plain reminder ("Sign up" button, notification ping). Used when motivation and ability are both above threshold; only the cue is missing.

When to add each:
- **Spark trigger** — the page has high ability (frictionless form) but low motivation. Add a value-proof element near the CTA (testimonial, before/after, calculator result). The trigger now carries motivation.
- **Facilitator trigger** — the page has high motivation (visitor scrolled 4 pages, read 3 testimonials) but the form looks long. Add a "sign in with Google" or "use a passkey" button next to the email form. The trigger now reduces friction.
- **Signal trigger** — the page is fine; the visitor just needs a clear button. Make the primary CTA the loudest element above the fold. No extra cleverness.

Triggers that fail:
- A primary CTA hidden in the middle of a 5-column footer.
- A primary CTA in the same visual weight as 4 secondary links.
- A primary CTA whose copy is generic ("Click here", "Submit"). The user can't predict what happens after the click.
- A primary CTA on a page with conflicting CTAs (signup + book a demo + download PDF + contact sales above the fold). Choice paralysis kills conversion 20–40%.

## Diagnosing a low-converting CTA

The model gives a 3-step diagnosis:

1. **Is the trigger visible?** Is the primary CTA the loudest element above the fold? Is the copy specific? Is it the only primary CTA on the page? If no → fix the trigger first; it's the cheapest fix.
2. **Is the motivation present?** Can the visitor articulate, in 5 seconds, why they should act *today*? If no → add a specific value-claim or social-proof block near the CTA.
3. **Is the ability barrier acceptable?** Can the visitor act in under 60 seconds with no credit card and no mental decisions? If no → shorten the form, add SSO, or move credit-card-required steps later.

In production, ~40% of low-converting CTAs are a trigger problem (the button is invisible or competes with peer CTAs), ~40% are an ability problem (the form is too long or requires payment too early), ~20% are a motivation problem (the value isn't visible above the fold). Trigger and ability fixes are cheap (1 day each); motivation fixes are expensive (require new content, photography, testimonials).

## Two worked UI examples

### Example 1 — SaaS signup page with low trial-conversion

**Symptom.** The landing page gets traffic, scroll depth is good, the pricing page is visited, but the signup flow has a 60% drop-off on step 1 (email + password).

**Diagnosis.**
- Motivation: high (visitors browsed 3 pages, scrolled to pricing — they want it).
- Ability: low. The form asks for email, password, password confirmation, full name, company name, role, and team size before the user has even seen the product.
- Trigger: fine. The signup button is visible.

**Fix.** Reduce the step-1 form to just email + magic-link (no password). Move the other fields to onboarding-after-first-login.

```html
<!-- Before -->
<form>
  <input type="email" required>
  <input type="password" required>
  <input type="password" required>     <!-- confirm -->
  <input type="text" required>          <!-- name -->
  <input type="text" required>          <!-- company -->
  <select required>                     <!-- role -->
    <option>Engineer</option><option>PM</option><option>Designer</option>
  </select>
  <input type="number" required>        <!-- team size -->
  <button>Sign up</button>
</form>

<!-- After -->
<form>
  <label>
    Email
    <input type="email" required autocomplete="email">
  </label>
  <button type="submit">Get the magic link</button>
  <p class="muted">No password. We'll email you a one-click sign-in link.</p>
</form>
```

**Outcome.** Conversion on step 1 typically lifts from 40% to 70–80%; net trial-signup volume grows 60–80%.

### Example 2 — Pricing page with low trial-to-paid conversion

**Symptom.** Trial signups are healthy. But trial-to-paid conversion is 8% where the industry benchmark is 15–25%.

**Diagnosis.**
- Trigger: fine. The "Upgrade" button is visible.
- Ability: fine. Credit card form is one step, 4 fields.
- Motivation: low. The trial dashboard doesn't show the user what they're about to lose at trial-end.

**Fix.** Add an in-app banner on day 11 of the trial: "Your data: 47 records, 12 workflows. After May 22, the workflows pause and you can re-enable any time by upgrading. No data lost." The Motivation is loss-aversion (TECH-loss-aversion-pricing.md) — what they built becomes the thing they don't want to lose.

```html
<aside class="trial-banner" data-day="11-of-14">
  <strong>Your trial ends in 3 days.</strong>
  <p>You've built 12 workflows across 47 records. After May 22, your
    workflows will pause — your data is preserved and you can re-enable
    them any time by upgrading.</p>
  <a href="/billing" class="btn-primary">Add payment to keep them active</a>
  <a href="/contact" class="btn-link">Have questions? Talk to us</a>
</aside>
```

**Outcome.** Trial-to-paid lifts from 8% to 15–18%. The motivation lever (loss avoidance) was the missing piece.

## Breaks if

- The team treats the model as a checklist ("we added urgency, social proof, and a CTA, so we're done"). The model is diagnostic: only pull the lever that's below threshold.
- The team raises all three levers at once. Maxing motivation + ability + trigger reads as desperate; trust drops; conversion can *fall*.
- The motivation lever is faked (invented urgency, inflated social proof). The model assumes honest signals; faked signals invert the conversion effect over time.
- The trigger is everywhere on the page (5 primary CTAs). Choice paralysis kills 20–40% of conversion; pick one primary CTA per page.
- The model is applied without measurement. Each lever-pull needs A/B data or qualitative session-recording analysis; running on intuition produces random walks.

## Cross-references

- [TECH-cialdini-influence-principles.md](TECH-cialdini-influence-principles.md) — Motivation lever maps to scarcity, social proof, authority; Trigger lever maps to reciprocity, commitment.
- [TECH-loss-aversion-pricing.md](TECH-loss-aversion-pricing.md) — Motivation through loss-aversion framing on pricing pages.
- [TECH-microcopy-patterns.md](TECH-microcopy-patterns.md) — Trigger copy (button labels, reassurance lines, ability indicators).
- [TECH-form-validation-patterns.md](TECH-form-validation-patterns.md) — Ability-barrier reduction via live validation.
- [TECH-form-multi-step.md](TECH-form-multi-step.md) — Ability-barrier management in long forms (progress disclosure).
- [TECH-form-async-submit.md](TECH-form-async-submit.md) — Trigger feedback after click (preserve momentum).
- [TECH-influence-and-persuasion.md](TECH-influence-and-persuasion.md) — R3 catalogue of CRO numbers per principle.
- [ai-slop-avoid.md](../ai-slop-avoid.md) — rejects faked motivation levers (fake urgency, fake proof).
