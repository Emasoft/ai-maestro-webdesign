---
name: TECH-landing-anatomy
category: design-principles-workflow
source: clean-room reimplementation (T-052 batch9 Wave 2; canonical 9-section landing-page anatomy is common knowledge in conversion-focused web design — see common UX/CRO references such as Cialdini, Halligan & Shah, Casey Winters)
license: this file = MIT (plugin license); NO verbatim copy from any GPL-2.0 source — described as standard CRO/SaaS landing patterns and 2024–2026 conventions
also-in: `amw-ascii-sketch` (uses this anatomy as default scaffold for new pages); `amw-wireframe-builder-agent` (renders each section per its conversion job); `amw-seo-strategist-agent` (validates H1/H2 maps onto Hero+Problem+Solution)
---

# Landing-page anatomy — the canonical 9 sections

## Table of Contents

- [What this is](#what-this-is)
- [When to use this anatomy](#when-to-use-this-anatomy)
- [The 9-section ASCII scaffold](#the-9-section-ascii-scaffold)
- [Per-section conversion job](#per-section-conversion-job)
- [Hero copy formula](#hero-copy-formula)
- [Banned CTA copy](#banned-cta-copy)
- [Variation rules](#variation-rules)
- [Cross-references](#cross-references)

## What this is

A canonical 9-section anatomy for marketing/landing pages, with the conversion job each section has to do. Used as the default scaffold for any new landing/SaaS/product page when no other reference exists. Every section is justified by what it makes the visitor *do* or *believe* next.

The 9 sections answer, in order: *Is this for me? Are others doing it? What problem? What's the answer? What do I get? How does it work? What does it cost? What's still unclear? What now?*

Skipping a section is allowed when its conversion job is genuinely unneeded (e.g., a free tool with no Pricing). Reordering is allowed only with explicit justification — the order is sequenced for cumulative trust.

## When to use this anatomy

- Phase A ASCII iteration when the user says "landing page," "homepage," "marketing page," "product page," or "SaaS page" without other reference.
- As a checklist when auditing a third-party landing page during competitive research.
- As the default scaffold inside `amw-ascii-sketch` when no DESIGN.md and no reference URL is provided.

NOT for: dashboards, app screens, internal tools, documentation pages, blog articles. Those have their own anatomies.

## The 9-section ASCII scaffold

```
┌──────────────────────────────────────────────────────┐
│ [NAV]  Logo    Product  Pricing  Docs     [Sign in]  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. HERO                                             │
│  ┌────────────────────────────────────────────────┐  │
│  │  [H1 — outcome for who]                        │  │
│  │  [Sub — how different]                         │  │
│  │  [Primary CTA]    [Secondary CTA]              │  │
│  └────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────┤
│  2. SOCIAL PROOF — logo row OR rating + count        │
├──────────────────────────────────────────────────────┤
│  3. PROBLEM — name the pain in their words           │
├──────────────────────────────────────────────────────┤
│  4. SOLUTION — your specific fix, one screenshot     │
├──────────────────────────────────────────────────────┤
│  5. FEATURES — 3 columns, icon + 1-line + 1 sentence │
├──────────────────────────────────────────────────────┤
│  6. HOW IT WORKS — 3 numbered steps                  │
├──────────────────────────────────────────────────────┤
│  7. PRICING — 2 or 3 tiers, middle highlighted       │
├──────────────────────────────────────────────────────┤
│  8. FAQ — 4–6 questions, accordion                   │
├──────────────────────────────────────────────────────┤
│  9. FINAL CTA — restate outcome, single button       │
├──────────────────────────────────────────────────────┤
│ [FOOTER]  Legal / Social / Sitemap                   │
└──────────────────────────────────────────────────────┘
```

This is the canonical scaffold the orchestrator hands to `amw-ascii-sketch` when the user says "landing page" with no further detail.

## Per-section conversion job

| # | Section | Conversion job | Pass criterion |
|---|---|---|---|
| 1 | **Hero** | Answer "is this for me?" in 5 seconds | Visitor can paraphrase the value in their own words after one read of H1+sub |
| 2 | **Social proof** | Answer "are others doing this?" | Either 4+ recognizable logos, OR a quantified rating ("4.8/5 from 2,400 teams"), OR a named-customer quote |
| 3 | **Problem** | Make the visitor say "yes, that's me" | The pain is named in the visitor's words, not the vendor's jargon |
| 4 | **Solution** | Show the specific fix, with proof | One product screenshot (the hero shot), one sentence of mechanism |
| 5 | **Features** | List the 3 things the visitor gets that map to the 3 sub-pains | Exactly 3 features in a 3-up row; each: icon + one-line title + one-sentence detail. NOT a feature dump. |
| 6 | **How it works** | Remove the "feels complicated" objection | 3 numbered steps, each ≤ 8 words for the step name |
| 7 | **Pricing** | Trigger the "what does it cost?" decision | 2 or 3 tiers max; middle tier visually highlighted as "most popular"; show price OR explicit "Custom" with contact CTA |
| 8 | **FAQ** | Defuse the last 4–6 objections | 4–6 questions, sourced from sales-call transcripts or support tickets; answers ≤ 3 sentences each |
| 9 | **Final CTA** | Re-ask for the click after the visitor has the full picture | One CTA, same verb as the Hero CTA; no secondary CTA here (kill the indecision) |

## Hero copy formula

The Hero is the load-bearing section. Use the formula:

```
H1:     [OUTCOME] for [WHO specific] [HOW different]
Sub:    [Concrete proof or mechanism in one sentence]
CTA:    [Verb + benefit]
```

**Examples (formula applied, not verbatim templates):**

| H1 | Why it works |
|---|---|
| "Ship faster for engineering teams without a release-day war room" | Outcome (ship faster) + Who specific (engineering teams) + How different (without war room) |
| "Tax filing for freelancers with one quarter of moonlighting income" | Outcome (tax filing) + Who specific (freelancers + side income) + How different (specialized) |
| "Generate brand-consistent designs for product teams in 5 minutes" | Outcome (designs) + Who specific (product teams) + How different (5 min) |

**Anti-patterns the formula explicitly rejects:**
- "The future of X" — no outcome, no who, no how
- "AI-powered X" — "AI-powered" is a how, not an outcome; visitor doesn't buy mechanisms
- "Welcome to X" — wastes the visitor's first 5 seconds
- "Built by ex-Google engineers" — that belongs in About, not the H1

## Banned CTA copy

The following CTA strings are banned in any Hero or Final CTA:

| Banned | Why | Replace with |
|---|---|---|
| "Get Started" | Generic; gives the visitor no information about what happens next | "Start free 14-day trial" / "Create your first invoice" / "See the dashboard" |
| "Learn More" | Defers the conversion to a wiki-walk | "See pricing" / "Watch the 2-min demo" / "Read the docs" |
| "Sign Up" | Friction-forward — leads with the cost, not the value | "Create your account" / "Claim your account" — same action, framed as gain |
| "Submit" | Form-end button on a primary CTA; reads as bureaucratic | "Send message" / "Book a call" / "Request access" |
| "Click Here" | A link is already obviously clickable | Use the destination as the label: "See pricing" |
| "Buy Now" | Pressure phrasing; converts worse than outcome phrasing | "Start your subscription" / "Add to cart" / "Pay $X today" |

The rule: **every CTA must contain a verb AND name the next benefit or action the visitor receives.** "Start free 14-day trial" has both. "Get Started" has neither.

## Variation rules

When `amw-ascii-sketch` produces the mandatory 3 variants per `amw-design-principles` rule 2:

- **Variant 1 (baseline):** all 9 sections in the canonical order.
- **Variant 2 (advanced):** combine sections 3+4 (Problem-Solution as one narrative section); promote section 5 (Features) above section 4 (Solution) when the product is a tool rather than a service.
- **Variant 3 (experimental):** kill section 6 (How it works) and let the screenshot in section 4 carry the explanation; OR kill section 8 (FAQ) when the product is impulse-purchase priced (< $30).

Never kill sections 1 (Hero), 2 (Social proof), 7 (Pricing), or 9 (Final CTA). Those four carry the conversion.

## Cross-references

- `amw-ascii-sketch/SKILL.md` — consumes this anatomy as the default landing scaffold when no DESIGN.md is provided.
- `agents/amw-wireframe-builder-agent.md` — renders each section to HTML per its conversion job; refuses to ship if Hero CTA is in the banned list.
- `agents/amw-seo-strategist-agent.md` — validates that H1 follows the Hero formula and that the section H2s map cleanly to keyword intent.
- `references/TECH-microcopy-patterns.md` — button labels and microcopy for the CTAs, empty states, and FAQ entries.
- `references/TECH-dial-configuration.md` — the dial settings steer which Variant (baseline / advanced / experimental) is the user's actual preference.
- `references/component-taste.md` — visual treatment for each section (Hero card, pricing tier highlighting, FAQ accordion).
